"""
🛠️ PEPPER'S TOOL ARSENAL - ReAct agent tools for enhanced functionality

WHAT IS THIS MODULE?
This is Pepper's toolkit - a collection of tools that the ReAct agent can use to:
- Search the web for current information
- Search and store memories about users
- Manage calendar and scheduling
- Handle file operations
- Complete tasks (Done tool)

WHY TOOLS?
Tools give Pepper additional capabilities BEFORE deciding response format.
The flow is: llm_call_node → tool_handler_node → router_node → response_nodes

ARCHITECTURE CLARIFICATION:
- Tools are for FUNCTIONALITY (search, memory, calendar)
- Router still decides RESPONSE FORMAT (text/image/voice/call)  
- Response nodes (conversation_node, image_node, audio_node) stay unchanged

TOOL ORGANIZATION:
- base.py: Shared utilities and base classes
- basic/: Core ReAct tools (Done tool)
- search/: Web search and information retrieval  
- memory/: Memory search and storage
- calendar/: Calendar and scheduling tools
- file/: File operations and management

IMPORT PATTERN:
```python
from ai_companion.tools import get_tools, get_tools_by_name

# Get all available tools
all_tools = get_tools()

# Get specific tools  
selected_tools = get_tools(["Done", "web_search", "search_memories"])

# Get tools by name dictionary for lookup
tools_by_name = get_tools_by_name(all_tools)
```
"""

from typing import List, Optional, Dict
from langchain_core.tools import BaseTool

def get_tools(tool_names: Optional[List[str]] = None) -> List[BaseTool]:
    """
    Get specified tools or all available tools.
    
    Args:
        tool_names: List of tool names to get, or None for all tools
        
    Returns:
        List of LangChain BaseTool objects ready for LLM binding
    """
    # IMPORT COMPLETION TOOLS
    from .completion import Done, Question
    
    # IMPORT MOCK TOOLS FOR TESTING REACT WORKFLOW
    from .mock_tools import (
        mock_generate_text,
        mock_generate_image, 
        mock_generate_audio,
        mock_search_memory,
        mock_store_memory,
        mock_web_search,
        mock_create_note,
        mock_schedule_reminder
    )
    
    # BUILD COMPLETE TOOL REGISTRY
    all_tools = {
        # COMPLETION TOOLS - Signal when ReAct agent is done
        "Done": Done,
        "Question": Question,
        
        # CONTENT CREATION MOCK TOOLS - For testing creative workflows
        "mock_generate_text": mock_generate_text,
        "mock_generate_image": mock_generate_image,
        "mock_generate_audio": mock_generate_audio,
        
        # MEMORY MOCK TOOLS - For testing memory workflows  
        "mock_search_memory": mock_search_memory,
        "mock_store_memory": mock_store_memory,
        
        # SEARCH MOCK TOOLS - For testing information gathering
        "mock_web_search": mock_web_search,
        
        # TASK MANAGEMENT MOCK TOOLS - For testing productivity workflows
        "mock_create_note": mock_create_note,
        "mock_schedule_reminder": mock_schedule_reminder,
    }
    
    # Return requested tools or all tools
    if tool_names is None:
        return list(all_tools.values())
    
    return [all_tools[name] for name in tool_names if name in all_tools]

def get_tools_by_name(tools: List[BaseTool]) -> Dict[str, BaseTool]:
    """
    Create name-to-tool mapping for tool execution.
    
    Args:
        tools: List of tools from get_tools()
        
    Returns:
        Dictionary mapping tool names to tool objects
    """
    return {tool.name: tool for tool in tools}