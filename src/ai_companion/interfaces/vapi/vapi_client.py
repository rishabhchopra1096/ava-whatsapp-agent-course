# VAPI CLIENT - Handles making phone calls through Vapi's service
# 
# 🎯 PURPOSE: This is like having a "phone dialer" that can call any number on demand
# and connect them to Ava's voice interface
#
# 🔗 REAL-WORLD ANALOGY: This is like a smart phone system that can:
# - Dial any number automatically when requested
# - Set up the call with specific instructions for the conversation
# - Connect the caller to Ava's voice personality
# - Track call status and results
#
# 📞 TECHNICAL ROLE: This handles the "outbound calling" side of voice integration
# - Creates Vapi assistants configured to use Ava's personality
# - Makes phone calls using your Vapi phone number
# - Passes WhatsApp context to voice calls for continuity
#
# 🌐 INTEGRATION: Works with vapi_endpoints.py to create complete voice system:
# - This file: Makes outbound calls TO users
# - vapi_endpoints.py: Processes voice conversations when users talk

import os
import logging
from typing import Dict, Optional, Any, List
from datetime import datetime

# Import Vapi SDK (we tested this works in Phase 1)
# Note: The import name is vapi_python, not just vapi
try:
    from vapi_python import Vapi
except ImportError:
    logging.error("❌ Vapi SDK not installed. Run: pip install vapi-python")
    raise

# Import Ava's settings (for API keys and configuration)
try:
    from ai_companion.settings import settings
except ImportError:
    # Fallback for development - use environment variables directly
    logging.warning("⚠️ Could not import settings, using environment variables directly")
    settings = None

