"""
angGraph models agent workflows as graphs, using three main components:

🔶 State - A shared data structure that tracks the current status of your app (workflow).

🔶 Nodes - Python functions that define the agent behaviour. They take in the current state, perform actions, and return the updated state.

🔶 Edges - Python functions that decide which Node runs next based on the State, allowing for conditional or fixed transitions (we'll see an example of conditional edge later 😉)

By combining Nodes and Edges, you can build dynamic workflows, like Pepper! In the next section, we'll take a look at Pepper's graph and its Nodes and Edges.


"""
from typing import Dict
from langgraph.graph import MessagesState


class AICompanionState(MessagesState):
    """
    🧠 pepper'S WORKING MEMORY - The "clipboard" that gets passed between all graph nodes
    
    This is like Pepper's scratch pad that accumulates information as your message 
    flows through her brain. Each node can read from and write to these fields.
    
    Extends MessagesState to automatically get:
    - messages: List[BaseMessage] - Full conversation history 
    - This gives us chat context for free!

    As we mentioned earlier, LangGraph keeps track of your app's current status using the State. Pepper’s state has these attributes:

    summary - The summary of the conversation so far (more on this in Lesson 3)

    workflow - The current workflow Pepper is in. Can be “conversation”, “image” or “audio”. More on this when we talk about the Router Node.

    audio_buffer - The buffer containing audio data for voice messages. This is something we’ll cover in Speech Mdoules. 

    image_path - Path to the current image being generated. More about this in Image Generation Module. 

    current_activity - Description of Pepper’s current simulated activity.

    apply_activity - Flag indicating whether to apply or update the current activity.
    """

    # 💭 CONVERSATION MANAGEMENT
    summary: str           # Summary of the conversation so far
                          # Prevents Pepper from "forgetting" in long chats
                          # Example: "User asked about weather, discussed plans for weekend"

    # 🤖 RESPONSE TYPE DECISION  
    workflow: str         # How should Pepper respond? Set by router_node
                         # Values: "conversation" | "image" | "audio"
                         # This tells the graph which response node to execute

    # 🎵 AUDIO PROCESSING
    audio_buffer: bytes   # Raw audio data when user sends voice note
                         # Gets filled by WhatsApp handler, processed by speech nodes
                         # Empty for text messages

    # 🖼️ IMAGE GENERATION
    image_path: str       # File path where generated image is saved
                         # Used by WhatsApp handler to send image back to user
                         # Example: "/tmp/pepper_activity_image.png"

    # 📅 pepper'S LIFE & PERSONALITY
    current_activity: str # What is Pepper doing right now based on her schedule?
                         # Example: "reviewing ML papers", "coding a Python script"
                         # Makes her feel more human and alive

    apply_activity: bool  # Should Pepper mention her current activity in response?
                         # Sometimes she talks about what she's doing, sometimes not
                         # Adds natural variation to conversations

    # 🧠 LONG-TERM MEMORY
    memory_context: str   # Relevant memories about THIS USER retrieved from vector DB
                         # Example: "John is a developer, likes pizza, lives in NYC, working on AI project"
                         # This is the key to personalized responses!

    # 📞 VOICE CALLING SUPPORT (WHATSAPP → PHONE)
    user_phone_number: str = ""  # WhatsApp sender's phone number for voice calls
                                 # Format: "+1234567890" (E.164 international format)
                                 # Used by voice_calling_node to initiate outbound calls
                                 # Example: "+15551234567"

    user_id: str = ""           # Unique user identifier (usually same as phone number)
                               # Used for user isolation and memory retrieval
                               # For WhatsApp: same as user_phone_number
                               # For Chainlit: could be session ID or user login

    interface: str = "unknown"  # Which interface is this message from?
                              # Values: "whatsapp" | "chainlit" | "unknown"
                              # Helps nodes adapt behavior based on platform
                              # Example: voice_calling only works for WhatsApp

    # 🎯 ACTIVE CALL TRACKING
    active_call: Dict = {}      # Details about ongoing voice call (if any)
                               # Contains: call_id, status, start_time, assistant_id
                               # Used to track call progress and handle callbacks
                               # Example: {"call_id": "abc123", "status": "ringing"}

    call_initiated_at: str = "" # Timestamp when voice call was initiated
                               # ISO format: "2024-01-15T10:30:00Z"
                               # Used for call duration tracking and timeouts
                               # Empty string when no active call

    voice_context_used: Dict = {} # WhatsApp conversation context passed to voice call
                                 # Contains: userName, recentContext, conversationTopic
                                 # Ensures continuity between WhatsApp chat and phone call
                                 # Example: {"userName": "John", "conversationTopic": "AI project help"}
