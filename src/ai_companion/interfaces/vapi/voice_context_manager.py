# VOICE CONTEXT MANAGER - Prepares WhatsApp context for voice calls
#
# 🎯 PURPOSE: This file creates "briefing documents" for voice calls based on 
# recent WhatsApp conversations with the user
#
# 🔗 REAL-WORLD ANALOGY: This is like a personal assistant who:
# - Reviews recent email conversations before a phone meeting
# - Prepares talking points and background information
# - Creates a summary of "what you need to know" for the call
# - Identifies the main topic and user preferences
#
# 📞 TECHNICAL ROLE: Bridges WhatsApp and voice conversations by:
# - Extracting relevant context from WhatsApp message history
# - Summarizing conversations for voice assistant personality
# - Identifying user names, topics, and calling reasons
# - Formatting context for Vapi's variableValues system
#
# 🌐 INTEGRATION: Works with both vapi_client.py and LangGraph:
# - Called by voice_calling_node in LangGraph workflow
# - Provides context to vapi_client for assistant creation
# - Ensures voice-Ava knows what WhatsApp-Ava was discussing

import re
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

class VoiceContextManager:
    """
    VOICE CONTEXT MANAGER - Creates briefing documents for voice calls
    
    🎯 PURPOSE: Analyzes WhatsApp conversations and prepares context
    that voice-Ava needs to have natural, continuous conversations
    
    🔗 REAL-WORLD ANALOGY: Like a research assistant who:
    - Reviews all recent correspondence with a client
    - Identifies key topics and user preferences  
    - Creates a briefing document for the phone call
    - Ensures continuity between written and verbal communication
    
    📞 KEY FUNCTIONS:
    - prepare_voice_context(): Main function that creates complete context
    - extract_user_name(): Finds user's name from conversation
    - summarize_conversation(): Creates concise conversation summary
    - identify_topic(): Determines main conversation topic
    - format_for_vapi(): Formats context for Vapi's variable system
    """
    
    def __init__(self):
        """Initialize the context manager with logging"""
        self.logger = logging.getLogger(__name__)
    
    def prepare_voice_context(self, messages: List[BaseMessage], user_id: Optional[str] = None, 
                            calling_reason: str = "User requested callback") -> Dict[str, Any]:
        """
        PREPARE VOICE CONTEXT - Main function that creates complete context for voice calls
        
        🎯 PURPOSE: This is the "master briefing function" that analyzes a WhatsApp
        conversation and creates everything voice-Ava needs to know
        
        🔗 REAL-WORLD ANALOGY: Like a personal assistant who:
        1. Reviews all recent emails and messages with a client
        2. Identifies who they are and what they've been discussing
        3. Creates a one-page briefing for the phone call
        4. Highlights key topics and any special requests
        
        📞 TECHNICAL PROCESS:
        1. Extract user's name from conversation history
        2. Summarize recent messages into key points
        3. Identify main conversation topic
        4. Count interaction history for relationship context
        5. Format everything for Vapi's variableValues system
        
        Args:
            messages: List of WhatsApp messages (HumanMessage and AIMessage objects)
            user_id: User identifier (phone number from WhatsApp)
            calling_reason: Why we're making this call
            
        Returns:
            context: Dictionary with all context needed for voice call
        """
        try:
            # 📊 LOG CONTEXT PREPARATION INITIATION
            self.logger.info(f"📋 PREPARING VOICE CONTEXT FOR CALL:")
            self.logger.info(f"   🆔 User ID: {user_id}")
            self.logger.info(f"   💬 Messages provided: {len(messages) if messages else 0}")
            self.logger.info(f"   📋 Calling reason: {calling_reason}")
            self.logger.info(f"   ⏰ Start time: {datetime.now().isoformat()}")
            
            # STEP 1: VALIDATE INPUT
            if not messages:
                self.logger.warning("⚠️ No messages provided for voice context")
                return self._create_empty_context(calling_reason)
            
            # STEP 2: EXTRACT USER INFORMATION 
            # Find the user's name from their messages
            user_name = self.extract_user_name(messages)
            
            # STEP 3: ANALYZE CONVERSATION CONTENT
            # Get recent messages for context (last 10 messages or all if fewer)
            recent_messages = messages[-10:] if len(messages) > 10 else messages
            
            # Create conversation summary
            conversation_summary = self.summarize_conversation(recent_messages)
            
            # Identify main topic
            main_topic = self.identify_conversation_topic(recent_messages)
            
            # Get the most recent user message
            last_user_message = self._get_last_user_message(messages)
            
            # STEP 4: BUILD COMPLETE CONTEXT DICTIONARY
            context = {
                # USER IDENTIFICATION
                "userName": user_name or "there",  # Fallback to generic greeting
                "userId": user_id or "unknown",
                
                # CONVERSATION CONTEXT  
                "recentContext": conversation_summary,
                "conversationTopic": main_topic,
                "lastWhatsAppMessage": last_user_message,
                
                # RELATIONSHIP CONTEXT
                "messageCount": len(messages),
                "conversationLength": self._categorize_conversation_length(len(messages)),
                
                # CALL CONTEXT
                "callingReason": calling_reason,
                "callInitiatedAt": datetime.now().isoformat(),
                
                # TECHNICAL CONTEXT
                "interface": "voice_from_whatsapp",
                "contextPreparedAt": datetime.now().isoformat()
            }
            
            # STEP 5: LOG COMPREHENSIVE CONTEXT CREATION SUCCESS
            context_size = len(str(context))
            self.logger.info(f"✅ VOICE CONTEXT PREPARED SUCCESSFULLY:")
            self.logger.info(f"   👤 User: {context['userName']}")
            self.logger.info(f"   💬 Topic: {context['conversationTopic']}")
            self.logger.info(f"   📝 Messages: {context['messageCount']}")
            self.logger.info(f"   📋 Reason: {calling_reason}")
            self.logger.info(f"   📄 Summary length: {len(context['recentContext'])} chars")
            self.logger.info(f"   🔢 Total context size: {context_size} chars")
            self.logger.info(f"   ⏰ Preparation completed: {datetime.now().isoformat()}")
            
            return context
            
        except Exception as e:
            self.logger.error(f"🚨 VOICE CONTEXT PREPARATION ERROR: {str(e)}")
            self.logger.error(f"   🆔 User ID: {user_id}")
            self.logger.error(f"   💬 Messages count: {len(messages) if messages else 0}")
            self.logger.error(f"   🗺 Message types: {[type(msg).__name__ for msg in messages[:3]] if messages else 'None'}")
            self.logger.error(f"   📋 Calling reason: {calling_reason}")
            # Include full exception details for debugging
            import traceback
            self.logger.error(f"   📚 Full traceback: {traceback.format_exc()}")
            # Return minimal context to avoid breaking the call
            return self._create_empty_context(calling_reason)
    
    def extract_user_name(self, messages: List[BaseMessage]) -> Optional[str]:
        """
        EXTRACT USER NAME - Find user's name from conversation history
        
        🔗 REAL-WORLD ANALOGY: Like reading through email correspondence
        to find how someone introduces themselves or signs their messages
        
        📞 PATTERNS WE LOOK FOR:
        - "I'm John" or "I am Sarah"
        - "My name is David"
        - "Call me Mike"
        - "This is Jennifer"
        """
        try:
            # SEARCH THROUGH USER MESSAGES (HumanMessage = from user)
            for message in messages:
                if isinstance(message, HumanMessage):
                    content = message.content.lower()
                    
                    # PATTERN MATCHING FOR NAME EXTRACTION
                    # Look for common ways people introduce themselves
                    patterns = [
                        r"i'?m ([A-Z][a-z]+)",           # "I'm John" or "I am John"
                        r"my name is ([A-Z][a-z]+)",     # "My name is Sarah"
                        r"call me ([A-Z][a-z]+)",        # "Call me Mike"
                        r"this is ([A-Z][a-z]+)",        # "This is Jennifer"
                        r"i'?m called ([A-Z][a-z]+)",    # "I'm called David"
                        r"name'?s ([A-Z][a-z]+)",        # "Name's Alex"
                    ]
                    
                    for pattern in patterns:
                        match = re.search(pattern, content, re.IGNORECASE)
                        if match:
                            name = match.group(1).title()  # Capitalize first letter
                            self.logger.info(f"👤 USER NAME FOUND: {name}")
                            return name
            
            # NO NAME FOUND
            self.logger.info("👤 No user name found in conversation")
            return None
            
        except Exception as e:
            self.logger.error(f"🚨 NAME EXTRACTION ERROR: {str(e)}")
            return None
    
    def summarize_conversation(self, messages: List[BaseMessage]) -> str:
        """
        SUMMARIZE CONVERSATION - Create brief summary of recent WhatsApp conversation
        
        🔗 REAL-WORLD ANALOGY: Like creating "meeting notes" from recent correspondence:
        "User asked about X, we discussed Y, they mentioned Z"
        
        📞 PURPOSE: Give voice-Ava context about what's been happening
        in the WhatsApp conversation so she can reference it naturally
        """
        try:
            if not messages:
                return "No previous conversation context available."
            
            # BUILD CONVERSATION SUMMARY
            # Get last few exchanges between user and Ava
            recent_exchanges = []
            
            # Take recent messages and create summary
            for message in messages[-6:]:  # Last 3 exchanges (6 messages)
                if isinstance(message, HumanMessage):
                    role = "User"
                elif isinstance(message, AIMessage):
                    role = "Ava"
                else:
                    continue  # Skip system messages
                
                # TRUNCATE LONG MESSAGES FOR SUMMARY
                content = message.content
                if len(content) > 100:
                    content = content[:97] + "..."
                
                recent_exchanges.append(f"{role}: {content}")
            
            # JOIN INTO READABLE SUMMARY
            if recent_exchanges:
                summary = " | ".join(recent_exchanges)
                self.logger.debug(f"📝 CONVERSATION SUMMARY: {summary[:200]}...")
                return summary
            else:
                return "Recent conversation available but no clear exchanges found."
                
        except Exception as e:
            self.logger.error(f"🚨 CONVERSATION SUMMARY ERROR: {str(e)}")
            return "Error creating conversation summary."
    
    def identify_conversation_topic(self, messages: List[BaseMessage]) -> str:
        """
        IDENTIFY CONVERSATION TOPIC - Determine main topic of recent conversation
        
        🔗 REAL-WORLD ANALOGY: Like reading through recent emails and saying
        "This conversation is mainly about work", "vacation planning", or "technical support"
        
        📞 PURPOSE: Help voice-Ava understand the context and continue
        the conversation naturally on the same topic
        """
        try:
            if not messages:
                return "General conversation"
            
            # COMBINE RECENT MESSAGE CONTENT
            # Get text from last 5 messages to analyze
            recent_content = " ".join([
                msg.content for msg in messages[-5:] 
                if hasattr(msg, 'content') and msg.content
            ])
            
            content_lower = recent_content.lower()
            
            # TOPIC CLASSIFICATION BASED ON KEYWORDS
            # Simple keyword-based topic identification
            topics = {
                "work": ["work", "job", "office", "meeting", "project", "boss", "colleague", "deadline", "presentation"],
                "health": ["health", "doctor", "medicine", "pain", "sick", "wellness", "exercise", "diet"],
                "travel": ["travel", "trip", "vacation", "flight", "hotel", "destination", "visit", "journey"],
                "food": ["food", "restaurant", "recipe", "cooking", "eat", "meal", "dinner", "lunch"],
                "technology": ["app", "phone", "computer", "software", "AI", "tech", "website", "internet"],
                "personal": ["family", "friend", "relationship", "personal", "life", "home", "kids", "children"],
                "shopping": ["buy", "purchase", "order", "shopping", "store", "price", "cost", "product"],
                "entertainment": ["movie", "music", "game", "show", "book", "fun", "watch", "play"],
                "education": ["learn", "study", "school", "course", "education", "teaching", "university"],
                "finance": ["money", "bank", "budget", "investment", "financial", "cost", "payment", "price"]
            }
            
            # FIND BEST MATCHING TOPIC
            topic_scores = {}
            for topic, keywords in topics.items():
                score = sum(1 for keyword in keywords if keyword in content_lower)
                if score > 0:
                    topic_scores[topic] = score
            
            if topic_scores:
                # Return the topic with the highest score
                best_topic = max(topic_scores, key=topic_scores.get)
                self.logger.info(f"🎯 IDENTIFIED TOPIC: {best_topic.title()} (score: {topic_scores[best_topic]})")
                return best_topic.title()
            else:
                return "General conversation"
                
        except Exception as e:
            self.logger.error(f"🚨 TOPIC IDENTIFICATION ERROR: {str(e)}")
            return "General conversation"
    
    def _get_last_user_message(self, messages: List[BaseMessage]) -> str:
        """Get the most recent message from the user"""
        try:
            # Search backwards through messages to find last user message
            for message in reversed(messages):
                if isinstance(message, HumanMessage):
                    return message.content[:200] + "..." if len(message.content) > 200 else message.content
            return "No recent user message found"
        except:
            return "Error retrieving last message"
    
    def _categorize_conversation_length(self, message_count: int) -> str:
        """Categorize the relationship based on message count"""
        if message_count <= 2:
            return "new_user"
        elif message_count <= 10:
            return "getting_acquainted"
        elif message_count <= 50:
            return "regular_user"
        else:
            return "long_time_user"
    
    def _create_empty_context(self, calling_reason: str) -> Dict[str, Any]:
        """Create minimal context when no conversation history is available"""
        return {
            "userName": "there",
            "userId": "unknown",
            "recentContext": "No previous conversation context available",
            "conversationTopic": "General conversation",
            "lastWhatsAppMessage": "No recent messages available",
            "messageCount": 0,
            "conversationLength": "new_user",
            "callingReason": calling_reason,
            "callInitiatedAt": datetime.now().isoformat(),
            "interface": "voice_from_whatsapp",
            "contextPreparedAt": datetime.now().isoformat()
        }

