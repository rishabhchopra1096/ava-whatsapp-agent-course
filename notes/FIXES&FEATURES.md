# FEATURES

1. Calling + Email Ability is easy to add in interfaces. Basically, you use the same brain, and talk to AI. A demo where you're on call with AI, and you tell it to find you a restaurant. It sends you a picture on whatsapp. Once you say on call to book it, it sends you an email with the booking details. Basically, fast, like a real-person. This is something that can be used in the AI-Co-Founder. Very interesting. The thing is that whether it's an AI Tutor, AI Employee, or personal AI Assistant, you need to be able to talk to it anywhere.
2. Basically, you already have 2 interfaces: ChainLit + Whatsapp. Now, the thing is that whatsapp uses async operations so that multiple users can chat at the same time. I'll need to implement something similar with VAPI.
3. This can be used for:

- Calls: "This AI just made a real phone call"
- Workflow Generator: "Check Product Hunt daily for AI tutoring tools"
- Integration: "It found the restaurant, called them, and put the dinner in my calendar" "All from one WhatsApp message"
- Research | Contextualised Intelligence: Based on what it knows about you, gives a restaurant pick.
- Email Handling: Drafts responses for me. I can call it to discuss the emails for today, and what to reply to them.
- Habit Tracking: It calls me everyday/whatsapps me to discuss my habit-tracker - and fills it automatically.
- Note-Taking: Takes notes in google sheets, docs, notion databaset, etc.
- Todo-List: Stores/updates TODO-Lists
- Reminders: Calls/Whatsapps for Reminding the person
- AI Memory | Very Long Term Memory: "Remind me about the conversation with Joh about the contractor"

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
6. Switch to pure Supabase
7. The current personality is super rude. Doesn't analyse images, etc. Always busy. Don't like this behavior. Not smart, doesnt' understand context.
8. It needs to be able to take in youtube links, pdf, locations, links, etc and be able to analyse them easily.

# LEARN

1. FastAPI/Webhook
2. Docker

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

### Moving to Supabase

📁 Files That Need Changes:

🔴 Major Changes (Core Database Logic):

1. src/ai_companion/modules/memory/long_term/vector_store.py

- Current: 500 lines using QdrantClient
- Change: Replace with Supabase client + pgvector
- Effort: Complete rewrite (80% of file)

2. src/ai_companion/modules/memory/long_term/memory_manager.py

- Current: Uses vector_store methods
- Change: Update method calls to match new Supabase interface
- Effort: Moderate changes (30% of file)

🟡 Medium Changes (Configuration):

3. src/ai_companion/settings.py

# Current Qdrant settings

QDRANT_URL: str
QDRANT_API_KEY: str | None

# New Supabase settings

SUPABASE_URL: str
SUPABASE_KEY: str
DATABASE_URL: str # PostgreSQL connection
Effort: 10-15 lines changed

4. docker-compose.yml

- Remove: Qdrant service (entire section)
- Remove: Qdrant volumes and dependencies
- Effort: Delete ~30 lines

5. .env

# Remove

QDRANT_URL=...
QDRANT_API_KEY=...

# Add

SUPABASE_URL=...
SUPABASE_ANON_KEY=...
DATABASE_URL=postgresql://...
Effort: 3-4 lines changed

🟢 Minor Changes (Dependencies):

6. pyproject.toml

# Remove

qdrant-client = "^1.13.0"

# Add

supabase = "^2.0.0"
asyncpg = "^0.29.0" # PostgreSQL driver
Effort: 2-3 lines

7. Dockerfile & Dockerfile.chainlit

- Remove: Qdrant-related packages
- Add: PostgreSQL client libraries
- Effort: 2-3 lines each

📊 Code Change Breakdown:

| File               | Lines Changed | Effort Level | Time Estimate |
| ------------------ | ------------- | ------------ | ------------- |
| vector_store.py    | 400+ lines    | High         | 6-8 hours     |
| memory_manager.py  | 50-80 lines   | Medium       | 2-3 hours     |
| settings.py        | 10-15 lines   | Low          | 30 minutes    |
| docker-compose.yml | 30 lines      | Low          | 15 minutes    |
| .env               | 4 lines       | Low          | 5 minutes     |
| pyproject.toml     | 3 lines       | Low          | 5 minutes     |
| Dockerfiles        | 6 lines       | Low          | 15 minutes    |

🎯 Core Challenge: vector_store.py Rewrite

Current Structure:

class VectorStore:
def **init**(self):
self.client = QdrantClient(url=..., api_key=...)

      def store_memory(self, text: str, metadata: dict):
          # Qdrant-specific code

      def search_memories(self, query: str, k: int):
          # Qdrant-specific search

New Structure:

class VectorStore:
def **init**(self):
self.supabase = create_client(url=..., key=...)

      def store_memory(self, text: str, metadata: dict):
          # PostgreSQL with pgvector

      def search_memories(self, query: str, k: int):
          # SQL with vector similarity search

🚧 Migration Strategy:

Phase 1: Drop-in Replacement (1-2 days)

- Rewrite vector_store.py with same interface
- Update dependencies and config
- Result: Same functionality, different database

Phase 2: Enhanced Features (Later)

- Add user management tables
- Add todos, calendar, notes tables
- Enhance LangGraph integration

🎯 Effort Assessment:

Total code changes needed:

- 7 files modified
- ~500 lines of meaningful changes
- 80% concentrated in vector_store.py

Migration complexity: Medium

