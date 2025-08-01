"""
🚪 WHATSAPP PRODUCTION INTERFACE - Where Ava talks to real users through WhatsApp Business API

WHAT IS THIS FILE?
This is Ava's production brain interface for WhatsApp. When real users send messages to Ava's
WhatsApp number, this file processes them through the SAME LangGraph workflow as Chainlit,
then sends responses back through WhatsApp Business API.

BEGINNER CONCEPTS YOU NEED TO KNOW:

📱 WHAT IS WHATSAPP BUSINESS API?
WhatsApp Business API is Meta's system that lets programs (like Ava) send and receive
WhatsApp messages programmatically. Think of it like Ava having her own WhatsApp account
that can automatically respond to thousands of users simultaneously.
- Regular WhatsApp: You manually type messages on your phone
- WhatsApp Business API: Ava's LangGraph brain automatically processes and responds
- Same end result: Users get messages in their normal WhatsApp app

🔗 WHAT ARE WEBHOOKS IN AVA'S CONTEXT?
Webhooks are how WhatsApp instantly notifies Ava when someone sends a message.
Instead of Ava constantly asking "any new messages?", WhatsApp immediately sends
a notification to whatsapp_handler() function whenever a message arrives.
- User sends message → WhatsApp servers receive it → Webhook fired → whatsapp_handler() called
- This enables instant responses like a real conversation

🌐 WHAT IS HTTP IN AVA'S ARCHITECTURE?
HTTP is the communication protocol between Ava and WhatsApp's servers.
- WhatsApp sends webhooks via HTTP POST to our server
- Ava sends responses back via HTTP POST to WhatsApp API
- Different from Chainlit which uses WebSocket connections for real-time chat

📦 WHAT IS ASYNC PROCESSING FOR AVA?
Async lets Ava handle multiple WhatsApp conversations simultaneously without blocking.
- User A sends message → Ava starts processing (doesn't wait)
- User B sends message → Ava processes this too (parallel processing)
- Both get responses as soon as Ava's LangGraph workflow completes
- Critical for production: thousands of users can chat with Ava at once

THE COMPLETE AVA WHATSAPP FLOW:
1. User sends message to Ava's WhatsApp number
2. WhatsApp Business API receives message on Meta servers
3. Meta fires webhook → calls whatsapp_handler() function
4. whatsapp_handler() extracts message content (text/image/audio)
5. Content processed through IDENTICAL LangGraph workflow as Chainlit
6. Ava's response flows through router_node → conversation/image/audio nodes
7. send_response() delivers Ava's response via WhatsApp Business API
8. User receives Ava's response in their WhatsApp app

REAL-WORLD ANALOGY GROUNDED IN AVA'S FUNCTIONALITY:
This file is like Ava's WhatsApp office that handles real customer service:
- whatsapp_handler() is Ava's receptionist that receives all incoming calls (webhooks)
- The LangGraph workflow is Ava's brain that processes each conversation
- send_response() is Ava's communication system that calls customers back
- Each phone number gets its own conversation thread (user isolation)
- The SAME Ava personality and intelligence as the Chainlit demo, just different communication method

COMPARED TO CHAINLIT INTERFACE:
┌─────────────────┬─────────────────┬──────────────────────┐
│ Feature         │ WhatsApp        │ Chainlit             │
├─────────────────┼─────────────────┼──────────────────────┤
│ Users           │ Real customers  │ Demo/development     │
│ Authentication  │ Phone numbers   │ None (open demo)     │
│ Media Handling  │ Download from   │ Direct file access   │
│                 │ Meta servers    │                      │
│ Response Method │ HTTP POST to    │ Chainlit elements    │
│                 │ WhatsApp API    │                      │
│ Session ID      │ Phone number    │ Fixed thread_id = 1  │
│ Error Handling  │ Production-     │ Development-friendly │
│                 │ grade logging   │                      │
│ Ava Brain       │ IDENTICAL       │ IDENTICAL            │
└─────────────────┴─────────────────┴──────────────────────┘

WEBHOOK SECURITY:
WhatsApp requires webhook verification to prevent spam:
- GET request: Verify webhook with secret token
- POST request: Process actual messages

CROSS-SYSTEM CONNECTIONS:
- graph_builder: IDENTICAL Ava brain as Chainlit interface
- AsyncSqliteSaver: SAME conversation persistence mechanism  
- AI modules: SAME speech/image processing as Chainlit
- settings.py: SAME configuration across all interfaces

PRODUCTION CONSIDERATIONS:
- Handles multiple concurrent users (phone number isolation)
- Robust error handling and logging for debugging
- Media download from WhatsApp servers (not local files)
- HTTP response codes for WhatsApp API reliability
"""

# STANDARD LIBRARY IMPORTS - Python's built-in tools we need

# logging = Python's built-in error reporting system (like a black box recorder for problems)
# Think of it like a flight recorder that saves what went wrong when Ava crashes
import logging

# os = Python's tool for reading environment variables (secret settings stored outside code)
# Like reading Ava's API keys from a secure lockbox instead of hardcoding them in files
import os

# BytesIO = Python's tool for handling files in memory (like a temporary file holder)
# When users send images/audio, we need to hold the file data in memory to process it
# Think of it like a temporary clipboard that holds file contents while Ava works on them
from io import BytesIO

# Dict = Python's type hint for dictionary data structures (key-value pairs)
# Helps code editors and developers understand what type of data functions expect
# Like labeling a box "contains WhatsApp message data" instead of just "contains stuff"
from typing import Dict

# EXTERNAL LIBRARY IMPORTS - Third-party tools for specific functionality

# httpx = Modern HTTP client library for making web requests (like a web browser for Python)
# This is how Ava talks to WhatsApp's servers - sending and receiving data over the internet
# AsyncClient() = version that can handle multiple requests at once (non-blocking)
# Think of it like Ava having multiple phone lines to talk to WhatsApp instead of just one
import httpx

# FastAPI components for building web servers that receive HTTP requests
# APIRouter = organizes related web endpoints together (like grouping related phone extensions)
# Request = incoming data from WhatsApp (like an envelope with message contents)
# Response = outgoing data back to WhatsApp (like a reply letter with status codes)
from fastapi import APIRouter, Request, Response

# LangChain message format - standardized way to represent chat messages
# HumanMessage = wrapper that tells Ava "this message came from a human user"
# Same format used in Chainlit interface, so Ava's brain processes WhatsApp and web messages identically
from langchain_core.messages import HumanMessage

# AsyncSqliteSaver = LangGraph's conversation memory system using SQLite database
# Stores conversation history so Ava remembers what you talked about previously
# AsyncSqliteSaver = version that doesn't block other conversations while saving memory
# Think of it like Ava's diary that she writes in without stopping her conversations
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

# AVA'S CORE BRAIN COMPONENTS - The same AI modules used in Chainlit interface

# graph_builder = Ava's complete workflow system (the conductor that orchestrates all AI modules)
# Contains the IDENTICAL LangGraph workflow: memory→router→context→response nodes
# Same brain that processes messages in Chainlit web interface, just different input/output methods
from ai_companion.graph import graph_builder

# AI processing modules for different media types (same capabilities as Chainlit)
# ImageToText = Ava's vision system (analyzes photos users send via WhatsApp)
# SpeechToText = Ava's hearing system (transcribes voice messages to text for processing)
# TextToSpeech = Ava's speaking system (converts Ava's text responses to audio files)
from ai_companion.modules.image import ImageToText
from ai_companion.modules.speech import SpeechToText, TextToSpeech

