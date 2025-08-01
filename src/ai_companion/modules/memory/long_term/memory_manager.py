# STANDARD LIBRARY IMPORTS - Python's built-in tools for memory management

# logging is Python's system for recording what happens when Ava processes memories
# This helps us debug issues like "Why didn't Ava remember what I told her yesterday?"
import logging

# uuid generates unique identifiers for each memory Ava stores
# Think of it like giving each memory a unique serial number so we can find it later
# Example: "abc123-def456-789xyz" - completely unique across all of Ava's memories
import uuid

# datetime handles timestamps for when memories were created
# Ava needs to know WHEN she learned something, not just what she learned
# Example: "I learned the user's name is John on 2024-03-15 at 2:30 PM"
from datetime import datetime

# typing provides type hints for clearer code documentation
# List = list of items, Optional = value that might be None
from typing import List, Optional

# CUSTOM IMPORTS - Ava-specific memory components

# MEMORY_ANALYSIS_PROMPT is a pre-written instruction that teaches Ava how to analyze messages
# It tells her: "Look at this message and decide if it contains important information worth remembering"
from ai_companion.core.prompts import MEMORY_ANALYSIS_PROMPT

# get_vector_store connects to Ava's long-term memory database (like her brain's storage system)
# This is where Ava permanently stores important facts she learns about users
from ai_companion.modules.memory.long_term.vector_store import get_vector_store

# settings contains Ava's configuration like which AI models to use for memory analysis
from ai_companion.settings import settings

# BaseMessage is LangChain's standard format for chat messages
# It wraps messages with metadata like "this came from a human" or "this came from AI"
from langchain_core.messages import BaseMessage

# ChatGroq provides access to Groq's language models for analyzing message importance
# Same service Ava uses for conversation, but here for memory decision-making
from langchain_groq import ChatGroq

# Pydantic provides data validation and structure for memory analysis results
# BaseModel = creates structured data classes, Field = adds validation rules
# Ensures memory analysis results have consistent format
from pydantic import BaseModel, Field


class MemoryAnalysis(BaseModel):
    """
    🧠 MEMORY ANALYSIS RESULT - Structure for Ava's memory decisions
    
    WHAT IT DOES:
    This is like a form that Ava fills out after analyzing each message to decide
    if it contains important information worth remembering long-term.
    
    WHY WE NEED STRUCTURED RESULTS:
    When Ava analyzes a message, she needs to make two decisions:
    1. Is this important enough to remember? (Yes/No)
    2. If yes, how should I format it for storage? (Clean, standardized text)
    
    REAL-WORLD ANALOGY:
    This is like a doctor's assessment form after examining a patient:
    - "Is this condition serious enough to record in medical history?" (is_important)
    - "If yes, what should the medical record say?" (formatted_memory)
    
    EXAMPLE ANALYSIS:
    User says: "My birthday is March 15th and I love chocolate cake!"
    Ava's analysis:
    - is_important: True (personal information worth remembering)
    - formatted_memory: "User's birthday is March 15th and their favorite cake is chocolate"
    """

    # IS_IMPORTANT FIELD - Ava's decision about memory worthiness
    # Field(...) means this field is required (Ava must make a decision)
    # bool = True or False (either worth remembering or not)
    is_important: bool = Field(
        ...,  # Required field - Ava can't skip this decision
        description="Whether the message is important enough to be stored as a memory",
    )
    
    # FORMATTED_MEMORY FIELD - How Ava wants to store the information
    # Optional[str] = either text string or None (if not important)
    # This is the cleaned-up version that goes into permanent memory
    formatted_memory: Optional[str] = Field(
        ...,  # Required field - if important, must provide formatted version
        description="The formatted memory to be stored"
    )