- Not a complete rewrite (interfaces stay same)
- Core logic preserved (just database calls change)
- Most files barely touched (just config changes)

Time estimate:

- Experienced developer: 1-2 days
- Learning as you go: 3-4 days
- With testing: Add 1-2 days

💡 The Good News:

What DOESN'T need to change:

- ✅ LangGraph workflow (stays identical)
- ✅ Memory injection/extraction logic
- ✅ All the AI modules (STT, TTS, etc.)
- ✅ Chainlit and WhatsApp interfaces
- ✅ 90% of the codebase!

Migration verdict: Moderate effort, high reward - most of Ava stays
untouched!

🏗️ Feature Dependency Analysis:

🎯 Foundation Layer (Build First - Everything Depends on
These)

1. AI Memory | Very Long Term Memory 🔥

- Dependencies: None (pure foundation)
- Enables: Research, Note-Taking, Todo-List, Contextual
  Intelligence, Email Handling
- Why first: Without memory, AI can't be contextual or
  personal
- Implementation: Enhanced Supabase migration we discussed

2. Note-Taking 🔥

- Dependencies: AI Memory (to organize/categorize)
- Enables: Todo-List, Research, Email Handling, Habit
  Tracking
- Why second: Data capture foundation for everything else
- Implementation: Structured storage + categorization

3. Research | Contextualised Intelligence 🔥

- Dependencies: AI Memory + Note-Taking (for context)
- Enables: Workflow Generator, Integration, Email Handling
- Why third: The "brain" that makes decisions
- Implementation: Web search + memory-based personalization

🔧 Action Layer (Build Second - These Take Actions)

4. Todo-List

- Dependencies: Note-Taking + AI Memory
- Enables: Reminders, Workflow Generator, Integration
- Natural flow: Notes → Todos → Actions

5. Reminders

- Dependencies: Todo-List + AI Memory
- Enables: Habit Tracking, Workflow Generator
- Natural flow: Todos → Scheduled reminders

6. Calls

- Dependencies: AI Memory (for context), Research (for
  information)
- Enables: Habit Tracking, Email Handling, Integration
- Why later: Complex infrastructure, but unlocks major
  capabilities

🤖 Automation Layer (Build Third - These Coordinate
Everything)

7. Workflow Generator

- Dependencies: Research + Note-Taking + Todo-List +
  Reminders
- Enables: Integration, advanced automations
- Why later: Needs all foundation pieces working

8. Integration

- Dependencies: ALL previous features
- Enables: Complex multi-step workflows
- Why last: Orchestrates everything together

🎨 Specialized Features (Build in Parallel)

9. Email Handling

- Dependencies: AI Memory + Research + Calls (for
  discussion)
- Can build: After foundation layer is solid

10. Habit Tracking

- Dependencies: AI Memory + Calls/Reminders + Note-Taking
- Can build: After action layer is ready

🎯 Optimal Build Sequence:

Phase 1: Intelligence Foundation (Months 1-2)

AI Memory → Note-Taking → Research/Contextual Intelligence
Result: Smart AI that remembers and understands context

Phase 2: Action Foundation (Months 3-4)

Todo-List → Reminders → Calls
Result: AI that can take real-world actions

Phase 3: Specialization (Months 5-6)

Email Handling + Habit Tracking (parallel development)
Result: AI that handles specific use cases well

Phase 4: Automation (Months 7-8)

Workflow Generator → Integration
Result: AI that works autonomously and coordinates
everything

💡 Why This Order is Natural:

Data Flow Logic:

Memory (stores) → Notes (capture) → Research (enhance) →
Todos (plan) → Reminders (schedule) → Calls (execute) →
Workflows (automate) → Integration (orchestrate)

Complexity Graduation:

- Phase 1: Data management (easier)
- Phase 2: External actions (moderate)
- Phase 3: Domain expertise (moderate)
- Phase 4: Orchestration (hardest)

User Value Progression:

- Phase 1: "It remembers everything I tell it"
- Phase 2: "It actually does things for me"
- Phase 3: "It handles my specific needs"
- Phase 4: "It works like a human assistant"

🚀 Strategic Advantage of This Order:

1. Each phase is demoable - You can show progress at every
   stage
2. Each phase is useful - Users get value even if you stop
   early
3. Technical debt minimized - Foundation supports
   everything built on top
4. Risk managed - If complex features fail, simpler ones
   still work

The key insight: Build the "memory and intelligence" first,
then add "actions and automation" on top. This creates a
solid foundation that makes every subsequent feature easier
to build and more powerful!

### Feature Priority For Getting Users

1.  Core Feature: AI Memory | Very Long Term Memory ⭐⭐⭐⭐⭐

- User behavior: "Remember what I told you about John's
  contractor issue last month"
- Why it drives adoption: This is INSTANT value that no
  other WhatsApp user has
- Stickiness: Once they store memories, they can't leave
- Word-of-mouth: "Holy shit, my WhatsApp never forgets
  anything!"

2. Supporting Feature: Note-Taking with "Don't Reply Feature" ⭐⭐⭐

- User behavior: Voice note → clean organized text
- Why needed: Captures the memories in the first place
- Demo value: Send rambling voice note, get back perfect
  summary

3. Research - "Look up the best Thai restaurants near me"
4. Simple Reminders - "Remind me to call John tomorrow at
   3pm"

### Feature Priority For "WOW"

5. Calling
6. Voice Email-Handling
7. Voice Habit Tracking
8. Workflow Builder
