"""
🛠️ pepper'S UTILITY TOOLBOX - Helper functions that keep everything running smoothly

WHAT IS THIS FILE?
This file contains "helper functions" - small, reusable utilities that other parts
of Pepper need. Think of it as a toolbox with useful gadgets:
- AI model configurator (wrench)
- Text cleaner (sandpaper)
- Module factories (assembly tools)

WHY CENTRALIZE HELPERS?
Instead of repeating the same code everywhere, we put common utilities here:
- get_chat_model() used by: router_node, conversation_node, summarize_node
- Text/image/speech modules used by: all response nodes
- Output parsers used by: chains that need clean text

THE FACTORY PATTERN:
These functions are "factories" - they create and configure objects:
- get_chat_model() → Creates configured Groq AI model
- get_text_to_speech_module() → Creates ElevenLabs TTS client
- get_text_to_image_module() → Creates FLUX image generator

REAL USAGE EXAMPLES:
router_node: model = get_chat_model(temperature=0.3)  # Low creativity
conversation_node: model = get_chat_model()           # Default creativity  
audio_node: tts = get_text_to_speech_module()         # Voice synthesis
image_node: tti = get_text_to_image_module()          # Image generation

THE HELPER CATEGORIES:
🤖 AI MODEL FACTORIES - Create configured AI service clients
🧹 TEXT PARSERS - Clean up AI output formatting
🏭 MODULE FACTORIES - Create media processing modules
"""

# Regular expressions for text cleaning
import re

# LangChain components for output processing
from langchain_core.output_parsers import StrOutputParser
# Groq integration for fast LLM inference
from langchain_groq import ChatGroq

# Our custom modules for different AI capabilities
from ai_companion.modules.image.image_to_text import ImageToText    # Describe images
from ai_companion.modules.image.text_to_image import TextToImage    # Generate images  
from ai_companion.modules.speech import TextToSpeech               # Convert text to voice
# Configuration settings
from ai_companion.settings import settings


def get_chat_model(temperature: float = 0.7):
    """
    🤖 AI MODEL FACTORY - Creates a configured Groq AI model for text generation
    
    WHAT IT DOES:
    Creates a ready-to-use AI model with all the right settings.
    Like getting a pre-tuned race car instead of building one from scratch.
    
    🚀 GROQ MODELS:
    Returns standard ChatGroq with Llama models:
    - EXTREMELY fast inference (275+ tokens/second)
    - Cost-effective for high-volume usage
    - Reliable and consistent performance
    - Perfect for real-time chat applications
    
    TEMPERATURE PARAMETER:
    Controls AI creativity/randomness (0.0 to 1.0):
    - 0.0 = Completely predictable, same response every time
    - 0.3 = Slightly creative, good for consistent decisions (router)
    - 0.7 = Balanced creativity, natural conversations (default)
    - 1.0 = Maximum creativity, can be chaotic
    
    USAGE EXAMPLES:
    - router_node uses temperature=0.3 (consistent routing decisions)
    - conversation_node uses default 0.7 (natural personality)
    - summarize_node might use 0.5 (creative but focused)
    
    CONFIGURATION SOURCE:
    All settings come from settings.py:
    - API_KEY: Your Groq authentication
    - MODEL_NAME: Model to use (typically "llama-3.3-70b-versatile")
    - TEMPERATURE: Creativity level for this specific use
    """
    
    # 🌐 DETECT GPT-OSS MODEL AND ADD REASONING CAPABILITIES
    return ChatGroq(
        api_key=settings.GROQ_API_KEY,        # Authentication for Groq API
        model_name=settings.TEXT_MODEL_NAME,  # GPT-OSS model name from settings
        temperature=temperature,              # Creativity level (0.0-1.0)
        # reasoning_effort="medium",            # GPT-OSS reasoning level (low/medium/high)
        # max_tokens=2000,                      # Longer responses for detailed reasoning
    )


def get_text_to_speech_module():
    """
    🎵 VOICE SYNTHESIS FACTORY - Creates ElevenLabs text-to-speech client
    
    WHAT IT DOES:
    Creates a configured ElevenLabs client that can convert Pepper's text responses
    into natural-sounding speech using her specific voice.
    
    WHY ELEVENLABS?
    - Most natural-sounding AI voices pepperilable
    - Consistent voice identity (Pepper always sounds like Pepper)
    - Supports emotional expression and tone variation
    - High-quality audio output for professional feel
    
    HOW IT'S USED:
    audio_node calls this to get a TTS client, then:
    1. Generates text response (like conversation_node)
    2. Converts text to speech using Pepper's voice
    3. Returns audio buffer for WhatsApp voice message
    
    VOICE CONFIGURATION:
    - Voice ID stored in settings.ELEVENLABS_VOICE_ID
    - API key from settings.ELEVENLABS_API_KEY
    - Model settings optimized for conversational speech
    """
    return TextToSpeech()


