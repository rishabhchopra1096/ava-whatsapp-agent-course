# STANDARD LIBRARY IMPORTS - Python's built-in tools for data management

# os provides access to operating system functions like environment variables
# Used to safely access Qdrant database credentials stored as environment variables
import os

# dataclasses creates simple data structures (like lightweight classes for holding data)
# We use this to create Memory objects that hold text, metadata, and similarity scores
from dataclasses import dataclass

# datetime handles timestamps for when memories were created
# Helps track when Ava learned each piece of information
from datetime import datetime

# functools provides utilities for working with functions
# lru_cache creates singleton pattern - ensures only one vector store instance exists
from functools import lru_cache

# typing provides type hints for clearer code documentation
# List = list of items, Optional = value that might be None
from typing import List, Optional

# CUSTOM IMPORTS - Ava-specific configuration

# settings contains Ava's configuration like database URLs and API keys
from ai_companion.settings import settings

# QDRANT IMPORTS - Vector database for storing and searching memories

# QdrantClient is the main interface for talking to Qdrant database
# Qdrant is a specialized database designed for storing and searching vector embeddings
# Think of it as a database optimized for "finding similar meanings" rather than exact matches
from qdrant_client import QdrantClient

# These are specific data structures that Qdrant uses for configuration and data storage
# Distance = how to measure similarity between memories (cosine, euclidean, etc.)
# PointStruct = format for storing individual memories in the database
# VectorParams = configuration for the vector space (dimensions, distance metric)
from qdrant_client.models import Distance, PointStruct, VectorParams

# SENTENCE TRANSFORMERS IMPORT - Converts text to vector embeddings

# SentenceTransformer converts text into numerical vectors (embeddings)
# This is the key technology that enables semantic search in memories
# Instead of searching for exact words, we search for similar meanings
# Example: "job" and "career" have similar embeddings even though they're different words
from sentence_transformers import SentenceTransformer


@dataclass
class Memory:
    """
    📝 MEMORY DATA STRUCTURE - Represents a single memory stored in Ava's long-term database
    
    WHAT IT IS:
    This is like a single index card in Ava's memory filing system. Each Memory object
    contains the actual information Ava learned, when she learned it, and how relevant
    it is to current conversation.
    
    WHAT EACH FIELD CONTAINS:
    - text: The actual memory content ("User's birthday is March 15th")
    - metadata: Additional info like unique ID and when memory was created
    - score: How similar this memory is to current search (0.0 to 1.0)
    
    REAL-WORLD ANALOGY:
    This is like a library index card that contains:
    - The actual information (text)
    - Card catalog info like ID number and date added (metadata)
    - How relevant it is to your current search (score)
    
    USED BY:
    Vector search functions return lists of these Memory objects when Ava searches
    her long-term memory for information relevant to current conversation.
    """

    # TEXT FIELD - The actual memory content that Ava learned
    # Example: "User works as a software engineer at Google"
    text: str
    
    # METADATA FIELD - Additional information about this memory
    # Dictionary containing ID, timestamp, and other relevant data
    # Example: {"id": "abc123", "timestamp": "2024-03-15T14:30:25"}
    metadata: dict
    
    # SCORE FIELD - How relevant this memory is to current search
    # Optional[float] = either a number between 0.0-1.0 or None
    # 1.0 = perfect match, 0.0 = completely unrelated
    # None = score not calculated (when creating new memories)
    score: Optional[float] = None

    @property
    def id(self) -> Optional[str]:
        """
        🏷️ MEMORY ID EXTRACTOR - Gets the unique identifier for this memory
        
        WHAT IT DOES:
        Extracts the unique ID from this memory's metadata dictionary.
        Each memory has a unique identifier like a library book's catalog number.
        
        WHY WE NEED IDS:
        - Finding specific memories later
        - Updating existing memories without creating duplicates
        - Debugging memory storage issues
        
        RETURNS:
        String ID like "abc123-def456" or None if no ID in metadata
        """
        # SAFELY GET ID FROM METADATA DICTIONARY
        # .get("id") returns the ID value or None if "id" key doesn't exist
        # This prevents crashes if metadata doesn't contain an ID
        return self.metadata.get("id")

    @property
    def timestamp(self) -> Optional[datetime]:
        """
        🕓 MEMORY TIMESTAMP EXTRACTOR - Gets when this memory was created
        
        WHAT IT DOES:
        Extracts the creation timestamp from metadata and converts it to Python datetime object.
        This tells us when Ava learned this piece of information.
        
        WHY TIMESTAMPS MATTER:
        - Debugging memory issues ("When did Ava learn this?")
        - Potentially expiring old memories in the future
        - Understanding conversation history and context
        
        RETURNS:
        Python datetime object or None if no timestamp in metadata
        """
        # GET TIMESTAMP STRING FROM METADATA
        # .get("timestamp") safely retrieves timestamp or None if missing
        ts = self.metadata.get("timestamp")
        
        # CONVERT TIMESTAMP STRING TO DATETIME OBJECT
        # datetime.fromisoformat() converts ISO format string to datetime object
        # ISO format example: "2024-03-15T14:30:25"
        # Returns datetime object if timestamp exists, None if timestamp is missing
        return datetime.fromisoformat(ts) if ts else None