# settings = Ava's configuration file containing API keys, model choices, database paths
# Shared across all interfaces so Chainlit and WhatsApp use same AI models and settings
from ai_companion.settings import settings

# CREATE LOGGER INSTANCE - Sets up error reporting for this specific file
# __name__ = automatic variable containing this file's name ("whatsapp_response")
# Think of this like creating a labeled logbook specifically for WhatsApp problems
# When something goes wrong, errors get written to this logbook with timestamps
logger = logging.getLogger(__name__)

# GLOBAL AI MODULE INSTANCES - Create once, reuse for all users (performance optimization)

# Why create these globally instead of inside functions?
# These AI modules are expensive to initialize (load models, connect to APIs)
# Creating them once at startup and reusing them is much faster than recreating for each message
# Think of it like keeping Ava's brain modules "warmed up" and ready to process any user's message

# speech_to_text = Ava's hearing system using Whisper AI model via Groq API
# Converts audio files (voice messages) into text that Ava's LangGraph brain can understand
# Same instance used in Chainlit interface - consistent speech processing across all interfaces
speech_to_text = SpeechToText()

# text_to_speech = Ava's speaking system using ElevenLabs API
# Converts Ava's text responses into realistic speech audio files
# Same instance used in Chainlit interface - consistent voice across all interfaces
text_to_speech = TextToSpeech()

# image_to_text = Ava's vision system using multimodal AI models
# Analyzes images and describes what Ava "sees" in text format for LangGraph processing
# Same instance used in Chainlit interface - consistent image understanding across interfaces
image_to_text = ImageToText()

# CREATE FASTAPI ROUTER - Organizes all WhatsApp-related web endpoints
# APIRouter() = creates a group of related web endpoints (like organizing related phone extensions)
# This router gets connected to the main server in webhook_endpoint.py
# Think of it like creating a "WhatsApp department" within Ava's web server
whatsapp_router = APIRouter()

# LOAD WHATSAPP BUSINESS API CREDENTIALS FROM ENVIRONMENT VARIABLES
# Environment variables = secure way to store secrets outside of code files
# These get set on the server where Ava runs, not hardcoded in the source code

# os.getenv() = Python function that reads environment variables (like reading from a secure lockbox)
# Returns None if the environment variable doesn't exist (safer than crashing)

# WHATSAPP_TOKEN = Secret key that proves to Meta's servers that we're authorized to use WhatsApp API
# Like Ava's ID card that lets her send/receive messages through WhatsApp Business
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")

# WHATSAPP_PHONE_NUMBER_ID = Identifies which business phone number Ava uses for messaging
# Not the actual phone number, but Meta's internal ID that references Ava's WhatsApp number
# Like how your credit card has both a number and an internal bank ID
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")


