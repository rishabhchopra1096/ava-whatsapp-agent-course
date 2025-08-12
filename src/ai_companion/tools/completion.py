"""
🏁 COMPLETION TOOLS - Tools that signal when Pepper has finished her tasks

WHAT IS THIS FILE?
This file contains tools that help Pepper's ReAct agent know when it has completed its work.
Think of it like a "DONE" button that Pepper can press when she's finished helping you.

WHY DO WE NEED COMPLETION TOOLS?
In ReAct (Reasoning + Acting) architecture, the AI agent needs to decide:
- "Should I use another tool to gather more information?"
- "Should I ask the user a question?"  
- "Am I done and ready to give my final response?"

Without these tools, Pepper might keep using tools forever, never knowing when to stop!

HOW IT WORKS IN PEPPER'S BRAIN:
1. User: "Can you help me plan a trip to Paris?"
2. Pepper uses tools: search_web("Paris attractions"), search_memory("user travel preferences")
3. Pepper has enough info → calls Done tool 
4. ReAct system sees Done tool → stops tool calling → gives final response

REAL-WORLD ANALOGY:
This is like Pepper being a research assistant who:
- Gathers information from multiple sources (tools)
- Organizes her findings 
- Says "I'm ready to present my research" (Done tool)
- Gives you the final comprehensive answer
"""

from langchain_core.tools import tool
from pydantic import BaseModel, Field


@tool
class Done(BaseModel):
    """
    🎯 TASK COMPLETION SIGNAL - Pepper's way of saying "I'm done helping with this request"
    
    WHAT IT DOES:
    This tool signals that Pepper has completed the user's request and is ready to provide
    her final response. It's like pressing a "FINISHED" button.
    
    WHEN PEPPER USES THIS:
    - After gathering all necessary information through other tools
    - When she has enough context to provide a complete answer
    - When no additional tools are needed to fulfill the user's request
    
    REAL-WORLD EXAMPLE:
    User: "What should I cook for dinner with chicken and rice?"
    1. Pepper might use: search_recipes("chicken rice recipes")
    2. Pepper might use: search_memory("user's dietary preferences") 
    3. Pepper has enough info → calls Done(summary="Found 3 great chicken rice recipes matching your preferences")
    4. ReAct system stops tool calling → Pepper gives final recipe recommendations
    
    WHY THE SUMMARY FIELD?
    The summary helps Pepper organize her thoughts and ensures she's captured
    the key points before giving her final response to the user.
    """
    
    # SUMMARY FIELD - What Pepper accomplished during this interaction
    # This is like Pepper's internal notes about what she learned and did
    # Example: "Found user's preferred recipes and checked dietary restrictions"
    summary: str = Field(
        description="A brief summary of what was accomplished and any key findings from tool usage"
    )


@tool 
class Question(BaseModel):
    """
    ❓ USER CLARIFICATION TOOL - Pepper's way of asking for more information
    
    WHAT IT DOES:
    When Pepper needs more information from the user to complete their request,
    she uses this tool instead of guessing or making assumptions.
    
    WHEN PEPPER USES THIS:
    - When the user's request is ambiguous or unclear
    - When she needs specific details to provide the best help
    - When there are multiple valid options and she needs user preference
    
    REAL-WORLD EXAMPLE:
    User: "Help me book a flight"
    Pepper realizes she needs more info → calls Question(content="I'd love to help you book a flight! Could you tell me your departure city, destination, and travel dates?")
    ReAct system stops → Pepper asks the clarifying question
    
    WHY THIS IS BETTER THAN GUESSING:
    Instead of Pepper saying "Here are flights from New York to Los Angeles for next week"
    (which might be completely wrong), she asks for the specific details she needs.
    """
    
    # CONTENT FIELD - The actual question Pepper wants to ask the user
    # This should be specific, helpful, and guide the user toward providing useful information
    # Example: "What's your budget range for this trip?" vs "Tell me more"
    content: str = Field(
        description="The specific question to ask the user for clarification or additional information"
    )