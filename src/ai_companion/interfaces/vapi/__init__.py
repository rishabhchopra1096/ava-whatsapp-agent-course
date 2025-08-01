# VAPI INTERFACE MODULE - Voice calling integration for Ava
# 
# 🎯 PURPOSE: This module handles voice calling functionality using Vapi's infrastructure
# 
# 🔗 REAL-WORLD ANALOGY: This is like adding a "phone department" to Ava's office
# - The office already has WhatsApp and web chat departments (existing interfaces)
# - Now we're adding a phone department that can make and receive calls
# - The same "manager" (LangGraph + Groq LLM) handles all departments
# 
# 📦 MODULE CONTENTS:
# - vapi_client.py: The "phone dialer" that makes calls through Vapi
# - vapi_endpoints.py: The "phone system" that processes voice conversations  
# - voice_context_manager.py: The "briefing system" that prepares context for calls
#
# 🌐 HOW IT CONNECTS TO AVA:
# Voice calls → Vapi → This module → LangGraph → Same Groq LLM → Response → Voice