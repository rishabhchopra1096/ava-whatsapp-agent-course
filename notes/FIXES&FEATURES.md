# FEATURES

1. Calling + Email Ability is easy to add in interfaces. Basically, you use the same brain, and talk to AI. A demo where you're on call with AI, and you tell it to find you a restaurant. It sends you a picture on whatsapp. Once you say on call to book it, it sends you an email with the booking details. Basically, fast, like a real-person. This is something that can be used in the AI-Co-Founder. Very interesting. The thing is that whether it's an AI Tutor, AI Employee, or personal AI Assistant, you need to be able to talk to it anywhere.
2. Basically, you already have 2 interfaces: ChainLit + Whatsapp. Now, the thing is that whatsapp uses async operations so that multiple users can chat at the same time. I'll need to implement something similar with VAPI.
3. This can be used for:

- AI Co-Founder for Solo Founders
- AI Employee (Voice Agent for Businesses)
- AI Job Searcher
- AI Stylist - Whatsapp/Text Deals at the right time + Browser Use for Buying It

4. Customer Personality/Schedule of your AI.
5. Need to customise personality to be more dynamic than a simple schedule. Can go for holidays, or whatever. Literal Pepper Potts routine. You literally need to consider it as a character of a video game. For this, you'll need to change CharacterCard and Schedule.

### FIXES

1. The current setting only shows AI's POV. But doesn't really generate an AI image. Basically, there needs to be a difference in routing based on whether the user is asking to see a picture of what AVA is doing, as compared to a general image.
2. I think this routing behavior is rather simple. Like text, audio, image, there can be another which is "Call". Once the call is over, the data should be sent to our backend.
   -Move to a smarter model like gemini-1.5-prop that is as fast as Llama 3.3 70B - see groq's most up to data, smartest model.
3. Change elevenlabs (expensive) to Groq Chip (cheaper)
4. Llama is dumb, fast. I should use a smarter model like gemini-flash which is fast, but not dumb.
5. Image should only be shared when asked for. Not when inferred. Can't work like that.
6.

# LEARN

1. FastAPI/Webhook
2. Docker
3.

# FIXES.md

Critical issues identified in the Ava WhatsApp Agent and their solutions.

## 🚨 CRITICAL: User Conversation Isolation Issue

### Problem Description

The current system **does NOT maintain separate conversations per user**. While short-term memory is isolated per user, long-term memory is shared globally across all users.

**What happens in practice:**

```
User A (John) texts: "What's the weather like?"
User B (Jane) texts: "Help me with math homework"
User A texts again: "Thanks for the weather info"
```

**Current behavior:**

- John's conversation thread is isolated ✅
- Jane's conversation thread is isolated ✅
- BUT: Jane's math memories could leak into John's context ❌
- AND: John's weather memories could leak into Jane's context ❌

### Root Cause Analysis

**Short-term memory (WORKS CORRECTLY):**

- File: `src/ai_companion/interfaces/whatsapp/whatsapp_response.py:47`
- Uses phone number as `session_id = from_number`
- SQLite checkpointer properly isolates by `thread_id`

**Long-term memory (BROKEN):**

- File: `src/ai_companion/modules/memory/long_term/memory_manager.py:67-73`
- `get_relevant_memories()` searches ALL memories from ALL users
- No user filtering in Qdrant vector store queries
- Memories stored without user context

### Technical Details

#### Memory Storage (Line 58-65 in memory_manager.py)

```python
self.vector_store.store_memory(
    text=analysis.formatted_memory,
    metadata={
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(),
        # ❌ MISSING: "user_id": user_id
    },
)
```

#### Memory Retrieval (Line 69 in memory_manager.py)

```python
def get_relevant_memories(self, context: str) -> List[str]:
    memories = self.vector_store.search_memories(context, k=settings.MEMORY_TOP_K)
    # ❌ No user filtering - searches ALL memories from ALL users
    return [memory.text for memory in memories]
```

### Solution Implementation

#### 1. Update Memory Storage

**File:** `src/ai_companion/modules/memory/long_term/memory_manager.py`

