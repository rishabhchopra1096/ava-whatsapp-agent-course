"""
🧪 MOCK TOOLS - Placeholder tools for testing Pepper's ReAct workflow

WHAT IS THIS FILE?
This file contains "fake" versions of Pepper's AI capabilities that return mock responses.
Think of them like training wheels for testing the ReAct workflow before connecting real AI services.

WHY DO WE NEED MOCK TOOLS?
Testing ReAct (Reasoning + Acting) workflow is complex with real AI services:
- Real tools are slow (API calls take seconds)
- Real tools cost money (every test burns API credits)
- Real tools can fail (network issues, rate limits)
- Real tools are unpredictable (different responses each time)

Mock tools solve this by:
- Returning instant, predictable responses
- Costing nothing to run
- Never failing due to external issues
- Letting us focus on workflow logic, not AI service integration

HOW MOCK TOOLS WORK IN TESTING:
1. User: "Generate an image of a sunset"
2. ReAct agent calls: mock_generate_image("sunset scene")
3. Mock tool returns: "🎨 MOCK: Generated image of sunset scene (saved as mock_image_123.png)"
4. Agent sees "success" response → continues workflow
5. We can test the complete ReAct flow without real image generation

REAL-WORLD ANALOGY:
This is like using cardboard props during a movie rehearsal:
- Actors practice their scenes and timing
- Director tests camera angles and blocking  
- Everyone learns their roles and interactions
- When ready, they replace props with real objects for filming

THE MOCK TOOL CATEGORIES:
🎨 Content Creation: Text, image, and audio generation tools
🧠 Memory Tools: Search and storage of user information
🔍 Search Tools: Web search and information retrieval
📝 Task Management: Note-taking and organization tools
"""

from datetime import datetime
from langchain_core.tools import tool
from typing import List, Optional
import uuid


# 🎨 CONTENT CREATION MOCK TOOLS
# These simulate Pepper's creative capabilities without calling real AI services

@tool
def mock_generate_text(prompt: str, max_words: int = 100) -> str:
    """
    📝 MOCK TEXT GENERATOR - Simulates Pepper's conversation generation
    
    WHAT IT SIMULATES:
    Pepper's ability to generate creative, contextual text responses using language models.
    In real implementation, this would call Groq/OpenAI APIs.
    
    MOCK BEHAVIOR:
    Returns a predictable mock response that includes the original prompt,
    making it easy to verify the ReAct workflow is passing data correctly.
    
    REAL EXAMPLE USAGE IN REACT:
    User: "Write a short poem about coding"
    ReAct Agent: "I need to generate creative content" → calls mock_generate_text("poem about coding")
    Mock Response: "🎭 MOCK TEXT: Here's a poem about coding - Code flows like poetry, bugs dance away..."
    Agent: "Perfect! I have generated text" → continues workflow
    """
    # SIMULATE REALISTIC RESPONSE TIME (optional - could add async sleep)
    response_id = str(uuid.uuid4())[:8]
    
    return f"""🎭 MOCK TEXT GENERATION COMPLETE:
Request ID: {response_id}
Prompt: "{prompt[:50]}{'...' if len(prompt) > 50 else ''}"
Word limit: {max_words}
Generated content: "Here's some mock creative text based on your request about {prompt.split()[0] if prompt.split() else 'the topic'}. This would be replaced with real AI-generated content in production. The text is engaging, relevant, and follows the specified parameters."

Status: ✅ Success - Mock text generated successfully"""


@tool 
def mock_generate_image(description: str, style: str = "realistic") -> str:
    """
    🎨 MOCK IMAGE GENERATOR - Simulates Pepper's visual creation abilities
    
    WHAT IT SIMULATES:
    Pepper's ability to create images from text descriptions using FLUX/DALL-E models.
    In real implementation, this would call Together AI or OpenAI APIs.
    
    MOCK BEHAVIOR:
    Returns a realistic mock response as if an image was actually generated,
    including fake file paths and metadata that downstream systems can handle.
    
    REAL EXAMPLE USAGE IN REACT:
    User: "Show me what a futuristic city looks like"
    ReAct Agent: "User wants visual content" → calls mock_generate_image("futuristic city skyline")
    Mock Response: "🖼️ MOCK: Generated futuristic city image (saved as mock_city_abc123.png)"
    Agent: "Perfect! I have created an image" → continues workflow
    """
    image_id = str(uuid.uuid4())[:8] 
    mock_filename = f"mock_image_{image_id}.png"
    
    return f"""🖼️ MOCK IMAGE GENERATION COMPLETE:
Description: "{description}"
Style: {style}
Generated file: generated_images/{mock_filename}
Dimensions: 1024x768
Model: MOCK-FLUX-1.0
Processing time: 2.3 seconds (simulated)

Status: ✅ Success - Mock image saved to file system
Note: In production, this would be a real AI-generated image file"""


