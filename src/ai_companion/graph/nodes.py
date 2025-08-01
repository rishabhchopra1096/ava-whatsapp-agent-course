"""
🧠 AVA'S BRAIN WORKERS - Each function is a "node" that does one specific job

WHAT IS THIS FILE?
This file contains all the "workers" in Ava's brain factory. Each function (called a "node") 
does ONE specific job, like:
- Deciding how to respond (text/image/audio)  
- Generating text responses
- Creating images
- Converting text to speech
- Managing memories

HOW DO NODES WORK?
1. Each node is a Python function
2. Takes AICompanionState (the "clipboard") as input
3. Does some work (calls APIs, processes data, etc.)
4. Returns updates to put back on the "clipboard"
5. Next node gets the updated clipboard

EXECUTION ORDER (set in graph.py):
Message arrives → memory_extraction → router → context injection → memory injection 
→ [conversation OR image OR audio node] → summarize (if needed) → response sent

REAL EXAMPLE:
You: "What are you up to?"
1. memory_extraction: Stores "User asked about activities" 
2. router: Decides "conversation" (text response)
3. context_injection: Gets "Ava is coding Python"
4. memory_injection: Retrieves "User is a developer"  
5. conversation: Generates "Hey! I'm coding Python too. How's your project going?"
"""

 # For creating directories (generated_images folder)
import os                    
# For generating unique filenames (image_12345.png)
from uuid import uuid4        

# LangChain imports - these are the "message" types Ava uses internally
from langchain_core.messages import AIMessage, HumanMessage, RemoveMessage
# Configuration for LLM calls
from langchain_core.runnables import RunnableConfig  

# Our custom imports
from ai_companion.graph.state import AICompanionState   # The "clipboard" 
# Pre-built LLM chains
from ai_companion.graph.utils.chains import (                           
    # Chain for Ava's personality responses
    get_character_response_chain,  
     # Chain for deciding response type
    get_router_chain,             
)
from ai_companion.graph.utils.helpers import (                          # Helper functions
    get_chat_model,               # Gets configured Groq LLM (Llama 3.3)
    get_text_to_image_module,     # Gets FLUX image generator
    get_text_to_speech_module,    # Gets ElevenLabs voice synthesizer
)

# Vector DB manager
from ai_companion.modules.memory.long_term.memory_manager import get_memory_manager  
# Ava's daily schedule
from ai_companion.modules.schedules.context_generation import ScheduleContextGenerator  
# Configuration values (API keys, model names, etc.)
from ai_companion.settings import settings  


async def router_node(state: AICompanionState):
    """
    🤖 THE DECISION MAKER - Ava's "brain" that decides how to respond
    
    WHAT IT DOES:
    Analyzes your message to decide response type:
    - "conversation" = text response ("Hey there!")
    - "image" = picture response (generates image of what she's doing)
    - "audio" = voice note response (sends you a voice message)
    
    WHY IT EXISTS:
    This makes Ava autonomous! Instead of always responding with text,
    she can decide "this person wants to see what I'm up to" → sends image
    
    REAL EXAMPLE:
    You: "What are you up to?" → router decides "image" 
    You: "How are you feeling?" → router decides "conversation"
    You: "Can you call me?" → router decides "audio"
    """
    
    # STEP 1: Get the "router chain" - this is a pre-configured LLM setup
    # What is a "chain"? It's: prompt + LLM model + output format
    # Located in: ai_companion/graph/utils/chains.py (get_router_chain function)
    chain = get_router_chain()
    
    # STEP 2: Prepare the input - only look at recent messages (performance optimization)
    # Why not all messages? Too many messages = expensive API call + slower response
    # settings.ROUTER_MESSAGES_TO_ANALYZE = probably 3-5 recent messages
    recent_messages = state["messages"][-settings.ROUTER_MESSAGES_TO_ANALYZE :]
    
    # STEP 3: Ask the LLM to make the decision
    # What is await? Python keyword for waiting for async operations
    # What is ainvoke? LangChain method to call the LLM asynchronously  
    # What gets sent? Recent messages + router prompt (stored in chains.py)
    # What comes back? RouterResponse object with response_type field
    response = await chain.ainvoke({"messages": recent_messages})
    
    # STEP 4: Update the state (the "clipboard") with the decision
    # This tells the graph: "execute the conversation/image/audio node next"
    # Why return a dict? LangGraph expects nodes to return state updates as dicts
    return {"workflow": response.response_type}


