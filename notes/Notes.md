### Tutorial 1:

- A system is a workflow if you decide what the steps are to complete a task.
- A system is an agent if the LLM (not you) decides how many steps it needs to complete a task.

### Tutorial 2:

- So bascially, based on whoever messages, you could have just changed the scope of the conversation, added long-term memory, and do a memory injection in N8N also. So truly, it is possible to build in N8N.
- But this is a good project to learn lang-graph and learn whatsapp ai agent.
- Question: There is a router node to decide how to respond (autdio, text, image) but can I have multiple router nodes? For example, based on the user's query whether they want to: - Make a call - Schedule a reminder - Cross off a TODO
  ⏺ Multiple Router Nodes in
  LangGraph

  Yes, absolutely possible and
  recommended! You can have
  hierarchical routing layers for
  complex decision trees like
  action type → specific action →
  execution method.

  Code Example:

  # First router: Action type

  async def
  action_router_node(state:
  AICompanionState) ->
  AICompanionState:
  chain = action_prompt |
  llm.with_structured_output(Acti
  onRouter)
  result = await
  chain.ainvoke({"message":
  state["messages"][-1].content})
  state["action_type"] =
  result.action_type
  return state

  # Second router: Specific

  productivity action
  async def
  productivity_router_node(state:
  AICompanionState) ->
  AICompanionState:
  chain = productivity_prompt
  | llm.with_structured_output(P
  roductivityRouter)
  result = await
  chain.ainvoke({"message":
  state["messages"][-1].content})

  state["productivity_action"] =
  result.action
  return state

  # Graph edges

  graph_builder.add_conditional_e
  dges(
  "action_router_node",
  lambda state:
  state["action_type"],
  {
  "communication":
  "communication_router_node",
  "productivity":
  "productivity_router_node"
  }
  )

  graph_builder.add_conditional_e
  dges(
  "productivity_router_node",
  lambda state:
  state["productivity_action"],
  {
  "schedule":
  "schedule_reminder_node",
  "todo":
  "todo_management_node",
  "call":
  "make_call_node"
  }
  )

  Key Benefits:

  - Cleaner prompts - Each router
    has focused responsibility
  - Better accuracy - Fewer
    classification options per step

  - Easier debugging - Can trace
    exactly where routing decisions
    occur
  - Modular architecture - Add
    new actions without changing
    existing routers

  This hierarchical approach is
  exactly how production AI
  agents handle complex decision
  trees.

- Order to understand:
  - Nodes
  - Graph
  - State
  - Edges
- https://academy.langchain.com/courses/take/intro-to-langgraph/texts/58238105-getting-set-up: 6 hours of Video
  - Welcome: 3 + 13 = 16
  - Basic Concepts (Enough for This): 1 + 8 + 6 + 3 + 6+ 7 + 8 + 6 = 45
  - State & Memory: 1 + 4 + 10 + 5 + 8 + 9 + 8 = 45
  - UX & Human in the Loop: 1 + 11 + 9 + 11 + 4 + 19 = 55
  - Building Your Assistant: 2 + 11 + 8 + 13 + 27 = 61
  - 13 + 11 + 18 + 13 + 23 = 78
  - 7 + 6 + 20 + 7 + 9 = 49

### What is State? See (states.py)

    - Anything that I want each node to be able to access at any point in time, should be part of the state.
    - This is like the AI's scratch pad that accumulates information as your message flows through her brain. Each node can read from and write to these fields.
    - Examples of what goes in state:
    - ✅ User preferences from memory lookup (any node
    might need this)
    - ✅ Current conversation mode (text/audio/image)
    - ✅ Generated content paths (audio files, images)
    - ❌ Temporary variables used only within one node
    - ❌ API keys or configuration (those go in settings)

The flow pattern is:

1. Node reads current state
2. Node does its work (calls APIs, processes data,
   etc.)
3. Node updates state with its findings
4. Next node gets the enriched state

So as your message flows through Ava's brain, each
node adds its "discoveries" to this shared clipboard,
building up a complete picture for the final
response.