class VapiClient:
    """
    VAPI CLIENT WRAPPER - Ava's phone dialing system
    
    🎯 PURPOSE: This class handles all phone call operations for Ava
    
    🔗 REAL-WORLD ANALOGY: Like a smart phone that can:
    - Dial any number automatically (make_outbound_call)
    - Set up the call with specific instructions (create_voice_assistant)
    - Connect the caller to Ava's voice personality
    - Check if calls are still active (get_call_status)
    
    📞 KEY FEATURES:
    - Creates custom voice assistants for each call with relevant context
    - Uses your existing ElevenLabs voice for consistency
    - Passes WhatsApp conversation context to voice calls
    - Handles errors gracefully with helpful messages
    
    🌐 CONFIGURATION NEEDED:
    - VAPI_API_PRIVATE_KEY: Your Vapi API key (for authentication)
    - PHONE_NUMBER_ID: Your Vapi phone number ID (for outbound calls)
    - ELEVENLABS_VOICE_ID: Your ElevenLabs voice (for consistent personality)
    - Railway URL: Your deployed app URL (for custom LLM endpoint)
    """
    
    def __init__(self):
        """
        INITIALIZE VAPI CLIENT - Set up the phone dialing system
        
        🔗 REAL-WORLD ANALOGY: Like setting up a new phone system in an office:
        - Connect to the phone service (Vapi API)
        - Configure your phone number (Phone Number ID)
        - Set up call routing (to your Railway app)
        """
        # GET API CREDENTIALS FROM ENVIRONMENT
        # These were already configured in your .env file
        self.api_key = os.getenv("VAPI_API_PRIVATE_KEY")
        if not self.api_key:
            raise ValueError("❌ VAPI_API_PRIVATE_KEY not found in environment variables")
        
        # GET PHONE NUMBER FOR OUTBOUND CALLS
        # This is your Vapi phone number that will show up as caller ID
        self.phone_number_id = os.getenv("PHONE_NUMBER_ID")
        if not self.phone_number_id:
            raise ValueError("❌ PHONE_NUMBER_ID not found in environment variables")
        
        # GET VOICE CONFIGURATION
        # Use same ElevenLabs voice as WhatsApp for consistency
        self.voice_id = os.getenv("ELEVENLABS_VOICE_ID", "uju3wxzG5OhpWcoi3SMy")
        
        # GET RAILWAY URL FOR CUSTOM LLM ENDPOINT
        # This tells Vapi where to send voice conversations for processing
        self.railway_url = os.getenv("RAILWAY_URL", "https://ava-whatsapp-agent-course-production.up.railway.app")
        
        # INITIALIZE VAPI CLIENT
        # This creates the actual connection to Vapi's service
        try:
            self.client = Vapi(token=self.api_key)
            logging.info("✅ Vapi client initialized successfully")
        except Exception as e:
            logging.error(f"❌ Failed to initialize Vapi client: {str(e)}")
            raise
        
        # SET UP LOGGING
        self.logger = logging.getLogger(__name__)
        
        # LOG CONFIGURATION FOR DEBUGGING
        self.logger.info(f"📞 VAPI CLIENT CONFIGURED:")
        self.logger.info(f"   Phone Number ID: {self.phone_number_id}")
        self.logger.info(f"   Voice ID: {self.voice_id}")
        self.logger.info(f"   Railway URL: {self.railway_url}")
    
    async def create_voice_assistant(self, context: Dict[str, Any]) -> str:
        """
        CREATE VOICE ASSISTANT - Sets up Ava's voice personality for a specific call
        
        🎯 PURPOSE: Before making a phone call, we need to create a "voice version" of Ava
        that knows about the specific user and their WhatsApp conversation context
        
        🔗 REAL-WORLD ANALOGY: This is like creating a "briefing document" for Ava 
        before she takes a phone call:
        - What's her personality? (Same as WhatsApp)
        - What should she know about this caller? (Recent WhatsApp messages)
        - How should she handle the conversation? (Natural, helpful, concise)
        - Where should she get her intelligence? (Your Groq LLM via Railway)
        
        📞 TECHNICAL DETAILS:
        - Creates a Vapi assistant configured to use YOUR Groq LLM (not Vapi's)
        - Passes WhatsApp context via variableValues
        - Uses same ElevenLabs voice as WhatsApp for consistency
        - Configures personality to match WhatsApp Ava
        
        Args:
            context: Dictionary with user context from WhatsApp conversation
            
        Returns:
            assistant_id: Unique ID for this voice assistant configuration
        """
        try:
            # PREPARE VOICE ASSISTANT CONFIGURATION
            # This tells Vapi how to make Ava sound and behave on phone calls
            assistant_config = {
                "name": f"Ava Voice Assistant - {datetime.now().strftime('%Y%m%d_%H%M%S')}",
                
                # MODEL CONFIGURATION - Use OUR Groq LLM instead of Vapi's default
                # This is the key part that makes Vapi use YOUR existing AI brain!
                "model": {
                    "provider": "custom-llm",  # Tell Vapi to use our custom endpoint
                    "model": "groq-llama-3.3-70b-versatile",  # Our actual model name
                    "url": f"{self.railway_url}/vapi/chat/completions",  # Our endpoint
                    "temperature": 0.7,  # Conversational but not too random
                    "maxTokens": 150,  # Keep responses concise for voice (people don't like long speeches)
                },
                
                # VOICE CONFIGURATION - Use same voice as WhatsApp voice messages
                # This ensures Ava sounds the same whether on WhatsApp or phone calls
                "voice": {
                    "provider": "elevenlabs",
                    "voiceId": self.voice_id,  # Same voice for consistency
                    "stability": 0.5,  # Balanced voice stability
                    "similarityBoost": 0.8,  # High similarity to original voice
                    "style": 0.0,  # Natural style, not overly dramatic
                    "useSpeakerBoost": True,  # Enhance voice quality
                },
                
                # CONVERSATION SETUP
                # First thing Ava says when the call connects
                "firstMessage": self._create_first_message(context),
                
                # SYSTEM PROMPT - Same personality as WhatsApp Ava
                # This is like giving Ava her "job description" for phone calls
                "systemPrompt": self._create_system_prompt(context),
                
                # CALL SETTINGS
                "endCallMessage": "Thanks for calling! I'll send you a summary on WhatsApp. Talk to you soon!",
                "recordingEnabled": True,  # Record for transcript processing
                "hipaaEnabled": False,  # Not handling medical data
                "clientMessages": ["conversation-update", "function-call", "hang", "speech-update"],
                "serverMessages": ["conversation-update", "end-of-call-report", "function-call"],
                
                # SILENCE DETECTION - Prevent awkward pauses
                "silenceTimeoutSeconds": 30,  # End call if silent for 30 seconds
                "maxDurationSeconds": 600,  # Max 10-minute calls to control costs
                
                # BACKGROUND SOUND HANDLING
                "backgroundSound": "office",  # Subtle background to feel natural
            }
            
            # CREATE ASSISTANT VIA VAPI API
            # This actually creates the voice assistant on Vapi's servers
            assistant = self.client.assistants.create(**assistant_config)
            assistant_id = assistant.id
            
            self.logger.info(f"✅ VOICE ASSISTANT CREATED: {assistant_id} for {context.get('userName', 'unknown user')}")
            return assistant_id
            
        except Exception as e:
            self.logger.error(f"🚨 ASSISTANT CREATION ERROR: {str(e)}")
            self.logger.error(f"   📋 Context provided: {context}")
            self.logger.error(f"   🌐 Railway URL: {self.railway_url}")
            self.logger.error(f"   🎤 Voice ID: {self.voice_id}")
            self.logger.error(f"   📞 Phone Number ID: {self.phone_number_id}")
            # Include full exception details for debugging
            import traceback
            self.logger.error(f"   📚 Full traceback: {traceback.format_exc()}")
            raise
    
    def _create_first_message(self, context: Dict[str, Any]) -> str:
        """
        CREATE FIRST MESSAGE - What Ava says when the call connects
        
        🔗 REAL-WORLD ANALOGY: Like the greeting a receptionist gives when 
        they call someone back: "Hi John, this is Sarah from ABC Company 
        calling you back about your inquiry..."
        """
        user_name = context.get('userName', 'there')
        calling_reason = context.get('callingReason', 'You requested a callback')
        
        # Create personalized greeting
        greeting = f"Hi {user_name}! This is Ava calling you back from WhatsApp."
        
        # Add context about why we're calling
        if 'recent_context' in context and context['recent_context']:
            greeting += f" I have our recent conversation context, so we can pick up right where we left off."
        else:
            greeting += f" {calling_reason}."
        
        greeting += " How can I help you today?"
        
        return greeting
    
    def _create_system_prompt(self, context: Dict[str, Any]) -> str:
        """
        CREATE SYSTEM PROMPT - Ava's "job description" for phone calls
        
        🔗 REAL-WORLD ANALOGY: Like giving an employee a detailed job description
        before they handle customer calls, including:
        - What's their role and personality?
        - What information do they have about this specific caller?
        - How should they handle different situations?
        """
        user_name = context.get('userName', 'the caller')
        recent_context = context.get('recentContext', 'No recent context available')
        conversation_topic = context.get('conversationTopic', 'General conversation')
        
        system_prompt = f"""You are Ava, a helpful AI assistant. You're currently on a phone call with {user_name}.

RECENT CONTEXT FROM WHATSAPP:
{recent_context}

CONVERSATION TOPIC: {conversation_topic}

PHONE CALL GUIDELINES:
- Be conversational and natural (this is a phone call, not text messages)
- Reference the WhatsApp conversation naturally when relevant
- Keep responses concise - people don't like long speeches on phone calls
- If you need to share detailed information, offer to send it via WhatsApp
- Be the same helpful, friendly Ava they know from messaging
- If the caller asks about something not in your context, politely ask them to elaborate
- End responses with questions to keep the conversation flowing naturally

PERSONALITY:
- Warm and friendly, like talking to a good friend
- Professional but not formal or robotic
- Genuinely interested in helping
- Patient and good at listening
- Quick to understand and respond appropriately

REMEMBER: This is a continuation of your WhatsApp relationship with this user. They called because they wanted to talk, so make it a great conversation!"""
        
        return system_prompt
    
    async def make_outbound_call(self, to_number: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        MAKE OUTBOUND CALL - Dials a phone number and connects them to voice Ava
        
        🎯 PURPOSE: This is the main function that actually makes phone calls happen!
        
        🔗 REAL-WORLD ANALOGY: Like a secretary who:
        1. Gets briefed about who to call and what they need to know
        2. Dials the number on the office phone
        3. When someone answers, introduces them to the expert (Ava)
        4. Provides a reference number for tracking the call
        
        📞 TECHNICAL PROCESS:
        1. Create a voice assistant configured with user context
        2. Set up the call with Vapi (who to call, which assistant to use)
        3. Pass WhatsApp context via variableValues
        4. Initiate the actual phone call
        5. Return call details for tracking
        
        Args:
            to_number: Phone number to call (from WhatsApp user)
            context: Context about the user and conversation
            
        Returns:
            call_details: Information about the initiated call
        """
        try:
            # 📊 LOG CALL INITIATION DETAILS
            self.logger.info(f"📞 INITIATING OUTBOUND CALL:")
            self.logger.info(f"   📱 To: {to_number}")
            self.logger.info(f"   👤 User: {context.get('userName', 'Unknown')}")
            self.logger.info(f"   💬 Topic: {context.get('conversationTopic', 'General')}")
            self.logger.info(f"   🔤 Context length: {len(str(context.get('recentContext', '')))} chars")
            
            # STEP 1: VALIDATE PHONE NUMBER
            # Make sure we have a valid phone number to call
            if not to_number or not to_number.startswith('+'):
                self.logger.error(f"❌ INVALID PHONE NUMBER: '{to_number}'")
                self.logger.error(f"   Expected format: +1234567890")
                raise ValueError(f"Invalid phone number: {to_number}")
            
            self.logger.info(f"✅ Phone number validation passed: {to_number}")
            
            # STEP 2: CREATE VOICE ASSISTANT FOR THIS SPECIFIC CALL
            # This sets up Ava's voice personality with the user's context
            self.logger.info(f"🤖 Creating voice assistant with context...")
            assistant_id = await self.create_voice_assistant(context)
            self.logger.info(f"✅ Voice assistant created: {assistant_id}")
            
            # STEP 3: PREPARE CALL CONFIGURATION
            # This tells Vapi who to call, which assistant to use, and what context to provide
            call_config = {
                "phoneNumberId": self.phone_number_id,  # Your Vapi phone number (caller ID)
                "customer": {"number": to_number},       # Who to call
                "assistantId": assistant_id,             # Voice Ava configuration
                
                # ASSISTANT OVERRIDES - Pass WhatsApp context to voice call
                # This is like giving Ava a "cheat sheet" before the call
                "assistantOverrides": {
                    "variableValues": {
                        "userName": context.get("userName", ""),
                        "recentContext": context.get("recentContext", ""),
                        "conversationTopic": context.get("conversationTopic", ""),
                        "callingReason": context.get("callingReason", "User requested callback"),
                        "lastWhatsAppMessage": context.get("lastWhatsAppMessage", ""),
                        "messageCount": str(context.get("messageCount", 0)),
                    }
                }
            }
            
            # STEP 4: MAKE THE ACTUAL PHONE CALL
            # This sends the call request to Vapi's servers
            self.logger.info(f"📡 Sending call request to Vapi...")
            self.logger.info(f"   📞 Phone Number ID: {self.phone_number_id}")
            self.logger.info(f"   🎯 Target: {to_number}")
            self.logger.info(f"   🤖 Assistant: {assistant_id}")
            
            call = self.client.calls.create(**call_config)
            self.logger.info(f"✅ Vapi call request successful: {call.id}")
            
            # STEP 5: PREPARE RESPONSE WITH CALL DETAILS
            # Return information about the call for tracking and user feedback
            call_details = {
                "call_id": call.id,
                "status": "initiated", 
                "to_number": to_number,
                "assistant_id": assistant_id,
                "timestamp": datetime.now().isoformat(),
                "expected_caller_id": os.getenv("PHONE_NUMBER", "+1 (650) 681 2449"),
                "estimated_ring_time": "10-15 seconds"
            }
            
            self.logger.info(f"🎉 OUTBOUND CALL SUCCESSFULLY INITIATED:")
            self.logger.info(f"   📞 Call ID: {call.id}")
            self.logger.info(f"   📱 Calling: {to_number}")
            self.logger.info(f"   🤖 Assistant: {assistant_id}")
            self.logger.info(f"   ⏰ Timestamp: {datetime.now().isoformat()}")
            self.logger.info(f"   📋 Expected caller ID: {call_details['expected_caller_id']}")
            
            return call_details
            
        except Exception as e:
            self.logger.error(f"🚨 OUTBOUND CALL FAILED: {str(e)}")
            self.logger.error(f"   📱 Target number: {to_number}")
            self.logger.error(f"   👤 User context: {context.get('userName', 'Unknown')}")
            self.logger.error(f"   📞 Phone Number ID: {self.phone_number_id}")
            self.logger.error(f"   🌐 Railway URL: {self.railway_url}")
            # Log the full exception details
            import traceback
            self.logger.error(f"   📚 Full traceback: {traceback.format_exc()}")
            # Re-raise with more context for debugging
            raise Exception(f"Failed to initiate call to {to_number}: {str(e)}")
    
    async def get_call_status(self, call_id: str) -> Dict[str, Any]:
        """
        GET CALL STATUS - Check if a call is still active, ended, etc.
        
        🔗 REAL-WORLD ANALOGY: Like checking "Is that phone call still going on?"
        or "Did the call go through successfully?"
        
        📞 USAGE: Can be used to check if calls are connecting properly,
        how long they lasted, why they ended, etc.
        """
        try:
            call = self.client.calls.get(call_id)
            return {
                "id": call.id,
                "status": call.status,
                "duration": getattr(call, 'duration', None),
                "ended_reason": getattr(call, 'endedReason', None),
                "created_at": getattr(call, 'createdAt', None),
                "updated_at": getattr(call, 'updatedAt', None)
            }
        except Exception as e:
            self.logger.error(f"🚨 CALL STATUS CHECK FAILED: {str(e)}")
            self.logger.error(f"   📞 Call ID: {call_id}")
            import traceback
            self.logger.error(f"   📚 Full traceback: {traceback.format_exc()}")
            return {"error": str(e), "call_id": call_id}
    
    async def list_recent_calls(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        LIST RECENT CALLS - Get information about recent calls made
        
        🔗 REAL-WORLD ANALOGY: Like looking at your phone's "recent calls" list
        to see who you called, when, and how long the calls were
        
        📞 USAGE: Useful for debugging, tracking usage, or providing
        call history to users
        """
        try:
            calls = self.client.calls.list(limit=limit)
            call_list = []
            
            for call in calls:
                call_info = {
                    "id": call.id,
                    "status": call.status,
                    "customer_number": getattr(call, 'customer', {}).get('number', 'unknown'),
                    "duration": getattr(call, 'duration', None),
                    "created_at": getattr(call, 'createdAt', None),
                    "ended_reason": getattr(call, 'endedReason', None)
                }
                call_list.append(call_info)
            
            return call_list
            
        except Exception as e:
            self.logger.error(f"🚨 LIST CALLS ERROR: {str(e)}")
            return []

# SINGLETON INSTANCE - One phone dialer for the whole application
# This creates a single VapiClient that can be used throughout Ava
# Like having one phone system for the entire office
try:
    vapi_client = VapiClient()
    logging.info("✅ Global Vapi client created successfully")
except Exception as e:
    logging.error(f"❌ Failed to create global Vapi client: {str(e)}")
    vapi_client = None  # Will cause graceful failures in other parts of the system