"""
⚙️ AVA'S CONTROL PANEL - All the knobs and dials that control how Ava behaves

WHAT IS THIS FILE?
This is Ava's "settings dashboard" - like the control panel in a car where you adjust:
- Which AI models to use (engine type)
- How much memory to remember (fuel efficiency) 
- When to summarize conversations (cruise control settings)
- API keys for different services (keys to start different systems)

WHY CENTRALIZED SETTINGS?
Instead of hardcoding values throughout the codebase, we put them all here:
- Easy to change Ava's behavior without touching code
- Different environments (dev/prod) can have different settings
- Sensitive info (API keys) stays in environment variables

HOW IT WORKS:
1. Values come from .env file (GROQ_API_KEY=your_key_here)
2. Pydantic validates types and provides defaults
3. Other files import 'settings' to access these values
4. If .env missing, app crashes with clear error message

REAL EXAMPLE:
In .env file: TOTAL_MESSAGES_SUMMARY_TRIGGER=20
In nodes.py: if len(messages) > settings.TOTAL_MESSAGES_SUMMARY_TRIGGER:
Result: Ava summarizes conversations after 20 messages

THE SETTINGS CATEGORIES:
🔑 API KEYS - Passwords for different AI services
🤖 MODEL NAMES - Which AI models to use for different tasks  
🧠 MEMORY LIMITS - How much Ava remembers and when to compress
💾 DATABASE PATHS - Where to store conversation data
"""

# Pydantic for type-safe settings management with automatic .env loading
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    🎛️ AVA'S CONFIGURATION CLASS - Type-safe settings with automatic validation
    
    WHAT IS BASESETTINGS?
    A Pydantic class that automatically:
    - Loads values from .env file
    - Validates data types (str, int, etc.)
    - Provides helpful error messages if config is wrong
    - Handles optional values with defaults
    
    WHY PYDANTIC?
    Instead of manually reading environment variables:
    - Automatic type conversion ("20" → 20 for integers)
    - Clear error messages ("GROQ_API_KEY is required but missing")  
    - IDE autocompletion (settings.GROQ_API_KEY shows up in autocomplete)
    - Runtime validation (catches config errors early)
    """
    
    # CONFIGURATION: How to load and handle settings
    model_config = SettingsConfigDict(
        env_file=".env",                # Read from .env file in project root
        extra="ignore",                 # Ignore unknown environment variables  
        env_file_encoding="utf-8"       # Handle international characters properly
    )

    # 🔑 API KEYS SECTION - Authentication for different AI services
    # These MUST be provided in .env file or app won't start
    
    GROQ_API_KEY: str                   # For Llama models (main conversation AI)
                                        # Get from: https://console.groq.com/keys
                                        # Used by: router_node, conversation_node, all text generation
    
    ELEVENLABS_API_KEY: str             # For text-to-speech (Ava's voice)
                                        # Get from: https://elevenlabs.io/app/settings/api-keys
                                        # Used by: audio_node when generating voice responses
    
    ELEVENLABS_VOICE_ID: str            # Which voice to use for Ava  
                                        # Get from: ElevenLabs voice library
                                        # Used by: audio_node to make Ava sound consistent
    
    TOGETHER_API_KEY: str               # For FLUX image generation
                                        # Get from: https://api.together.xyz/settings/api-keys
                                        # Used by: image_node when creating visual responses

    # 🏛️ VECTOR DATABASE SECTION - Where Ava stores her memories about you
    # Qdrant is like Ava's long-term memory bank
    
    QDRANT_API_KEY: str | None          # Optional API key for cloud Qdrant
                                        # None = use local Qdrant instance
                                        # Used by: memory_manager for storing/retrieving memories
    
    QDRANT_URL: str                     # Where the Qdrant database lives
                                        # Examples: "localhost" (local) or "cloud-url.qdrant.io" (cloud)
                                        # Used by: memory_manager to connect to database
    
    QDRANT_PORT: str = "6333"           # Which port Qdrant listens on
                                        # Default 6333 is standard Qdrant port
                                        # Used by: memory_manager for database connection
    
    QDRANT_HOST: str | None = None      # Override host if needed (advanced usage)
                                        # Usually None = use QDRANT_URL
                                        # Used by: memory_manager for complex network setups

    # 🤖 AI MODEL NAMES - Which specific AI models to use for different tasks
    # These determine Ava's "brain power" and capabilities
    
    TEXT_MODEL_NAME: str = "llama-3.3-70b-versatile"    # Main conversation model
                                                         # Groq's most capable model for text
                                                         # Used by: conversation_node, router_node
    
    SMALL_TEXT_MODEL_NAME: str = "gemma2-9b-it"         # Smaller, faster model  
                                                         # For simple tasks where speed > quality
                                                         # Used by: summarization, simple processing
    
    STT_MODEL_NAME: str = "whisper-large-v3-turbo"      # Speech-to-text model
                                                         # Converts your voice messages to text
                                                         # Used by: WhatsApp voice message processing
    
    TTS_MODEL_NAME: str = "eleven_flash_v2_5"           # Text-to-speech model
                                                         # Converts Ava's text to her voice
                                                         # Used by: audio_node for voice responses
    
    TTI_MODEL_NAME: str = "black-forest-labs/FLUX.1-schnell-Free"  # Text-to-image model
                                                                    # Creates images from descriptions
                                                                    # Used by: image_node for visual responses
    
    ITT_MODEL_NAME: str = "meta-llama/llama-4-scout-17b-16e-instruct"          # Image-to-text model
                                                                    # Describes images you send to Ava
                                                                    # Used by: Processing images you share

    # 🧠 MEMORY AND PERFORMANCE LIMITS - Control how much Ava remembers and processes
    # These numbers directly affect Ava's behavior and response speed
    
    MEMORY_TOP_K: int = 3               # How many relevant memories to retrieve
                                        # Higher = more context, slower responses
                                        # Used by: memory_injection_node retrieval
    
    ROUTER_MESSAGES_TO_ANALYZE: int = 3 # How many recent messages router considers
                                        # Higher = better decisions, more expensive
                                        # Used by: router_node for response type decisions
    
    TOTAL_MESSAGES_SUMMARY_TRIGGER: int = 20  # When to compress conversation
                                              # 20 messages = roughly 1-2 pages of chat
                                              # Used by: should_summarize_conversation edge
    
    TOTAL_MESSAGES_AFTER_SUMMARY: int = 5     # How many messages to keep after summarizing
                                              # Rest get compressed into summary text
                                              # Used by: summarize_conversation_node

    # 💾 DATABASE PATHS - Where Ava stores different types of data
    
    SHORT_TERM_MEMORY_DB_PATH: str = "/app/data/memory.db"  # Local database for conversation state
                                                            # Different from Qdrant (long-term memory)
                                                            # Used by: conversation persistence


# STEP 5: Create the global settings instance
# This object gets imported by other files to access configuration
# Why global? Every part of Ava needs access to these settings
settings = Settings()