### How Nodes, Edges, Graph & State Work Together

🧠 The Complete Picture

State (state.py) = The shared "clipboard"

- Flows through every node carrying
  accumulated information
- Like a delivery truck carrying packages
  between buildings

Nodes (nodes.py) = The "workers"

- Each does one specific job (generate
  text, create images, manage memories)
- Like specialized buildings in a city
  (office, factory, restaurant)

Edges (edges.py) = The "decision points"

- Control which node runs next based on
  current state
- Like traffic controllers at
  intersections deciding which road to take

Graph (graph.py) = The "blueprint"

- Connects everything together into Ava's
  complete brain
- Like the city planner's master plan
  showing how traffic flows

### Prompt for Good Explanations

To get this quality for any file, prompt
me with:

"Please add detailed pedagogical comments
to [filename] following the same
approach you used for graph.py. Include:

1. Comprehensive file header explaining
   purpose, analogies, and flow
2. Detailed import explanations
3. Step-by-step code walkthrough with
   inline comments
4. Real-world analogies to make concepts
   concrete
5. Explanations of WHY code exists, not
   just what it does"

### My own understanding

🔄 Complete Ava Pipeline - Technical Deep Dive

✅ "when a new message comes, we first see if
there is something worth memorizing"

- Exactly! memory_extraction_node analyzes your
  message
- Extracts facts like "I'm a developer" or "I
  live in NYC"
- Stores to Qdrant vector database using semantic embeddings
- Qdrant acts as Ava's long-term memory bank
  across all conversations

✅ "router node...will probably select how should we respond"

- Perfect! Router_node uses Groq's Llama 3.3 70B to decide
- Analyzes recent messages from SQLite database
  (conversation history)
- Returns decision: text/image/audio response
  type
- Graph State (clipboard) gets updated with
  workflow decision

✅ "context injection node...lets us know what
Ava is doing right now"

- Spot on! Context_injection_node reads Ava
  Activities schedule
- Calendar/time-based system tells us: "coding
  Python at 2 PM"
- Gets current activity from predefined daily
  schedule
- Injects this context into the Graph State for
  personalization

✅ "memory injection node reads certain memories
that are relevant"

- Exactly! Memory_injection_node queries Qdrant
  database
- Uses semantic search to find memories related
  to recent messages
- Retrieves: "User is developer, likes pizza,
  works on AI projects"
- Injects personal context from long-term memory
  into Graph State

✅ "all of this context goes to either
conversation/image/audio node"

- Perfect! Select_workflow edge routes to the
  chosen response node:
  - Text Node → Groq Llama 3.3 generates
    personalized text
  - Image Node → Together.ai FLUX creates visual
    response
  - Audio Node → ElevenLabs converts text to
    voice
- All nodes access the complete Graph State with accumulated context

✅ "if response messages are crossing a
threshold, we summarize or end"

- Exactly right! Summarize_conversation checks
  message count
- SQLite database tracks conversation length per
  user
- If >20 messages: compress old messages into
  summary text
- Prevents hitting token limits, maintains
  conversation flow

🧠 The Complete Context Accumulation Pipeline

By the time we reach response generation, Ava's
Graph State contains:

📊 From SQLite Database:

- Full conversation history with you
- Message count for summarization logic
- Your user ID for isolation

🧠 From Qdrant Vector Database:

- "User is a software engineer at Google"
- "Loves Star Wars and pizza"
- "Working on ML project, lives in SF"

📅 From Ava Activities System:

- "Currently debugging Python code"
- "Has a meeting at 3 PM"
- "Learning oil painting on weekends"

🎯 From Router Decision:

- Response type: text/image/audio
- Conversation context and intent

That's why her responses feel so natural and
personalized - she's not just responding to your
latest message, but combining:

- Your personal history (Qdrant)
- Her current life (Activities)
- Conversation flow (SQLite)
- Response strategy (Router)

Into one contextually-aware, human-like response!

###
