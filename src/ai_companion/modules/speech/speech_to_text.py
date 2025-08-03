# STANDARD LIBRARY IMPORTS - Python's built-in tools for file and system operations

# os provides access to operating system functions like environment variables
# Used to safely access API keys and clean up temporary files
import os

# tempfile creates temporary files for processing audio data
# Voice messages are bytes in memory, but Groq's API needs actual files on disk
# This module handles creating and cleaning up temporary audio files safely
import tempfile

# typing provides type hints for better code clarity and error prevention
# Optional = value that might be None
from typing import Optional

# CUSTOM IMPORTS - Pepper-specific modules

# Custom exception for speech processing errors (more specific than generic Python exceptions)
# Provides consistent error handling across Pepper's speech recognition system
from ai_companion.core.exceptions import SpeechToTextError

# Pepper's centralized configuration containing API keys and model names
# Single source of truth for all AI service configurations
from ai_companion.settings import settings

# GROQ IMPORT - AI service for speech recognition

# Groq provides fast, cost-effective access to OpenAI's Whisper speech recognition models
# Same service that powers Pepper's language processing and image analysis
# Offers better performance and pricing than directly using OpenAI's API
from groq import Groq


class SpeechToText:
    """
    👂 pepper'S HEARING SYSTEM - Pepper's ability to listen and understand voice messages
    
    WHAT IT DOES:
    This class gives Pepper the ability to "hear" and understand voice messages that users send.
    When you record audio in Chainlit or send voice messages via WhatsApp, this system
    converts your speech into text that Pepper's brain can process and respond to.
    
    HOW IT WORKS (USER STORY):
    1. User sends voice message: "Hey Pepper, what's the weather like today?"
    2. Audio bytes get passed to transcribe() method
    3. Creates temporary audio file for Groq's API processing
    4. Whisper AI model converts speech to text: "Hey Pepper, what's the weather like today?"
    5. Text gets processed through Pepper's normal LangGraph workflow
    6. Pepper responds as if user had typed the message
    
    REAL-WORLD ANALOGY:
    This is like Pepper having excellent hearing and perfect note-taking skills.
    You speak to her in a voice message, and she "listens" carefully and writes down
    exactly what you said, word-for-word. Then she can think about your words and respond.
    
    TECHNICAL APPROACH:
    - Uses OpenAI's Whisper model via Groq's API for fast, accurate transcription
    - Supports multiple audio formats (.wav, .mp3, .ogg, etc.)
    - Optimized for English language processing
    - Handles temporary file management automatically
    
    USED BY:
    - WhatsApp interface: When users send voice messages via WhatsApp
    - Chainlit interface: When users record audio in web chat
    - Voice-to-voice conversations: First step in processing voice input
    
    INTEGRATION WITH pepper'S BRAIN:
    Transcribed text gets processed through identical LangGraph workflow as typed messages.
    Voice input becomes indistinguishable from text input after this conversion.
    """

    # REQUIRED ENVIRONMENT VARIABLES - API keys needed for speech recognition
    # GROQ_API_KEY provides access to Whisper models via Groq's optimized infrastructure
    REQUIRED_ENV_VARS = ["GROQ_API_KEY"]

    def __init__(self):
        """
        🔧 INITIALIZE pepper'S HEARING SYSTEM - Set up speech recognition capabilities
        
        WHAT HAPPENS DURING INITIALIZATION:
        1. Validates that GROQ_API_KEY is pepperilable for Whisper access
        2. Prepares (but doesn't create yet) the Groq client connection
        
        WHY GROQ FOR SPEECH RECOGNITION:
        - Faster processing than OpenAI's direct API
        - More cost-effective for production use
        - Same infrastructure as Pepper's other AI capabilities
        - Consistent API patterns across all of Pepper's AI modules
        """
        # VALIDATE API KEY IS CONFIGURED
        # Better to fail fast during startup than during user's first voice message
        self._validate_env_vars()
        
        # PREPARE CLIENT STORAGE (LAZY INITIALIZATION)
        # _client starts as None, gets created only when first voice message arrives
        # Avoids expensive network connections during Pepper's startup process
        self._client: Optional[Groq] = None

    def _validate_env_vars(self) -> None:
        """
        🔒 ENVIRONMENT VALIDATOR - Ensures speech recognition API key is configured
        
        WHAT IT DOES:
        Checks that GROQ_API_KEY is set in environment variables before trying to use
        speech recognition. Prevents crashes when users send their first voice message.
        
        WHY THIS VALIDATION IS IMPORTANT:
        Voice messages are time-sensitive - users expect quick responses.
        Better to discover configuration issues during startup than during
        a user's voice conversation with Pepper.
        
        REAL-WORLD ANALOGY:
        This is like checking your hearing aids have batteries before going to a concert.
        Better to discover the problem at home than miss the entire performance.
        """
        # CHECK FOR MISSING ENVIRONMENT VARIABLES
        # Creates list of any required variables that are not set
        # os.getenv() returns None if environment variable doesn't exist
        missing_vars = [var for var in self.REQUIRED_ENV_VARS if not os.getenv(var)]
        
        # RAISE CLEAR ERROR IF API KEY IS MISSING
        # Provides specific guidance about which environment variable needs to be set
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

    @property
    def client(self) -> Groq:
        """
        🔌 GROQ CLIENT MANAGER - Creates and reuses connection to speech recognition service
        
        WHAT IT DOES:
        Creates a connection to Groq's Whisper speech recognition service, but only when needed.
        Once created, reuses the same connection for all future voice message transcriptions.
        
        WHY SINGLETON PATTERN:
        Creating new API clients is expensive (network setup, authentication, etc.).
        Voice messages often come in quick succession, so reusing one connection
        provides much better performance than creating new connections each time.
        
        REAL-WORLD ANALOGY:
        This is like having one dedicated phone line to Groq's speech recognition service
        instead of dialing a new connection every time someone sends Pepper a voice message.
        Much more efficient for handling multiple voice conversations.
        
        TECHNICAL BENEFITS:
        - Faster response times for subsequent voice messages
        - Reduced network overhead and connection setup costs
        - Thread-safe for handling multiple simultaneous voice messages
        """
        # CHECK IF CLIENT ALREADY EXISTS (SINGLETON PATTERN)
        # self._client starts as None during initialization
        # Once created, this condition becomes False and we reuse existing client
        if self._client is None:
            # CREATE NEW GROQ CLIENT WITH API KEY
            # settings.GROQ_API_KEY comes from environment variables via settings.py
            # Groq() constructor creates authenticated connection to Groq's AI services
            # This is the expensive operation we only want to do once
            self._client = Groq(api_key=settings.GROQ_API_KEY)
        
        # RETURN CLIENT (EITHER NEWLY CREATED OR EXISTING)
        # Caller gets a working Groq client ready for speech recognition
        # Same client instance will be returned for all future calls (singleton)
        return self._client

    async def transcribe(self, audio_data: bytes) -> str:
        """
        🎤 SPEECH TRANSCRIPTION ENGINE - Converts voice messages to text for Pepper's brain
        
        WHAT IT DOES:
        Takes raw audio bytes (voice messages) and converts them into text that Pepper
        can understand and process through her normal conversation workflow.
        
        HOW IT WORKS (USER STORY):
        1. User sends voice message: "Hey Pepper, how's your day going?"
        2. WhatsApp/Chainlit provides audio as bytes in memory
        3. Creates temporary .wav file for Groq's API (APIs need files, not memory bytes)
        4. Sends file to Groq's Whisper model for speech recognition
        5. Returns text: "Hey Pepper, how's your day going?"
        6. Text flows into Pepper's LangGraph brain for normal processing
        
        PARAMETERS:
        audio_data: Raw audio bytes from voice message (any audio format supported)
                   Usually .ogg from WhatsApp, .webm from Chainlit, or .wav from files
        
        RETURNS:
        Transcribed text string that Pepper's brain can process like typed messages
        
        REAL-WORLD ANALOGY:
        This is like having a court stenographer who listens to speech and types it out
        word-for-word. The audio becomes text that can be read and understood.
        
        TECHNICAL DETAILS:
        - Uses OpenAI's Whisper large model via Groq (state-of-the-art accuracy)
        - Optimized for English language processing
        - Handles temporary file management automatically
        - Supports most audio formats (Whisper is very flexible)
        """
        # VALIDATE INPUT AUDIO DATA
        # Empty audio would cause API errors, better to catch early with clear message
        # "not audio_data" is True if audio_data is None, empty bytes, or falsy
        if not audio_data:
            raise ValueError("Audio data cannot be empty")

        # ERROR HANDLING WRAPPER
        # try/except ensures graceful failure with helpful error messages
        # All errors get converted to SpeechToTextError for consistent handling
        try:
            # STEP 1: CREATE TEMPORARY FILE FOR API PROCESSING
            # Groq's API needs actual files on disk, not bytes in memory
            # tempfile.NamedTemporaryFile creates a secure temporary file
            
            # CREATE TEMPORARY AUDIO FILE
            # suffix=".wav" gives file proper extension (helps with audio format detection)
            # delete=False means we control when to delete it (in finally block)
            # with statement ensures file gets closed properly even if errors occur
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                # WRITE AUDIO BYTES TO TEMPORARY FILE
                # temp_file.write() saves the voice message bytes to disk
                # Now we have an actual audio file that APIs can process
                temp_file.write(audio_data)
                
                # SAVE FILE PATH FOR LATER USE
                # temp_file.name contains the full path to our temporary audio file
                # We'll need this path to open the file for the API request
                temp_file_path = temp_file.name

            # STEP 2: SEND AUDIO FILE TO GROQ'S WHISPER MODEL
            # Wrapped in try/finally to ensure temporary file cleanup
            try:
                # OPEN TEMPORARY FILE FOR API REQUEST
                # "rb" = read binary mode (audio files are binary data, not text)
                # with open() automatically closes file after API call completes
                with open(temp_file_path, "rb") as audio_file:
                    
                    # CALL GROQ'S WHISPER SPEECH RECOGNITION API
                    # self.client gets our singleton Groq client (created once, reused)
                    # .audio.transcriptions.create() is the standard Whisper API call
                    transcription = self.client.audio.transcriptions.create(
                        # FILE: The actual audio file to transcribe
                        file=audio_file,
                        
                        # MODEL: Whisper large v3 turbo (best balance of speed and accuracy)
                        # "turbo" version is optimized for faster processing
                        model="whisper-large-v3-turbo",
                        
                        # LANGUAGE: Optimize for English processing
                        # Could support other languages by changing this parameter
                        language="en",
                        
                        # RESPONSE_FORMAT: Return plain text (not JSON or other formats)
                        # We just want the transcribed words, not metadata
                        response_format="text",
                    )

                # VALIDATE API RESPONSE
                # Check that Whisper actually returned transcribed text
                # Empty responses would break Pepper's conversation flow
                if not transcription:
                    raise SpeechToTextError("Transcription result is empty")

                # RETURN TRANSCRIBED TEXT FOR pepper'S BRAIN TO PROCESS
                # This text will flow into Pepper's LangGraph workflow just like typed messages
                # From here, voice input becomes indistinguishable from text input
                return transcription

            # CLEANUP TEMPORARY FILE (ALWAYS RUNS)
            # finally block ensures file deletion even if API call fails
            # Important for not filling up disk space with temporary audio files
            finally:
                # DELETE TEMPORARY AUDIO FILE
                # os.unlink() removes the file from disk
                # Cleans up after ourselves to prevent temporary file accumulation
                os.unlink(temp_file_path)

        # CATCH ALL ERRORS AND CONVERT TO CONSISTENT FORMAT
        # except Exception catches any error that occurred during transcription
        except Exception as e:
            # WRAP ERROR IN CUSTOM EXCEPTION TYPE
            # SpeechToTextError provides consistent error handling across Pepper's system
            # "from e" preserves original error details for debugging
            # str(e) converts any exception to readable error message
            raise SpeechToTextError(f"Speech-to-text conversion failed: {str(e)}") from e