class VectorStore:
    """
    🗄 AVA'S VECTOR DATABASE INTERFACE - Manages storage and retrieval of memories using semantic search
    
    WHAT IS A VECTOR DATABASE:
    A vector database stores information as numerical vectors (lists of numbers) instead of text.
    This allows searching by meaning rather than exact word matches. When you search for "job",
    it also finds memories about "career", "work", "employment", etc.
    
    HOW VECTOR SEARCH WORKS:
    1. Text gets converted to vectors (numbers that represent meaning)
    2. Similar meanings have similar numbers
    3. Database can find "nearby" vectors = similar meanings
    4. Much smarter than traditional text search
    
    REAL-WORLD ANALOGY:
    Traditional database = Library organized alphabetically
    - To find books about "dogs", you look under "D"
    - You miss books about "puppies", "canines", "pets" filed elsewhere
    
    Vector database = Library organized by topics/meaning
    - Books about similar topics are stored near each other
    - Search for "dogs" finds "puppies", "canines", "pets" too
    - Much better for finding related information
    
    WHY QDRANT:
    Qdrant is a specialized vector database designed for AI applications.
    It's fast, reliable, and great for storing AI-generated embeddings.
    
    SINGLETON PATTERN:
    Only one VectorStore instance exists across Ava's entire system.
    All memory operations use the same database connection.
    """

    # REQUIRED ENVIRONMENT VARIABLES - Database connection credentials
    # QDRANT_URL = where the Qdrant database is running (like "http://localhost:6333")
    # QDRANT_API_KEY = authentication key for accessing the database
    REQUIRED_ENV_VARS = ["QDRANT_URL", "QDRANT_API_KEY"]
    
    # EMBEDDING MODEL - AI model that converts text to vectors
    # "all-MiniLM-L6-v2" is a popular sentence transformer model
    # Small, fast, and good quality for semantic similarity tasks
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    
    # COLLECTION NAME - Database table name for Ava's memories
    # "long_term_memory" is like a table name in traditional databases
    # All of Ava's permanent memories are stored in this collection
    COLLECTION_NAME = "long_term_memory"
    
    # SIMILARITY THRESHOLD - How similar memories must be to be considered duplicates
    # 0.9 = very similar (90% similarity), prevents storing near-identical memories
    # Scale: 0.0 = completely different, 1.0 = identical
    SIMILARITY_THRESHOLD = 0.9

    # SINGLETON PATTERN VARIABLES - Ensures only one instance exists
    # _instance stores the single VectorStore object across entire application
    # _initialized tracks whether this instance has been set up with database connection
    _instance: Optional["VectorStore"] = None
    _initialized: bool = False

    def __new__(cls) -> "VectorStore":
        """
        🏭 SINGLETON CONSTRUCTOR - Ensures only one VectorStore exists in entire system
        
        WHAT THIS DOES:
        This is Python's special method that controls object creation. Instead of creating
        a new VectorStore every time someone calls VectorStore(), it returns the same
        single instance that was created the first time.
        
        WHY SINGLETON PATTERN:
        - Database connections are expensive to create
        - All parts of Ava should use the same memory storage
        - Prevents conflicts from multiple database connections
        - Ensures consistent memory access across entire system
        
        REAL-WORLD ANALOGY:
        This is like having one shared filing cabinet for the entire office.
        Instead of everyone getting their own filing cabinet (expensive and confusing),
        everyone uses the same one. Much more efficient and organized.
        
        HOW IT WORKS:
        First call: Creates new VectorStore instance and saves it
        All subsequent calls: Returns the same saved instance
        """
        # CHECK IF INSTANCE ALREADY EXISTS
        # cls._instance is class variable shared across all VectorStore objects
        # First time this runs, _instance is None
        if cls._instance is None:
            # CREATE NEW INSTANCE ONLY IF NONE EXISTS
            # super().__new__(cls) creates the actual VectorStore object
            # Store it in _instance so we can reuse it later
            cls._instance = super().__new__(cls)
        
        # RETURN THE SINGLE SHARED INSTANCE
        # Whether newly created or previously existing, return the same instance
        # This ensures all code uses the same VectorStore object
        return cls._instance

    def __init__(self) -> None:
        """
        🔧 VECTOR STORE INITIALIZATION - Sets up database connection and AI model
        
        WHAT HAPPENS DURING INITIALIZATION:
        1. Validates that database credentials are configured
        2. Loads AI model for converting text to vectors
        3. Connects to Qdrant vector database
        4. Marks instance as fully initialized
        
        WHY CHECK _initialized:
        Since we use singleton pattern, __init__ might be called multiple times
        on the same object. We only want to do expensive setup once.
        
        COMPONENTS BEING SET UP:
        - model: AI that converts text like "User likes coffee" to vectors [0.1, 0.8, -0.3, ...]
        - client: Connection to Qdrant database for storing and searching vectors
        """
        # ONLY INITIALIZE ONCE (SINGLETON PATTERN PROTECTION)
        # self._initialized prevents running expensive setup multiple times
        # If already initialized, skip all setup and return immediately
        if not self._initialized:
            
            # VALIDATE DATABASE CREDENTIALS
            # Check that QDRANT_URL and QDRANT_API_KEY environment variables are set
            # Better to fail fast if misconfigured than fail during memory operations
            self._validate_env_vars()
            
            # LOAD AI MODEL FOR TEXT-TO-VECTOR CONVERSION
            # SentenceTransformer loads the embedding model from Hugging Face
            # self.EMBEDDING_MODEL = "all-MiniLM-L6-v2" (small, fast, good quality)
            # This model converts text to 384-dimensional vectors
            self.model = SentenceTransformer(self.EMBEDDING_MODEL)
            
            # CONNECT TO QDRANT VECTOR DATABASE
            # QdrantClient creates connection to database server
            # settings.QDRANT_URL = database location (like "http://localhost:6333")
            # settings.QDRANT_API_KEY = authentication credential
            self.client = QdrantClient(url=settings.QDRANT_URL, api_key=settings.QDRANT_API_KEY)
            
            # MARK AS FULLY INITIALIZED
            # Prevents running this expensive setup again if __init__ called multiple times
            self._initialized = True

    def _validate_env_vars(self) -> None:
        """Validate that all required environment variables are set."""
        missing_vars = [var for var in self.REQUIRED_ENV_VARS if not os.getenv(var)]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

    def _collection_exists(self) -> bool:
        """Check if the memory collection exists."""
        collections = self.client.get_collections().collections
        return any(col.name == self.COLLECTION_NAME for col in collections)

    def _create_collection(self) -> None:
        """Create a new collection for storing memories."""
        sample_embedding = self.model.encode("sample text")
        self.client.create_collection(
            collection_name=self.COLLECTION_NAME,
            vectors_config=VectorParams(
                size=len(sample_embedding),
                distance=Distance.COSINE,
            ),
        )

    def find_similar_memory(self, text: str) -> Optional[Memory]:
        """Find if a similar memory already exists.

        Args:
            text: The text to search for

        Returns:
            Optional Memory if a similar one is found
        """
        results = self.search_memories(text, k=1)
        if results and results[0].score >= self.SIMILARITY_THRESHOLD:
            return results[0]
        return None

    def store_memory(self, text: str, metadata: dict) -> None:
        """
        💾 MEMORY STORAGE ENGINE - Stores new memories in vector database
        
        WHAT IT DOES:
        Takes a piece of text (like "User's birthday is March 15th") and stores it
        in Ava's vector database so she can find it later through semantic search.
        
        HOW VECTOR STORAGE WORKS:
        1. Convert text to vector: "User likes coffee" → [0.1, 0.8, -0.3, 0.2, ...]
        2. Store vector + text + metadata in database
        3. Later searches find similar vectors = similar meanings
        
        WHY CHECK FOR COLLECTION:
        Collections are like tables in traditional databases. If this is Ava's first memory,
        we need to create the "long_term_memory" collection to store it in.
        
        DUPLICATE HANDLING:
        If similar memory already exists, we update it instead of creating duplicate.
        Keeps Ava's memory clean and prevents storage bloat.
        
        PARAMETERS:
        text: The actual memory content to store
        metadata: Additional info like ID and timestamp
        """
        # ENSURE DATABASE COLLECTION EXISTS
        # Collections are like tables - we need one to store memories in
        # If this is first memory ever, create the collection
        if not self._collection_exists():
            self._create_collection()

        # CHECK FOR DUPLICATE MEMORIES
        # find_similar_memory() searches for existing memories with similar meaning
        # If found, we'll update the existing one instead of creating duplicate
        similar_memory = self.find_similar_memory(text)
        if similar_memory and similar_memory.id:
            # REUSE EXISTING ID FOR UPDATE
            # Keep same ID so we update existing memory instead of creating new one
            metadata["id"] = similar_memory.id

        # CONVERT TEXT TO VECTOR EMBEDDING
        # self.model.encode() uses AI to convert text to numerical vector
        # Example: "User likes coffee" becomes [0.1, 0.8, -0.3, 0.2, ...]
        # These numbers represent the meaning of the text
        embedding = self.model.encode(text)
        
        # CREATE DATABASE POINT STRUCTURE
        # PointStruct is Qdrant's format for storing a single memory
        point = PointStruct(
            # ID: Unique identifier for this memory point
            # Uses provided ID or generates one from text hash
            id=metadata.get("id", hash(text)),
            
            # VECTOR: The numerical representation of the text meaning
            # .tolist() converts numpy array to regular Python list
            vector=embedding.tolist(),
            
            # PAYLOAD: The actual data we want to store and retrieve
            payload={
                "text": text,  # Original text content
                **metadata,   # Additional info like timestamp, ID
            },
        )

        # STORE IN DATABASE
        # client.upsert() either inserts new memory or updates existing one
        # "upsert" = update if exists, insert if new
        self.client.upsert(
            collection_name=self.COLLECTION_NAME,  # "long_term_memory" table
            points=[point],  # List of memory points to store
        )

    def search_memories(self, query: str, k: int = 5) -> List[Memory]:
        """
        🔍 SEMANTIC MEMORY SEARCH - Finds memories related to current conversation
        
        WHAT IT DOES:
        Takes current conversation context and searches Ava's memory database
        for information that's semantically related (similar in meaning).
        
        HOW SEMANTIC SEARCH WORKS:
        1. Convert search query to vector: "job" → [0.2, 0.9, -0.1, ...]
        2. Database finds vectors with similar numbers
        3. Similar vectors = similar meanings
        4. Returns memories about "work", "career", "employment", etc.
        
        WHY BETTER THAN TEXT SEARCH:
        Traditional search: "job" only finds memories containing word "job"
        Semantic search: "job" finds "career", "work", "employment", "position"
        
        REAL-WORLD ANALOGY:
        Traditional search = Looking for exact book titles in card catalog
        Semantic search = Asking librarian "What do you have about space?"
        Librarian finds books about astronauts, NASA, planets, rockets, etc.
        
        PARAMETERS:
        query: What we're looking for (current conversation context)
        k: Maximum number of memories to return (typically 3-5)
        
        RETURNS:
        List of Memory objects ranked by similarity to query
        """
        # HANDLE EMPTY DATABASE
        # If no memories stored yet, return empty list
        # Prevents errors when searching non-existent collection
        if not self._collection_exists():
            return []

        # CONVERT SEARCH QUERY TO VECTOR
        # Same AI model that stores memories also searches for them
        # query_embedding represents the meaning of what we're looking for
        query_embedding = self.model.encode(query)
        
        # SEARCH DATABASE FOR SIMILAR VECTORS
        # client.search() finds vectors most similar to our query vector
        results = self.client.search(
            # COLLECTION: Which database table to search in
            collection_name=self.COLLECTION_NAME,
            
            # QUERY_VECTOR: What we're looking for (as numerical vector)
            query_vector=query_embedding.tolist(),
            
            # LIMIT: Maximum number of results to return
            limit=k,
        )

        # CONVERT DATABASE RESULTS TO MEMORY OBJECTS
        # results contains raw database hits, we convert to Memory objects
        return [
            Memory(
                # TEXT: Original memory content
                text=hit.payload["text"],
                
                # METADATA: Additional info excluding text (to avoid duplication)
                # {k: v for k, v in items if k != "text"} = copy all except "text" key
                metadata={k: v for k, v in hit.payload.items() if k != "text"},
                
                # SCORE: How similar this memory is to search query (0.0 to 1.0)
                score=hit.score,
            )
            for hit in results  # Convert each database hit to Memory object
        ]


