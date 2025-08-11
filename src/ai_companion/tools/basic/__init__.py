"""
🎯 BASIC REACT TOOLS - Core tools for ReAct agent completion

WHAT ARE BASIC TOOLS?
Essential tools that every ReAct agent needs:
- Done: Signals task completion to end the tool loop

WHY SEPARATE BASIC TOOLS?
The Done tool is the minimal tool needed to make ReAct work - it tells the agent
when to stop calling tools and proceed to the router for response formatting.
"""