def get_text_to_image_module():
    """
    🖼️ IMAGE GENERATION FACTORY - Creates FLUX text-to-image client
    
    WHAT IT DOES:
    Creates a configured FLUX AI client that can generate photorealistic images
    based on text descriptions of what Pepper is doing.
    
    WHY FLUX?
    - State-of-the-art image quality (better than DALL-E 2)
    - Fast generation (good for real-time responses)
    - Excellent at photorealistic scenes
    - Cost-effective through Together AI
    
    HOW IT'S USED:
    image_node calls this to get an image generator, then:
    1. Creates scenario prompt ("Pepper coding at her desk...")
    2. Generates photorealistic image using FLUX
    3. Saves image file and returns path for WhatsApp
    
    MODEL CONFIGURATION:
    - Uses "black-forest-labs/FLUX.1-schnell-Free" model
    - API access through Together AI platform
    - Optimized for realistic lifestyle photography
    """
    return TextToImage()


def get_image_to_text_module():
    """
    👁️ VISION ANALYSIS FACTORY - Creates image-to-text client for understanding images
    
    WHAT IT DOES:
    Creates a client that can "see" and describe images that users send to Pepper.
    Like giving Pepper eyes to understand visual content.
    
    WHY IMAGE-TO-TEXT?
    Users might send Pepper photos and expect her to understand them:
    - "What do you think of my setup?" (with desk photo)
    - "Look at this sunset!" (with sunset photo)  
    - "Can you help me with this code?" (with screenshot)
    
    HOW IT WORKS:
    1. User sends image to WhatsApp
    2. This module analyzes the image content
    3. Converts visual information to text description
    4. Pepper can then respond contextually about the image
    
    MODEL USED:
    - "llama-3.2-90b-vision-preview" (multimodal model)
    - Can understand both images and text simultaneously
    - Provides detailed, contextual descriptions
    """
    return ImageToText()


def remove_asterisk_content(text: str) -> str:
    """
    🧹 TEXT CLEANER - Removes asterisk-wrapped formatting from AI responses
    
    WHAT IT DOES:
    Removes text wrapped in asterisks (*like this*) from AI responses.
    Cleans up formatting that looks awkward in chat messages.
    
    WHY REMOVE ASTERISKS?
    AI models often use asterisks for emphasis or actions:
    - "I'm working on code *excitedly*" → "I'm working on code"
    - "That's amazing! *claps hands*" → "That's amazing!"
    - "*thinking* Let me check that..." → "Let me check that..."
    
    This makes responses feel more natural in WhatsApp conversations.
    
    HOW IT WORKS:
    Uses regex pattern r"\\*.*?\\*" to find and remove:
    - \\* = literal asterisk character
    - .*? = any characters (non-greedy)
    - \\* = closing asterisk
    - .strip() removes extra whitespace
    
    EXAMPLES:
    Input: "Hey! *waves* How are you doing *today*?"
    Output: "Hey! How are you doing?"
    
    Input: "I'm *really* excited about this project!"
    Output: "I'm excited about this project!"
    """
    return re.sub(r"\*.*?\*", "", text).strip()


class AsteriskRemovalParser(StrOutputParser):
    """
    🔧 CUSTOM OUTPUT PARSER - LangChain parser that automatically cleans asterisk formatting
    
    WHAT IT IS:
    A custom LangChain output parser that extends the standard StrOutputParser
    to automatically clean asterisk formatting from AI responses.
    
    WHY EXTEND STROUTPUTPARSER?
    LangChain's StrOutputParser converts AI output to clean strings, but doesn't
    handle formatting removal. This class adds that capability.
    
    HOW IT WORKS:
    1. Inherits all functionality of StrOutputParser
    2. Overrides the parse() method to add asterisk removal
    3. super().parse(text) gets the standard string conversion
    4. remove_asterisk_content() cleans the formatting
    5. Returns clean, natural text
    
    USAGE IN CHAINS:
    get_character_response_chain() uses this parser:
    prompt | model | AsteriskRemovalParser()
    
    This ensures Pepper's responses are always clean and natural-looking.
    
    EXAMPLE TRANSFORMATION:
    AI Output: "I'm *currently* debugging some Python *code*!"
    After Parser: "I'm currently debugging some Python code!"
    """
    def parse(self, text):
        # First, use the parent class to convert to string
        # Then, remove asterisk formatting for clean output
        return remove_asterisk_content(super().parse(text))
