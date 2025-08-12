"""
🔗 pepper'S BRAIN ASSEMBLY LINE - Where prompts get connected to AI models to create "chains"

WHAT IS THIS FILE?
This file creates "chains" - pre-assembled combinations of:
- PROMPT (the instructions for the AI)
- MODEL (the AI that follows the instructions)  
- OUTPUT PARSER (cleans up the AI's response)

Think of it like assembling a sandwich:
- Prompt = The recipe ("make a ham sandwich")
- Model = The chef (AI that follows the recipe)
- Parser = Quality control (removes burned edges)

WHY ARE CHAINS IMPORTANT?
Instead of manually connecting prompts + models + parsers every time,
chains pre-package them for easy reuse. Like having pre-made meal kits!

THE CHAIN CONCEPT:
prompt | model | parser
This "|" symbol means "pipe the output to the next step"
Like: Instructions → AI → Clean Response

HOW CHAINS ARE USED IN pepper:
1. router_node calls get_router_chain() → decides text/image/audio
2. conversation_node calls get_character_response_chain() → generates Pepper's personality
3. All other response nodes use these same chains

REAL EXAMPLE FLOW:
You: "What are you up to?"
→ get_router_chain(): ROUTER_PROMPT + Groq + RouterResponse = "image"
→ get_character_response_chain(): CHARACTER_CARD_PROMPT + Groq + Parser = "I'm coding!"

THE TWO MAIN CHAINS:
🤖 get_router_chain() - Decides how to respond (text/image/audio)
👩‍💻 get_character_response_chain() - Generates Pepper's personality responses
"""

# LangChain core components for building prompt templates
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# Pydantic for structured output validation
from pydantic import BaseModel, Field

# Our custom prompts (the "instructions" for the AI)
from ai_companion.core.prompts import CHARACTER_CARD_PROMPT, ROUTER_PROMPT
# Helper functions and parsers
from ai_companion.graph.utils.helpers import AsteriskRemovalParser, get_chat_model


class RouterResponse(BaseModel):
    """
    📋 STRUCTURED OUTPUT FORMAT - Forces the router to return valid responses only
    
    WHAT IS THIS?
    A Pydantic model that defines exactly what the router AI can return.
    Think of it as a form with strict validation rules.
    
    WHY USE STRUCTURED OUTPUT?
    Without this, AI might return:
    - "I think you want an image response" (too verbose)
    - "img" (wrong format)
    - "conversation or maybe image?" (indecisive)
    
    WITH STRUCTURED OUTPUT, AI must return:
    - RouterResponse(response_type="image") ✅
    - RouterResponse(response_type="conversation") ✅
    - RouterResponse(response_type="audio") ✅
    - RouterResponse(response_type="voice_call") ✅
    
    HOW IT WORKS:
    1. AI generates its decision
    2. LangChain forces it into this RouterResponse format
    3. If invalid, AI tries again until it fits the schema
    4. We get guaranteed valid output: response.response_type
    """
    response_type: str = Field(
        description="The response type to give to the user. It must be one of: 'conversation', 'image', 'audio', or 'voice_call'"
    )


def get_router_chain():
    """
    🤖 THE DECISION MAKER CHAIN - Assembles the router that decides response type
    
    WHAT IT BUILDS:
    A complete "decision-making assembly line" that takes conversation messages
    and returns a structured decision about how Pepper should respond.
    
    THE ASSEMBLY LINE:
    1. PROMPT: Takes messages + ROUTER_PROMPT instructions
    2. MODEL: Google Gemini 2.5 Flash analyzes and decides  
    3. STRUCTURED OUTPUT: Forces response into RouterResponse format
    
    WHY TEMPERATURE 0.3?
    - Temperature = "creativity level" (0 = robotic, 1 = chaotic)
    - 0.3 = slightly creative but mostly consistent
    - We want consistent routing decisions, not random creativity
    
    THE CHAIN COMPONENTS EXPLAINED:
    """
    
    # STEP 1: Get the AI model with specific settings
    # get_chat_model() returns Google Gemini 2.5 Flash (from helpers.py)
    # temperature=0.3 makes decisions more consistent/predictable
    # .with_structured_output() forces responses into RouterResponse format
    model = get_chat_model(temperature=0.3).with_structured_output(RouterResponse)

    # STEP 2: Create the prompt template
    # ChatPromptTemplate structures the conversation for the AI
    # ("system", ROUTER_PROMPT) = System instructions (how to behave)
    # MessagesPlaceholder = Where actual conversation messages get inserted
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", ROUTER_PROMPT),                        # The router's instructions
            MessagesPlaceholder(variable_name="messages")     # Recent conversation messages
        ]
    )

    # STEP 3: Chain everything together using the pipe operator
    # prompt | model means: "send prompt output to model input"
    # Result: A ready-to-use chain that takes messages and returns RouterResponse
    return prompt | model


def get_character_response_chain(summary: str = ""):
    """
    👩‍💻 pepper'S PERSONALITY CHAIN - Assembles the response generator with Pepper's complete personality
    
    WHAT IT BUILDS:
    The complete "Pepper personality generator" that takes conversation context
    and produces responses that sound exactly like Pepper - witty, tech-savvy, human.
    
    THE ASSEMBLY LINE:
    1. PROMPT: Pepper's personality + conversation context + optional summary
    2. MODEL: Google Gemini 2.5 Flash generates response in Pepper's voice
    3. PARSER: Removes asterisk formatting (*like this*) for clean output
    
    WHY NO STRUCTURED OUTPUT?
    Unlike the router, we want creative, natural text responses.
    No rigid format needed - just Pepper being herself.
    
    SUMMARY PARAMETER:
    - Used for long conversations that have been compressed
    - Gives Pepper context about what happened earlier
    - Example: "User discussed work projects, asked about weekend plans"
    """
    
    # STEP 1: Get the AI model with default creativity settings
    # No temperature specified = uses default (0.7) for more natural responses
    # No structured output = AI can respond freely in natural language
    model = get_chat_model()
    
    # STEP 2: Build the system message (Pepper's personality instructions)
    # Start with CHARACTER_CARD_PROMPT (Pepper's complete identity)
    system_message = CHARACTER_CARD_PROMPT

    # STEP 3: Add conversation summary if pepperilable (for long conversations)
    # This gives Pepper context about what happened before the current messages
    # Helps maintain consistency across long chats that have been summarized
    if summary:
        system_message += f"\n\nSummary of conversation earlier between Pepper and the user: {summary}"

    # STEP 4: Create the prompt template with personality + messages
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_message),                       # Pepper's complete personality + summary
            MessagesPlaceholder(variable_name="messages"),    # Current conversation messages
        ]
    )

    # STEP 5: Chain everything together with output cleaning
    # prompt | model | AsteriskRemovalParser means:
    # 1. Send prompt to model
    # 2. Model generates response  
    # 3. Parser cleans up formatting (removes *emphasis* marks)
    # Result: Clean, natural-sounding Pepper responses
    return prompt | model | AsteriskRemovalParser()
