# STANDARD LIBRARY IMPORTS - Python's built-in tools

# base64 handles binary data encoding/decoding for image files
# Images from Together AI come as base64 strings that need conversion to bytes
import base64

# logging records success/failure of image generation for debugging
# Essential for monitoring Pepper's creative capabilities in production
import logging

# os provides access to operating system functions like environment variables and file operations
# Used for creating directories and reading API keys securely
import os

# typing provides type hints for better code clarity and error prevention
# Optional = value that might be None
from typing import Optional

# CUSTOM IMPORTS - Pepper-specific modules

# Custom exception for image generation errors (more specific than generic Python exceptions)
from ai_companion.core.exceptions import TextToImageError

# Pre-written prompts that help create better image generation instructions
# IMAGE_ENHANCEMENT_PROMPT = improves simple prompts with artistic details
# IMAGE_SCENARIO_PROMPT = creates narrative scenes from conversation context
from ai_companion.core.prompts import IMAGE_ENHANCEMENT_PROMPT, IMAGE_SCENARIO_PROMPT

# Pepper's centralized configuration containing API keys and model names
from ai_companion.settings import settings

# LANGCHAIN IMPORTS - AI framework components

# PromptTemplate formats dynamic prompts with variables (like Mad Libs for AI)
from langchain.prompts import PromptTemplate

# ChatGroq provides access to Groq's language models for prompt enhancement
# Same service Pepper uses for conversation, but here for improving image prompts
from langchain_groq import ChatGroq

# PYDANTIC IMPORTS - Data validation and structure

# BaseModel creates validated data structures with automatic type checking
# Field adds descriptions and validation rules to model fields
# Ensures AI responses match expected format (like forms with required fields)
from pydantic import BaseModel, Field

# TOGETHER AI IMPORT - Image generation service

# Together provides access to FLUX and other state-of-the-art image generation models
# Different from Groq (text/speech) - Together specializes in image creation
from together import Together


# PYDANTIC DATA MODELS - Structured formats for AI responses
# These ensure AI returns data in exact formats we expect (like validated forms)

class ScenarioPrompt(BaseModel):
    """
    🎨 SCENARIO RESPONSE MODEL - Structure for narrative + image prompt pairs
    
    WHAT IT DOES:
    Defines the exact format for when Pepper creates a story scenario with matching image.
    Forces the AI to return both a narrative text AND a visual prompt in structured format.
    
    REAL-WORLD ANALOGY:
    This is like a form that must be filled out completely - both the story description
    AND the image prompt are required fields that can't be left blank.
    
    USED BY:
    create_scenario() method when generating contextual images from conversation history
    """
    # NARRATIVE FIELD - Pepper's first-person story about what's happening
    # Field(...) means this field is required (can't be empty)
    # Example: "I'm currently working on ML optimization at my desk at Groq"
    narrative: str = Field(..., description="The AI's narrative response to the question")
    
    # IMAGE PROMPT FIELD - Visual description for image generation
    # Example: "A modern tech office with a woman at a computer, ML diagrams on screens"
    image_prompt: str = Field(..., description="The visual prompt to generate an image representing the scene")


class EnhancedPrompt(BaseModel):
    """
    🚀 ENHANCED PROMPT MODEL - Structure for improved image generation prompts
    
    WHAT IT DOES:
    Ensures AI returns enhanced prompts in consistent format.
    Takes simple requests like "draw a robot" and returns detailed artistic descriptions.
    
    REAL-WORLD ANALOGY:
    This is like having an art director improve your basic idea.
    You say "draw a robot" and they return "A sleek humanoid robot with blue LED eyes,
    metallic silver finish, standing in a futuristic laboratory with soft lighting."
    
    USED BY:
    enhance_prompt() method when improving user's simple image requests
    """
    # CONTENT FIELD - The improved, detailed image prompt
    # Enhanced with artistic details, lighting, composition, style
    content: str = Field(
        ...,  # Required field
        description="The enhanced text prompt to generate an image",
    )