def context_injection_node(state: AICompanionState):
    """
    📅 AVA'S LIFE INJECTION - Makes Ava feel human by giving her a daily routine
    
    WHAT IT DOES:
    Checks what Ava is "doing" right now based on her schedule:
    - 9 AM: "reviewing machine learning papers"  
    - 2 PM: "coding a Python data analysis script"
    - 6 PM: "cooking dinner while listening to podcasts"
    
    WHY IT EXISTS:
    Makes conversations feel natural! Instead of "I'm an AI", she says 
    "I'm currently working on a ML project" - feels more human and alive.
    
    REAL EXAMPLE:
    You: "What are you up to?"
    Without this: "I'm an AI assistant, how can I help?"
    With this: "I'm analyzing some data for a ML project. What about you?"
    """
    
    # STEP 1: Get Ava's current activity from her schedule
    # What is ScheduleContextGenerator? A class that reads Ava's daily schedule
    # Located in: ai_companion/modules/schedules/context_generation.py
    # How does it work? Checks current time against a predefined schedule
    # Example return: "reviewing research papers on neural networks"
    schedule_context = ScheduleContextGenerator.get_current_activity()
    
    # STEP 2: Should we mention her activity in the response?
    # Why this logic? If she's doing the same thing as last message, don't be repetitive
    # state.get("current_activity", "") = get current_activity from clipboard, or "" if empty
    if schedule_context != state.get("current_activity", ""):
        apply_activity = True   # New activity! Worth mentioning to make conversation fresh
    else:
        apply_activity = False  # Same activity as before, skip mentioning to avoid repetition
    
    # STEP 3: Update the state (clipboard) with activity info
    # apply_activity = should we mention it? (True/False)
    # current_activity = what is she doing? ("coding Python script")
    # Later nodes will use this info to craft personalized responses
    return {"apply_activity": apply_activity, "current_activity": schedule_context}


async def conversation_node(state: AICompanionState, config: RunnableConfig):
    """
    💬 TEXT RESPONSE GENERATOR - The main "thinking" node that creates Ava's replies
    
    WHAT IT DOES:
    Takes everything Ava knows and crafts a personalized text response:
    - Your conversation history ("we talked about coding yesterday")
    - What she remembers about you ("John is a developer, likes pizza")  
    - What she's currently doing ("I'm working on a ML project")
    - Previous conversation summary (for long chats)
    
    WHY TWO PARAMETERS?
    - state: The "clipboard" with all accumulated information
    - config: LLM settings (temperature, timeouts, etc.) - needed for API calls
    
    REAL EXAMPLE:
    You: "How's your day going?"
    Context: memory="User is developer", activity="coding Python"
    Response: "Great! I've been debugging a Python script. How's your coding going?"
    """
    
    # STEP 1: Gather all the context pieces
    # Why get activity again? Because it might have changed since context_injection_node
    current_activity = ScheduleContextGenerator.get_current_activity()
    
    # Get what Ava remembers about you (set by memory_injection_node)
    # state.get("memory_context", "") = get memory_context from clipboard, or "" if empty
    memory_context = state.get("memory_context", "")
    
    # STEP 2: Get the "character response chain" 
    # What is this chain? It's: Ava's personality prompt + LLM + output parsing
    # Why pass summary? For long conversations, include previous chat summary
    # Located in: ai_companion/graph/utils/chains.py (get_character_response_chain function)
    chain = get_character_response_chain(state.get("summary", ""))
    
    # STEP 3: Generate the response using ALL available context
    # This is where the magic happens! All context pieces come together
    response = await chain.ainvoke(
        {
            # Everything that's been said in this conversation
            "messages": state["messages"],
            # What Ava is currently doing ("coding", "reading papers", etc.)
            "current_activity": current_activity,
            # What she knows about you personally ("developer", "likes pizza", etc.)
            "memory_context": memory_context,
        },
        config,  # LLM configuration (temperature, timeouts, etc.)
    )
    
    # STEP 4: Return the response as an AIMessage and update the conversation
    # Why AIMessage? LangChain message type that represents Ava's responses
    # This gets added to state["messages"] so future nodes see the full conversation
    return {"messages": AIMessage(content=response)}


async def image_node(state: AICompanionState, config: RunnableConfig):
    """🖼️ IMAGE RESPONSE GENERATOR - Creates visual responses
    
    Two-step process:
    1. Generate image of Ava's current activity using FLUX model
    2. Create text caption to accompany the image
    
    Example: You ask "What are you up to?" 
    → Generates image of Ava coding + text "Working on ML project!"
    """
    current_activity = ScheduleContextGenerator.get_current_activity()
    memory_context = state.get("memory_context", "")

    chain = get_character_response_chain(state.get("summary", ""))  # For text caption
    text_to_image_module = get_text_to_image_module()  # FLUX image generator

    # Step 1: Create image scenario based on recent conversation
    scenario = await text_to_image_module.create_scenario(state["messages"][-5:])  # Last 5 messages
    os.makedirs("generated_images", exist_ok=True)  # Ensure folder exists
    img_path = f"generated_images/image_{str(uuid4())}.png"  # Unique filename
    await text_to_image_module.generate_image(scenario.image_prompt, img_path)  # Generate actual image

    # Step 2: Tell LLM what image was generated (so caption matches image)
    scenario_message = HumanMessage(content=f"<image attached by Ava generated from prompt: {scenario.image_prompt}>")
    updated_messages = state["messages"] + [scenario_message]  # Add image context

    # Generate text caption that goes with the image
    response = await chain.ainvoke(
        {
            "messages": updated_messages,         # Includes image description
            "current_activity": current_activity, # What Ava is doing
            "memory_context": memory_context,     # What she knows about you
        },
        config,
    )

    return {"messages": AIMessage(content=response), "image_path": img_path}  # Text + image path