@whatsapp_router.api_route("/whatsapp_response", methods=["GET", "POST"])
async def whatsapp_handler(request: Request) -> Response:
    """
    🎯 MAIN WEBHOOK HANDLER - The heart of WhatsApp message processing
    
    WHAT IT DOES:
    This is the main entry point for ALL WhatsApp interactions. Handles:
    - Webhook verification (GET requests from Meta)
    - Message processing (POST requests with actual user messages)
    - Multi-modal content (text, images, voice messages)
    - Response delivery back to WhatsApp users
    
    THE WHATSAPP WEBHOOK FLOW:
    1. User sends message in WhatsApp app
    2. Meta receives message on their servers
    3. Meta sends HTTP POST to this function
    4. We process through IDENTICAL Ava brain (same as Chainlit)
    5. We send response back to Meta's API
    6. Meta delivers response to user's WhatsApp
    
    WEBHOOK SECURITY (GET REQUEST):
    WhatsApp requires webhook verification to ensure your server is legitimate:
    - Meta sends GET request with hub.verify_token and hub.challenge
    - We check token matches our WHATSAPP_VERIFY_TOKEN environment variable
    - If match: return hub.challenge (verification successful)
    - If no match: return 403 error (blocks connection)
    
    MESSAGE PROCESSING (POST REQUEST):
    Real message handling with the exact same pipeline as Chainlit:
    1. Extract message content (text/image/audio)
    2. Use phone number as session_id (user isolation)
    3. Process through graph_builder (IDENTICAL to Chainlit)
    4. Send appropriate response type via WhatsApp API
    
    CROSS-SYSTEM CONNECTIONS:
    - graph_builder.compile(): IDENTICAL Ava brain as Chainlit
    - AsyncSqliteSaver: SAME conversation persistence mechanism
    - image_to_text/speech_to_text: SAME AI modules as Chainlit
    - Multi-modal responses: SAME workflow routing from router_node
    """

    # WEBHOOK VERIFICATION PROCESS (GET REQUEST FROM META)
    # When you set up WhatsApp Business API, Meta needs to verify your server is legitimate
    # This is like Meta calling your phone to confirm you actually control this webhook URL
    
    # request.method = HTTP method (GET, POST, etc.) that tells us what type of request this is
    # GET = verification request, POST = actual message data
    if request.method == "GET":
        
        # STEP 1: Extract verification parameters from the URL query string
        # Query parameters = data sent in the URL after the ? mark
        # Example URL: https://yourserver.com/whatsapp_response?hub.verify_token=abc123&hub.challenge=xyz789
        # request.query_params = dictionary containing {"hub.verify_token": "abc123", "hub.challenge": "xyz789"}
        params = request.query_params
        
        # STEP 2: Security check - verify the secret token matches what we expect
        # hub.verify_token = secret password that proves Meta is really talking to us (not a hacker)
        # We set WHATSAPP_VERIFY_TOKEN in our environment variables when setting up the webhook
        # params.get() = safely get value from dictionary (returns None if key doesn't exist)
        # os.getenv() = read our secret token from environment variables
        if params.get("hub.verify_token") == os.getenv("WHATSAPP_VERIFY_TOKEN"):
            
            # VERIFICATION SUCCESSFUL - Return the challenge code to complete handshake
            # hub.challenge = random code Meta sends that we must echo back to prove we received it
            # Like Meta saying "repeat this random number back to me to prove you got my message"
            # Response() = HTTP response object with content and status code
            # status_code=200 = HTTP "OK" status (successful response)
            return Response(content=params.get("hub.challenge"), status_code=200)
        
        # VERIFICATION FAILED - Reject the connection for security
        # If tokens don't match, this might be a hacker trying to connect to our webhook
        # status_code=403 = HTTP "Forbidden" status (access denied)
        return Response(content="Verification token mismatch", status_code=403)

    # ACTUAL MESSAGE PROCESSING (POST REQUEST FROM META)
    # This is where real user messages get processed through Ava's brain
    # POST requests contain the actual message data, not just verification
    
    # try/except = error handling block (like wearing a seatbelt while driving)
    # If anything goes wrong inside try, the except block handles the error gracefully
    try:
        
        # 🔍 ENVIRONMENT VARIABLE VALIDATION FOR DEBUGGING
        required_vars = [
            "GROQ_API_KEY", "ELEVENLABS_API_KEY", "ELEVENLABS_VOICE_ID",
            "TOGETHER_API_KEY", "QDRANT_URL", "QDRANT_API_KEY",
            "WHATSAPP_TOKEN", "WHATSAPP_PHONE_NUMBER_ID", "WHATSAPP_VERIFY_TOKEN"
        ]
        
        print("🔍 ENV VAR CHECK:")
        for var in required_vars:
            value = os.getenv(var)
            status = "✅ SET" if value else "❌ MISSING"
            # Don't log full values for security, just first/last few chars
            masked_value = f"{value[:4]}...{value[-4:]}" if value and len(value) > 8 else "MISSING"
            print(f"  {var}: {status} ({masked_value})")
        print()
        
        # STEP 1: PARSE THE WEBHOOK DATA FROM META
        # When users send messages, Meta packages the data in a complex nested structure
        # await = wait for this to complete (HTTP data might take time to arrive)
        # request.json() = convert incoming HTTP data from JSON string to Python dictionary
        # JSON = text format for structured data (like a standardized filing system)
        data = await request.json()
        
        # NAVIGATE META'S NESTED DATA STRUCTURE
        # Meta wraps message data in multiple layers: entry → changes → value → actual message
        # This is like opening nested envelopes: outer envelope → inner envelope → actual letter
        # data["entry"] = list of webhook entries (usually just one)
        # [0] = take the first (and usually only) entry
        # ["changes"] = list of changes in this entry (what happened)
        # [0] = take the first change
        # ["value"] = the actual webhook payload containing message data
        change_value = data["entry"][0]["changes"][0]["value"]
        
        # STEP 2: CHECK IF THIS IS AN ACTUAL MESSAGE (NOT A STATUS UPDATE)
        # Meta sends different webhook types: messages, status updates, etc.
        # "messages" in change_value = check if the dictionary contains a "messages" key
        # Only process if it's actually a message from a user, not a delivery receipt
        if "messages" in change_value:
            
            # EXTRACT MESSAGE DETAILS
            # change_value["messages"] = list of messages in this webhook (usually just one)
            # [0] = take the first message
            message = change_value["messages"][0]
            
            # from_number = user's phone number who sent this message
            # This is like caller ID - tells us who is talking to Ava
            # Example: "+15551234567"
            from_number = message["from"]
            
            # session_id = unique identifier for this user's conversation with Ava
            # We use phone number as session ID so each user gets their own conversation thread
            # Like giving each customer their own file folder in Ava's memory system
            # Different users with different phone numbers = completely separate conversations
            session_id = from_number

            # STEP 3: EXTRACT MESSAGE CONTENT BASED ON TYPE (TEXT/AUDIO/IMAGE)
            # Users can send different types of messages - Ava needs to handle all of them
            # This is the same multi-modal processing logic used in Chainlit interface
            
            # content = variable that will hold the final text for Ava's brain to process
            # Start with empty string, then fill based on message type
            content = ""
            
            # HANDLE VOICE MESSAGES
            # message["type"] = tells us what kind of message this is
            # "audio" = user sent a voice message (like a voicemail)
            if message["type"] == "audio":
                
                # Voice messages need special processing: download audio file → transcribe to text
                # await = wait for this to complete (downloading and transcribing takes time)
                # process_audio_message() = function that downloads audio and converts speech to text
                # Returns: transcribed text of what the user said in their voice message
                content = await process_audio_message(message)
            
            # HANDLE IMAGE MESSAGES    
            elif message["type"] == "image":
                
                # EXTRACT USER'S CAPTION (IF ANY)
                # Users can send images with optional text captions
                # message.get() = safely get value from dictionary (returns empty dict {} if key missing)
                # .get("caption", "") = get caption text, or empty string if no caption
                # This is like reading the text someone wrote below their photo
                content = message.get("image", {}).get("caption", "")
                
                # DOWNLOAD THE ACTUAL IMAGE FILE FROM META'S SERVERS
                # Meta doesn't send image data directly in webhook (too large for HTTP)
                # Instead they send an ID that we use to download the image separately
                # message["image"]["id"] = Meta's reference number for this image file
                # await = wait for download to complete (images can be large)
                # download_media() = function that gets actual image bytes from Meta's servers
                image_bytes = await download_media(message["image"]["id"])
                
                # ANALYZE IMAGE CONTENT USING AVA'S VISION
                # Now we have the image data, let Ava "see" what's in the picture
                try:
                    # image_to_text.analyze_image() = Ava's vision system (same as Chainlit)
                    # Takes: image data (bytes) and a prompt asking what to look for
                    # Returns: text description of what Ava sees in the image
                    # await = wait for AI vision processing to complete
                    description = await image_to_text.analyze_image(
                        image_bytes,  # The actual image data we downloaded
                        "Please describe what you see in this image in the context of our conversation.",
                    )
                    
                    # ADD IMAGE ANALYSIS TO CONTENT
                    # content += means "add this text to the end of existing content"
                    # f"..." = f-string formatting to insert the description variable
                    # Final content = user's caption + "\n[Image Analysis: what Ava saw]"
                    content += f"\n[Image Analysis: {description}]"
                    
                # HANDLE VISION PROCESSING ERRORS
                # except = catch any errors that happen in the try block above
                # If image analysis fails, log the error but continue processing (graceful degradation)
                except Exception as e:
                    # logger.warning() = record this problem in our error log for debugging
                    # f"..." = f-string to include the actual error message
                    logger.warning(f"Failed to analyze image: {e}")
            
            # HANDLE TEXT MESSAGES (DEFAULT CASE)
            else:
                # Regular text message - simplest case, just extract the text directly
                # message["text"]["body"] = the actual text content the user typed
                # Like reading someone's text message - no processing needed
                content = message["text"]["body"]

            # STEP 4: PROCESS THROUGH AVA'S BRAIN (IDENTICAL TO CHAINLIT PROCESSING)
            # Now we have the content text, send it through Ava's complete LangGraph workflow
            
            # 🔍 DEBUG: LOG MESSAGE PROCESSING START
            print(f"📋 STARTING LANGGRAPH PROCESSING:")
            print(f"  📱 User: {from_number}")
            print(f"  💬 Content: {content[:100]}{'...' if len(content) > 100 else ''}")
            print(f"  🔗 Session ID: {session_id}")
            print(f"  📄 Content Length: {len(content)} chars")
            print()
            
            # SETUP CONVERSATION MEMORY DATABASE CONNECTION
            # async with = Python context manager that automatically handles opening/closing resources
            # Like automatically locking/unlocking a file cabinet when you're done using it
            # AsyncSqliteSaver = Ava's memory system that remembers conversation history
            # .from_conn_string() = connect to SQLite database file at the specified path
            # settings.SHORT_TERM_MEMORY_DB_PATH = file path where conversation history is stored
            try:
                print(f"🔍 CONNECTING TO MEMORY DATABASE:")
                print(f"  📁 Database Path: {settings.SHORT_TERM_MEMORY_DB_PATH}")
                
                async with AsyncSqliteSaver.from_conn_string(settings.SHORT_TERM_MEMORY_DB_PATH) as short_term_memory:
                    print(f"✅ MEMORY DATABASE CONNECTED SUCCESSFULLY")
                    
                    # BUILD AVA'S COMPLETE WORKFLOW GRAPH
                    # graph_builder.compile() = creates Ava's complete LangGraph workflow
                    # checkpointer=short_term_memory = connect the memory system so Ava remembers conversations
                    # This creates the IDENTICAL workflow used in Chainlit: memory→router→context→response nodes
                    print(f"🔍 BUILDING LANGGRAPH WORKFLOW:")
                    print(f"  🧠 Compiling graph with memory checkpointer...")
                    
                    graph = graph_builder.compile(checkpointer=short_term_memory)
                    print(f"✅ LANGGRAPH WORKFLOW COMPILED SUCCESSFULLY")
                    
                    # PREPARE GRAPH INPUT DATA
                    # VALIDATE PHONE NUMBER FORMAT
                    # WhatsApp sends numbers without + prefix, but Vapi needs E.164 format
                    formatted_phone = from_number
                    if not formatted_phone.startswith('+'):
                        # Add + prefix if missing (WhatsApp sometimes omits it)
                        formatted_phone = f"+{formatted_phone}"
                        print(f"📱 PHONE NUMBER FORMATTING:")
                        print(f"  Original: {from_number}")
                        print(f"  Formatted: {formatted_phone}")
                    
                    graph_input = {
                        "messages": [HumanMessage(content=content)],  # Wrap user's text in LangChain message format
                        "user_phone_number": formatted_phone,         # Pass formatted phone number for voice calling
                        "user_id": from_number,                       # Use original phone as user ID
                        "interface": "whatsapp",                      # Track that this came from WhatsApp
                    }
                    graph_config = {"configurable": {"thread_id": session_id}}
                    
                    print(f"🔍 INVOKING LANGGRAPH WORKFLOW:")
                    print(f"  📨 Input: {len(graph_input)} keys")
                    print(f"  📱 Phone: {graph_input.get('user_phone_number')}")
                    print(f"  🆔 User ID: {graph_input.get('user_id')}")
                    print(f"  🌐 Interface: {graph_input.get('interface')}")
                    print(f"  🔧 Config: thread_id = {session_id}")
                    print(f"  🚀 Starting graph.ainvoke()...")
                    
                    # PROCESS USER MESSAGE THROUGH COMPLETE AVA WORKFLOW
                    # await = wait for Ava's brain to complete processing (this takes time)
                    # graph.ainvoke() = run the message through Ava's complete LangGraph workflow
                    await graph.ainvoke(graph_input, graph_config)
                    
                    print(f"✅ LANGGRAPH WORKFLOW COMPLETED SUCCESSFULLY")
                    
                    # HumanMessage(content=content) = tells Ava "this text came from a human user"
                    # thread_id: session_id = each phone number gets its own conversation thread
                    # This is how Ava keeps different users' conversations separate
                    
                    # GET AVA'S FINAL STATE AFTER PROCESSING
                    # After the workflow completes, we need to see what Ava decided to do
                    # await = wait for state retrieval to complete
                    # graph.aget_state() = get the final state of Ava's workflow
                    # config = same configuration (thread_id) to get the right conversation's state
                    print(f"🔍 RETRIEVING FINAL WORKFLOW STATE:")
                    print(f"  🔧 Config: thread_id = {session_id}")
                    
                    output_state = await graph.aget_state(config={"configurable": {"thread_id": session_id}})
                    print(f"✅ FINAL STATE RETRIEVED SUCCESSFULLY")
                    print(f"  📊 State Keys: {list(output_state.values.keys()) if output_state.values else 'None'}")
                    
            except Exception as graph_error:
                print(f"🚨 LANGGRAPH PROCESSING ERROR:")
                print(f"  📱 User: {from_number}")
                print(f"  💬 Content: {content[:100]}...")
                print(f"  ❌ Error: {str(graph_error)}")
                
                # Get detailed traceback
                import traceback
                full_traceback = traceback.format_exc()
                print(f"  📚 Full Traceback:\n{full_traceback}")
                
                # Log to standard logger as well
                logger.error(f"LangGraph processing failed for {from_number}: {str(graph_error)}\n{full_traceback}")
                
                # Re-raise the exception so outer try/catch handles it
                raise

            # STEP 5: EXTRACT AVA'S RESPONSE DETAILS FROM FINAL STATE
            # output_state.values = dictionary containing all data from Ava's workflow
            # This is like looking at Ava's final decision after thinking through the workflow
            
            # GET WORKFLOW TYPE (WHAT KIND OF RESPONSE AVA DECIDED TO GIVE)
            # .get("workflow", "conversation") = get the workflow value, default to "conversation" if missing
            # router_node in Ava's graph decides this: "conversation", "audio", or "image"
            # Like asking Ava "how do you want to respond - with text, voice, or a picture?"
            workflow = output_state.values.get("workflow", "conversation")
            
            # GET AVA'S RESPONSE TEXT
            # output_state.values["messages"] = list of all messages in conversation
            # [-1] = get the last message (most recent)
            # .content = the actual text content of that message (Ava's response)
            # This is what Ava wants to say to the user
            response_message = output_state.values["messages"][-1].content

            # STEP 6: SEND APPROPRIATE RESPONSE TYPE VIA WHATSAPP API
            # Based on router_node's decision, send different types of responses
            # This matches the exact same multi-modal handling used in Chainlit interface
            
            # AUDIO RESPONSE - AVA WANTS TO SEND A VOICE MESSAGE
            if workflow == "audio":
                
                # GET AUDIO DATA FROM AVA'S AUDIO_NODE
                # audio_buffer = the actual audio file data (bytes) that audio_node generated
                # This is Ava's voice saying the response_message text (ElevenLabs TTS)
                audio_buffer = output_state.values["audio_buffer"]
                
                # SEND VOICE MESSAGE TO USER
                # await = wait for message delivery to complete
                # send_response() = function that uploads media to WhatsApp and sends message
                # Returns: True if successful, False if failed
                success = await send_response(from_number, response_message, "audio", audio_buffer)
            
            # IMAGE RESPONSE - AVA WANTS TO SEND A GENERATED IMAGE    
            elif workflow == "image":
                
                # GET IMAGE FILE PATH FROM AVA'S IMAGE_NODE
                # image_path = file path where image_node saved the generated image
                # This is a picture Ava created using FLUX image generation AI
                image_path = output_state.values["image_path"]
                
                # READ IMAGE FILE FROM DISK
                # with open() = Python context manager that automatically closes files
                # "rb" = read in binary mode (for image files, not text)
                # f.read() = read the entire file contents into memory as bytes
                with open(image_path, "rb") as f:
                    image_data = f.read()
                
                # SEND IMAGE MESSAGE TO USER
                # await = wait for image upload and message delivery
                # response_message = caption text that goes with the image
                # image_data = actual image file bytes
                success = await send_response(from_number, response_message, "image", image_data)
            
            # VOICE CALL RESPONSE - AVA INITIATED A PHONE CALL
            elif workflow == "voice_call":
                
                # 📞 LOG VOICE CALL COMPLETION
                print(f"📞 VOICE CALL REQUEST COMPLETED:")
                print(f"  📱 User: {from_number}")
                print(f"  💬 Confirmation: {response_message[:100]}{'...' if len(response_message) > 100 else ''}")
                
                # SEND CONFIRMATION MESSAGE TO WHATSAPP
                # voice_calling_node has already initiated the call and prepared confirmation text
                # We just need to send this confirmation back to the user via WhatsApp
                # This lets them know the call is coming
                success = await send_response(from_number, response_message, "text")
                
                # LOG CALL TRACKING INFO (if available)
                if "active_call" in output_state.values and output_state.values["active_call"]:
                    call_details = output_state.values["active_call"]
                    print(f"📞 CALL TRACKING:")
                    print(f"  🆔 Call ID: {call_details.get('call_id', 'Unknown')}")
                    print(f"  ⏰ Initiated: {call_details.get('timestamp', 'Unknown')}")
                    print(f"  📋 Status: Call should ring within 10-15 seconds")
            
            # TEXT RESPONSE - AVA WANTS TO SEND A REGULAR TEXT MESSAGE (MOST COMMON)
            else:
                # SEND TEXT MESSAGE TO USER
                # No media needed, just send Ava's response text directly
                # This is the most common case - regular conversation
                success = await send_response(from_number, response_message, "text")

            # STEP 7: RETURN HTTP STATUS CODE TO META (CONFIRM WE PROCESSED THE MESSAGE)
            # Meta's servers are waiting for our response to know if message processing succeeded
            # HTTP status codes = standardized numbers that indicate success/failure
            
            # CHECK IF MESSAGE DELIVERY FAILED
            # success = boolean (True/False) returned by send_response() function
            # if not success = if message delivery failed
            if not success:
                # RETURN ERROR STATUS TO META
                # status_code=500 = "Internal Server Error" (something went wrong on our end)
                # Meta will see this and know the message wasn't processed successfully
                return Response(content="Failed to send message", status_code=500)
            
            # MESSAGE PROCESSED SUCCESSFULLY
            # status_code=200 = "OK" (everything worked perfectly)
            # Meta sees this and marks the webhook as successfully processed
            return Response(content="Message processed", status_code=200)

        # HANDLE STATUS UPDATES (NOT ACTUAL MESSAGES)
        elif "statuses" in change_value:
            # Status updates = notifications about message delivery ("delivered", "read", etc.)
            # These aren't messages from users, just Meta telling us about delivery status
            # We acknowledge receipt but don't need to process through Ava's brain
            # Like getting a "message delivered" notification - we note it but don't respond
            return Response(content="Status update received", status_code=200)

        # HANDLE UNKNOWN WEBHOOK TYPES
        else:
            # Sometimes Meta sends webhook types we don't recognize
            # Better to reject these explicitly rather than trying to process them
            # status_code=400 = "Bad Request" (we don't understand this type of data)
            return Response(content="Unknown event type", status_code=400)

    # HANDLE ANY ERRORS THAT OCCURRED DURING PROCESSING
    # except Exception as e = catch ANY error that happened in the try block above
    # This is our safety net - if anything goes wrong, we handle it gracefully
    except Exception as e:
        
        # 🚨 ENHANCED ERROR LOGGING FOR DEBUGGING
        import traceback
        
        # GET DETAILED ERROR INFORMATION
        error_msg = f"Error processing message: {str(e)}"
        full_traceback = traceback.format_exc()
        
        # LOG ERROR DETAILS MULTIPLE WAYS FOR VISIBILITY
        print(f"🚨 WEBHOOK ERROR: {error_msg}")
        print(f"🚨 FULL TRACEBACK:\n{full_traceback}")
        
        # Also log using standard logger
        logger.error(f"{error_msg}\n{full_traceback}")
        
        # RETURN GENERIC ERROR TO META (DON'T EXPOSE INTERNAL DETAILS)
        # status_code=500 = "Internal Server Error"
        # We log detailed errors privately but return generic message publicly for security
        return Response(content="Internal server error", status_code=500)


