"""
💬 CHAINLIT WEB INTERFACE - Pepper's demo and development chat interface

WHAT IS THIS FILE?
This is Pepper's web-based chat interface built with Chainlit - perfect for:
- Testing Pepper during development
- Demonstrating capabilities to stakeholders  
- Debugging conversation flows
- Prototyping new features

WHY CHAINLIT?
Chainlit provides a ChatGPT-like web interface with zero frontend coding:
- Built-in support for text, images, audio, and file uploads
- Real-time streaming responses (watch Pepper think!)
- Session management and conversation history
- Perfect for AI agent development and demos

THE COMPLETE USER EXPERIENCE:
1. User opens web browser → Chainlit interface loads
2. User types/uploads/records → on_message/on_audio_end handlers
3. SAME Pepper brain processes (graph.py + nodes.py)
4. Chainlit displays response with rich media support

COMPARED TO WHATSAPP INTERFACE:
┌──────────────────┬─────────────────┬──────────────────────┐
│ Feature          │ Chainlit        │ WhatsApp             │
├──────────────────┼─────────────────┼──────────────────────┤
│ Purpose          │ Demo/Development│ Production           │
│ User Experience  │ Rich web UI     │ Standard WhatsApp    │
│ Streaming        │ Real-time       │ Store-and-forward    │
│ File Upload      │ Drag & drop     │ WhatsApp sharing     │
│ Session ID       │ Fixed (demo)    │ Phone number         │
│ Pepper Brain        │ IDENTICAL       │ IDENTICAL            │
└──────────────────┴─────────────────┴──────────────────────┘

CROSS-SYSTEM CONNECTIONS:
- graph_builder: Uses IDENTICAL workflow as WhatsApp (same Pepper brain)
- AsyncSqliteSaver: Same conversation persistence mechanism
- AI modules: Same speech/image processing as production
- settings.py: Same configuration across all interfaces

HOW TO USE:
1. Run: chainlit run interfaces/chainlit/app.py
2. Open: http://localhost:8000
3. Chat with Pepper exactly like production, but with rich UI!

HOW CHAINLIT HANDLES DIFFERENT USER ACTIONS:
Chainlit uses Python decorators (special @ symbols) to automatically call functions when users do things.
Think of decorators like automatic triggers - when user types a message, @cl.on_message automatically calls our function.

THE THREE CHAINLIT EVENT HANDLERS:
- @cl.on_chat_start: Runs when user first opens the web page (like greeting a customer)
- @cl.on_message: Runs when user types text or uploads images (main conversation handler)
- @cl.on_audio_end: Runs when user finishes recording voice message (voice conversation handler)

Each handler follows Pepper's standard processing pattern:
1. Get user input (text from typing, image from upload, or audio from recording)
2. Send input through Pepper's identical LangGraph brain (same workflow as WhatsApp production)
3. Display Pepper's response in web interface (text, image, or audio player)
"""

# STANDARD LIBRARY IMPORTS - Python's built-in tools

# BytesIO = Python's tool for handling file data in memory (like a temporary file holder)
# When users upload audio/images, we need to hold the file data in memory while processing
# Think of it like a clipboard that temporarily holds file contents while Pepper works on them
from io import BytesIO

# EXTERNAL LIBRARY IMPORTS - Third-party tools for specific functionality

# chainlit = Framework for building ChatGPT-like web interfaces with zero frontend coding
# Provides built-in support for text, images, audio, file uploads, and real-time streaming
# Like having a pre-built chat website that we just need to connect Pepper's brain to
import chainlit as cl

# LangChain message format - standardized way to represent chat messages
# AIMessageChunk = pieces of AI responses during streaming (word-by-word display)
# HumanMessage = wrapper that tells Pepper "this message came from a human user"
# Same format used in WhatsApp interface, so Pepper's brain processes messages identically
from langchain_core.messages import AIMessageChunk, HumanMessage

