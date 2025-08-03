# Voice Calling Setup Guide for Pepper

## Overview

This guide walks you through setting up voice calling functionality for Pepper, allowing WhatsApp users to request phone calls by saying "call me" or similar phrases. When triggered, Pepper will initiate an actual phone call using Vapi's voice infrastructure while maintaining conversation context from WhatsApp.

## Prerequisites

1. **Pepper WhatsApp Agent** deployed and working on Railway
2. **Vapi Account** at https://vapi.ai
3. **ElevenLabs API Key** (already configured for Pepper)
4. **WhatsApp Business API** configured and receiving messages

## Step 1: Create Vapi Account

1. Go to https://vapi.ai and sign up
2. Complete the onboarding process
3. You'll receive:
   - API Private Key (starts with `priv_`)
   - API Public Key (starts with `pub_`)

## Step 2: Configure Vapi Phone Number

1. In Vapi Dashboard, go to **Phone Numbers**
2. Click **Buy Number** or **Import Number**
3. Choose a phone number (this will be your caller ID)
4. Once configured, copy the **Phone Number ID** (UUID format)
   - Example: `12345678-abcd-efgh-ijkl-1234567890ab`

## Step 3: Update Environment Variables

Add these to your Railway environment variables:

```env
# Vapi Configuration (Required for voice calling)
VAPI_API_PRIVATE_KEY=priv_your_actual_key_here
VAPI_PHONE_NUMBER_ID=your-phone-number-uuid-here
VAPI_PUBLIC_KEY=pub_your_public_key_here  # Optional but recommended

# Your Railway deployment URL (update with your actual URL)
RAILWAY_URL=https://your-app-name.up.railway.app
```

## Step 4: Configure Vapi Assistant

1. In Vapi Dashboard, go to **Assistants**
2. Create a new assistant with these settings:

### Model Configuration

- **Model Provider**: Custom LLM
- **Model**: `openai/gpt-4` (this is just a label)
- **Base URL**: `https://your-app-name.up.railway.app/vapi`
- **API Key**: Any value (e.g., `dummy-key`)

### Voice Configuration

- **Provider**: ElevenLabs
- **Voice ID**: Use same as your `ELEVENLABS_VOICE_ID`
- **Model**: `eleven_flash_v2_5`

### First Message

```
Hi {{userName}}! This is Pepper calling you back from WhatsApp. {{recentContext}} How can I help you today?
```

### System Prompt

```
You are Pepper, a helpful AI assistant. You're currently on a phone call with {{userName}}.

RECENT CONTEXT FROM WHATSAPP:
{{recentContext}}

CONVERSATION TOPIC: {{conversationTopic}}

PHONE CALL GUIDELINES:
- Be conversational and natural (this is a phone call, not text messages)
- Reference the WhatsApp conversation naturally when relevant
- Keep responses concise - people don't like long speeches on phone calls
- If you need to share detailed information, offer to send it via WhatsApp
- Be the same helpful, friendly Pepper they know from messaging
```

### Variables

Add these custom variables:

- `userName` (string)
- `recentContext` (string)
- `conversationTopic` (string)
- `callingReason` (string)

## Step 5: Test Voice Calling

### 1. Check Health Status

```bash
curl https://your-app-name.up.railway.app/vapi/health
```

Expected response:

```json
{
  "status": "healthy",
  "message": "Voice calling system is operational",
  "components": {
    "vapi_client": { "status": "initialized" },
    "vapi_connection": { "status": "connected" },
    "phone_config": {
      "phone_number_id": "your-uuid",
      "voice_id": "your-voice-id",
      "railway_url": "your-url"
    }
  }
}
```

### 2. Test Call (Admin Only)

```bash
curl -X POST "https://your-app-name.up.railway.app/vapi/test-call?phone_number=+1234567890"
```

### 3. WhatsApp Test

Send "call me" to your WhatsApp bot. You should:

1. See confirmation message in WhatsApp
2. Receive phone call within 10-15 seconds
3. Voice-Pepper will reference your WhatsApp conversation

## Troubleshooting

### Common Issues

#### 1. "Voice calling is temporarily unpepperilable"

- **Cause**: Vapi client initialization failed
- **Fix**: Check VAPI_API_PRIVATE_KEY and VAPI_PHONE_NUMBER_ID in Railway

#### 2. "Could you share your phone number?"

- **Cause**: Phone number not passed to voice_calling_node
- **Fix**: This is now fixed in the latest code. Redeploy if seeing this.

#### 3. No phone call after "Calling you now" message

- **Cause**: Vapi configuration issue
- **Fix**:
  - Check Vapi dashboard for call logs
  - Verify phone number is active
  - Check Railway logs for specific errors

#### 4. "Failed to create global Vapi client"

- **Cause**: Missing environment variables
- **Fix**: Ensure all VAPI\_\* variables are set in Railway

### Checking Logs

In Railway dashboard, look for these log patterns:

**Successful call initiation:**

```
📞 INITIATING OUTBOUND CALL:
   📱 To: +1234567890
   👤 User: John
✅ VOICE CALL SUCCESSFULLY INITIATED:
   📞 Call ID: abc123
```

**Failed call:**

```
❌ VAPI NOT CONNECTED - Cannot make calls
❌ INVALID PHONE NUMBER: '1234567890'
🚨 VAPI CALL ERROR: [specific error]
```

## How It Works

1. **User says "call me"** in WhatsApp
2. **Router detects** voice_call intent using LLM (not hardcoded)
3. **Voice calling node**:
   - Extracts phone number from WhatsApp
   - Prepares conversation context
   - Creates Vapi assistant with context
   - Initiates outbound call
4. **During call**:
   - Vapi handles speech-to-text
   - Sends text to Pepper's `/vapi/chat/completions` endpoint
   - Pepper processes through same LangGraph workflow
   - Response sent back to Vapi
   - Vapi converts to speech
5. **Call ends**:
   - User returns to WhatsApp conversation
   - Context maintained between channels

## Security Considerations

1. **Disable test endpoints** in production:

   - Remove `/vapi/test-call` endpoint
   - Or add authentication middleware

2. **Rate limiting**:

   - Add rate limits to prevent abuse
   - Limit calls per user per hour

3. **Phone number validation**:
   - Verify phone numbers belong to WhatsApp users
   - Consider allowlist for production

## Cost Considerations

Voice calling incurs costs:

- **Vapi**: ~$0.08/minute for calls
- **ElevenLabs**: TTS character usage
- **Groq**: LLM token usage
- **Phone number**: Monthly rental fee

Monitor usage in respective dashboards.

## Next Steps

1. **Test thoroughly** with different scenarios
2. **Monitor logs** during initial deployment
3. **Gather user feedback** on voice quality
4. **Consider adding**:
   - Call duration limits
   - Call scheduling
   - Voicemail functionality
   - Multi-language support

## Support

If you encounter issues:

1. Check Railway logs for detailed errors
2. Verify all environment variables
3. Test Vapi connection with health endpoint
4. Check Vapi dashboard for call logs
5. Review this guide for missed steps

Remember: Voice calling requires all components (WhatsApp, Railway, Vapi, ElevenLabs) to work together. Debug systematically by checking each component.