async def download_media(media_id: str) -> bytes:
    """
    📥 MEDIA DOWNLOADER - Downloads user images/videos for Ava's image_to_text analysis
    
    WHAT IT DOES:
    When users send images to Ava via WhatsApp, Meta doesn't include the actual image
    in the webhook. Instead, they send a media_id that this function uses to download
    the image so Ava's image_to_text module can analyze what the user shared.
    
    THE TWO-STEP DOWNLOAD PROCESS:
    1. Get metadata: Use media_id to get actual download URL from Meta's Graph API
    2. Download file: Use download URL to get the actual image bytes for image_to_text
    
    WHY TWO STEPS IN AVA'S WORKFLOW?
    Security and efficiency. Meta doesn't want to send large files in webhooks to whatsapp_handler(),
    and they control access with time-limited URLs so only Ava can download the user's image.
    
    GROUNDED ANALOGY FOR AVA:
    This function is like Ava's image pickup service:
    - User sends photo → WhatsApp gives Ava a pickup ticket (media_id)
    - This function goes to Meta's storage facility with the ticket
    - Downloads the actual image for Ava's image_to_text brain to analyze
    - Just like how Chainlit gets images directly, but WhatsApp requires this extra step
    
    CROSS-SYSTEM CONNECTION IN AVA'S WORKFLOW:
    - Called by: whatsapp_handler() when processing image messages (line 172)
    - Returns: Raw image bytes that get passed to image_to_text.analyze_image() (line 176)
    - Different from Chainlit: Chainlit reads files directly, WhatsApp requires API download
    - Same destination: Both end up feeding image_to_text module for Ava's vision analysis
    
    SECURITY NOTES FOR AVA'S PRODUCTION:
    - Download URLs expire quickly (minutes) for security
    - Requires valid WHATSAPP_TOKEN for authentication with Meta
    - Media is automatically deleted from Meta servers after a few days
    """
    # STEP 1: GET MEDIA METADATA FROM META'S GRAPH API
    # We can't download the image directly - we need to ask Meta for a download URL first
    
    # BUILD THE API URL FOR GETTING METADATA
    # f"..." = f-string formatting to insert the media_id variable
    # media_id = the ID number Meta gave us in the webhook for this specific image
    # Graph API v21.0 = Meta's current API version for WhatsApp Business
    media_metadata_url = f"https://graph.facebook.com/v21.0/{media_id}"
    
    # CREATE AUTHENTICATION HEADERS
    # headers = dictionary containing HTTP headers (like an envelope's address info)
    # Authorization header = proves to Meta that we're allowed to access this image
    # Bearer token = specific format Meta expects for API authentication
    # f"Bearer {WHATSAPP_TOKEN}" = combines "Bearer " + our secret token
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}"}

    # CREATE HTTP CLIENT FOR MAKING WEB REQUESTS
    # async with = context manager that automatically cleans up the client when done
    # httpx.AsyncClient() = creates a web request client that can handle multiple requests simultaneously
    # Think of this like opening a web browser that can download files from Meta's servers
    async with httpx.AsyncClient() as client:
        
        # MAKE API REQUEST TO GET IMAGE METADATA
        # await = wait for this web request to complete (internet requests take time)
        # client.get() = make an HTTP GET request (like clicking a link)
        # headers=headers = include our authentication info with the request
        metadata_response = await client.get(media_metadata_url, headers=headers)
        
        # CHECK IF THE API REQUEST SUCCEEDED
        # .raise_for_status() = check if Meta returned an error (like 404 not found, 403 forbidden)
        # If there's an error, this throws an exception that gets caught by our outer try/except
        metadata_response.raise_for_status()
        
        # PARSE THE METADATA RESPONSE
        # .json() = convert Meta's JSON response text into a Python dictionary
        # JSON = text format for structured data (like a standardized way to organize information)
        metadata = metadata_response.json()
        
        # EXTRACT THE ACTUAL DOWNLOAD URL
        # metadata.get("url") = get the "url" field from Meta's response dictionary
        # This URL is where the actual image file is stored on Meta's servers
        # It's time-limited and expires quickly for security
        download_url = metadata.get("url")

        # STEP 2: DOWNLOAD THE ACTUAL IMAGE FILE USING THE DOWNLOAD URL
        # Now we use the download URL to get the actual image bytes
        
        # MAKE SECOND REQUEST TO DOWNLOAD THE IMAGE
        # await = wait for image download to complete (image files can be large)
        # client.get() = make HTTP GET request to the download URL
        # headers=headers = still need authentication even for the download
        media_response = await client.get(download_url, headers=headers)
        
        # CHECK IF THE DOWNLOAD SUCCEEDED
        # .raise_for_status() = ensure the download worked (didn't get 404, 403, etc.)
        media_response.raise_for_status()
        
        # RETURN THE RAW IMAGE BYTES
        # .content = the actual binary data of the image file
        # These bytes can be fed to Ava's image_to_text module for analysis
        # Like getting the actual photo data that Ava's vision can "see"
        return media_response.content