@tool
def mock_generate_audio(text: str, voice_style: str = "pepper_voice") -> str:
    """
    🎵 MOCK AUDIO GENERATOR - Simulates Pepper's voice synthesis
    
    WHAT IT SIMULATES:
    Pepper's ability to convert text to speech using ElevenLabs or similar TTS services.
    In real implementation, this would generate actual audio files.
    
    MOCK BEHAVIOR:
    Returns a mock response as if audio was synthesized, including fake audio metadata
    and file paths that audio playback systems could theoretically handle.
    
    REAL EXAMPLE USAGE IN REACT:
    User: "Can you record this message for me?"
    ReAct Agent: "User wants audio output" → calls mock_generate_audio("Hello, this is your message")
    Mock Response: "🎙️ MOCK: Generated audio file message_xyz789.mp3"
    Agent: "Audio is ready!" → continues workflow
    """
    audio_id = str(uuid.uuid4())[:8]
    mock_filename = f"mock_audio_{audio_id}.mp3"
    
    # SIMULATE REALISTIC AUDIO METADATA
    estimated_duration = len(text.split()) * 0.6  # ~0.6 seconds per word
    
    return f"""🎙️ MOCK AUDIO GENERATION COMPLETE:
Text to synthesize: "{text[:100]}{'...' if len(text) > 100 else ''}"
Voice style: {voice_style}
Generated file: generated_audio/{mock_filename}
Duration: {estimated_duration:.1f} seconds
Sample rate: 44.1 kHz
Voice model: MOCK-ElevenLabs-v2

Status: ✅ Success - Mock audio file generated
Note: In production, this would be actual synthesized speech"""


# 🧠 MEMORY MOCK TOOLS  
# These simulate Pepper's ability to remember and retrieve information about users

@tool
def mock_search_memory(query: str, max_results: int = 5) -> str:
    """
    🧠 MOCK MEMORY SEARCH - Simulates Pepper's long-term memory retrieval
    
    WHAT IT SIMULATES:
    Pepper's ability to search through past conversations and stored facts about users
    using vector similarity search (Qdrant/embeddings in real implementation).
    
    MOCK BEHAVIOR:
    Returns realistic fake memories that could plausibly exist in Pepper's memory bank,
    making it easy to test memory-dependent conversation flows.
    
    REAL EXAMPLE USAGE IN REACT:
    User: "What did I tell you about my job last week?"
    ReAct Agent: "I should check what I remember" → calls mock_search_memory("user job information")
    Mock Response: "🧠 FOUND: User is a software engineer at Google, enjoys Python"
    Agent: "Based on what I remember..." → continues with personalized response
    """
    memory_results = [
        f"User mentioned they work in software development",
        f"User prefers {query.split()[0] if query.split() else 'various topics'} over other options", 
        f"User lives in a major city and enjoys technology",
        f"User has asked about similar topics in past conversations",
        f"User tends to prefer detailed explanations"
    ]
    
    # RETURN SUBSET OF MOCK MEMORIES BASED ON max_results
    selected_memories = memory_results[:max_results]
    
    return f"""🧠 MOCK MEMORY SEARCH COMPLETE:
Query: "{query}"
Results found: {len(selected_memories)}/{max_results}
Memories retrieved:
{chr(10).join([f"• {memory}" for memory in selected_memories])}

Search method: Vector similarity (mock)
Confidence scores: 0.85-0.92 (simulated)
Status: ✅ Success - Relevant memories found"""


@tool  
def mock_store_memory(fact: str, category: str = "general") -> str:
    """
    💾 MOCK MEMORY STORAGE - Simulates storing new information about users
    
    WHAT IT SIMULATES: 
    Pepper's ability to extract important facts from conversations and store them
    in long-term memory for future reference (vector database in real implementation).
    
    MOCK BEHAVIOR:
    Pretends to store the fact and returns a confirmation, allowing ReAct workflow
    to continue as if memory storage was successful.
    
    REAL EXAMPLE USAGE IN REACT:
    User: "I just got a promotion at work!"
    ReAct Agent: "This is important info to remember" → calls mock_store_memory("User got promoted at work")
    Mock Response: "💾 STORED: User got promoted at work (ID: mem_abc123)"
    Agent: "I've noted your good news!" → continues conversation
    """
    memory_id = f"mem_{str(uuid.uuid4())[:8]}"
    
    return f"""💾 MOCK MEMORY STORAGE COMPLETE:
Fact stored: "{fact}"
Category: {category}
Memory ID: {memory_id}
Storage location: vector_memory_db (mock)
Embedding model: text-embedding-ada-002 (simulated)

Status: ✅ Success - Fact permanently stored
Note: In production, this would be saved to Qdrant vector database"""


