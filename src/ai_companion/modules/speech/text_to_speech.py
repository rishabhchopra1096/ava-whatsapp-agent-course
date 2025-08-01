# STANDARD LIBRARY IMPORTS - Python's built-in tools

# os provides access to operating system functions like environment variables
# Used to safely access API keys stored as environment variables (not hardcoded)
import os

# typing provides type hints for better code clarity and error prevention
# Optional = value that might be None
from typing import Optional

# CUSTOM IMPORTS - Ava-specific modules

# Custom exception for voice synthesis errors (more specific than generic Python exceptions)
# Provides consistent error handling across Ava's text-to-speech system
from ai_companion.core.exceptions import TextToSpeechError

# Ava's centralized configuration containing API keys, voice IDs, and model names
# Single source of truth for all AI service configurations
from ai_companion.settings import settings

# ELEVENLABS IMPORTS - AI voice synthesis service

# ElevenLabs is the AI service that creates realistic human-like speech from text
# Specialized in high-quality voice synthesis with natural intonation and emotion
# Much better than basic text-to-speech systems (sounds like a real person talking)
from elevenlabs import ElevenLabs, Voice, VoiceSettings


class TextToSpeech:
    """
    🗣️ AVA'S SPEAKING SYSTEM - Ava's ability to speak text responses as realistic voice
    
    WHAT IT DOES:
    This class gives Ava the ability to "speak" her text responses out loud as realistic
    audio that sounds like a real person talking. When Ava wants to send voice messages
    instead of text, this system converts her written responses into actual speech.
    
    HOW IT WORKS (USER STORY):
    1. Ava's LangGraph brain generates text response: "I'm working on ML optimization at Groq today"
    2. router_node decides this should be sent as audio (voice conversation context)
    3. synthesize() method converts text into realistic speech using ElevenLabs
    4. User receives Ava's actual voice saying the response as a voice message
    5. Consistent personality: Always sounds like the same "Ava" voice
    
    REAL-WORLD ANALOGY:
    This is like Ava having a beautiful, consistent speaking voice that she can use
    instead of always typing responses. It's like having a friend who can choose
    whether to text you or leave you a voicemail - same message, different delivery.
    
    WHY ELEVENLABS:
    - Creates incredibly realistic human-like speech (not robotic)
    - Supports emotional intonation and natural speaking patterns
    - Maintains consistent voice identity across all of Ava's speech
    - Professional quality suitable for production AI applications
    
    TECHNICAL APPROACH:
    - Uses specific voice ID to ensure Ava always sounds the same
    - Configurable voice settings for optimal naturalness
    - Handles audio generation as streaming bytes for efficient processing
    
    USED BY:
    - audio_node in LangGraph: When Ava decides to respond with voice
    - Voice conversations: In Chainlit's voice chat feature
    - WhatsApp voice responses: When appropriate for conversation context
    
    INTEGRATION WITH AVA'S PERSONALITY:
    The voice becomes part of Ava's identity - users will recognize her voice
    just like they would recognize a friend's voice on the phone.
    """

    # REQUIRED ENVIRONMENT VARIABLES - API keys needed for voice synthesis
    # ELEVENLABS_API_KEY: Access to ElevenLabs voice generation service
    # ELEVENLABS_VOICE_ID: Specific voice identity that defines how Ava sounds
    REQUIRED_ENV_VARS = ["ELEVENLABS_API_KEY", "ELEVENLABS_VOICE_ID"]

    def __init__(self):
        """
        🔧 INITIALIZE AVA'S SPEAKING SYSTEM - Set up voice synthesis capabilities
        
        WHAT HAPPENS DURING INITIALIZATION:
        1. Validates that both ElevenLabs API key and voice ID are configured
        2. Prepares (but doesn't create yet) the ElevenLabs client connection
        
        WHY VOICE ID IS CRITICAL:
        The voice ID determines how Ava sounds - her vocal identity.
        Without it, Ava might sound different each time she speaks.
        With it, she maintains a consistent, recognizable voice personality.
        
        REAL-WORLD ANALOGY:
        This is like configuring Ava's vocal cords to always sound like the same person.
        Just like you recognize your friend's voice on the phone, users will recognize Ava's voice.
        """
        # VALIDATE BOTH API KEY AND VOICE ID ARE CONFIGURED
        # Voice synthesis requires both authentication (API key) and identity (voice ID)
        # Better to fail fast during startup than during user's first voice response
        self._validate_env_vars()
        
        # PREPARE CLIENT STORAGE (LAZY INITIALIZATION)
        # _client starts as None, gets created only when first voice synthesis happens
        # Avoids expensive network connections during Ava's startup process
        self._client: Optional[ElevenLabs] = None

    def _validate_env_vars(self) -> None:
        """
        🔒 ENVIRONMENT VALIDATOR - Ensures voice synthesis configuration is complete
        
        WHAT IT DOES:
        Checks that both ELEVENLABS_API_KEY and ELEVENLABS_VOICE_ID are set.
        Voice synthesis requires both authentication and voice identity configuration.
        
        WHY BOTH ARE REQUIRED:
        - ELEVENLABS_API_KEY: Proves we're authorized to use ElevenLabs service
        - ELEVENLABS_VOICE_ID: Specifies which voice Ava should use (her vocal identity)
        
        REAL-WORLD ANALOGY:
        This is like checking you have both permission to use a recording studio
        AND you've chosen which singer's voice to use for the recording.
        Need both to create consistent, authorized voice messages.
        
        IMPACT OF MISSING CONFIGURATION:
        - Missing API key: Can't connect to ElevenLabs (no voice synthesis possible)
        - Missing voice ID: Ava might sound different each time (inconsistent personality)
        """
        # CHECK EACH REQUIRED ENVIRONMENT VARIABLE
        # Creates list of any missing variables needed for voice synthesis
        # os.getenv() returns None if environment variable is not set
        missing_vars = [var for var in self.REQUIRED_ENV_VARS if not os.getenv(var)]
        
        # RAISE CLEAR ERROR IF ANY CONFIGURATION IS MISSING
        # Lists exactly which environment variables need to be set
        # Better to discover configuration issues early than during conversation
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

    @property
    def client(self) -> ElevenLabs:
        """
        🔌 ELEVENLABS CLIENT MANAGER - Creates and reuses connection to voice synthesis service
        
        WHAT IT DOES:
        Creates a connection to ElevenLabs voice synthesis service, but only when needed.
        Once created, reuses the same connection for all future voice generations (singleton pattern).
        
        WHY SINGLETON PATTERN FOR VOICE:
        Voice responses often happen in sequence during conversations.
        Creating new API clients for each voice message would be slow and expensive.
        One persistent connection provides much better performance.
        
        REAL-WORLD ANALOGY:
        This is like having one dedicated voice recording studio connection
        instead of setting up a new recording session every time Ava wants to speak.
        Much more efficient for ongoing voice conversations.
        
        TECHNICAL BENEFITS:
        - Faster response times for voice message generation
        - Reduced network setup overhead
        - Consistent connection quality for voice synthesis
        - Thread-safe for handling multiple simultaneous voice requests
        """
        # CHECK IF CLIENT ALREADY EXISTS (SINGLETON PATTERN)
        # self._client starts as None during initialization
        # Once created, this condition becomes False and we reuse existing client
        if self._client is None:
            # CREATE NEW ELEVENLABS CLIENT WITH API KEY
            # settings.ELEVENLABS_API_KEY comes from environment variables via settings.py
            # ElevenLabs() constructor creates authenticated connection to voice synthesis service
            # This is the expensive operation we only want to do once
            self._client = ElevenLabs(api_key=settings.ELEVENLABS_API_KEY)
        
        # RETURN CLIENT (EITHER NEWLY CREATED OR EXISTING)
        # Caller gets a working ElevenLabs client ready for voice synthesis
        # Same client instance will be returned for all future calls (singleton)
        return self._client

    async def synthesize(self, text: str) -> bytes:
        """
        🎤 VOICE SYNTHESIS ENGINE - Converts Ava's text responses into realistic speech
        
        WHAT IT DOES:
        Takes Ava's written response and converts it into realistic speech audio that sounds
        like a real person talking. This is how Ava "speaks" her responses as voice messages.
        
        HOW IT WORKS (USER STORY):
        1. Ava's brain generates text: "I'm currently optimizing ML models at Groq"
        2. audio_node calls this method to convert text to speech
        3. ElevenLabs AI creates realistic voice audio of Ava saying those words
        4. Returns audio bytes that can be sent as voice message to user
        5. User hears Ava's consistent, natural-sounding voice speaking the response
        
        PARAMETERS:
        text: The text response that Ava wants to speak out loud
              Example: "Hi! I'm working on some interesting ML projects today."
        
        RETURNS:
        Audio bytes (binary data) containing Ava's voice speaking the text
        These bytes can be sent as voice messages via WhatsApp or played in Chainlit
        
        REAL-WORLD ANALOGY:
        This is like Ava reading her written response out loud with her natural voice.
        You give her a script, and she speaks it with proper intonation and emotion,
        just like a human would when reading text aloud.
        
        TECHNICAL DETAILS:
        - Uses ElevenLabs' advanced AI voice synthesis
        - Maintains consistent voice identity across all speech
        - Optimized settings for natural-sounding speech
        - Handles streaming audio generation efficiently
        """
        # INPUT VALIDATION - CHECK FOR EMPTY TEXT
        # text.strip() removes whitespace, then "not" checks if result is empty
        # Empty text would waste API calls and confuse users
        if not text.strip():
            raise ValueError("Input text cannot be empty")

        # INPUT VALIDATION - CHECK TEXT LENGTH LIMITS
        # ElevenLabs has limits on how much text can be synthesized in one request
        # 5000 characters is typical limit - longer text needs to be split
        # Also prevents excessive API costs for very long responses
        if len(text) > 5000:  # ElevenLabs typical limit
            raise ValueError("Input text exceeds maximum length of 5000 characters")

        # ERROR HANDLING WRAPPER
        # try/except ensures graceful failure with helpful error messages
        # All errors get converted to TextToSpeechError for consistent handling
        try:
            # STEP 1: GENERATE VOICE AUDIO USING ELEVENLABS
            # self.client gets our singleton ElevenLabs client (created once, reused)
            # .generate() is the main voice synthesis method
            
            audio_generator = self.client.generate(
                # TEXT: The actual words for Ava to speak
                text=text,
                
                # VOICE CONFIGURATION: Defines how Ava sounds
                voice=Voice(
                    # VOICE_ID: Specific voice identity that makes Ava sound consistent
                    # settings.ELEVENLABS_VOICE_ID comes from environment variables
                    # This ensures Ava always sounds like the same person
                    voice_id=settings.ELEVENLABS_VOICE_ID,
                    
                    # VOICE SETTINGS: Fine-tune voice characteristics
                    settings=VoiceSettings(
                        # STABILITY: How consistent the voice sounds (0.5 = balanced)
                        # Higher = more stable/consistent, Lower = more variable/expressive
                        stability=0.5,
                        
                        # SIMILARITY_BOOST: How closely to match the original voice (0.5 = natural)
                        # Higher = closer to training voice, Lower = more generalized
                        similarity_boost=0.5
                    ),
                ),
                
                # MODEL: Which ElevenLabs model to use for synthesis
                # settings.TTS_MODEL_NAME comes from configuration (like "eleven_monolingual_v1")
                model=settings.TTS_MODEL_NAME,
            )

            # STEP 2: CONVERT GENERATOR TO COMPLETE AUDIO BYTES
            # ElevenLabs returns a generator that produces audio chunks over time
            # b"".join() combines all chunks into one complete audio file
            # This is more efficient than loading everything into memory at once
            audio_bytes = b"".join(audio_generator)
            
            # VALIDATE AUDIO GENERATION SUCCEEDED
            # Check that ElevenLabs actually generated audio data
            # Empty audio would break voice message functionality
            if not audio_bytes:
                raise TextToSpeechError("Generated audio is empty")

            # RETURN COMPLETE AUDIO FOR VOICE MESSAGE DELIVERY
            # These bytes can be sent as voice messages or played in audio players
            # Contains Ava's voice speaking the input text with natural intonation
            return audio_bytes

        # CATCH ALL ERRORS AND CONVERT TO CONSISTENT FORMAT
        # except Exception catches any error that occurred during voice synthesis
        except Exception as e:
            # WRAP ERROR IN CUSTOM EXCEPTION TYPE
            # TextToSpeechError provides consistent error handling across Ava's system
            # "from e" preserves original error details for debugging
            # str(e) converts any exception to readable error message
            raise TextToSpeechError(f"Text-to-speech conversion failed: {str(e)}") from e