async def process_audio_message(message: Dict) -> str:
    """
    🎤 VOICE MESSAGE PROCESSOR - Downloads and transcribes user voice messages for Ava's LangGraph brain
    
    WHAT IT DOES:
    When users send voice messages to Ava via WhatsApp, this function downloads the audio
    from Meta servers and transcribes it to text so Ava's LangGraph workflow can process
    the user's spoken words through the same conversation pipeline as text messages.
    
    AVA'S VOICE PROCESSING PIPELINE:
    User Voice → WhatsApp servers → download_media pattern → speech_to_text transcription → LangGraph workflow
    
    GROUNDED ANALOGY FOR AVA'S VOICE UNDERSTANDING:
    This function is like Ava's listening and transcription service:
    - User speaks to Ava via voice message (like leaving a voicemail)
    - This function downloads the audio (like retrieving the voicemail file)
    - speech_to_text transcribes it (like Ava listening and writing down what user said)
    - Transcribed text goes to LangGraph workflow (same as if user typed the message)
    - End result: Ava understands voice just like text, processes through same conversation_node
    
    COMPARED TO CHAINLIT VOICE HANDLING:
    - Chainlit: Direct audio buffer from real-time recording in web interface
    - WhatsApp: Download from Meta servers first, then transcribe
    - Processing: IDENTICAL speech_to_text module and Whisper model
    - Destination: Same LangGraph workflow processes the transcribed text
    
    CROSS-SYSTEM CONNECTIONS IN AVA'S WORKFLOW:
    - Called by: whatsapp_handler() for audio message type (line 165)
    - Uses: SAME speech_to_text.transcribe() module as Chainlit interface
    - Returns: Transcribed text that gets processed through IDENTICAL LangGraph workflow
    - Audio formats: WhatsApp typically sends .ogg files, Whisper handles automatically
    - Flow continues: Transcribed text → LangGraph → router_node → conversation/image/audio nodes
    
    PRODUCTION CONSIDERATIONS FOR AVA:
    - WhatsApp voice messages can be up to 16MB (long recordings)
    - Download URLs expire quickly, so we process immediately
    - Transcription costs apply per minute of audio (Groq Whisper pricing)
    """
    # STEP 1: EXTRACT AUDIO ID FROM WHATSAPP MESSAGE
    # WhatsApp voice messages are stored the same way as images - by ID reference
    # message["audio"] = dictionary containing audio message details
    # ["id"] = Meta's reference number for this specific voice message file
    audio_id = message["audio"]["id"]
    
    # STEP 2: GET AUDIO METADATA (SAME TWO-STEP PROCESS AS DOWNLOAD_MEDIA)
    # Voice messages use the exact same download pattern as images
    
    # BUILD API URL FOR AUDIO METADATA
    # f"..." = f-string to insert the audio_id into the URL
    # Same Graph API endpoint, just with audio ID instead of image ID
    media_metadata_url = f"https://graph.facebook.com/v21.0/{audio_id}"
    
    # CREATE AUTHENTICATION HEADERS (SAME AS IMAGE DOWNLOAD)
    # headers = dictionary with authentication info for Meta's API
    # Authorization header proves we're allowed to access this voice message
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}"}

    # GET AUDIO METADATA FROM META
    # async with = context manager for HTTP client (automatically cleans up)
    # httpx.AsyncClient() = web request client for talking to Meta's servers
    async with httpx.AsyncClient() as client:
        
        # REQUEST METADATA FROM META'S GRAPH API
        # await = wait for this web request to complete
        # client.get() = HTTP GET request to get audio file information
        metadata_response = await client.get(media_metadata_url, headers=headers)
        
        # CHECK IF METADATA REQUEST SUCCEEDED
        # .raise_for_status() = throw error if Meta returned failure code
        metadata_response.raise_for_status()
        
        # PARSE METADATA RESPONSE
        # .json() = convert Meta's JSON response into Python dictionary
        metadata = metadata_response.json()
        
        # EXTRACT DOWNLOAD URL FROM METADATA
        # metadata.get("url") = get the actual download URL for the audio file
        download_url = metadata.get("url")

    # STEP 3: DOWNLOAD THE ACTUAL AUDIO FILE
    # Now use the download URL to get the voice message bytes
    
    # CREATE NEW HTTP CLIENT FOR DOWNLOAD REQUEST
    # async with = second context manager for the download request
    # We could reuse the previous client, but this is clearer
    async with httpx.AsyncClient() as client:
        
        # DOWNLOAD THE VOICE MESSAGE FILE
        # await = wait for audio file download (voice messages can be several MB)
        # client.get() = HTTP GET request to the download URL
        # headers=headers = still need authentication for the actual download
        audio_response = await client.get(download_url, headers=headers)
        
        # CHECK IF DOWNLOAD SUCCEEDED
        # .raise_for_status() = ensure download worked (no 404, 403, etc.)
        audio_response.raise_for_status()

    # STEP 4: PREPARE AUDIO DATA FOR TRANSCRIPTION
    # Convert the raw audio bytes into a format Ava's speech_to_text can process
    
    # CREATE AUDIO BUFFER IN MEMORY
    # BytesIO() = creates a file-like object in memory (like a temporary audio file)
    # audio_response.content = the raw audio file bytes we downloaded
    # This is like putting the voice message into a temporary audio player
    audio_buffer = BytesIO(audio_response.content)
    
    # RESET BUFFER POSITION TO START
    # .seek(0) = move to the beginning of the audio file
    # Like rewinding a tape to the beginning before playing it
    audio_buffer.seek(0)
    
    # READ COMPLETE AUDIO FILE INTO MEMORY
    # .read() = read all audio data from the buffer
    # audio_data = the complete voice message as bytes, ready for Whisper processing
    audio_data = audio_buffer.read()

    # STEP 5: TRANSCRIBE USING SAME MODULE AS CHAINLIT INTERFACE
    # Now feed the audio data to Ava's speech recognition system
    # await = wait for Whisper AI to transcribe the speech (can take several seconds)
    # speech_to_text.transcribe() = IDENTICAL function used in Chainlit interface
    # Returns: text string of what the user said in their voice message
    return await speech_to_text.transcribe(audio_data)