# 🔍 SEARCH MOCK TOOLS
# These simulate Pepper's ability to find information from external sources

@tool
def mock_web_search(query: str, num_results: int = 3) -> str:
    """
    🌐 MOCK WEB SEARCH - Simulates searching the internet for current information
    
    WHAT IT SIMULATES:
    Pepper's ability to search Google/Bing for up-to-date information that she
    doesn't have in her training data or memory.
    
    MOCK BEHAVIOR:
    Returns plausible mock search results that look like real web search responses,
    allowing ReAct agents to practice information gathering workflows.
    
    REAL EXAMPLE USAGE IN REACT:
    User: "What's the weather like in Tokyo today?"
    ReAct Agent: "I need current info" → calls mock_web_search("Tokyo weather today")
    Mock Response: "🌐 FOUND: Tokyo weather is 23°C, partly cloudy..."
    Agent: "Based on current weather data..." → gives informed response
    """
    
    # GENERATE REALISTIC MOCK SEARCH RESULTS
    mock_results = [
        f"Latest information about {query} from reliable sources shows recent developments",
        f"Expert analysis on {query} indicates current trends and insights",
        f"Recent news about {query} provides up-to-date context and details"
    ]
    
    return f"""🌐 MOCK WEB SEARCH COMPLETE:
Query: "{query}"
Results returned: {num_results}
Search results:
{chr(10).join([f"{i+1}. {result}" for i, result in enumerate(mock_results[:num_results])])}

Search engine: MockGoogle (simulated)
Response time: 0.3 seconds
Status: ✅ Success - Current information retrieved"""


# 📝 TASK MANAGEMENT MOCK TOOLS  
# These simulate Pepper's ability to help with organization and productivity

@tool
def mock_create_note(title: str, content: str, tags: Optional[List[str]] = None) -> str:
    """
    📝 MOCK NOTE CREATOR - Simulates Pepper's note-taking capabilities
    
    WHAT IT SIMULATES:
    Pepper's ability to create organized notes and reminders for users,
    potentially integrating with systems like Notion or Obsidian.
    
    MOCK BEHAVIOR:
    Pretends to create a note with realistic metadata, allowing ReAct agents
    to practice task management and organization workflows.
    
    REAL EXAMPLE USAGE IN REACT:
    User: "Remember that I need to call the dentist tomorrow"
    ReAct Agent: "I should create a note for this" → calls mock_create_note("Call Dentist", "User reminder for tomorrow")
    Mock Response: "📝 NOTE CREATED: Call Dentist (ID: note_xyz123)"
    Agent: "I've saved that reminder for you!" → continues conversation
    """
    note_id = f"note_{str(uuid.uuid4())[:8]}"
    tags_str = f" | Tags: {', '.join(tags)}" if tags else ""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    return f"""📝 MOCK NOTE CREATION COMPLETE:
Title: "{title}"
Content: "{content[:100]}{'...' if len(content) > 100 else ''}"
Note ID: {note_id}
Created: {timestamp}{tags_str}
Storage: MockNotion workspace (simulated)

Status: ✅ Success - Note saved and organized
Note: In production, this would integrate with real note-taking apps"""


@tool
def mock_schedule_reminder(message: str, reminder_time: str) -> str:
    """
    ⏰ MOCK REMINDER SCHEDULER - Simulates Pepper's ability to set future reminders
    
    WHAT IT SIMULATES:
    Pepper's ability to schedule notifications or reminders for users at specified times,
    potentially integrating with calendar apps or notification systems.
    
    MOCK BEHAVIOR:
    Pretends to schedule a reminder with realistic confirmation details,
    allowing ReAct agents to practice time-based task management.
    
    REAL EXAMPLE USAGE IN REACT:
    User: "Remind me to submit the report by Friday at 2 PM"
    ReAct Agent: "I should set a reminder" → calls mock_schedule_reminder("Submit report", "Friday 2:00 PM")
    Mock Response: "⏰ REMINDER SET: Submit report for Friday 2:00 PM"
    Agent: "I'll remind you about the report!" → continues conversation
    """
    reminder_id = f"rem_{str(uuid.uuid4())[:8]}"
    
    return f"""⏰ MOCK REMINDER SCHEDULING COMPLETE:
Message: "{message}"
Scheduled for: {reminder_time}
Reminder ID: {reminder_id}
Notification method: MockCalendar + Push notification (simulated)
Status: Active

Status: ✅ Success - Reminder scheduled successfully
Note: In production, this would integrate with real calendar/notification systems"""