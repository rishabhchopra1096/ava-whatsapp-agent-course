# STANDARD LIBRARY IMPORTS - Python's built-in tools

# base64 is Python's module for encoding binary data (like images) as text
# Images are binary data, but APIs need text format - base64 converts between them
# Think of it like translating a picture into a special alphabet that computers can send over internet
import base64

# logging is Python's system for recording what happens in the program (like a flight recorder)
# When image analysis succeeds or fails, we write details to logs for debugging
# Essential for troubleshooting issues with real users in production
import logging

# os provides access to operating system functions like reading environment variables
# We use this to safely access API keys stored as environment variables (not hardcoded in files)
import os

# typing provides type hints that make code clearer and help catch errors
# Optional = value that might be None, Union = value that could be multiple types
from typing import Optional, Union

# CUSTOM IMPORTS - Ava-specific modules

# Custom exception class for image processing errors
# Better than generic Python exceptions because it's specific to our image analysis system
from ai_companion.core.exceptions import ImageToTextError

# Ava's configuration settings containing API keys and model names
# Centralized configuration makes it easy to change models or settings across the system
from ai_companion.settings import settings

# Groq is the AI service that provides vision capabilities
# Same company that provides Ava's LLM processing and speech recognition
# Offers fast, cost-effective access to advanced AI models including vision
from groq import Groq