# AsyncSqliteSaver is LangGraph's conversation memory system that uses SQLite database files.
# This system stores conversation history so Pepper remembers what you talked about previously.
# The "Async" version means it doesn't block other conversations while saving memory to disk.
# This is identical to the WhatsApp interface - both use the same conversation persistence mechanism.
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

# pepper'S CORE BRAIN COMPONENTS - The same AI modules used in WhatsApp interface

# graph_builder is Pepper's complete workflow system that acts like a conductor orchestrating all AI modules.
# This contains the identical LangGraph workflow used everywhere: memory→router→context→response nodes.
# This is the same brain that processes messages in WhatsApp interface, just with different input/output methods.
from ai_companion.graph import graph_builder

# AI processing modules for different media types (same capabilities as WhatsApp)
# These are Pepper's AI processing modules for different media types:
# ImageToText is Pepper's vision system that analyzes photos users upload via web interface.
# SpeechToText is Pepper's hearing system that transcribes voice recordings to text for processing.
# TextToSpeech is Pepper's speaking system that converts Pepper's text responses to audio files.
from ai_companion.modules.image import ImageToText
from ai_companion.modules.speech import SpeechToText, TextToSpeech

# settings is Pepper's configuration file that contains API keys, model choices, and database paths.
# This configuration is shared across all interfaces so Chainlit and WhatsApp use the same AI models and settings.
from ai_companion.settings import settings

# CREATE GLOBAL AI MODULE INSTANCES - Create once, reuse for all users (performance optimization)

# Why create these globally instead of inside functions?
# These AI modules are expensive to initialize (load models, connect to APIs)
# Creating them once at startup and reusing them is much faster than recreating for each message
# Think of it like keeping Pepper's brain modules "warmed up" and ready to process any user's message
# IDENTICAL pattern used in WhatsApp interface for consistency and performance

# speech_to_text = Pepper's hearing system using Whisper AI model via Groq API
# Converts audio recordings (voice messages) into text that Pepper's LangGraph brain can understand
# Same instance used in WhatsApp interface - consistent speech processing across all interfaces
speech_to_text = SpeechToText()

# text_to_speech = Pepper's speaking system using ElevenLabs API
# Converts Pepper's text responses into realistic speech audio files
# Same instance used in WhatsApp interface - consistent voice across all interfaces
text_to_speech = TextToSpeech()

# image_to_text = Pepper's vision system using multimodal AI models
# Analyzes images and describes what Pepper "sees" in text format for LangGraph processing
# Same instance used in WhatsApp interface - consistent image understanding across interfaces
image_to_text = ImageToText()


@cl.on_chat_start
async def on_chat_start():
    """
    🎬 SESSION INITIALIZATION - Sets up a new chat session when user first loads the page
    
    WHAT IT DOES:
    Initializes a new conversation session for the Chainlit web interface.
    Like greeting a customer when they walk into a store.
    
    WHY THREAD_ID = 1?
    For demo purposes, all Chainlit users share the same conversation thread.
    In production (WhatsApp), each user gets their own thread_id (phone number).
    
    CROSS-SYSTEM CONNECTION:
    - This thread_id is used by AsyncSqliteSaver (same as graph.py compilation)
    - Same thread_id mechanism as WhatsApp, just different values:
      - Chainlit: thread_id = 1 (shared demo session)
      - WhatsApp: thread_id = phone_number (isolated per user)
    
    MEMORY IMPLICATIONS:
    Since thread_id = 1 for all users, the Chainlit demo shares memory.
    If User A says "I'm John", User B will see "You mentioned you're John earlier"
    This is intentional for demo purposes - shows memory system working.
    
    WHEN IT RUNS:
    - User opens http://localhost:8000 for first time
    - Page refresh triggers this again
    - Before any messages are sent
    """
    # SET FIXED THREAD_ID FOR DEMO SESSION
    # thread_id = unique identifier for this user's conversation with Pepper
    # Different from WhatsApp where each phone number gets its own thread_id
    
    # WHY THREAD_ID = 1 FOR EVERYONE?
    # In demo mode, we want all users to share the same conversation thread
    # This shows how Pepper's memory system works - if User A says "I'm John", 
    # User B will see "You mentioned you're John earlier" because they share memory
    
    # PRODUCTION ALTERNATIVE (commented out):
    # thread_id = cl.user_session.get("id")  # Could use unique Chainlit session ID
    # This would give each user their own private conversation thread
    
    # SET DEMO THREAD_ID IN SESSION STORAGE
    # cl.user_session.set() = stores data that persists for this user's browser session
    # "thread_id" = key name we'll use to retrieve this value later
    # 1 = the actual thread_id value (all demo users share thread 1)
    cl.user_session.set("thread_id", 1)


