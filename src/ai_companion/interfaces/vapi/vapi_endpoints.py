# VAPI ENDPOINTS - Voice calling endpoints that connect Vapi to Ava's brain
# 
# 🎯 PURPOSE: This file creates "phone call processing" endpoints that receive voice conversations
# and process them through Ava's existing LangGraph workflow
#
# 🔗 REAL-WORLD ANALOGY: This is like a "telephone switchboard" at a company:
# - Phone calls come in (from Vapi's voice system)
# - The switchboard operator (this file) connects them to the right department
# - The expert (Ava's LangGraph + Groq LLM) handles the actual conversation
# - The switchboard relays the expert's response back to the caller
#
# 📞 TECHNICAL FLOW:
# Voice → Vapi (speech-to-text) → This endpoint → LangGraph → Groq LLM → Response → Vapi (text-to-speech) → Voice
#
# 🌐 KEY INSIGHT: Ava's brain (LangGraph + Groq) doesn't know this is voice vs WhatsApp!
# We just change the input/output format, but the AI processing stays identical.

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import asyncio
import logging
from datetime import datetime
import os

# Import Ava's existing brain components (no changes to these!)
# This is like importing the "department experts" who will handle the actual work
try:
    from ai_companion.graph.graph import graph
    from ai_companion.graph.state import AICompanionState
    from langchain_core.messages import HumanMessage, AIMessage
except ImportError as e:
    logging.error(f"❌ Could not import Ava's core components: {e}")
    # For development, we'll create a simple fallback
    graph = None

# VAPI REQUEST/RESPONSE MODELS
# These define the "language" that Vapi speaks when talking to our server
# Like standardized forms that phone operators use to pass messages

class VapiChatMessage(BaseModel):
    """
    VAPI CHAT MESSAGE - Individual message in a conversation
    Like a single line in a phone conversation transcript
    """
    role: str           # "user" (caller), "assistant" (Ava), or "system" (instructions)
    content: str        # The actual message text that was spoken/should be spoken

class VapiChatRequest(BaseModel):
    """
    VAPI CHAT REQUEST - What Vapi sends us during voice calls
    
    Real-world analogy: Like a phone operator saying:
    "I have a caller on line 1 who said: [message]. How should I respond?"
    
    This follows OpenAI's chat completions format so Vapi can talk to us
    like we're OpenAI's GPT, but we secretly use Ava's Groq LLM instead!
    """
    model: str                          # LLM model name (we ignore this, use our Groq)
    messages: List[VapiChatMessage]     # Conversation history from voice call
    temperature: Optional[float] = 0.7   # How creative responses should be (0=robotic, 1=creative)
    stream: Optional[bool] = False       # Whether to stream response chunks (for real-time)
    max_tokens: Optional[int] = 150      # Maximum response length (keep voice responses concise!)
    tools: Optional[List[Dict]] = None   # Available functions (for advanced features later)

class VapiChatChoice(BaseModel):
    """Single response choice in OpenAI format"""
    index: int                          # Choice number (always 0 for single response)
    message: VapiChatMessage           # The response message
    finish_reason: str                 # Why the response ended ("stop", "length", etc.)

class VapiChatResponse(BaseModel):
    """
    VAPI CHAT RESPONSE - What we send back to Vapi
    
    Real-world analogy: Like telling the phone operator:
    "Here's what to say to the caller: [Ava's response]"
    
    This uses OpenAI's response format so Vapi thinks we're OpenAI
    """
    id: str                           # Unique response ID
    object: str                       # Always "chat.completion" (OpenAI standard)
    created: int                      # Unix timestamp when response was created
    model: str                        # Model used (we'll say "groq-llama-3.3-70b-versatile")
    choices: List[VapiChatChoice]     # Response options (usually just one)
    usage: Optional[Dict] = None      # Token usage info (optional)

# CREATE ROUTER FOR VAPI ENDPOINTS
# This is like creating a "phone department" within Ava's office
vapi_router = APIRouter(prefix="/vapi", tags=["vapi"])