async def audio_node(state: AICompanionState, config: RunnableConfig):
    """🎵 VOICE RESPONSE GENERATOR - Creates Ava's voice notes
    
    Two-step process:
    1. Generate text response (same as conversation_node)
    2. Convert text to speech using ElevenLabs TTS
    
    Result: Ava sends you a voice note instead of text!
    """
    current_activity = ScheduleContextGenerator.get_current_activity()
    memory_context = state.get("memory_context", "")

    chain = get_character_response_chain(state.get("summary", ""))  # Generate text first
    text_to_speech_module = get_text_to_speech_module()  # ElevenLabs TTS

    # Step 1: Generate text response (same logic as conversation_node)
    response = await chain.ainvoke(
        {
            "messages": state["messages"],      # Conversation history
            "current_activity": current_activity, # What Ava is doing
            "memory_context": memory_context,     # What she knows about you
        },
        config,
    )
    # Step 2: Convert text to speech using Ava's voice
    output_audio = await text_to_speech_module.synthesize(response)  # Text → Audio bytes

    return {"messages": response, "audio_buffer": output_audio}  # Text + audio data


async def summarize_conversation_node(state: AICompanionState):
    """📝 MEMORY COMPRESSION - Prevents Ava from "forgetting" long conversations
    
    When chat gets too long (hits token limits):
    1. Creates/updates conversation summary
    2. Deletes old messages, keeps recent ones
    3. Summary becomes context for future responses
    
    Example: "User asked about weather, discussed weekend plans, shared work updates"
    """
    # LLM for summarization
    model = get_chat_model()  
    # Existing summary (if any)
    summary = state.get("summary", "")  

    # Different prompt depending on whether summary already exists
    if summary:
        # Update existing summary with new messages
        summary_message = (
            f"This is summary of the conversation to date between Ava and the user: {summary}\n\n"
            "Extend the summary by taking into account the new messages above:"
        )
    else:
        # Create first summary
        summary_message = (
            "Create a summary of the conversation above between Ava and the user. "
            "The summary must be a short description of the conversation so far, "
            "but that captures all the relevant information shared between Ava and the user:"
        )

    messages = state["messages"] + [HumanMessage(content=summary_message)]  # Add summary prompt
    response = await model.ainvoke(messages)  # Generate summary

    # Keep only recent messages, delete the rest (memory management)
    delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][: -settings.TOTAL_MESSAGES_AFTER_SUMMARY]]
    return {"summary": response.content, "messages": delete_messages}  # New summary + cleaned messages


async def memory_extraction_node(state: AICompanionState):
    """🧠 MEMORY WRITER - Stores important facts about YOU in long-term memory
    
    Analyzes your message for personal information worth remembering:
    - "I'm a developer" → stores "User is a software developer"
    - "I live in NYC" → stores "User lives in New York City"
    - "I love pizza" → stores "User enjoys eating pizza"
    
    ⚠️ BUG: Missing user isolation! All users share same memory.
    """
    if not state["messages"]:  # Safety check
        return {}

    # Vector database manager
    memory_manager = get_memory_manager()  
    # Extract important info from your latest message and store in Qdrant
    await memory_manager.extract_and_store_memories(state["messages"][-1])
    # Doesn't update state, just stores to database
    return {}  


def memory_injection_node(state: AICompanionState):
    """🧠 MEMORY READER - Retrieves what Ava remembers about YOU
    
    Uses semantic search to find relevant memories:
    1. Takes your recent messages as search query
    2. Finds similar memories from vector database
    3. Formats them for Ava's personality prompt
    
    Example: You mention "work" → retrieves "User is a developer"
    ⚠️ BUG: No user isolation! Might get other users' memories.
    """
    # Vector database manager
    memory_manager = get_memory_manager()  

    # Create search query from your recent messages (last 3)
    recent_context = " ".join([m.content for m in state["messages"][-3:]])
    # Semantic search: find memories similar to current conversation
    memories = memory_manager.get_relevant_memories(recent_context)

    # Convert memories to text format for LLM prompt
    memory_context = memory_manager.format_memories_for_prompt(memories)

    # Updates state with your memories
    return {"memory_context": memory_context} 