async def send_response(
    from_number: str,
    response_text: str,
    message_type: str = "text",
    media_content: bytes = None,
) -> bool:
    """
    📤 RESPONSE SENDER - Delivers Ava's LangGraph responses back to WhatsApp users
    
    WHAT IT DOES:
    The final step in Ava's WhatsApp workflow - takes responses generated by Ava's
    LangGraph nodes (conversation_node, image_node, audio_node) and delivers them
    to users through WhatsApp Business API based on router_node decisions.
    
    AVA'S MULTI-MODAL RESPONSE PIPELINE:
    Ava's Brain (LangGraph) → router_node decision → Response Generated → This Function → WhatsApp API → User's Phone
    
    GROUNDED ANALOGY FOR AVA'S RESPONSE DELIVERY:
    This function is like Ava's delivery service that adapts to different message types:
    - Text responses: Ava's conversation_node generates text → delivered directly via WhatsApp API
    - Image responses: Ava's image_node creates image → upload_media() first → then deliver with caption
    - Audio responses: Ava's audio_node generates voice → upload_media() first → then deliver as voice message
    - Just like how Chainlit displays different UI elements, this sends different WhatsApp message types
    
    AVA'S MULTI-MODAL HANDLING:
    1. Text: conversation_node output sent as simple JSON to WhatsApp API
    2. Audio: audio_node buffer uploaded via upload_media(), then sent with media_id reference
    3. Image: image_node file uploaded via upload_media(), then sent with caption and media_id
    4. Fallback: If media upload fails, fallback to text (keeps conversation flowing)
    
    CROSS-SYSTEM CONNECTIONS IN AVA'S WORKFLOW:
    - Called by: whatsapp_handler() with output from Ava's LangGraph state (lines 211, 218, 222)
    - Receives: response_text from conversation_node/image_node/audio_node
    - Receives: media_content from state.audio_buffer or state.image_path
    - Uses: upload_media() for audio/image delivery to WhatsApp servers
    - Compares to: Chainlit's cl.Message/cl.Audio/cl.Image UI elements (same content, different delivery)
    
    PRODUCTION RELIABILITY FOR AVA:
    - Returns bool for success/failure checking in whatsapp_handler()
    - Graceful fallback to text if media upload fails (keeps Ava responding)
    - Proper error logging for debugging user interaction issues
    """
    # CREATE STANDARD HEADERS FOR WHATSAPP BUSINESS API
    # headers = dictionary containing authentication and content type information
    # Every API request to Meta needs these headers to prove we're authorized
    headers = {
        # Authorization = proves we have permission to send messages
        # f"Bearer {WHATSAPP_TOKEN}" = specific format Meta expects for API tokens
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        
        # Content-Type = tells Meta what format our request data is in
        # "application/json" = we're sending structured JSON data
        "Content-Type": "application/json",
    }

    # HANDLE MEDIA RESPONSES (AUDIO & IMAGE FILES)
    # Audio and image responses require special handling: upload file first, then send message
    # Text responses can be sent directly without file upload
    
    # CHECK IF THIS IS A MEDIA RESPONSE
    # message_type in ["audio", "image"] = check if message type is either audio or image
    # if True = this is media, need special upload process
    # if False = this is text, can send directly
    if message_type in ["audio", "image"]:
        
        # TRY TO UPLOAD MEDIA FILE
        # try/except = error handling in case media upload fails
        # If upload fails, we'll fallback to text response to keep conversation flowing
        try:
            
            # DETERMINE MIME TYPE FOR FILE UPLOAD
            # MIME type = standard way to identify file formats (like file extensions)
            # Meta needs to know what type of file we're uploading
            # Conditional expression: "audio/mpeg" if audio, otherwise "image/png"
            mime_type = "audio/mpeg" if message_type == "audio" else "image/png"
            
            # PREPARE MEDIA DATA FOR UPLOAD
            # BytesIO() = creates file-like object in memory from raw bytes
            # media_content = the actual audio/image bytes from Ava's AI generation
            # This is like putting the file into a temporary container for uploading
            media_buffer = BytesIO(media_content)
            
            # UPLOAD MEDIA TO WHATSAPP SERVERS
            # await = wait for upload to complete (media files can be large)
            # upload_media() = function that uploads file to Meta and returns media_id
            # media_id = Meta's reference number for our uploaded file
            media_id = await upload_media(media_buffer, mime_type)
            
            # CREATE MESSAGE PAYLOAD WITH MEDIA REFERENCE
            # json_data = dictionary that will be sent to WhatsApp API as JSON
            json_data = {
                # messaging_product = tells Meta this is for WhatsApp (vs Instagram, etc.)
                "messaging_product": "whatsapp",
                
                # to = recipient's phone number (who gets this message)
                "to": from_number,
                
                # type = what kind of message this is ("audio" or "image")
                "type": message_type,
                
                # Dynamic key with media reference
                # message_type: {"id": media_id} creates either:
                # "audio": {"id": "123456"} OR "image": {"id": "789012"}
                # This tells WhatsApp "send the file we uploaded with this ID"
                message_type: {"id": media_id},
            }

            # ADD CAPTION FOR IMAGES (AUDIO DOESN'T SUPPORT CAPTIONS)
            # WhatsApp allows text captions with images but not with audio messages
            if message_type == "image":
                # Add Ava's response text as the image caption
                # json_data["image"]["caption"] = modifies the image section to include caption
                json_data["image"]["caption"] = response_text
        
        # HANDLE MEDIA UPLOAD ERRORS
        # except Exception as e = catch any error that happened during media upload
        except Exception as e:
            
            # LOG THE ERROR FOR DEBUGGING
            # logger.error() = record this problem in our error log
            # f"..." = f-string to include the actual error message
            logger.error(f"Media upload failed, falling back to text: {e}")
            
            # FALLBACK TO TEXT RESPONSE
            # If media upload fails, change message type to text so conversation continues
            # Better to send text than no response at all
            message_type = "text"

    # HANDLE TEXT RESPONSES (INCLUDING FALLBACK FROM FAILED MEDIA)
    # Text messages are the simplest and most reliable - no file upload needed
    # This handles both: 1) Normal text responses, 2) Fallback when media upload fails
    if message_type == "text":
        
        # CREATE TEXT MESSAGE PAYLOAD
        # json_data = dictionary that gets sent to WhatsApp API
        json_data = {
            # messaging_product = identifies this as WhatsApp message (vs other Meta products)
            "messaging_product": "whatsapp",
            
            # to = recipient's phone number (the user who sent us a message)
            "to": from_number,
            
            # type = "text" tells WhatsApp this is a simple text message
            "type": "text",
            
            # text = dictionary containing the actual message content
            # {"body": response_text} = puts Ava's response text in the message body
            "text": {"body": response_text},
        }

    # DEBUG OUTPUT (SHOULD BE REMOVED IN PRODUCTION)
    # These print statements help developers see what's being sent to WhatsApp
    # In production, this should be removed or replaced with proper logging
    print(headers)     # Shows authentication headers
    print(json_data)   # Shows message payload being sent

    # SEND MESSAGE VIA WHATSAPP BUSINESS API
    # Now make the actual HTTP request to deliver the message
    
    try:
        # CREATE HTTP CLIENT FOR API REQUEST
        # async with = context manager that automatically cleans up the client
        # httpx.AsyncClient() = web client for making HTTP requests to Meta's API
        async with httpx.AsyncClient() as client:
            
            # MAKE POST REQUEST TO WHATSAPP API
            # await = wait for message sending to complete
            # client.post() = HTTP POST request (sending data to Meta's servers)
            response = await client.post(
                # API URL: Graph API endpoint for sending messages
                # f"..." = f-string to insert our phone number ID
                f"https://graph.facebook.com/v21.0/{WHATSAPP_PHONE_NUMBER_ID}/messages",
                
                # headers = authentication and content type info
                headers=headers,
                
                # json = the message data (automatically converts dictionary to JSON)  
                json=json_data,
            )

        # 🚨 DETAILED WHATSAPP API RESPONSE LOGGING
        print(f"🔍 WHATSAPP API RESPONSE:")
        print(f"  Status Code: {response.status_code}")
        print(f"  Headers: {dict(response.headers)}")
        
        try:
            response_json = response.json()
            print(f"  Response Body: {response_json}")
        except:
            print(f"  Response Text: {response.text}")
        
        # CHECK FOR SUCCESS
        is_success = response.status_code == 200
        print(f"  Success: {is_success}")
        
        # LOG FAILURE DETAILS
        if not is_success:
            print(f"🚨 WHATSAPP API FAILED:")
            print(f"  Status: {response.status_code}")
            print(f"  Reason: {response.reason_phrase if hasattr(response, 'reason_phrase') else 'Unknown'}")
            
        return is_success
        
    except Exception as e:
        # 🚨 CATCH ANY HTTP/NETWORK ERRORS
        import traceback
        error_msg = f"WhatsApp API request failed: {str(e)}"
        full_traceback = traceback.format_exc()
        
        print(f"🚨 WHATSAPP API ERROR: {error_msg}")
        print(f"🚨 FULL TRACEBACK:\n{full_traceback}")
        logger.error(f"{error_msg}\n{full_traceback}")
        
        return False