@cl.on_message
async def on_message(message: cl.Message):
    """
    💬 TEXT & IMAGE MESSAGE HANDLER - Processes user messages and any attached images
    
    WHAT IT DOES:
    The main message processing pipeline for the Chainlit interface. Handles:
    - Text messages from user
    - Image uploads with automatic analysis
    - Streaming responses for real-time feel
    - Multi-modal responses (text/image/audio)
    
    THE PROCESSING PIPELINE:
    1. Extract user's text message
    2. Analyze any attached images (same as WhatsApp interface)
    3. Process through IDENTICAL Pepper brain (graph.py workflow)
    4. Stream response in real-time (unique to Chainlit)
    5. Handle multi-modal responses based on workflow decision
    
    CROSS-SYSTEM CONNECTIONS:
    - image_to_text: SAME image analysis as WhatsApp interface
    - graph_builder.compile(): IDENTICAL brain compilation as WhatsApp
    - AsyncSqliteSaver: SAME conversation persistence as WhatsApp
    - workflow decisions: SAME router_node logic from nodes.py
    
    WHY STREAMING?
    Unlike WhatsApp (store-and-forward), Chainlit supports real-time streaming.
    Users see Pepper "typing" her response word-by-word, like ChatGPT.
    """
    # CREATE EMPTY MESSAGE FOR STREAMING RESPONSE
    # cl.Message() = creates a Chainlit message object for display in the web interface
    # content="" = starts with empty text, we'll add words one-by-one during streaming
    # This is like creating a blank text box that we'll fill as Pepper "types" her response
    msg = cl.Message(content="")

    # STEP 1: EXTRACT THE USER'S MESSAGE TEXT
    # message = the complete message object Chainlit gives us (contains text + any files)
    # message.content = just the text part of what the user typed
    # Example: if user typed "Hello Pepper!", content = "Hello Pepper!"
    content = message.content

    # STEP 2: HANDLE ATTACHED IMAGES (IF ANY)
    # Users can drag and drop images into the Chainlit chat interface
    # Same image processing logic as WhatsApp interface, just different file access method
    
    # CHECK IF USER ATTACHED ANY FILES
    # message.elements = list of attached files (images, documents, etc.)
    # If empty list, user sent text only; if contains items, user attached files
    if message.elements:
        
        # LOOP THROUGH ALL ATTACHED FILES
        # for elem in message.elements = examine each attached file one by one
        for elem in message.elements:
            
            # CHECK IF THIS ATTACHMENT IS AN IMAGE
            # isinstance(elem, cl.Image) = Python function that checks if elem is an image object
            # Only process images - ignore other file types like PDFs, documents, etc.
            if isinstance(elem, cl.Image):
                
                # READ THE UPLOADED IMAGE FILE FROM DISK
                # elem.path = file path where Chainlit saved the uploaded image
                # with open() = Python context manager that automatically closes files
                # "rb" = read in binary mode (for image files, not text files)
                # f.read() = read the entire image file into memory as bytes
                with open(elem.path, "rb") as f:
                    image_bytes = f.read()

                # ANALYZE IMAGE USING pepper'S VISION SYSTEM
                # Same image_to_text module and process as WhatsApp interface
                # try/except = error handling in case image analysis fails
                try:
                    
                    # PROCESS IMAGE THROUGH pepper'S VISION
                    # await = wait for AI vision processing to complete (can take several seconds)
                    # image_to_text.analyze_image() = SAME function used in WhatsApp interface
                    # Takes: image data (bytes) and a prompt asking what to look for
                    # Returns: text description of what Pepper sees in the image
                    description = await image_to_text.analyze_image(
                        image_bytes,  # The actual image data we read from file
                        "Please describe what you see in this image in the context of our conversation.",
                    )
                    
                    # ADD IMAGE ANALYSIS TO MESSAGE CONTENT
                    # content += means "add this text to the end of existing content"
                    # f"..." = f-string formatting to insert the description variable
                    # Final content = user's text + "\n[Image Analysis: what Pepper saw]"
                    content += f"\n[Image Analysis: {description}]"
                    
                # HANDLE IMAGE ANALYSIS ERRORS
                # except Exception as e = catch any error that happened during image analysis
                except Exception as e:
                    # cl.logger.warning() = record this problem in Chainlit's log for debugging
                    # f"..." = f-string to include the actual error message
                    # If image analysis fails, log error but continue processing (graceful degradation)
                    cl.logger.warning(f"Failed to analyze image: {e}")

    # STEP 3: GET THE SESSION THREAD_ID (SET DURING CHAT INITIALIZATION)
    # thread_id = unique identifier for this conversation thread
    # cl.user_session.get() = retrieves data stored in this user's browser session
    # "thread_id" = the key name we used in on_chat_start() to store the ID
    # Returns: 1 (the demo thread ID we set for all users)
    thread_id = cl.user_session.get("thread_id")

    # STEP 4: PROCESS THROUGH pepper'S BRAIN (IDENTICAL TO WHATSAPP PROCESSING)
    # Now we have the content text (+ image analysis), send it through Pepper's complete LangGraph workflow
    
    # SHOW "THINKING" INDICATOR IN CHAINLIT UI
    # async with = Python context manager that automatically handles setup/cleanup
    # cl.Step(type="run") = shows a "thinking" or "processing" indicator in the web interface
    # Like showing a spinning wheel while Pepper processes the message
    async with cl.Step(type="run"):
        
        # SETUP CONVERSATION MEMORY DATABASE CONNECTION
        # async with = context manager that automatically handles opening/closing database
        # AsyncSqliteSaver = Pepper's memory system that remembers conversation history
        # .from_conn_string() = connect to SQLite database file at the specified path
        # settings.SHORT_TERM_MEMORY_DB_PATH = file path where conversation history is stored
        # IDENTICAL setup to WhatsApp interface - same memory system
        async with AsyncSqliteSaver.from_conn_string(settings.SHORT_TERM_MEMORY_DB_PATH) as short_term_memory:
            
            # BUILD pepper'S COMPLETE WORKFLOW GRAPH
            # graph_builder.compile() = creates Pepper's complete LangGraph workflow
            # checkpointer=short_term_memory = connect the memory system so Pepper remembers conversations
            # This creates the IDENTICAL workflow used in WhatsApp: memory→router→context→response nodes
            graph = graph_builder.compile(checkpointer=short_term_memory)
            
            # STREAM pepper'S RESPONSE IN REAL-TIME (UNIQUE TO CHAINLIT)
            # Unlike WhatsApp (store-and-forward), Chainlit supports real-time streaming
            # Users see Pepper "typing" her response word-by-word, like ChatGPT
            
            # PROCESS MESSAGE AND STREAM RESPONSE
            # async for = loop that processes streaming data as it arrives
            # graph.astream() = stream Pepper's processing in real-time (vs ainvoke() which waits for completion)
            async for chunk in graph.astream(
                # FIRST PARAMETER: The message data to process
                {"messages": [HumanMessage(content=content)]},  # Wrap user's text in LangChain message format
                
                # SECOND PARAMETER: Configuration for this processing run
                {"configurable": {"thread_id": thread_id}},     # Use thread_id to isolate conversations
                
                # THIRD PARAMETER: What type of streaming we want
                stream_mode="messages",                          # Stream individual message chunks (word-by-word)
            ):
                # FILTER AND DISPLAY STREAMING TEXT
                # chunk = each piece of streaming data from Pepper's workflow
                # chunk[1]["langgraph_node"] = which node in the workflow produced this chunk
                # "conversation_node" = we only want to stream text from the conversation node
                # isinstance(chunk[0], AIMessageChunk) = check if this chunk contains AI text
                if chunk[1]["langgraph_node"] == "conversation_node" and isinstance(chunk[0], AIMessageChunk):
                    # STREAM TEXT TO USER'S BROWSER IN REAL-TIME
                    # await = wait for this text chunk to be sent to user's browser
                    # msg.stream_token() = add this text to the streaming message display
                    # chunk[0].content = the actual text content from Pepper's response
                    await msg.stream_token(chunk[0].content)

            # GET pepper'S FINAL STATE AFTER PROCESSING COMPLETES
            # After streaming completes, we need to see Pepper's final decisions (text/image/audio response)
            # await = wait for state retrieval to complete
            # graph.aget_state() = get the final state of Pepper's workflow
            # config = same configuration (thread_id) to get the right conversation's state
            # IDENTICAL to WhatsApp interface
            output_state = await graph.aget_state(config={"configurable": {"thread_id": thread_id}})

    # STEP 5: HANDLE MULTI-MODAL RESPONSES BASED ON WORKFLOW DECISION
    # Based on router_node's decision, display different types of responses in Chainlit UI
    # This logic matches WhatsApp interface but with Chainlit web elements instead of API calls
    
    # AUDIO RESPONSE - pepper WANTS TO SEND A VOICE MESSAGE
    # output_state.values.get("workflow") = get router_node's decision from Pepper's final state
    # "audio" = router_node decided Pepper should respond with voice
    if output_state.values.get("workflow") == "audio":
        
        # EXTRACT AUDIO RESPONSE DATA FROM pepper'S STATE
        # output_state.values["messages"] = list of all messages in conversation
        # [-1] = get the last message (Pepper's response)
        # .content = the actual text content of Pepper's response
        response = output_state.values["messages"][-1].content
        
        # output_state.values["audio_buffer"] = the actual audio file data (bytes)
        # This is Pepper's voice saying the response text (generated by audio_node using ElevenLabs)
        audio_buffer = output_state.values["audio_buffer"]
        
        # CREATE CHAINLIT AUDIO ELEMENT FOR WEB DISPLAY
        # cl.Audio() = creates an audio player widget in the web interface
        # Same audio content as WhatsApp, but displayed as web audio player instead of sent via API
        output_audio_el = cl.Audio(
            name="Audio",                # Label shown in the web interface
            auto_play=True,              # Start playing immediately when message appears
            mime="audio/mpeg3",          # Audio format (MP3)
            content=audio_buffer,        # The actual audio data from audio_node
        )
        
        # SEND MESSAGE WITH TEXT + AUDIO TO WEB INTERFACE
        # await = wait for message to be sent to user's browser
        # cl.Message() = creates a message in the chat interface
        # content=response = Pepper's text (user can read while listening)
        # elements=[output_audio_el] = attach the audio player to this message
        await cl.Message(content=response, elements=[output_audio_el]).send()
        
    # IMAGE RESPONSE - pepper WANTS TO SEND A GENERATED IMAGE
    elif output_state.values.get("workflow") == "image":
        
        # EXTRACT IMAGE RESPONSE DATA FROM pepper'S STATE
        # output_state.values["messages"][-1].content = Pepper's caption text for the image
        response = output_state.values["messages"][-1].content
        
        # CREATE CHAINLIT IMAGE ELEMENT FOR WEB DISPLAY
        # cl.Image() = creates an image display widget in the web interface
        # path = file path where image_node saved the generated image
        # display="inline" = show image directly in chat (not as downloadable attachment)
        # Same image content as WhatsApp, but displayed in web UI instead of sent via API
        image = cl.Image(path=output_state.values["image_path"], display="inline")
        
        # SEND MESSAGE WITH CAPTION + IMAGE TO WEB INTERFACE
        # await = wait for message to be sent to user's browser
        # content=response = Pepper's caption text
        # elements=[image] = attach the image display to this message
        await cl.Message(content=response, elements=[image]).send()
        
    # TEXT RESPONSE - pepper WANTS TO SEND A REGULAR TEXT MESSAGE (MOST COMMON)
    else:
        # SEND THE STREAMED TEXT MESSAGE
        # msg = the message object we created at the start and filled during streaming
        # await msg.send() = send the complete streamed message to user's browser
        # This contains all the text that was streamed word-by-word during processing
        await msg.send()