@vapi_router.post("/chat/completions")
async def handle_voice_chat(request: VapiChatRequest):
    """
    VAPI CHAT COMPLETIONS ENDPOINT - The "brain connection" for voice calls
    
    🎯 PURPOSE: This is the main endpoint that makes Vapi think we're OpenAI,
    but secretly processes everything through Ava's existing Groq LLM setup.
    
    🔗 REAL-WORLD ANALOGY: This is like a telephone switchboard operator who:
    1. Receives phone calls (Vapi voice input converted to text)
    2. Connects to the office expert (Ava's LangGraph + Groq LLM)
    3. Relays the expert's response back to the caller (text that Vapi converts to voice)
    
    📞 TECHNICAL FLOW:
    Voice → Vapi → This endpoint → LangGraph → Groq → Response → This endpoint → Vapi → Voice
    
    🌐 KEY INSIGHT: Ava's existing brain doesn't change at all! We just:
    - Convert Vapi's format to LangGraph's format (like translating languages)
    - Process through existing workflow (same as WhatsApp messages)
    - Convert response back to Vapi's format (translate back)
    """
    try:
        # 📊 LOG INCOMING VAPI REQUEST DETAILS
        logging.info(f"🎙️ VAPI CHAT REQUEST RECEIVED:")
        logging.info(f"   📋 Model: {request.model}")
        logging.info(f"   🌡️ Temperature: {request.temperature}")
        logging.info(f"   📏 Max tokens: {request.max_tokens}")
        logging.info(f"   📨 Message count: {len(request.messages)}")
        logging.info(f"   📡 Stream mode: {request.stream}")
        
        # STEP 1: EXTRACT VOICE MESSAGE (like transcribing a phone call)
        # Get the latest message from the voice conversation
        # This is like asking: "What did the caller just say?"
        if not request.messages:
            logging.error("❌ VAPI REQUEST ERROR: No messages provided")
            raise HTTPException(status_code=400, detail="No messages provided")
        
        latest_message = request.messages[-1]
        if latest_message.role != "user":
            logging.error(f"❌ VAPI REQUEST ERROR: Last message role is '{latest_message.role}', expected 'user'")
            raise HTTPException(status_code=400, detail="Last message must be from user")
        
        voice_message_content = latest_message.content
        
        # LOG THE VOICE MESSAGE DETAILS
        logging.info(f"🎤 VOICE MESSAGE PROCESSED:")
        logging.info(f"   📝 Content: {voice_message_content[:100]}{'...' if len(voice_message_content) > 100 else ''}")
        logging.info(f"   📏 Length: {len(voice_message_content)} characters")
        logging.info(f"   👤 Role: {latest_message.role}")
        
        # STEP 2: PREPARE CONTEXT FOR AVA'S BRAIN
        # Create the same input format that WhatsApp messages use
        # This is like briefing Ava: "This came from a phone call, here's what they said"
        
        # TODO: Later we'll add WhatsApp context passing here
        # TODO: Add user identification from phone number
        # For now, we process the voice message as a standalone interaction
        
        # STEP 3: PROCESS THROUGH EXISTING LANGGRAPH WORKFLOW
        # Use Ava's existing "brain" - same LangGraph that handles WhatsApp
        # The beauty: Ava doesn't know this came from voice vs WhatsApp!
        
        if graph is None:
            # FALLBACK FOR DEVELOPMENT - Simple response if LangGraph not available
            ava_response = f"I heard you say: '{voice_message_content}'. This is Ava responding from a voice call! The LangGraph integration will make this much smarter."
            logging.warning("⚠️ VAPI FALLBACK: Using simple response - LangGraph not available")
            logging.warning("   📋 This means Ava's full brain is not connected to voice calls yet")
        else:
            # REAL PROCESSING - Use Ava's actual brain
            logging.info(f"🧠 PROCESSING THROUGH LANGGRAPH:")
            logging.info(f"   🔗 Using Ava's production brain for voice call")
            logging.info(f"   📝 Input message: {voice_message_content[:50]}...")
            
            graph_input = {
                "messages": [HumanMessage(content=voice_message_content)],
                "interface": "voice",                # Track that this is from voice call
                "conversation_id": f"voice_{datetime.now().isoformat()}",
                # TODO: Add user_id when we have phone number mapping
                # TODO: Add recent WhatsApp context when available
            }
            
            # INVOKE AVA'S BRAIN (same as WhatsApp processing!)
            # This is like asking the company expert to handle a phone call
            response = await graph.ainvoke(graph_input)
            
            # EXTRACT AVA'S RESPONSE
            # Get the response message that Ava generated
            if response and response.get("messages"):
                ava_response = response["messages"][-1].content
            else:
                ava_response = "I'm sorry, I couldn't process that right now. Could you try again?"
        
        # STEP 4: FORMAT FOR VAPI (OpenAI-compatible format)
        # Convert Ava's response into the format Vapi expects
        # This is like translating Ava's written response into speech instructions
        
        # Create response in OpenAI chat completions format
        response_message = VapiChatMessage(
            role="assistant",
            content=ava_response
        )
        
        response_choice = VapiChatChoice(
            index=0,
            message=response_message,
            finish_reason="stop"
        )
        
        vapi_response = VapiChatResponse(
            id=f"vapi-{int(datetime.now().timestamp())}",
            object="chat.completion",
            created=int(datetime.now().timestamp()),
            model="groq-llama-3.3-70b-versatile",  # Our actual model
            choices=[response_choice]
        )
        
        # LOG SUCCESS FOR DEBUGGING
        logging.info(f"✅ VOICE RESPONSE SENT: {ava_response[:100]}...")
        
        # Return as dictionary (FastAPI automatically converts to JSON)
        return vapi_response.dict()
        
    except Exception as e:
        # ERROR HANDLING - If anything goes wrong, provide graceful fallback
        # This is like a phone operator saying "Let me transfer you" when something goes wrong
        logging.error(f"🚨 VOICE CALL PROCESSING ERROR: {str(e)}")
        
        # Return polite error response that gets spoken to caller
        error_response = VapiChatResponse(
            id=f"error-{int(datetime.now().timestamp())}",
            object="chat.completion", 
            created=int(datetime.now().timestamp()),
            model="error-fallback",
            choices=[VapiChatChoice(
                index=0,
                message=VapiChatMessage(
                    role="assistant", 
                    content="I'm having trouble processing your request right now. Could you try again, or send me a WhatsApp message instead?"
                ),
                finish_reason="stop"
            )]
        )
        
        return error_response.dict()