# HELPER FUNCTIONS FOR EXTERNAL USE
# These can be imported and used directly in other parts of the system

def prepare_voice_context_simple(messages: List[BaseMessage], user_id: Optional[str] = None) -> Dict[str, Any]:
    """
    SIMPLE VOICE CONTEXT PREPARATION - Convenience function for quick context creation
    
    🔗 REAL-WORLD ANALOGY: Like having a "quick briefing" option that creates
    a basic summary without all the detailed analysis
    
    📞 USAGE: For when you need voice context quickly without creating
    a full VoiceContextManager instance
    """
    # 📊 LOG SIMPLE CONTEXT PREPARATION REQUEST
    logger = logging.getLogger(__name__)
    logger.info(f"🚀 SIMPLE VOICE CONTEXT REQUESTED:")
    logger.info(f"   🆔 User ID: {user_id}")
    logger.info(f"   💬 Message count: {len(messages) if messages else 0}")
    logger.info(f"   ⏰ Request time: {datetime.now().isoformat()}")
    
    try:
        manager = VoiceContextManager()
        context = manager.prepare_voice_context(messages, user_id)
        
        logger.info(f"✅ SIMPLE CONTEXT PREPARATION SUCCESSFUL")
        logger.info(f"   🔢 Context size: {len(str(context))} characters")
        return context
        
    except Exception as e:
        logger.error(f"🚨 SIMPLE CONTEXT PREPARATION FAILED: {str(e)}")
        logger.error(f"   🆔 User ID: {user_id}")
        logger.error(f"   💬 Messages: {len(messages) if messages else 0}")
        # Include full exception details for debugging
        import traceback
        logger.error(f"   📚 Full traceback: {traceback.format_exc()}")
        raise

def extract_calling_reason_from_message(message_content: str) -> str:
    """
    EXTRACT CALLING REASON - Determine why user wants a phone call
    
    🔗 REAL-WORLD ANALOGY: Like reading a message that says 
    "Can you call me about the project?" and extracting "about the project"
    """
    # 📊 LOG CALLING REASON EXTRACTION
    logger = logging.getLogger(__name__)
    logger.debug(f"🎯 EXTRACTING CALLING REASON:")
    logger.debug(f"   📝 Message: {message_content[:100]}{'...' if len(message_content) > 100 else ''}")
    
    content_lower = message_content.lower()
    
    # Look for specific calling reasons
    if "urgent" in content_lower or "emergency" in content_lower:
        return "Urgent matter - user requested immediate callback"
    elif "discuss" in content_lower:
        return "User wants to discuss something in detail"
    elif "explain" in content_lower:
        return "User needs detailed explanation"
    elif "help" in content_lower:
        return "User needs assistance with something"
    elif "talk" in content_lower:
        return "User prefers to talk rather than type"
    else:
        return "User requested callback from WhatsApp"