class ImageToText:
    """
    👁️ AVA'S VISION SYSTEM - Ava's ability to "see" and understand images
    
    WHAT IT DOES:
    This class gives Ava the ability to analyze images that users send her.
    When you upload a photo to Ava (via WhatsApp or Chainlit), this system describes
    what's in the image so Ava can talk about it intelligently.
    
    HOW IT WORKS:
    1. User sends image → Image gets converted to base64 text
    2. Text + image sent to Groq's vision AI model
    3. AI model analyzes image and returns text description
    4. Ava can now "see" the image and discuss it naturally
    
    REAL-WORLD ANALOGY:
    This is like Ava having eyes that can look at photos and describe what she sees.
    Instead of saying "I can't see images," she can say "I see a golden retriever
    playing in Golden Gate Park on a sunny day."
    
    USED BY:
    - WhatsApp interface: When users send photos via WhatsApp
    - Chainlit interface: When users drag and drop images in web chat
    - LangGraph workflow: Results get incorporated into conversation context
    
    TECHNICAL APPROACH:
    Uses Groq's implementation of vision models (like GPT-4 Vision) for fast,
    cost-effective image analysis with the same API ecosystem as Ava's other AI capabilities.
    """

    # REQUIRED ENVIRONMENT VARIABLES - Security configuration
    # These must be set as environment variables before Ava can analyze images
    # Environment variables keep API keys secure and out of source code
    REQUIRED_ENV_VARS = ["GROQ_API_KEY"]

    def __init__(self):
        """
        🔧 INITIALIZE AVA'S VISION SYSTEM - Set up image analysis capabilities
        
        WHAT HAPPENS DURING INITIALIZATION:
        1. Validates that required API keys are available
        2. Sets up logging for debugging image analysis issues
        3. Prepares (but doesn't create yet) the Groq client connection
        
        WHY DELAYED CLIENT CREATION:
        We use "lazy initialization" - only create the expensive Groq client
        when we actually need to analyze an image, not during startup.
        """
        # VALIDATE ENVIRONMENT VARIABLES BEFORE PROCEEDING
        # Checks that GROQ_API_KEY is set - fails fast if misconfigured
        # Better to catch configuration errors early than during actual image analysis
        self._validate_env_vars()
        
        # PREPARE CLIENT STORAGE (LAZY INITIALIZATION)
        # _client starts as None, gets created only when needed (singleton pattern)
        # This avoids creating expensive network connections during startup
        self._client: Optional[Groq] = None
        
        # SET UP LOGGING FOR THIS SPECIFIC MODULE
        # __name__ = "ai_companion.modules.image.image_to_text"
        # Creates a labeled logger for debugging image analysis issues
        # When image analysis succeeds/fails, logs include clear source identification
        self.logger = logging.getLogger(__name__)

    def _validate_env_vars(self) -> None:
        """
        🔒 ENVIRONMENT VARIABLE VALIDATOR - Ensures required API keys are configured
        
        WHAT IT DOES:
        Checks that all required environment variables (like API keys) are set
        before trying to use them. Prevents crashes later when we try to analyze images.
        
        WHY THIS IS IMPORTANT:
        If GROQ_API_KEY is missing, it's better to fail immediately during startup
        than to fail when a user sends their first image. Early failure = easier debugging.
        
        HOW IT WORKS:
        1. Checks each required environment variable
        2. Collects any that are missing
        3. Raises clear error message if any are missing
        
        REAL-WORLD ANALOGY:
        This is like checking you have your keys before leaving the house.
        Better to discover you forgot them at home than at the locked car.
        """
        # CHECK EACH REQUIRED ENVIRONMENT VARIABLE
        # List comprehension: creates list of variables that are missing (None or empty)
        # os.getenv(var) returns the environment variable value or None if not set
        # "not os.getenv(var)" is True if variable is None or empty string
        missing_vars = [var for var in self.REQUIRED_ENV_VARS if not os.getenv(var)]
        
        # RAISE ERROR IF ANY VARIABLES ARE MISSING
        # Only executes if missing_vars list contains items (missing variables found)
        if missing_vars:
            # Create clear error message listing all missing variables
            # ', '.join() converts ["VAR1", "VAR2"] into "VAR1, VAR2"
            # f"..." f-string inserts the joined variable names into error message
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

    @property
    def client(self) -> Groq:
        """
        🔌 GROQ CLIENT MANAGER - Creates and reuses connection to Groq's vision AI service
        
        WHAT IT DOES:
        Creates a connection to Groq's AI service for image analysis, but only when needed.
        Once created, reuses the same connection for all future image analyses (singleton pattern).
        
        WHY SINGLETON PATTERN:
        Creating new API clients is expensive (network setup, authentication, etc.).
        It's much faster to create one client and reuse it for all image analyses.
        
        REAL-WORLD ANALOGY:
        This is like having one phone line to Groq instead of dialing a new connection
        every time Ava needs to analyze an image. Much more efficient.
        
        TECHNICAL DETAILS:
        - @property makes this look like a variable but actually runs code
        - Lazy initialization: client created only when first image analysis happens
        - Thread-safe for handling multiple simultaneous image analyses
        """
        # CHECK IF CLIENT ALREADY EXISTS
        # self._client starts as None during initialization
        # Once created, this condition becomes False and we reuse existing client
        if self._client is None:
            # CREATE NEW GROQ CLIENT WITH API KEY
            # settings.GROQ_API_KEY comes from environment variables via settings.py
            # Groq() constructor creates authenticated connection to Groq's AI services
            # This is the expensive operation we only want to do once
            self._client = Groq(api_key=settings.GROQ_API_KEY)
        
        # RETURN CLIENT (EITHER NEWLY CREATED OR EXISTING)
        # Caller gets a working Groq client ready for image analysis
        # Same client instance will be returned for all future calls (singleton)
        return self._client

    async def analyze_image(self, image_data: Union[str, bytes], prompt: str = "") -> str:
        """Analyze an image using Groq's vision capabilities.

        Args:
            image_data: Either a file path (str) or binary image data (bytes)
            prompt: Optional prompt to guide the image analysis

        Returns:
            str: Description or analysis of the image

        Raises:
            ValueError: If the image data is empty or invalid
            ImageToTextError: If the image analysis fails
        """
        try:
            # Handle file path
            if isinstance(image_data, str):
                if not os.path.exists(image_data):
                    raise ValueError(f"Image file not found: {image_data}")
                with open(image_data, "rb") as f:
                    image_bytes = f.read()
            else:
                image_bytes = image_data

            if not image_bytes:
                raise ValueError("Image data cannot be empty")

            # Convert image to base64
            base64_image = base64.b64encode(image_bytes).decode("utf-8")

            # Default prompt if none provided
            if not prompt:
                prompt = "Please describe what you see in this image in detail."

            # Create the messages for the vision API
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                        },
                    ],
                }
            ]

            # Make the API call
            response = self.client.chat.completions.create(
                model=settings.ITT_MODEL_NAME,
                messages=messages,
                max_tokens=1000,
            )

            if not response.choices:
                raise ImageToTextError("No response received from the vision model")

            description = response.choices[0].message.content
            self.logger.info(f"Generated image description: {description}")

            return description

        except Exception as e:
            raise ImageToTextError(f"Failed to analyze image: {str(e)}") from e