@vapi_router.post("/webhook")
async def handle_vapi_webhook(request: Request):
    """
    VAPI WEBHOOK HANDLER - Receives call events and transcripts
    
    🎯 PURPOSE: This receives notifications from Vapi about call events
    (call started, call ended, transcript available, etc.)
    
    🔗 REAL-WORLD ANALOGY: Like a secretary who takes notes during phone meetings
    and then sends you a summary email afterwards
    
    📞 TECHNICAL PURPOSE: Process call results and integrate back into WhatsApp conversation
    
    🌐 EVENTS WE HANDLE:
    - call-started: When a phone call begins
    - call-ended: When a phone call ends (most important - we process transcripts here)
    - speech-started/ended: When user starts/stops talking
    - transcript: Real-time transcript updates (optional)
    """
    try:
        # EXTRACT WEBHOOK DATA
        # Get the event information that Vapi is sending us
        webhook_data = await request.json()
        event_type = webhook_data.get("message", {}).get("type", "unknown")
        
        # 📊 LOG COMPREHENSIVE WEBHOOK DETAILS
        logging.info(f"🔗 VAPI WEBHOOK RECEIVED:")
        logging.info(f"   🏷️ Event type: {event_type}")
        logging.info(f"   📞 Call ID: {webhook_data.get('message', {}).get('call', {}).get('id', 'unknown')}")
        logging.info(f"   📏 Data size: {len(str(webhook_data))} characters")
        logging.info(f"   ⏰ Timestamp: {datetime.now().isoformat()}")
        logging.debug(f"   📋 Full webhook data: {webhook_data}")
        
        # HANDLE DIFFERENT EVENT TYPES
        if event_type == "call-ended":
            # MOST IMPORTANT EVENT - Process completed call
            logging.info(f"🏁 PROCESSING CALL-ENDED EVENT")
            await handle_call_ended(webhook_data)
            
        elif event_type == "call-started":
            # Call began - log for tracking
            call_id = webhook_data.get("message", {}).get("call", {}).get("id", "unknown")
            customer_number = webhook_data.get("message", {}).get("call", {}).get("customer", {}).get("number", "unknown")
            logging.info(f"📞 CALL STARTED:")
            logging.info(f"   🆔 Call ID: {call_id}")
            logging.info(f"   📱 Customer: {customer_number}")
            
        elif event_type in ["speech-started", "speech-ended"]:
            # User started/stopped talking - log for debugging
            logging.debug(f"🗣️ SPEECH EVENT: {event_type}")
            
        elif event_type == "transcript":
            # Real-time transcript update - could use for live processing later
            transcript = webhook_data.get("message", {}).get("transcript", "")
            transcript_role = webhook_data.get("message", {}).get("role", "unknown")
            logging.debug(f"📝 TRANSCRIPT UPDATE:")
            logging.debug(f"   🎤 Role: {transcript_role}")
            logging.debug(f"   📝 Content: {transcript[:100]}{'...' if len(transcript) > 100 else ''}")
            
        else:
            # Unknown event type - log for investigation
            logging.info(f"❓ UNKNOWN WEBHOOK EVENT: {event_type}")
            logging.info(f"   📋 Available keys: {list(webhook_data.get('message', {}).keys())}")
        
        # Always return success to Vapi
        return {"status": "received", "event_type": event_type}
        
    except Exception as e:
        # ERROR HANDLING - Log error but don't fail the webhook
        logging.error(f"🚨 WEBHOOK PROCESSING ERROR: {str(e)}")
        logging.error(f"   🌐 Request URL: {request.url}")
        logging.error(f"   📋 Request method: {request.method}")
        logging.error(f"   📄 Raw request body: {await request.body() if hasattr(request, 'body') else 'unavailable'}")
        # Include full exception details for debugging
        import traceback
        logging.error(f"   📚 Full traceback: {traceback.format_exc()}")
        return {"status": "error", "message": str(e)}

