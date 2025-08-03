"""
🚪 WHATSAPP ENTRY POINT - The simple web server that receives WhatsApp messages

WHAT IS THIS FILE?
This file creates a web server that listens for messages from WhatsApp. When someone
sends a message to Pepper on WhatsApp, this server receives it and passes it to the 
code that actually processes the message.

BEGINNER CONCEPTS YOU NEED TO KNOW:

🌐 WHAT IS A WEB SERVER?
A web server is a program that sits on a computer and waits for other computers
to send it messages over the internet. Like a phone that's always ready to answer calls.
- When you visit a website, your browser sends a message to a web server
- The web server sends back the webpage
- In our case, WhatsApp sends messages to our web server

📦 WHAT IS DOCKER?
Docker is like a shipping container for computer programs. Just like how:
- A shipping container can hold anything (furniture, food, electronics)
- And can be moved between different ships, trucks, trains
- Docker containers hold our program and can run on any computer

Docker helps us because:
- Our program works the same way on my computer, your computer, and the cloud
- We don't have to worry about "it works on my machine but not yours"
- Easy to deploy (put our program online)

🔗 WHAT IS A WEBHOOK IN pepper'S CONTEXT?
A webhook is how WhatsApp notifies Pepper instantly when someone sends a message.
Instead of Pepper constantly asking "any new messages?", WhatsApp pushes messages to Pepper.

Why webhooks are perfect for Pepper:
- Instant response: User sends message, Pepper processes immediately 
- No polling overhead: Pepper doesn't waste resources checking for messages
- Scalable: Works with thousands of users simultaneously

Pepper's WhatsApp webhook flow:
1. User sends message to Pepper's WhatsApp number
2. WhatsApp Business API receives the message
3. WhatsApp immediately sends HTTP POST to our "/whatsapp_response" endpoint
4. This FastAPI server receives the webhook and processes through Pepper's LangGraph workflow
5. Pepper's response gets sent back to WhatsApp API
6. WhatsApp delivers Pepper's response to the user's phone

⚡ WHAT IS FASTAPI IN pepper'S ARCHITECTURE?
FastAPI is the Python web framework that creates Pepper's WhatsApp webhook server.
It handles the HTTP communication layer so Pepper can focus on AI processing.

Why FastAPI is perfect for Pepper:
- Fast async processing: Can handle multiple WhatsApp users simultaneously
- Automatic request parsing: Converts WhatsApp webhook JSON into Python objects
- Built-in validation: Ensures incoming webhooks have the right format
- Production-ready: Handles errors gracefully for real users

FastAPI's role in Pepper:
- Listens on port 8080 for WhatsApp webhook HTTP requests
- Routes "/whatsapp_response" calls to whatsapp_handler() function
- Manages async processing so Pepper can handle multiple conversations at once
- Returns proper HTTP status codes to WhatsApp API for reliability

🛣️ WHAT IS ROUTING IN pepper'S CONTEXT?
Routing directs incoming WhatsApp webhooks to the right processing function.
- WhatsApp sends HTTP request to "/whatsapp_response" endpoint
- FastAPI router automatically calls whatsapp_handler() function
- Different endpoints could handle different types of messages (if we had them)

In Pepper's case:
- All WhatsApp messages go to the same endpoint: "/whatsapp_response" 
- The whatsapp_handler() function then processes them through Pepper's LangGraph workflow
- This is different from Chainlit which uses WebSocket connections instead of HTTP endpoints

THE COMPLETE FLOW:
1. User sends WhatsApp message to Pepper
2. WhatsApp servers receive the message
3. WhatsApp makes HTTP POST request to our webhook URL
4. This FastAPI server receives the request
5. Router sends request to whatsapp_handler function
6. whatsapp_handler processes message through Pepper's brain
7. Response sent back to WhatsApp
8. WhatsApp delivers response to user

REAL-WORLD ANALOGY GROUNDED IN pepper'S ACTUAL FUNCTIONALITY:
This file is like Pepper's phone reception desk:
- The FastAPI server is always listening for WhatsApp webhook calls (like a phone always ready)
- When WhatsApp sends a message webhook, this server receives it immediately
- The router directs the webhook to whatsapp_handler() where Pepper's brain processes it
- The actual conversation happens in whatsapp_response.py using the SAME LangGraph workflow as Chainlit
- Just like how a receptionist connects callers to the right department, this connects WhatsApp messages to Pepper's AI processing

WHY IS THIS FILE SO SHORT?
This file only does ONE job: receive webhooks and pass them to the right handler.
All the actual work (processing messages, talking to Pepper's brain) happens in 
whatsapp_response.py. This keeps things simple and organized.

DOCKER CONNECTION:
This file gets packaged into a Docker container that runs on port 8080.
The docker-compose.yml file tells Docker to start this server automatically.
"""

# IMPORT SECTION - Getting the tools we need

# FastAPI: The web server framework that makes it easy to receive HTTP requests
# This is like importing a "web server construction kit" 
from fastapi import FastAPI

# whatsapp_router: The actual code that handles WhatsApp messages
# This is defined in whatsapp_response.py - it contains all the functions
# that process messages, download images, send responses, etc.
from ai_companion.interfaces.whatsapp.whatsapp_response import whatsapp_router

# vapi_router: The voice calling endpoints that handle phone conversations  
# This is defined in vapi_endpoints.py - it contains all the functions
# that process voice calls, create voice assistants, handle call webhooks, etc.
from ai_companion.interfaces.vapi.vapi_endpoints import vapi_router


# STEP 1: Create the web server
# FastAPI() creates a new web server instance - like opening a new restaurant
# This server will listen for HTTP requests from WhatsApp
app = FastAPI()

# STEP 2: Tell the server how to handle WhatsApp requests
# app.include_router() connects WhatsApp message processing to this web server
# Instead of handling WhatsApp logic directly in this simple file,
# we delegate to whatsapp_router which contains all the actual Pepper conversation processing
# This is like connecting a specialized Pepper brain module to our basic HTTP server

# What whatsapp_router contains:
# - A function that handles GET requests (for webhook verification)
# - A function that handles POST requests (for actual messages)  
# - Helper functions for downloading images/audio from WhatsApp
# - Helper functions for sending responses back to WhatsApp

# After this line, when WhatsApp sends a request to /whatsapp_response,
# it will automatically go to the right function in whatsapp_response.py
app.include_router(whatsapp_router)

# STEP 3: Add voice calling support via Vapi
# app.include_router(vapi_router) connects voice call processing to this web server
# This adds new endpoints like /vapi/chat/completions and /vapi/webhook
# 
# What vapi_router contains:
# - /vapi/chat/completions: OpenAI-compatible endpoint that connects Vapi to Pepper's Groq LLM
# - /vapi/webhook: Receives call events (call started, ended, transcripts)
# - /vapi/health: Health check for the voice calling system
# - /vapi/test-chat: Testing endpoint for development
#
# After this line, when Vapi sends voice conversations to /vapi/chat/completions,
# they will be processed through Pepper's existing LangGraph + Groq LLM workflow
app.include_router(vapi_router)