async def upload_media(media_content: BytesIO, mime_type: str) -> str:
    """
    📁 MEDIA UPLOADER - Uploads Ava's LangGraph-generated media to WhatsApp servers for delivery
    
    WHAT IT DOES:
    Takes audio/image files generated by Ava's LangGraph nodes (audio_node/image_node)
    and uploads them to WhatsApp's servers so they can be delivered to users.
    This is the opposite of download_media() - instead of getting user media, 
    we're sending Ava's generated media.
    
    AVA'S MEDIA UPLOAD PIPELINE:
    1. Ava's audio_node generates voice (ElevenLabs TTS) OR image_node generates image (FLUX)
    2. send_response() calls this function to upload Ava's creation to WhatsApp servers
    3. WhatsApp returns media_id for the uploaded file
    4. send_response() uses media_id in message to reference Ava's uploaded media
    
    GROUNDED ANALOGY FOR AVA'S MEDIA SHARING:
    This function is like Ava's media publishing service:
    - Ava creates content (audio_node voice or image_node picture)
    - This function uploads it to WhatsApp's content servers (like posting to a platform)
    - WhatsApp gives us a media_id (like a URL to the posted content)
    - send_response() shares that media_id with the user (like sharing a link)
    - Reverse of download_media(): download gets user content for Ava, upload shares Ava content with user
    
    AVA'S SUPPORTED MEDIA TYPES:
    - Audio: MP3 files from Ava's audio_node using ElevenLabs TTS (same generation as Chainlit)
    - Images: PNG files from Ava's image_node using FLUX generation (same AI art as Chainlit)
    - Size limits: WhatsApp enforces limits (16MB audio, 5MB images)
    
    CROSS-SYSTEM CONNECTIONS IN AVA'S WORKFLOW:
    - Called by: send_response() for audio/image message types (lines 399, 449)
    - Receives: Audio buffer from state.audio_buffer (audio_node output)
    - Receives: Image data from state.image_path (image_node output)
    - Returns: media_id that gets used in WhatsApp message payload by send_response()
    - Media source: IDENTICAL audio/image generation as Chainlit interface (same AI models)
    
    ERROR HANDLING FOR AVA'S RELIABILITY:
    - Upload failures cause send_response() to fallback to text responses
    - Media validation happens server-side at WhatsApp
    - Temporary storage on WhatsApp servers (expires after delivery to user)
    """
    # CREATE AUTHENTICATION HEADERS FOR WHATSAPP BUSINESS API
    # headers = dictionary containing authentication info for Meta's API
    # Only need Authorization header for file uploads (no Content-Type needed)
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}"}
    
    # PREPARE FILE UPLOAD PAYLOAD
    # Meta's media upload API expects specific format for file uploads
    
    # CREATE FILES DICTIONARY FOR MULTIPART UPLOAD
    # files = dictionary that httpx uses for file uploads
    # "file" = the key name Meta expects for the uploaded file
    # ("response.mp3", media_content, mime_type) = tuple with:
    #   - "response.mp3" = filename (doesn't affect functionality, just for debugging)
    #   - media_content = actual file bytes (the audio/image data)
    #   - mime_type = file format identifier ("audio/mpeg" or "image/png")
    files = {"file": ("response.mp3", media_content, mime_type)}
    
    # CREATE FORM DATA FOR UPLOAD REQUEST
    # data = additional form fields that Meta requires with file uploads
    data = {
        # messaging_product = tells Meta this file is for WhatsApp
        "messaging_product": "whatsapp", 
        
        # type = MIME type repeated in form data (Meta requirement)
        "type": mime_type
    }

    # UPLOAD FILE TO WHATSAPP MEDIA API
    # This is a different API endpoint than message sending - just for file storage
    
    try:
        # CREATE HTTP CLIENT FOR UPLOAD REQUEST
        # async with = context manager for automatic cleanup
        # httpx.AsyncClient() = web client for making HTTP requests
        async with httpx.AsyncClient() as client:
            
            # MAKE FILE UPLOAD REQUEST TO META
            # await = wait for file upload to complete (can take time for large files)
            # client.post() = HTTP POST request with file upload
            response = await client.post(
                # Media API URL: different endpoint than message sending
                # f"..." = f-string to insert our phone number ID
                f"https://graph.facebook.com/v21.0/{WHATSAPP_PHONE_NUMBER_ID}/media",
                
                # headers = authentication info
                headers=headers,
                
                # files = the actual file data to upload
                files=files,
                
                # data = additional form fields Meta requires
                data=data,
            )
            
            # 🚨 DETAILED MEDIA UPLOAD RESPONSE LOGGING
            print(f"🔍 MEDIA UPLOAD API RESPONSE:")
            print(f"  Status Code: {response.status_code}")
            
            try:
                result = response.json()
                print(f"  Response Body: {result}")
            except:
                print(f"  Response Text: {response.text}")
                result = {}

        # VALIDATE UPLOAD SUCCESS AND EXTRACT MEDIA_ID
        # Meta returns a dictionary with "id" field containing the media reference
        # if "id" not in result = check if upload failed
        if "id" not in result:
            # Upload failed - log details and throw exception
            print(f"🚨 MEDIA UPLOAD FAILED:")
            print(f"  Status: {response.status_code}")
            print(f"  Response: {result}")
            raise Exception(f"Failed to upload media: {result}")
        
        print(f"✅ MEDIA UPLOAD SUCCESS: ID = {result['id']}")
        return result["id"]
        
    except Exception as e:
        # 🚨 CATCH ANY UPLOAD ERRORS
        import traceback
        error_msg = f"Media upload failed: {str(e)}"
        full_traceback = traceback.format_exc()
        
        print(f"🚨 MEDIA UPLOAD ERROR: {error_msg}")
        print(f"🚨 FULL TRACEBACK:\n{full_traceback}")
        logger.error(f"{error_msg}\n{full_traceback}")
        
        raise Exception(error_msg)