async def handle_call_ended(webhook_data: Dict[str, Any]):
    """
    HANDLE CALL ENDED EVENT - Process completed phone call
    
    🎯 PURPOSE: When a voice call ends, process the transcript and integrate
    the conversation back into WhatsApp
    
    🔗 REAL-WORLD ANALOGY: Like a secretary who:
    1. Attended the phone meeting
    2. Types up meeting notes
    3. Sends summary to relevant parties
    4. Creates follow-up tasks if needed
    
    📞 PROCESSING STEPS:
    1. Extract call details (who called, how long, transcript)
    2. Summarize the conversation
    3. Send summary back to WhatsApp (TODO)
    4. Store conversation in memory system (TODO)
    5. Process any tasks or follow-ups mentioned (TODO)
    """
    try:
        # EXTRACT CALL DETAILS
        call_info = webhook_data.get("message", {}).get("call", {})
        call_id = call_info.get("id", "unknown")
        
        # Get customer info (who we called)
        customer_info = call_info.get("customer", {})
        customer_number = customer_info.get("number", "unknown")
        
        # Get call duration and status
        duration = call_info.get("duration", 0)  # Duration in seconds
        end_reason = call_info.get("endedReason", "unknown")
        
        # Get transcript if available
        transcript = webhook_data.get("message", {}).get("transcript", "")
        
        # LOG CALL COMPLETION
        logging.info(f"📞 CALL COMPLETED:")
        logging.info(f"   Call ID: {call_id}")
        logging.info(f"   Customer: {customer_number}")
        logging.info(f"   Duration: {duration} seconds")
        logging.info(f"   End Reason: {end_reason}")
        logging.info(f"   Transcript Length: {len(transcript)} characters")
        
        # TODO: PROCESS TRANSCRIPT AND CREATE SUMMARY
        # Here we would:
        # 1. Use Ava's LLM to summarize the call
        # 2. Extract any tasks or action items mentioned
        # 3. Send summary back to WhatsApp
        # 4. Store in memory system for future reference
        
        if transcript:
            # For now, just log a simple summary
            summary = f"Call completed with {customer_number}. Duration: {duration}s. Transcript available."
            logging.info(f"📋 CALL SUMMARY: {summary}")
            
            # TODO: Send this summary back to WhatsApp
            # TODO: Process any action items from the call
            # TODO: Store conversation in long-term memory
        
    except Exception as e:
        logging.error(f"🚨 CALL ENDED PROCESSING ERROR: {str(e)}")

@vapi_router.get("/health")
async def health_check():
    """
    HEALTH CHECK ENDPOINT - Simple endpoint to verify the service is running
    
    🎯 PURPOSE: Allows Vapi (and us) to check if our voice service is working
    
    🔗 REAL-WORLD ANALOGY: Like checking if the phone system is working
    by calling a test number that just says "The system is operational"
    """
    try:
        # Check if we can import core components
        from ai_companion.graph.graph import graph
        graph_status = "available" if graph else "not_available"
    except ImportError:
        graph_status = "import_error"
    
    return {
        "status": "healthy",
        "service": "vapi-voice-integration",
        "timestamp": datetime.now().isoformat(),
        "langgraph_status": graph_status,
        "version": "1.0.0"
    }

# DEVELOPMENT TESTING ENDPOINT
@vapi_router.post("/test-chat")
async def test_chat_endpoint(test_message: str = "Hello, this is a test call"):
    """
    TEST ENDPOINT - For development testing without Vapi
    
    🎯 PURPOSE: Allows us to test the chat completions logic without
    setting up a real Vapi call
    
    🔗 REAL-WORLD ANALOGY: Like having a practice phone call with a colleague
    to test if the phone system is working correctly
    
    💡 USAGE: POST to /vapi/test-chat with {"test_message": "your message"}
    """
    # Create a fake Vapi request for testing
    fake_request = VapiChatRequest(
        model="gpt-4o",
        messages=[VapiChatMessage(role="user", content=test_message)],
        temperature=0.7
    )
    
    # Process through our main chat handler
    response = await handle_voice_chat(fake_request)
    
    return {
        "test_message": test_message,
        "response": response,
        "note": "This is a test endpoint - not used by actual Vapi calls"
    }