```python
async def extract_and_store_memories(self, message: BaseMessage, user_id: str) -> None:
    """Extract important information from a message and store in vector store."""
    if message.type != "human":
        return

    analysis = await self._analyze_memory(message.content)
    if analysis.is_important and analysis.formatted_memory:
        # Check if similar memory exists FOR THIS USER
        similar = self.vector_store.find_similar_memory(
            analysis.formatted_memory,
            user_filter=user_id  # ✅ Add user filtering
        )
        if similar:
            self.logger.info(f"Similar memory already exists for user {user_id}")
            return

        # Store new memory WITH user context
        self.logger.info(f"Storing new memory for user {user_id}: '{analysis.formatted_memory}'")
        self.vector_store.store_memory(
            text=analysis.formatted_memory,
            metadata={
                "id": str(uuid.uuid4()),
                "timestamp": datetime.now().isoformat(),
                "user_id": user_id,  # ✅ Add user identification
            },
        )
```

#### 2. Update Memory Retrieval

```python
def get_relevant_memories(self, context: str, user_id: str) -> List[str]:
    """Retrieve relevant memories based on the current context FOR SPECIFIC USER."""
    memories = self.vector_store.search_memories(
        context,
        k=settings.MEMORY_TOP_K,
        user_filter=user_id  # ✅ Filter by user
    )
    if memories:
        for memory in memories:
            self.logger.debug(f"User {user_id} memory: '{memory.text}' (score: {memory.score:.2f})")
    return [memory.text for memory in memories]
```

#### 3. Update Vector Store Interface

**File:** `src/ai_companion/modules/memory/long_term/vector_store.py`

Add user filtering to Qdrant queries:

```python
def search_memories(self, query: str, k: int = 5, user_filter: str = None) -> List[Memory]:
    """Search for relevant memories with optional user filtering."""
    search_filter = None
    if user_filter:
        search_filter = models.Filter(
            must=[
                models.FieldCondition(
                    key="user_id",
                    match=models.MatchValue(value=user_filter)
                )
            ]
        )

    # Rest of search implementation with filter
```

#### 4. Update Graph Workflow

**File:** `src/ai_companion/graph/nodes.py`

Pass user_id through all memory operations:

```python
async def memory_extraction_node(state: AICompanionState) -> AICompanionState:
    memory_manager = get_memory_manager()
    user_id = state.get("user_id")  # ✅ Get from state

    await memory_manager.extract_and_store_memories(
        state["messages"][-1],
        user_id=user_id  # ✅ Pass user context
    )
    return state
```

#### 5. Update WhatsApp Handler

**File:** `src/ai_companion/interfaces/whatsapp/whatsapp_response.py`

Add user_id to graph state:

```python
# Line 72-75, modify to include user_id
await graph.ainvoke(
    {
        "messages": [HumanMessage(content=content)],
        "user_id": from_number  # ✅ Add user identification to state
    },
    {"configurable": {"thread_id": session_id}},
)
```

### Impact Assessment

**Before Fix:**

- User A asks about weather → stored globally
- User B asks about math → stored globally
- User A gets weather response + potential math context leak ❌

**After Fix:**

- User A asks about weather → stored for User A only
- User B asks about math → stored for User B only
- User A gets weather response + only User A's context ✅

### Testing Strategy

1. **Unit Tests:** Test memory isolation with mock user IDs
2. **Integration Tests:** Simulate multi-user WhatsApp conversations
3. **Manual Testing:** Use different phone numbers and verify memory separation

### Migration Considerations

- Existing memories in Qdrant lack `user_id` metadata
- Need migration script to either purge or attempt user attribution
- Consider gradual rollout with feature flag

---

## Additional Issues to Address

### 2. Error Handling in Media Processing

- Audio/image processing failures should gracefully fallback
- Need better error messages for users when media processing fails

### 3. Rate Limiting

- No rate limiting on WhatsApp webhook endpoints
- Could be abused for DoS attacks or excessive API usage

### 4. Security

- WhatsApp tokens should be properly validated
- Need input sanitization for user messages before LLM processing