@cl.on_audio_chunk
async def on_audio_chunk(chunk: cl.AudioChunk):
    """
    🎙️ AUDIO CHUNK RECEIVER - Handles real-time audio recording chunks
    
    WHAT IT DOES:
    Chainlit sends audio data in small chunks as the user records.
    This function assembles those chunks into a complete audio file.
    Like recording a voice message piece by piece.
    
    THE STREAMING PROCESS:
    1. User clicks record button → chunk.isStart = True
    2. User speaks → Multiple chunks with audio data
    3. User stops recording → on_audio_end() processes complete audio
    
    WHY CHUNKS?
    Real-time audio recording sends data continuously, not all at once.
    We buffer chunks until recording is complete, then process the full audio.
    
    CROSS-SYSTEM CONNECTION:
    This is unique to Chainlit - WhatsApp sends complete audio files directly.
    But the final processing (speech_to_text) is identical across both interfaces.
    """
    # CHECK IF THIS IS THE FIRST CHUNK (START OF RECORDING)
    # chunk.isStart = boolean that tells us if user just started recording
    # True = user clicked record button, False = continuing to record
    if chunk.isStart:
        
        # INITIALIZE AUDIO BUFFER FOR THIS RECORDING SESSION
        # BytesIO() = creates a file-like object in memory to store audio data
        # Like creating an empty audio file in memory that we'll fill as user records
        buffer = BytesIO()
        
        # SET FILENAME BASED ON AUDIO FORMAT
        # chunk.mimeType = audio format (like "audio/webm" or "audio/mp3")
        # .split('/')[1] = extract file extension ("webm" from "audio/webm")
        # f"input_audio.{...}" = create filename like "input_audio.webm"
        # buffer.name = give the memory file a name (helps with debugging)
        buffer.name = f"input_audio.{chunk.mimeType.split('/')[1]}"
        
        # STORE BUFFER IN USER'S SESSION
        # cl.user_session.set() = save data that persists for this user's browser session
        # "audio_buffer" = key name we'll use to retrieve this buffer later
        # buffer = the actual BytesIO object that will collect audio chunks
        cl.user_session.set("audio_buffer", buffer)
        
        # REMEMBER AUDIO FORMAT FOR LATER PROCESSING
        # cl.user_session.set() = store the MIME type for when we process complete audio
        # "audio_mime_type" = key name for retrieving format later
        # chunk.mimeType = the audio format (needed for speech recognition)
        cl.user_session.set("audio_mime_type", chunk.mimeType)
    
    # APPEND AUDIO DATA TO BUFFER (FOR ALL CHUNKS)
    # This happens for every chunk - first chunk AND continuing chunks
    # cl.user_session.get("audio_buffer") = retrieve the BytesIO buffer we created
    # .write(chunk.data) = append this chunk's audio data to the buffer
    # chunk.data = the actual audio bytes for this small piece of the recording
    cl.user_session.get("audio_buffer").write(chunk.data)


