"""
🔧 TOOL UTILITIES - Shared utilities and base classes for Pepper's ReAct tools

WHAT IS THIS FILE?
Common utilities, logging setup, and base patterns that all Pepper tools share.
Think of this as the "tool factory" that provides consistent patterns.

WHY SEPARATE UTILITIES?
- Consistent error handling across all tools
- Standardized logging and debugging
- Reusable validation patterns
- Mock/fallback implementations for development

UTILITIES PROVIDED:
- ToolLogger: Consistent logging with emoji indicators
- MockTool: Base class for development/testing tools
- format_tool_result(): Standardize LLM-friendly responses
- handle_tool_error(): Consistent error handling
"""

import logging
from typing import Any, Dict, Optional
from abc import ABC, abstractmethod

# Setup consistent logging for all tools
logging.basicConfig(level=logging.INFO)

class ToolLogger:
    """Consistent logging utility for all Pepper tools."""
    
    def __init__(self, tool_name: str):
        self.tool_name = tool_name
        self.logger = logging.getLogger(f"pepper.tools.{tool_name}")
    
    def info(self, message: str) -> None:
        """Log info message with tool context."""
        self.logger.info(f"🛠️ {self.tool_name}: {message}")
    
    def error(self, message: str) -> None:
        """Log error message with tool context.""" 
        self.logger.error(f"🚨 {self.tool_name}: {message}")
    
    def debug(self, message: str) -> None:
        """Log debug message with tool context."""
        self.logger.debug(f"🔍 {self.tool_name}: {message}")

class MockTool(ABC):
    """Base class for mock tool implementations during development."""
    
    def __init__(self, tool_name: str):
        self.tool_name = tool_name
        self.logger = ToolLogger(tool_name)
        
    @abstractmethod
    def mock_implementation(self, **kwargs) -> str:
        """Mock implementation for development/testing."""
        pass
    
    def execute(self, **kwargs) -> str:
        """Execute mock implementation with logging."""
        self.logger.info(f"Executing mock implementation")
        try:
            result = self.mock_implementation(**kwargs)
            self.logger.info(f"Mock execution successful")
            return result
        except Exception as e:
            self.logger.error(f"Mock execution failed: {str(e)}")
            return f"Mock {self.tool_name} failed: {str(e)}"

def format_tool_result(
    success: bool, 
    result_data: Any, 
    tool_name: str,
    action_description: Optional[str] = None
) -> str:
    """
    Format tool results into LLM-friendly strings.
    
    Args:
        success: Whether the tool execution succeeded
        result_data: The actual result data (path, bytes, text, etc.)
        tool_name: Name of the tool for context
        action_description: Optional description of what was done
        
    Returns:
        Human-readable string describing the result
    """
    if success:
        if action_description:
            return f"✅ {tool_name}: {action_description} - {str(result_data)}"
        else:
            return f"✅ {tool_name}: Completed successfully - {str(result_data)}"
    else:
        return f"❌ {tool_name}: Failed - {str(result_data)}"

def handle_tool_error(e: Exception, tool_name: str, fallback_message: str) -> str:
    """
    Consistent error handling for all tools.
    
    Args:
        e: The exception that occurred
        tool_name: Name of the tool for logging
        fallback_message: User-friendly fallback message
        
    Returns:
        Formatted error message for LLM consumption
    """
    logger = ToolLogger(tool_name)
    logger.error(f"Tool execution failed: {str(e)}")
    return f"⚠️ {tool_name} encountered an error: {fallback_message}"