class TextToImage:
    """
    🎨 pepper'S IMAGINATION SYSTEM - Pepper's ability to create visual art from text descriptions
    
    WHAT IT DOES:
    This class gives Pepper the power to create actual images based on text descriptions.
    When you ask Pepper to "show me what you're working on" or "draw me a sunset,"
    this system generates real images using state-of-the-art AI models.
    
    HOW IT WORKS (USER STORY):
    1. User: "Pepper, show me what your office at Groq looks like"
    2. create_scenario() analyzes conversation and creates detailed scene description
    3. enhance_prompt() adds artistic details for better image quality
    4. generate_image() uses Together AI's FLUX models to create actual image
    5. User receives beautiful generated image of Pepper's workspace
    
    THREE POWERFUL CAPABILITIES:
    1. **Basic Generation**: Convert simple text to images
    2. **Prompt Enhancement**: Improve simple requests with artistic details
    3. **Scenario Creation**: Generate contextual images from conversation history
    
    REAL-WORLD ANALOGY:
    This is like Pepper being a talented artist with an AI paintbrush.
    You describe what you want to see, and she creates an actual picture for you.
    The difference is her "paintbrush" is cutting-edge AI instead of physical art supplies.
    
    TECHNICAL APPROACH:
    - Uses Together AI's FLUX models (state-of-the-art image generation)
    - Integrates with Groq's LLMs for prompt enhancement
    - Supports both contextual scenarios and direct image requests
    
    USED BY:
    - image_node in LangGraph: When router decides Pepper should respond with images
    - Triggered by conversation context: "show me," "draw," "what does X look like"
    - Both WhatsApp and Chainlit interfaces
    """

    # REQUIRED ENVIRONMENT VARIABLES - API keys for image generation services
    # GROQ_API_KEY: For prompt enhancement using language models
    # TOGETHER_API_KEY: For actual image generation using FLUX models
    REQUIRED_ENV_VARS = ["GROQ_API_KEY", "TOGETHER_API_KEY"]

    def __init__(self):
        """
        🔧 INITIALIZE pepper'S IMAGINATION SYSTEM - Set up image creation capabilities
        
        WHAT HAPPENS DURING INITIALIZATION:
        1. Validates that required API keys are pepperilable (Groq + Together)
        2. Sets up logging for debugging image generation issues
        3. Prepares (but doesn't create yet) the Together AI client connection
        
        WHY DUAL API APPROACH:
        - Groq: Fast, cost-effective language models for prompt enhancement
        - Together: Specialized image generation with latest FLUX models
        - Best of both worlds: smart prompts + beautiful images
        """
        # VALIDATE BOTH API KEYS ARE CONFIGURED
        # Checks Groq (for prompt enhancement) and Together (for image generation)
        # Better to fail fast during startup than during user's first image request
        self._validate_env_vars()
        
        # PREPARE CLIENT STORAGE (LAZY INITIALIZATION)
        # _together_client starts as None, gets created only when needed
        # Avoids expensive network connections during Pepper's startup
        self._together_client: Optional[Together] = None
        
        # SET UP LOGGING FOR IMAGE GENERATION DEBUGGING
        # Records successful generations and failures for production monitoring
        self.logger = logging.getLogger(__name__)

    def _validate_env_vars(self) -> None:
        """
        🔒 ENVIRONMENT VALIDATOR - Ensures both image generation API keys are configured
        
        WHAT IT DOES:
        Checks that both GROQ_API_KEY and TOGETHER_API_KEY are set before trying to use them.
        Image generation requires both services working together.
        
        WHY BOTH KEYS ARE NEEDED:
        - GROQ_API_KEY: Powers prompt enhancement (making simple requests more detailed)
        - TOGETHER_API_KEY: Powers actual image generation (creating the visual art)
        
        REAL-WORLD ANALOGY:
        This is like checking you have both a pencil AND paper before starting to draw.
        Need both tools for the complete image creation process.
        """
        # CHECK EACH REQUIRED API KEY
        # Creates list of any missing environment variables
        # os.getenv() returns None if environment variable is not set
        missing_vars = [var for var in self.REQUIRED_ENV_VARS if not os.getenv(var)]
        
        # RAISE CLEAR ERROR IF ANY KEYS ARE MISSING
        # Lists exactly which API keys need to be configured
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

    @property
    def together_client(self) -> Together:
        """
        🔌 TOGETHER AI CLIENT MANAGER - Creates and reuses connection to image generation service
        
        WHAT IT DOES:
        Creates a connection to Together AI's image generation service, but only when needed.
        Once created, reuses the same connection for all future image generations (singleton pattern).
        
        WHY TOGETHER AI:
        - Specializes in state-of-the-art image generation models like FLUX
        - Better image quality than older models like DALL-E 2
        - Cost-effective for production use with high-quality results
        
        REAL-WORLD ANALOGY:
        This is like having one dedicated art studio connection instead of setting up
        a new studio every time Pepper wants to create an image. Much more efficient.
        """
        # CHECK IF CLIENT ALREADY EXISTS (SINGLETON PATTERN)
        # Only create the expensive network connection once
        if self._together_client is None:
            # CREATE NEW TOGETHER AI CLIENT WITH API KEY
            # settings.TOGETHER_API_KEY comes from environment variables
            # Together() constructor authenticates with Together's image generation service
            self._together_client = Together(api_key=settings.TOGETHER_API_KEY)
        
        # RETURN CLIENT (EITHER NEWLY CREATED OR EXISTING)
        # Same client instance used for all of Pepper's image generation needs
        return self._together_client

    async def generate_image(self, prompt: str, output_path: str = "") -> bytes:
        """Generate an image from a prompt using Together AI."""
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty")

        try:
            self.logger.info(f"Generating image for prompt: '{prompt}'")

            response = self.together_client.images.generate(
                prompt=prompt,
                model=settings.TTI_MODEL_NAME,
                width=1024,
                height=768,
                steps=4,
                n=1,
                response_format="b64_json",
            )

            image_data = base64.b64decode(response.data[0].b64_json)

            if output_path:
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                with open(output_path, "wb") as f:
                    f.write(image_data)
                self.logger.info(f"Image saved to {output_path}")

            return image_data

        except Exception as e:
            raise TextToImageError(f"Failed to generate image: {str(e)}") from e

    async def create_scenario(self, chat_history: list = None) -> ScenarioPrompt:
        """Creates a first-person narrative scenario and corresponding image prompt based on chat history."""
        try:
            formatted_history = "\n".join([f"{msg.type.title()}: {msg.content}" for msg in chat_history[-5:]])

            self.logger.info("Creating scenario from chat history")

            llm = ChatGroq(
                model=settings.TEXT_MODEL_NAME,
                api_key=settings.GROQ_API_KEY,
                temperature=0.4,
                max_retries=2,
            )

            structured_llm = llm.with_structured_output(ScenarioPrompt)

            chain = (
                PromptTemplate(
                    input_variables=["chat_history"],
                    template=IMAGE_SCENARIO_PROMPT,
                )
                | structured_llm
            )

            scenario = chain.invoke({"chat_history": formatted_history})
            self.logger.info(f"Created scenario: {scenario}")

            return scenario

        except Exception as e:
            raise TextToImageError(f"Failed to create scenario: {str(e)}") from e

    async def enhance_prompt(self, prompt: str) -> str:
        """Enhance a simple prompt with additional details and context."""
        try:
            self.logger.info(f"Enhancing prompt: '{prompt}'")

            llm = ChatGroq(
                model=settings.TEXT_MODEL_NAME,
                api_key=settings.GROQ_API_KEY,
                temperature=0.25,
                max_retries=2,
            )

            structured_llm = llm.with_structured_output(EnhancedPrompt)

            chain = (
                PromptTemplate(
                    input_variables=["prompt"],
                    template=IMAGE_ENHANCEMENT_PROMPT,
                )
                | structured_llm
            )

            enhanced_prompt = chain.invoke({"prompt": prompt}).content
            self.logger.info(f"Enhanced prompt: '{enhanced_prompt}'")

            return enhanced_prompt

        except Exception as e:
            raise TextToImageError(f"Failed to enhance prompt: {str(e)}") from e
