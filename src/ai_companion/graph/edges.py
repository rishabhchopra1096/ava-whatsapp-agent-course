"""
🔀 DECISION POINTS IN AVA'S BRAIN - "Edges" that control the flow between nodes

WHAT IS THIS FILE?
This file contains "edge functions" - the decision makers that control which node runs next.
Think of these as traffic controllers at intersections, deciding which road to take.

WHY "EDGES"?
In graph theory, edges are the connections between nodes. In LangGraph:
- Nodes = Workers that do tasks (generate text, create images, etc.)
- Edges = Decision points that route between workers

HOW EDGE FUNCTIONS WORK:
1. Take the current state (clipboard) as input
2. Look at specific information in the state
3. Return the name of the next node to execute
4. LangGraph automatically routes to that node

EXECUTION FLOW:
After each node completes, LangGraph checks if there's an edge function.
If yes → runs edge function → goes to returned node
If no → follows default path (defined in graph.py)

REAL EXAMPLE:
After conversation_node creates response:
→ should_summarize_conversation checks message count
→ If > 30 messages: returns "summarize_conversation_node" 
→ If ≤ 30 messages: returns END (conversation ends)
"""

# LangGraph special constant that means "stop processing"
from langgraph.graph import END
# Python type hint for functions that return specific string values
from typing_extensions import Literal

# Our custom imports
from ai_companion.graph.state import AICompanionState  # The "clipboard" with all info
from ai_companion.settings import settings             # Configuration (message limits, etc.)


def should_summarize_conversation(
    state: AICompanionState,
) -> Literal["summarize_conversation_node", "__end__"]:
    """
    📊 MEMORY MANAGEMENT DECISION - Should we compress the conversation?
    
    WHAT IT DOES:
    Checks if the conversation is getting too long and needs summarization.
    Like deciding "this chat is huge, let's make notes before I forget early parts"
    
    WHY IT EXISTS:
    LLMs have token limits (context window). Too many messages = errors or slowness.
    Solution: Summarize old messages, keep only recent ones + summary.
    
    WHEN IT'S CALLED:
    After conversation_node, image_node, or audio_node completes.
    (Defined in graph.py using add_conditional_edges)
    
    RETURN VALUES:
    - "summarize_conversation_node" → Run summarization to compress chat
    - END → Stop processing, conversation complete
    
    REAL EXAMPLE:
    32 messages in chat, TOTAL_MESSAGES_SUMMARY_TRIGGER = 30
    → Returns "summarize_conversation_node"
    → Old messages get summarized: "User discussed weather, weekend plans..."
    → Keeps last 5 messages + summary
    
    TYPE HINT EXPLANATION:
    Literal["summarize_conversation_node", "__end__"] means this function
    can ONLY return one of these exact strings, nothing else.
    """
    
    # STEP 1: Get all messages from the conversation
    # This includes both user messages (HumanMessage) and Ava's responses (AIMessage)
    messages = state["messages"]

    # STEP 2: Check if we've hit the message limit
    # settings.TOTAL_MESSAGES_SUMMARY_TRIGGER is probably 30-50 messages
    # Why check length? More messages = more tokens = slower/expensive API calls
    if len(messages) > settings.TOTAL_MESSAGES_SUMMARY_TRIGGER:
        # Too many messages! Route to summarization node
        # This will compress old messages into a summary
        return "summarize_conversation_node"

    # STEP 3: Conversation is still manageable size
    # END is a LangGraph constant that means "stop processing"
    # The response has been sent, nothing more to do
    return END


def select_workflow(
    state: AICompanionState,
) -> Literal["conversation_node", "image_node", "audio_node", "voice_calling_node"]:
    """
    🎯 RESPONSE TYPE ROUTER - Directs to the appropriate response generator
    
    WHAT IT DOES:
    Routes to the correct node based on the router's decision.
    Like a train switch operator: "Text response? → Track 1. Image? → Track 2"
    
    WHY IT EXISTS:
    The router_node decided HOW to respond (text/image/audio).
    This edge function actually ROUTES to the right response generator.
    
    WHEN IT'S CALLED:
    After memory_injection_node completes.
    (The last step before generating the actual response)
    
    WORKFLOW DECISION FLOW:
    1. User: "What are you up to?" 
    2. router_node: "This needs an image response" → sets workflow="image"
    3. THIS FUNCTION: Reads workflow="image" → returns "image_node"
    4. LangGraph: Routes to image_node to generate image
    
    TYPE HINT EXPLANATION:
    Can only return one of three exact node names. This ensures
    we can't accidentally route to a non-existent node.
    
    REAL EXAMPLES:
    - workflow="conversation" → "conversation_node" (text response)
    - workflow="image" → "image_node" (picture + caption)  
    - workflow="audio" → "audio_node" (voice message)
    """
    
    # STEP 1: Get the workflow decision from state
    # This was set by router_node earlier in the flow
    # Will be one of: "conversation", "image", or "audio"
    workflow = state["workflow"]

    # STEP 2: Route to the appropriate response generator
    # Simple if-elif-else routing based on the workflow type
    
    # Image response requested
    if workflow == "image":
        # Route to image_node which will:
        # 1. Generate an image of Ava's current activity
        # 2. Create a text caption to go with it
        return "image_node"

    # Audio response requested  
    elif workflow == "audio":
        # Route to audio_node which will:
        # 1. Generate text response (like conversation_node)
        # 2. Convert text to speech using ElevenLabs
        return "audio_node"
    
    # NEW: Voice call requested
    elif workflow == "voice_call":
        # Route to voice_calling_node which will:
        # 1. Extract user's phone number from WhatsApp
        # 2. Prepare conversation context for voice call
        # 3. Create Vapi assistant with user's context
        # 4. Initiate outbound phone call
        # 5. Send WhatsApp confirmation message
        return "voice_calling_node"

    # Default to text response (includes "conversation" and any unexpected values)
    else:
        # Route to conversation_node which will:
        # Generate a text-only response using Ava's personality
        # This is the most common response type
        return "conversation_node"
