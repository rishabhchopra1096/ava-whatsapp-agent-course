# Understanding Vapi Implementation - Sequential Reading Guide

## 📚 How to Read This Documentation

This guide helps you understand how voice calling works in our WhatsApp AI companion. Follow the reading order below to build your understanding step by step.

---

## 🚀 Entry Point - How Voice Calls Start

**File:** `src/ai_companion/graph/nodes.py`

- **Function:** `voice_calling_node()` (around line 469)
- **Purpose:** This is where voice calls are initiated when user says "call me"

## 📞 Voice Call Manager

**File:** `src/ai_companion/interfaces/vapi/vapi_client.py`

- **Function:** `make_outbound_call()` (around line 393)
- **Function:** `create_voice_assistant()` (around line 214)
- **Purpose:** Creates Vapi assistants and makes actual phone calls

## 🧠 Voice Context Preparation

**File:** `src/ai_companion/interfaces/vapi/voice_context_manager.py`

- **Function:** `prepare_context_for_voice_call()`
- **Purpose:** Prepares WhatsApp conversation context for voice calls

## 💬 Voice Conversation Processing

**File:** `src/ai_companion/interfaces/vapi/vapi_endpoints.py`

- **Function:** `handle_voice_chat()` (around line 258)
- **Purpose:** Processes voice conversation when Vapi calls our custom LLM endpoint

## 🔗 Integration Point

**File:** `src/ai_companion/interfaces/whatsapp/webhook_endpoint.py`

- **Function:** `whatsapp_handler()` → `router` → `voice_calling_node`
- **Purpose:** How WhatsApp "call me" messages trigger voice calls

---

## 📖 Vapi Documentation Sections to Read

### 🔥 Essential (Read These First)

1. **"Introduction"** - Understanding what Vapi does
2. **"Custom LLMs > Bring your own server"** - This is exactly what we implemented
3. **"Phone calls"** - How phone calling works in Vapi
4. **"Place calls"** - Making outbound calls (what we do)

### 🎯 Relevant to Our Implementation

5. **"Assistants"** - Understanding assistant configuration (we create these dynamically)
6. **"Model configurations"** - How we configure the custom LLM endpoint
7. **"Webhooks"** - How Vapi communicates with our server
8. **"How Vapi works"** - Overall architecture understanding

### 📚 Nice to Have

9. **"Debugging voice agents"** - For troubleshooting (like we're doing now)
10. **"Call insights"** - Understanding call logs and analytics

---

## 🔄 How Documentation Relates to Our Code

### "Custom LLMs > Bring your own server"

- **Our Implementation:** `vapi_endpoints.py:handle_voice_chat()`
- **What it does:** Makes Vapi think we're OpenAI, but we route to LangGraph

### "Phone calls > Place calls"

- **Our Implementation:** `vapi_client.py:make_outbound_call()`
- **What it does:** Uses Vapi SDK to make outbound calls

### "Assistants"

- **Our Implementation:** `vapi_client.py:create_voice_assistant()`
- **What it does:** Creates dynamic assistants with WhatsApp context

### "Webhooks"

- **Our Implementation:** `vapi_endpoints.py:handle_vapi_webhook()` (not fully used yet)
- **What it does:** Receives call status updates from Vapi

---

## 📋 Complete Reading Flow

For complete understanding, follow this order:

1. **Start with "Introduction"** to understand Vapi's role
2. **Read "Custom LLMs > Bring your own server"** to understand our exact approach
3. **Read our code in this order:**
   - `nodes.py:voice_calling_node()` (the trigger)
   - `vapi_client.py:make_outbound_call()` (the call maker)
   - `vapi_endpoints.py:handle_voice_chat()` (the brain)
4. **Read "Phone calls"** to understand the full calling flow
5. **Read "Debugging voice agents"** to understand what we're doing now