@lru_cache
def get_vector_store() -> VectorStore:
    """
    🏭 VECTOR STORE FACTORY - Returns the single shared VectorStore instance
    
    WHAT IT DOES:
    Simple factory function that returns Ava's vector database interface.
    Combined with singleton pattern, ensures entire system uses same database connection.
    
    WHY @lru_cache:
    @lru_cache makes Python remember the result of this function call.
    First call: Creates VectorStore and remembers it
    Subsequent calls: Returns the remembered VectorStore without recreating
    
    SINGLETON + CACHE = DOUBLE PROTECTION:
    - VectorStore class ensures only one instance can exist
    - @lru_cache ensures this function only runs once
    - Result: Guaranteed single database connection across entire system
    
    REAL-WORLD ANALOGY:
    This is like having one phone number for the office filing department.
    Everyone who needs to access files calls the same number and reaches
    the same filing department. No confusion, no duplicate work.
    
    RETURNS:
    Fully configured VectorStore ready for storing and searching memories
    
    USED BY:
    - MemoryManager for storing and retrieving memories
    - Any part of Ava's system that needs access to long-term memory
    """
    # CREATE AND RETURN VECTOR STORE INSTANCE
    # VectorStore() constructor handles singleton pattern internally
    # @lru_cache ensures this function only runs once per program execution
    # Result: Single database connection shared across entire system
    return VectorStore()