@cl.on_audio_end
async def on_audio_end(elements):
    """
    🎤 VOICE MESSAGE PROCESSOR - Handles complete voice messages from user
    
    WHAT IT DOES:
    Processes a complete voice message recording from the user:
    1. Transcribes speech to text (same as WhatsApp)
    2. Processes through Pepper's brain (same logic as text messages)  
    3. Generates voice response (full voice conversation)
    
    THE VOICE-TO-VOICE PIPELINE:
    User Voice → Transcription → Pepper's Brain → Text Response → Voice Synthesis → Audio Reply
    
    COMPARED TO TEXT MESSAGES:
    - Input: Audio instead of text
    - Processing: IDENTICAL graph workflow  
    - Output: Always audio (no router decision needed)
    
    CROSS-SYSTEM CONNECTIONS:
    - speech_to_text: SAME Whisper transcription as WhatsApp
    - graph processing: IDENTICAL workflow as on_message()
    - text_to_speech: SAME ElevenLabs synthesis as audio_node
    - AsyncSqliteSaver: SAME conversation persistence
    
    WHY ALWAYS AUDIO RESPONSE?
    Voice conversations feel more natural when both sides use voice.
    We bypass the router_node decision and always synthesize audio responses.
    """
    # STEP 1: GET THE COMPLETE AUDIO DATA FROM BUFFERED CHUNKS
    # Now that recording is complete, we need to process the full audio file
    
    # RETRIEVE THE AUDIO BUFFER FROM SESSION STORAGE
    # cl.user_session.get("audio_buffer") = get the BytesIO buffer we filled during recording
    # This contains all the audio chunks combined into one complete voice message
    audio_buffer = cl.user_session.get("audio_buffer")
    
    # RESET BUFFER POSITION TO START
    # .seek(0) = move to the beginning of the audio data
    # Like rewinding a tape to the beginning before playing it
    # Necessary because we were writing to the end, now we need to read from the start
    audio_buffer.seek(0)
    
    # READ COMPLETE AUDIO FILE INTO MEMORY
    # .read() = read all audio data from the buffer
    # audio_data = the complete voice message as bytes, ready for processing
    audio_data = audio_buffer.read()

    # STEP 2: DISPLAY USER'S VOICE MESSAGE IN THE CHAT
    # Show the user's recording in the chat interface before processing it
    
    # CREATE AUDIO ELEMENT FOR USER'S VOICE MESSAGE
    # cl.Audio() = creates an audio player widget in the web interface
    # mime="audio/mpeg3" = audio format for web browser playback
    # content=audio_data = the actual audio recording data
    input_audio_el = cl.Audio(mime="audio/mpeg3", content=audio_data)
    
    # SEND USER'S VOICE MESSAGE TO CHAT INTERFACE
    # await = wait for message to appear in user's browser
    # cl.Message() = creates a message in the chat interface
    # author="You" = label this message as coming from the user (not Pepper)
    # content="" = no text content, just the audio
    # elements=[input_audio_el, *elements] = attach audio player + any other elements
    # *elements = spread operator to include any additional elements passed to function
    await cl.Message(author="You", content="", elements=[input_audio_el, *elements]).send()

    # STEP 3: TRANSCRIBE SPEECH TO TEXT (SAME MODULE AS WHATSAPP INTERFACE)
    # Convert the user's voice recording into text that Pepper's brain can process
    
    # PROCESS AUDIO THROUGH pepper'S HEARING SYSTEM
    # await = wait for speech recognition to complete (can take several seconds)
    # speech_to_text.transcribe() = IDENTICAL function used in WhatsApp interface
    # Takes: raw audio data (bytes)
    # Returns: text string of what the user said in their voice message
    # Uses Whisper AI model via Groq API (same as WhatsApp)
    transcription = await speech_to_text.transcribe(audio_data)

    # STEP 4: PROCESS TRANSCRIPTION THROUGH pepper'S BRAIN (IDENTICAL TO TEXT PROCESSING)
    # Now we have text from the voice message, process it through same workflow as typed messages
    
    # GET SESSION THREAD_ID FOR CONVERSATION ISOLATION
    # cl.user_session.get("thread_id") = retrieve the thread ID we set in on_chat_start()
    # Same session isolation mechanism as text messages (thread_id = 1 for demo)
    thread_id = cl.user_session.get("thread_id")

    # SETUP CONVERSATION MEMORY AND PROCESS THROUGH pepper'S WORKFLOW
    # async with = context manager that automatically handles database connection cleanup
    # AsyncSqliteSaver = same conversation memory system used for text messages
    # settings.SHORT_TERM_MEMORY_DB_PATH = same database file as text message processing
    async with AsyncSqliteSaver.from_conn_string(settings.SHORT_TERM_MEMORY_DB_PATH) as short_term_memory:
        
        # BUILD pepper'S COMPLETE WORKFLOW GRAPH
        # graph_builder.compile() = creates Pepper's complete LangGraph workflow
        # checkpointer=short_term_memory = connect memory system (same as on_message handler)
        # IDENTICAL workflow: memory→router→context→response nodes
        graph = graph_builder.compile(checkpointer=short_term_memory)
        
        # PROCESS TRANSCRIBED TEXT THROUGH COMPLETE WORKFLOW
        # await = wait for Pepper's complete processing to finish
        # graph.ainvoke() = run through complete workflow and wait for final result
        # Note: Using ainvoke() instead of astream() because we don't need word-by-word streaming for voice
        output_state = await graph.ainvoke(
            # FIRST PARAMETER: The message data to process
            {"messages": [HumanMessage(content=transcription)]},  # Transcribed user speech as LangChain message
            
            # SECOND PARAMETER: Configuration for this processing run
            {"configurable": {"thread_id": thread_id}},           # Same thread isolation as text messages
        )

    # STEP 5: CONVERT pepper'S TEXT RESPONSE TO SPEECH (SAME MODULE AS AUDIO_NODE)
    # For voice conversations, we always respond with voice (more natural than text reply to voice)
    
    # EXTRACT pepper'S TEXT RESPONSE FROM WORKFLOW STATE
    # output_state["messages"] = list of all messages in the conversation
    # [-1] = get the last message (Pepper's response)
    # .content = the actual text content of Pepper's response
    response_text = output_state["messages"][-1].content
    
    # SYNTHESIZE pepper'S RESPONSE INTO SPEECH
    # await = wait for text-to-speech conversion to complete
    # text_to_speech.synthesize() = IDENTICAL function used in audio_node
    # Takes: Pepper's response text
    # Returns: audio buffer (bytes) of Pepper speaking the response
    # Uses ElevenLabs API with Pepper's configured voice (same as audio_node)
    audio_buffer = await text_to_speech.synthesize(response_text)

    # STEP 6: SEND VOICE RESPONSE BACK TO USER
    # Display both text and audio so user can read along while listening
    
    # CREATE AUDIO ELEMENT FOR pepper'S VOICE RESPONSE
    # cl.Audio() = creates an audio player widget in the web interface
    output_audio_el = cl.Audio(
        name="Audio",                    # Label shown in the web interface
        auto_play=True,                  # Start playing immediately when message appears
        mime="audio/mpeg3",              # Audio format (MP3) for web browser playback
        content=audio_buffer,            # The actual synthesized audio data
    )
    
    # SEND MESSAGE WITH BOTH TEXT AND AUDIO TO WEB INTERFACE
    # await = wait for message to be sent to user's browser
    # cl.Message() = creates a message in the chat interface
    # content=response_text = Pepper's text response (user can read while listening)
    # elements=[output_audio_el] = attach the audio player to this message
    # This creates a message with both readable text and playable audio
    await cl.Message(content=response_text, elements=[output_audio_el]).send()