class MemoryManager:
    """
    📚 AVA'S LONG-TERM MEMORY SYSTEM - Manages what Ava remembers permanently
    
    WHAT IT DOES:
    This is Ava's long-term memory system that decides what information is important
    enough to remember permanently and stores it in a way she can find later.
    Think of it as Ava's personal diary combined with a smart filing system.
    
    HOW AVA'S MEMORY WORKS:
    1. **Analysis**: When users say something, Ava analyzes if it's worth remembering
    2. **Storage**: Important information gets stored in her vector database
    3. **Retrieval**: During conversations, Ava searches for relevant memories
    4. **Context**: Retrieved memories get added to her responses for personalization
    
    REAL-WORLD ANALOGY:
    This is like having a personal assistant who:
    - Listens to all your conversations
    - Decides what's important to write down
    - Files information in a smart way
    - Brings up relevant information when needed
    
    MEMORY TYPES AVA STORES:
    - Personal information: "User's birthday is March 15th"
    - Preferences: "User prefers coffee over tea"
    - Important events: "User got promoted at work last week"
    - Relationships: "User's sister lives in Seattle"
    
    TECHNICAL APPROACH:
    - Uses AI to analyze message importance (not everything is worth remembering)
    - Stores memories in vector database for semantic search
    - Formats memories consistently for better retrieval
    
    USED BY:
    - memory_extraction_node: Analyzes new messages for important information
    - memory_injection_node: Retrieves relevant memories for conversation context
    """

    def __init__(self):
        """
        🔧 INITIALIZE AVA'S MEMORY SYSTEM - Set up all memory processing components
        
        WHAT GETS SET UP:
        1. Connection to vector database (where memories are stored)
        2. Logging system for debugging memory issues
        3. AI model for analyzing message importance
        
        WHY THESE COMPONENTS:
        - vector_store: The actual "brain storage" where memories live
        - logger: Helps debug when memory storage/retrieval goes wrong
        - llm: AI that decides what's important enough to remember
        """
        # CONNECT TO AVA'S LONG-TERM MEMORY STORAGE
        # get_vector_store() returns the vector database where Ava stores permanent memories
        # This is like connecting to Ava's "brain storage" where important information lives
        self.vector_store = get_vector_store()
        
        # SET UP LOGGING FOR MEMORY OPERATIONS
        # __name__ = this file's name for labeled logging
        # Helps debug issues like "Why didn't Ava remember my birthday?"
        self.logger = logging.getLogger(__name__)
        
        # CREATE AI MODEL FOR MEMORY ANALYSIS
        # This AI decides what information is important enough to remember permanently
        self.llm = ChatGroq(
            # MODEL: Use smaller, faster model for memory analysis (not main conversation)
            # settings.SMALL_TEXT_MODEL_NAME = something like "llama3-8b-8192"
            model=settings.SMALL_TEXT_MODEL_NAME,
            
            # API_KEY: Authentication for Groq's AI service
            api_key=settings.GROQ_API_KEY,
            
            # TEMPERATURE: Low randomness for consistent memory decisions
            # 0.1 = very consistent (same input usually gives same decision)
            # We want reliable memory analysis, not creative responses
            temperature=0.1,
            
            # MAX_RETRIES: Try again if API call fails (network issues, etc.)
            # 2 = try up to 2 more times if first attempt fails
            max_retries=2,
        ).with_structured_output(MemoryAnalysis)  # Force AI to return MemoryAnalysis format

    async def _analyze_memory(self, message: str) -> MemoryAnalysis:
        """
        🔍 MEMORY IMPORTANCE ANALYZER - Decides if a message contains information worth remembering
        
        WHAT IT DOES:
        Takes a user's message and uses AI to decide if it contains important information
        that Ava should remember permanently. Not everything users say is worth storing.
        
        HOW IT WORKS:
        1. Takes user's message: "I just got a new job at Google!"
        2. Formats it with analysis prompt: "Analyze this message for important info..."
        3. AI analyzes and returns structured decision
        4. Result: {is_important: True, formatted_memory: "User got new job at Google"}
        
        WHY NOT REMEMBER EVERYTHING:
        - Storage costs: Vector databases aren't free
        - Relevance: Too much information makes it hard to find what matters
        - Privacy: Some things users say aren't meant to be permanently stored
        
        EXAMPLES OF IMPORTANT VS UNIMPORTANT:
        Important: "My name is Sarah", "I live in Seattle", "I'm allergic to peanuts"
        Unimportant: "It's raining today", "I'm feeling tired", "What time is it?"
        
        PARAMETERS:
        message: The user's actual message text to analyze
        
        RETURNS:
        MemoryAnalysis object with importance decision and formatted memory text
        """
        # FORMAT THE ANALYSIS PROMPT WITH USER'S MESSAGE
        # MEMORY_ANALYSIS_PROMPT is a template with placeholder for {message}
        # .format() replaces {message} with actual user message
        # Creates complete prompt like: "Analyze this message for important information: [user message]"
        prompt = MEMORY_ANALYSIS_PROMPT.format(message=message)
        
        # SEND PROMPT TO AI FOR ANALYSIS
        # await = wait for AI to analyze the message (takes time to process)
        # self.llm.ainvoke() = send prompt to Groq's AI model
        # Returns MemoryAnalysis with importance decision and formatted memory
        return await self.llm.ainvoke(prompt)

    async def extract_and_store_memories(self, message: BaseMessage) -> None:
        """
        💾 MEMORY EXTRACTION AND STORAGE - Main function that processes messages for permanent storage
        
        WHAT IT DOES:
        This is the main function called by Ava's memory_extraction_node in her workflow.
        It takes each user message, analyzes it for important information, and stores
        anything worth remembering in Ava's long-term memory database.
        
        THE COMPLETE MEMORY STORAGE PROCESS:
        1. Check if message is from human (ignore Ava's own messages)
        2. Analyze message for importance using AI
        3. If important, check if we already have similar information
        4. If new information, store it with timestamp and unique ID
        
        WHY CHECK FOR DUPLICATES:
        If user says "My name is John" today and "My name is John" tomorrow,
        we don't want two identical memories cluttering Ava's storage.
        
        REAL-WORLD ANALOGY:
        This is like a personal assistant who:
        - Listens to everything you say
        - Decides what's worth writing in your personal file
        - Checks if they already wrote it down before
        - Only adds new information to avoid duplicates
        
        PARAMETERS:
        message: LangChain message object containing user's text and metadata
        
        CALLED BY:
        memory_extraction_node in Ava's LangGraph workflow
        """
        # STEP 1: ONLY PROCESS HUMAN MESSAGES
        # message.type tells us who sent this message: "human" or "ai"
        # We only want to remember what users tell us, not what Ava says
        # If it's not from a human, exit early (return immediately)
        if message.type != "human":
            return

        # STEP 2: ANALYZE MESSAGE FOR IMPORTANCE
        # await = wait for AI analysis to complete (takes time)
        # _analyze_memory() uses AI to decide if this message contains important information
        # Returns MemoryAnalysis with decision and formatted text
        analysis = await self._analyze_memory(message.content)
        
        # STEP 3: PROCEED ONLY IF MESSAGE IS IMPORTANT AND HAS FORMATTED CONTENT
        # analysis.is_important = True if AI thinks this is worth remembering
        # analysis.formatted_memory = cleaned-up text ready for storage
        # Both must be true to proceed with storage
        if analysis.is_important and analysis.formatted_memory:
            
            # STEP 4: CHECK FOR DUPLICATE MEMORIES
            # find_similar_memory() searches existing memories for similar content
            # Returns existing memory if we already have something very similar
            # Prevents storing "My name is John" multiple times
            similar = self.vector_store.find_similar_memory(analysis.formatted_memory)
            
            if similar:
                # DUPLICATE FOUND - SKIP STORAGE
                # Log that we found duplicate so developers can debug memory system
                # f"..." = f-string formatting to include the actual memory text
                self.logger.info(f"Similar memory already exists: '{analysis.formatted_memory}'")
                return  # Exit early, don't store duplicate

            # STEP 5: STORE NEW MEMORY WITH METADATA
            # Log successful storage for debugging and monitoring
            self.logger.info(f"Storing new memory: '{analysis.formatted_memory}'")
            
            # Actually store the memory in vector database
            self.vector_store.store_memory(
                # TEXT: The formatted memory content to store
                text=analysis.formatted_memory,
                
                # METADATA: Additional information about this memory
                metadata={
                    # ID: Unique identifier for this specific memory
                    # str(uuid.uuid4()) generates unique string like "abc123-def456-789xyz"
                    "id": str(uuid.uuid4()),
                    
                    # TIMESTAMP: When this memory was created
                    # datetime.now().isoformat() creates timestamp like "2024-03-15T14:30:25"
                    "timestamp": datetime.now().isoformat(),
                },
            )

    def get_relevant_memories(self, context: str) -> List[str]:
        """
        🔍 MEMORY RETRIEVAL SYSTEM - Finds relevant memories for current conversation
        
        WHAT IT DOES:
        When Ava is having a conversation, this function searches her long-term memory
        to find information that's relevant to what's being discussed right now.
        
        HOW IT WORKS (USER STORY):
        1. User says: "What do you remember about my job?"
        2. context = "What do you remember about my job?"
        3. Searches vector database for memories related to "job"
        4. Finds: ["User works at Google as software engineer", "User got promoted last month"]
        5. Returns these memories to be included in Ava's response
        
        WHY VECTOR SEARCH:
        Traditional search looks for exact word matches. Vector search understands meaning.
        - Traditional: "job" only finds memories containing word "job"
        - Vector: "job" finds "work", "career", "employment", "position", etc.
        
        REAL-WORLD ANALOGY:
        This is like asking a librarian "Find me books about space exploration."
        A good librarian doesn't just look for books with "space exploration" in the title.
        They also find books about "astronauts", "NASA", "rockets", "planets", etc.
        
        PARAMETERS:
        context: Current conversation context to search for (what user is talking about)
        
        RETURNS:
        List of memory text strings relevant to the current conversation
        
        USED BY:
        memory_injection_node in Ava's LangGraph workflow
        """
        # SEARCH VECTOR DATABASE FOR RELEVANT MEMORIES
        # self.vector_store.search_memories() finds memories semantically similar to context
        # k=settings.MEMORY_TOP_K limits number of results (typically 3-5 memories)
        # Too many memories would overwhelm Ava's response context
        memories = self.vector_store.search_memories(context, k=settings.MEMORY_TOP_K)
        
        # LOG RETRIEVED MEMORIES FOR DEBUGGING
        # Only log if we actually found memories (if memories list is not empty)
        if memories:
            # Loop through each found memory and log it with similarity score
            for memory in memories:
                # Log at debug level (only shows in detailed logs)
                # memory.score = how similar this memory is to search context (0.0 to 1.0)
                # .2f = format score to 2 decimal places (like 0.85 instead of 0.8532451)
                self.logger.debug(f"Memory: '{memory.text}' (score: {memory.score:.2f})")
        
        # RETURN JUST THE TEXT CONTENT OF MEMORIES
        # memories contains Memory objects with text, metadata, and scores
        # [memory.text for memory in memories] extracts just the text content
        # This is what goes into Ava's conversation context
        return [memory.text for memory in memories]

    def format_memories_for_prompt(self, memories: List[str]) -> str:
        """
        📝 MEMORY FORMATTER - Prepares memories for inclusion in Ava's conversation prompt
        
        WHAT IT DOES:
        Takes a list of relevant memories and formats them as clean bullet points
        that can be added to Ava's conversation prompt. This gives Ava context
        about what she knows about the user.
        
        HOW IT WORKS:
        INPUT: ["User works at Google", "User likes coffee", "User's birthday is March 15"]
        OUTPUT: 
        "- User works at Google
        - User likes coffee  
        - User's birthday is March 15"
        
        WHY BULLET POINT FORMAT:
        - Clean and readable for AI processing
        - Clear separation between different memories
        - Easy for Ava's language model to parse and understand
        
        REAL-WORLD ANALOGY:
        This is like preparing notes for someone before they meet a client.
        Instead of handing them a messy pile of information, you organize it
        into clean bullet points they can quickly scan and understand.
        
        PARAMETERS:
        memories: List of memory text strings to format
        
        RETURNS:
        Formatted string with bullet points, or empty string if no memories
        
        USED BY:
        memory_injection_node when adding context to Ava's conversation prompt
        """
        # HANDLE EMPTY MEMORIES LIST
        # If no relevant memories found, return empty string
        # This prevents adding empty bullet points to Ava's prompt
        if not memories:
            return ""
        
        # FORMAT MEMORIES AS BULLET POINTS
        # "\n".join() combines list items with newline characters
        # f"- {memory}" adds bullet point format to each memory
        # Result: Each memory becomes a separate line starting with "- "
        return "\n".join(f"- {memory}" for memory in memories)


def get_memory_manager() -> MemoryManager:
    """
    🏭 MEMORY MANAGER FACTORY - Creates and returns Ava's memory management system
    
    WHAT IT DOES:
    Simple factory function that creates and returns a MemoryManager instance.
    This is used by Ava's LangGraph nodes that need to work with long-term memory.
    
    WHY A FACTORY FUNCTION:
    - Consistent way to create memory manager across different parts of Ava's system
    - Could be extended later to implement singleton pattern or caching
    - Provides clear interface for accessing memory functionality
    
    REAL-WORLD ANALOGY:
    This is like having a personnel department that assigns you a personal assistant.
    Instead of you figuring out how to hire an assistant, you just call the department
    and they give you a qualified assistant ready to work.
    
    RETURNS:
    Fully configured MemoryManager ready to analyze and store memories
    
    USED BY:
    - memory_extraction_node: For analyzing and storing new memories
    - memory_injection_node: For retrieving relevant memories for conversation
    """
    # CREATE AND RETURN NEW MEMORY MANAGER INSTANCE
    # MemoryManager() constructor sets up vector store connection, logging, and AI model
    # Returns fully configured memory system ready for immediate use
    return MemoryManager()
