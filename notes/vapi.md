---
title: Introduction
subtitle: Build voice AI agents that can make and receive phone calls
slug: quickstart/introduction
---

## What is Vapi?

Vapi is the developer platform for building voice AI agents. We handle the complex infrastructure so you can focus on creating great voice experiences.

**Voice agents** allow you to:

- Have natural conversations with users
- Make and receive phone calls
- Integrate with your existing systems and APIs
- Handle complex workflows like appointment scheduling, customer support, and more

## How voice agents work

Every Vapi assistant combines three core technologies:

<CardGroup cols={3}>
  <Card title="Speech-to-Text" icon="microphone" iconType="solid">
    Converts user speech into text that your agent can understand
  </Card>
  <Card title="Large Language Model" icon="brain" iconType="solid">
    Processes the conversation and generates intelligent responses
  </Card>
  <Card title="Text-to-Speech" icon="volume-high" iconType="solid">
    Converts your agent's responses back into natural speech
  </Card>
</CardGroup>

You have full control over each component, with dozens of providers and models to choose from; OpenAI, Anthropic, Google, Deepgram, ElevenLabs, and many, many more.

## Two ways to build voice agents

Vapi offers two main primitives for building voice agents, each designed for different use cases:

<CardGroup cols={2}>
  <Card 
    title="Assistants" 
    icon="robot" 
    iconType="solid"
    href="/assistants/dynamic-variables"
  >
    <div className='absolute top-4 right-4'>
      <Icon icon="arrow-up-right-from-square" />
    </div>
    **Best for:** Quick kickstart for simple conversations
    <br />
    Assistants use a single system prompt to control behavior. Perfect for:
    - Customer support chatbots
    - Simple question-answering agents
    - Getting started quickly with minimal setup
  </Card>
  <Card 
    title="Workflows" 
    icon="diagram-project" 
    iconType="solid"
    href="/workflows/quickstart"
  >
    <div className='absolute top-4 right-4'>
      <Icon icon="arrow-up-right-from-square" />
    </div>
    **Best for:** Complex logic and multi-step processes
    <br />
    Workflows use visual decision trees and conditional logic. Perfect for:
    - Appointment scheduling with availability checks
    - Lead qualification with branching questions
    - Complex customer service flows with escalation
  </Card>
</CardGroup>

## Key capabilities

- **Real-time conversations:** Sub-600ms response times with natural turn-taking
- **Phone integration:** Make and receive calls on any phone number
- **Web integration:** Embed voice calls directly in your applications
- **Tool integration:** Connect to your APIs, databases, and existing systems
- **Custom workflows:** Build complex multi-step processes with decision trees

## Choose your path

<CardGroup cols={2}>
  <Card
    title="Phone Calls"
    icon="phone"
    iconType="solid"
    href="/quickstart/phone"
  >
    <div className='absolute top-4 right-4'>
      <Icon icon="arrow-up-right-from-square" />
    </div>
    - Create a voice agent for inbound/outbound calls
    - Build customer support or sales automation
    - Get started with no coding required

    *Build your first voice agent in 5 minutes using our dashboard.*

  </Card>
  <Card
    title="Web Integration"
    icon="browser"
    iconType="solid"
    href="/quickstart/web"
  >
    <div className='absolute top-4 right-4'>
      <Icon icon="arrow-up-right-from-square" />
    </div>
    - Add voice capabilities to your web application
    - Integrate voice chat into your existing product
    - Build with code and SDKs

    *Embed live voice conversations directly in your app.*

  </Card>
</CardGroup>

## Developer tools

### Vapi CLI

The Vapi CLI brings the full power of the platform to your terminal:

<CardGroup cols={2}>
  <Card
    title="CLI Overview"
    icon="terminal"
    iconType="solid"
    href="/cli"
  >
    <div className='absolute top-4 right-4'>
      <Icon icon="arrow-up-right-from-square" />
    </div>
    Install in seconds with:
    ```bash
    curl -sSL https://vapi.ai/install.sh | bash
    ```
    Everything from the dashboard, now in your terminal.
  </Card>
  <Card
    title="Key Features"
    icon="sparkles"
    iconType="solid"
  >
    - **Project Integration:** Auto-detect and set up Vapi in any codebase
    - **Webhook Forwarding:** Test webhooks on your local server
    - **MCP Support:** Turn your IDE into a Vapi expert
    - **Multi-account:** Switch between environments seamlessly
  </Card>
</CardGroup>

## Popular use cases

<CardGroup cols={3}>
  <Card 
    title="Customer Support" 
    icon="headset" 
    iconType="solid"
    href="/assistants/examples/inbound-support"
  >
    <div className='absolute top-4 right-4'>
      <Icon icon="arrow-up-right-from-square" />
    </div>
    <div class="vapi-badge vapi-badge-assistant">Built with Assistants</div>
    
    Automate inbound support calls with agents that can access your knowledge base and escalate to humans when needed.
  </Card>
  <Card 
    title="Sales & Lead Qualification" 
    icon="phone-office" 
    iconType="solid"
    href="/workflows/examples/lead-qualification"
  >
    <div className='absolute top-4 right-4'>
      <Icon icon="arrow-up-right-from-square" />
    </div>
    <div class="vapi-badge vapi-badge-workflow">Built with Workflows</div>
    
    Make outbound sales calls, qualify leads, and schedule appointments with sophisticated branching logic.
  </Card>
  <Card 
    title="Appointment Scheduling" 
    icon="calendar-check" 
    iconType="solid"
    href="/workflows/examples/appointment-scheduling"
  >
    <div className='absolute top-4 right-4'>
      <Icon icon="arrow-up-right-from-square" />
    </div>
    <div class="vapi-badge vapi-badge-workflow">Built with Workflows</div>
    
    Handle booking requests, check availability, and confirm appointments with conditional routing.
  </Card>
  <Card 
    title="Medical Triage & Scheduling" 
    icon="stethoscope" 
    iconType="solid"
    href="/workflows/examples/clinic-triage-scheduling"
  >
    <div className='absolute top-4 right-4'>
      <Icon icon="arrow-up-right-from-square" />
    </div>
    <div class="vapi-badge vapi-badge-workflow">Built with Workflows</div>
    
    Emergency routing and appointment scheduling for healthcare.
  </Card>
  <Card 
    title="E-commerce Order Management" 
    icon="shopping-cart" 
    iconType="solid"
    href="/workflows/examples/ecommerce-order-management"
  >
    <div className='absolute top-4 right-4'>
      <Icon icon="arrow-up-right-from-square" />
    </div>
    <div class="vapi-badge vapi-badge-workflow">Built with Workflows</div>
    
    Order tracking, returns, and customer support workflows.
  </Card>
  <Card 
    title="See more examples" 
    icon="book" 
    iconType="solid" 
    href="/examples"
  >
    <div className='absolute top-4 right-4'>
      <Icon icon="arrow-up-right-from-square" />
    </div>
    See our collection of examples covering a wide range of use cases.
  </Card>
</CardGroup>

---

title: Phone calls
subtitle: Learn to make your first phone call with a voice agent
slug: quickstart/phone

---

## Overview

Vapi makes it easy to build voice agents that can make and receive phone calls. In under 5 minutes, you'll create a voice assistant and start talking to it over the phone.

**In this quickstart, you'll learn to:**

- Create an assistant using the Dashboard or programmatically
- Set up a phone number
- Make your first inbound and outbound calls

## Prerequisites

- [A Vapi account](https://dashboard.vapi.ai)
- For SDK usage: API key from the Dashboard

<Tip>
**Using the Vapi CLI?** You can create assistants, manage phone numbers, and make calls directly from your terminal:

```bash
# Install the CLI
curl -sSL https://vapi.ai/install.sh | bash

# Login and create an assistant
vapi login
vapi assistant create
```

[Learn more about the Vapi CLI →](/cli)
</Tip>

## Create your first voice assistant

<Tabs>
  <Tab title="Dashboard">
    <Steps>
      <Step title="Open the Vapi Dashboard">
        Go to [dashboard.vapi.ai](https://dashboard.vapi.ai) and log in to your account.
      </Step>

      <Step title="Create a new assistant">
        In the dashboard, create a new assistant using the customer support specialist template.

        <Frame caption="Creating a new assistant">
          <img src="file:bafbdcde-6bb6-4015-91d6-b0b3e6dc861f" />
        </Frame>
      </Step>

      <Step title="Configure your assistant">
        Set the first message and system prompt for your assistant:

        **First message:**
        ```plaintext
        Hi there, this is Alex from TechSolutions customer support. How can I help you today?
        ```

        **System prompt:**
        ```plaintext
        You are Alex, a customer service voice assistant for TechSolutions. Your primary purpose is to help customers resolve issues with their products, answer questions about services, and ensure a satisfying support experience.
        - Sound friendly, patient, and knowledgeable without being condescending
        - Use a conversational tone with natural speech patterns
        - Speak with confidence but remain humble when you don't know something
        - Demonstrate genuine concern for customer issues
        ```
      </Step>
    </Steps>

  </Tab>

  <Tab title="TypeScript (Server SDK)">
    <Steps>
      <Step title="Install the SDK">
        <CodeBlocks>
        ```bash title="npm"
        npm install @vapi-ai/server-sdk
        ```

        ```bash title="yarn"
        yarn add @vapi-ai/server-sdk
        ```

        ```bash title="pnpm"
        pnpm add @vapi-ai/server-sdk
        ```

        ```bash title="bun"
        bun add @vapi-ai/server-sdk
        ```
        </CodeBlocks>
      </Step>

      <Step title="Create the assistant">
        ```typescript
        import { VapiClient } from '@vapi-ai/server-sdk';

        // Initialize the Vapi client
        const vapi = new VapiClient({
          token: 'your-api-key', // Replace with your actual API key
        });

        // Define the system prompt for customer support
        const systemPrompt = `You are Alex, a customer service voice assistant for TechSolutions. Your primary purpose is to help customers resolve issues with their products, answer questions about services, and ensure a satisfying support experience.
        - Sound friendly, patient, and knowledgeable without being condescending
        - Use a conversational tone with natural speech patterns
        - Speak with confidence but remain humble when you don'\''t know something
        - Demonstrate genuine concern for customer issues`;

        async function createSupportAssistant() {
          try {
            const assistant = await vapi.assistants.create({
              name: 'Customer Support Assistant',
              // Configure the AI model
              model: {
                provider: 'openai',
                model: 'gpt-4o',
                messages: [
                  {
                    role: 'system',
                    content: systemPrompt,
                  },
                ],
              },
              // Configure the voice
              voice: {
                provider: 'playht',
                voice_id: 'jennifer',
              },
              // Set the first message
              firstMessage: 'Hi there, this is Alex from TechSolutions customer support. How can I help you today?',
            });

            console.log('Assistant created:', assistant.id);
            return assistant;
          } catch (error) {
            console.error('Error creating assistant:', error);
            throw error;
          }
        }

        // Create the assistant
        createSupportAssistant();
        ```
      </Step>
    </Steps>

  </Tab>

  <Tab title="Python (Server SDK)">
    <Steps>
      <Step title="Install the SDK">
        ```bash
        pip install vapi_server_sdk
        ```
      </Step>

      <Step title="Create the assistant">
        ```python
        from vapi import Vapi

        # Initialize the Vapi client
        client = Vapi(token="your-api-key")  # Replace with your actual API key

        # Define the system prompt for customer support
        system_prompt = """You are Alex, a customer service voice assistant for TechSolutions. Your primary purpose is to help customers resolve issues with their products, answer questions about services, and ensure a satisfying support experience.
        - Sound friendly, patient, and knowledgeable without being condescending
        - Use a conversational tone with natural speech patterns
        - Speak with confidence but remain humble when you don't know something
        - Demonstrate genuine concern for customer issues"""

        def create_support_assistant():
            try:
                assistant = client.assistants.create(
                    name="Customer Support Assistant",
                    # Configure the AI model
                    model={
                        "provider": "openai",
                        "model": "gpt-4o",
                        "messages": [
                            {
                                "role": "system",
                                "content": system_prompt,
                            }
                        ],
                    },
                    # Configure the voice
                    voice={
                        "provider": "playht",
                        "voice_id": "jennifer",
                    },
                    # Set the first message
                    first_message="Hi there, this is Alex from TechSolutions customer support. How can I help you today?",
                )

                print(f"Assistant created: {assistant.id}")
                return assistant
            except Exception as error:
                print(f"Error creating assistant: {error}")
                raise error

        # Create the assistant
        create_support_assistant()
        ```
      </Step>
    </Steps>

  </Tab>

  <Tab title="cURL">
    <Steps>
      <Step title="Create the assistant">
        ```bash
        curl -X POST "https://api.vapi.ai/assistant" \
          -H "Authorization: Bearer your-api-key" \
          -H "Content-Type: application/json" \
          -d '{
            "name": "Customer Support Assistant",
            "model": {
              "provider": "openai",
              "model": "gpt-4o",
              "messages": [
                {
                  "role": "system",
                  "content": "You are Alex, a customer service voice assistant for TechSolutions. Your primary purpose is to help customers resolve issues with their products, answer questions about services, and ensure a satisfying support experience.\n- Sound friendly, patient, and knowledgeable without being condescending\n- Use a conversational tone with natural speech patterns\n- Speak with confidence but remain humble when you don'\''t know something\n- Demonstrate genuine concern for customer issues"
                }
              ]
            },
            "voice": {
              "provider": "playht",
              "voice_id": "jennifer"
            },
            "firstMessage": "Hi there, this is Alex from TechSolutions customer support. How can I help you today?"
          }'
        ```
      </Step>
    </Steps>
  </Tab>
</Tabs>

## Set up a phone number

<Tabs>
  <Tab title="Dashboard">
    <Steps>
      <Step title="Create a phone number">
        In the Phone Numbers tab, create a free US phone number or import an existing number from another provider.
        
        <Frame caption="Create a phone number">
          <img src="file:d4a342c6-2dc9-4891-ae78-446e3f8fb3a3" />
        </Frame>
        
        <Warning>
          Free Vapi phone numbers are only available for US national use. For international calls, you'll need to import a number from Twilio or another provider.
        </Warning>
      </Step>

      <Step title="Attach your assistant to the number">
        Select your assistant in the inbound settings for your phone number. When this number is called, your assistant will automatically answer.

        <Frame>
          <img src="file:8d774b9e-434f-4980-a6ed-5d18fccfa57e" />
        </Frame>
      </Step>
    </Steps>

  </Tab>

  <Tab title="TypeScript (Server SDK)">
    <Steps>
      <Step title="Purchase a phone number">
        ```typescript
        async function purchasePhoneNumber() {
          try {
            // Purchase a phone number
            const phoneNumber = await vapi.phoneNumbers.create({
              fallbackDestination: {
                type: 'number',
                number: '+1234567890', // Your fallback number
              },
            });
            
            console.log('Phone number created:', phoneNumber.number);
            return phoneNumber;
          } catch (error) {
            console.error('Error creating phone number:', error);
            throw error;
          }
        }
        ```
      </Step>

      <Step title="Configure inbound calls">
        ```typescript
        async function configureInboundCalls(phoneNumberId: string, assistantId: string) {
          try {
            // Update phone number with assistant configuration
            const updatedNumber = await vapi.phoneNumbers.update(phoneNumberId, {
              assistantId: assistantId,
            });

            console.log('Phone number configured for inbound calls');
            return updatedNumber;
          } catch (error) {
            console.error('Error configuring phone number:', error);
            throw error;
          }
        }
        ```
      </Step>
    </Steps>

  </Tab>

  <Tab title="Python (Server SDK)">
    <Steps>
      <Step title="Purchase a phone number">
        ```python
        def purchase_phone_number():
            try:
                # Purchase a phone number
                phone_number = client.phone_numbers.create(
                    fallback_destination={
                        "type": "number",
                        "number": "+1234567890",  # Your fallback number
                    }
                )
                
                print(f"Phone number created: {phone_number.number}")
                return phone_number
            except Exception as error:
                print(f"Error creating phone number: {error}")
                raise error
        ```
      </Step>

      <Step title="Configure inbound calls">
        ```python
        def configure_inbound_calls(phone_number_id: str, assistant_id: str):
            try:
                # Update phone number with assistant configuration
                updated_number = client.phone_numbers.update(
                    phone_number_id,
                    assistant_id=assistant_id,
                )

                print("Phone number configured for inbound calls")
                return updated_number
            except Exception as error:
                print(f"Error configuring phone number: {error}")
                raise error
        ```
      </Step>
    </Steps>

  </Tab>

  <Tab title="cURL">
    <Steps>
      <Step title="Purchase a phone number">
        ```bash
        curl -X POST "https://api.vapi.ai/phone-number" \
          -H "Authorization: Bearer your-api-key" \
          -H "Content-Type: application/json" \
          -d '{
            "fallbackDestination": {
              "type": "number",
              "number": "+1234567890"
            }
          }'
        ```
      </Step>

      <Step title="Configure inbound calls">
        ```bash
        curl -X PATCH "https://api.vapi.ai/phone-number/{phone-number-id}" \
          -H "Authorization: Bearer your-api-key" \
          -H "Content-Type: application/json" \
          -d '{
            "assistantId": "your-assistant-id"
          }'
        ```
      </Step>
    </Steps>

  </Tab>
</Tabs>

## Make your first calls

<Steps>
  <Step title="Test inbound calling">
    Call the phone number you just created. Your assistant will pick up and start the conversation with your configured first message.
  </Step>

  <Step title="Try outbound calling">
    **Using the Dashboard:**
    
    In the dashboard, go to the outbound calls section:
    1. Enter your own phone number as the target
    2. Select your assistant
    3. Click "Make Call"

    <Frame caption="Making an outbound call">
      <img src="file:a7908e79-0223-4a96-877e-80906634e110" />
    </Frame>

    **Using the SDK:**

    <Tabs>
      <Tab title="TypeScript (Server SDK)">
        ```typescript
        async function makeOutboundCall(assistantId: string, phoneNumber: string) {
          try {
            const call = await vapi.calls.create({
              assistant: {
                assistantId: assistantId,
              },
              phoneNumberId: 'your-phone-number-id', // Your Vapi phone number ID
              customer: {
                number: phoneNumber, // Target phone number
              },
            });

            console.log('Outbound call initiated:', call.id);
            return call;
          } catch (error) {
            console.error('Error making outbound call:', error);
            throw error;
          }
        }

        // Make a call to your own number for testing
        makeOutboundCall('your-assistant-id', '+1234567890');
        ```
      </Tab>

      <Tab title="Python (Server SDK)">
        ```python
        def make_outbound_call(assistant_id: str, phone_number: str):
            try:
                call = client.calls.create(
                    assistant_id=assistant_id,
                    phone_number_id="your-phone-number-id",  # Your Vapi phone number ID
                    customer={
                        "number": phone_number,  # Target phone number
                    },
                )

                print(f"Outbound call initiated: {call.id}")
                return call
            except Exception as error:
                print(f"Error making outbound call: {error}")
                raise error

        # Make a call to your own number for testing
        make_outbound_call("your-assistant-id", "+1234567890")
        ```
      </Tab>

      <Tab title="cURL">
        ```bash
        curl -X POST "https://api.vapi.ai/call" \
          -H "Authorization: Bearer your-api-key" \
          -H "Content-Type: application/json" \
          -d '{
            "assistant": {
              "assistantId": "your-assistant-id"
            },
            "phoneNumberId": "your-phone-number-id",
            "customer": {
              "number": "+1234567890"
            }
          }'
        ```
      </Tab>
    </Tabs>

    Your assistant will call the specified number immediately.

  </Step>

  <Step title="Test web calling (optional)">
    You can also test your assistant directly in the dashboard by clicking the call button—no phone number required.
    
    <Frame>
      <img src="file:f8041a62-937a-4f5f-9ba7-5ca9453ef08f" />
    </Frame>
  </Step>
</Steps>

## Next steps

Now that you have a working voice assistant:

- **Customize the conversation:** Update the system prompt to match your use case
- **Add tools:** Connect your assistant to external APIs and databases
- **Configure models:** Try different speech and language models for better performance
- **Scale with APIs:** Use Vapi's REST API to create assistants programmatically

<Tip>
Ready to integrate voice into your application? Check out the [Web integration guide](/quickstart/web-integration) to embed voice calls directly in your app.
</Tip>

---

title: Web calls
subtitle: >-
Build voice interfaces and backend integrations using Vapi's Web and Server
SDKs
slug: quickstart/web

---

## Overview

Build powerful voice applications that work across web browsers, mobile apps, and backend systems. This guide covers both client-side voice interfaces and server-side call management using Vapi's comprehensive SDK ecosystem.

**In this quickstart, you'll learn to:**

- Create real-time voice interfaces for web and mobile
- Build automated outbound and inbound call systems
- Handle events and webhooks for call management
- Implement voice widgets and backend integrations

<Tip>
**Developing locally?** The Vapi CLI makes it easy to initialize projects and test webhooks:

```bash
# Initialize Vapi in your project
vapi init

# Forward webhooks to local server
vapi listen --forward-to localhost:3000/webhook
```

[Learn more about the Vapi CLI →](/cli)
</Tip>

## Choose your integration approach

<CardGroup cols={2}>
  <Card title="Client-Side Voice Interfaces" icon="globe">
    **Best for:** User-facing applications, voice widgets, mobile apps
    - Browser-based voice assistants and widgets
    - Real-time voice conversations
    - Mobile voice applications (iOS, Android, React Native, Flutter)
    - Direct user interaction with assistants
  </Card>
  <Card title="Server-Side Call Management" icon="server">
    **Best for:** Backend automation, bulk operations, system integrations
    - Automated outbound call campaigns
    - Inbound call routing and management
    - CRM integrations and bulk operations
    - Webhook processing and real-time events
  </Card>
</CardGroup>

## Web voice interfaces

Build browser-based voice assistants and widgets for real-time user interaction.

### Installation and setup

<Tabs>
  <Tab title="Web SDK">
    Build browser-based voice interfaces:

    <CodeBlocks>
    ```bash title="npm"
    npm install @vapi-ai/web
    ```

    ```bash title="yarn"
    yarn add @vapi-ai/web
    ```

    ```bash title="pnpm"
    pnpm add @vapi-ai/web
    ```

    ```bash title="bun"
    bun add @vapi-ai/web
    ```
    </CodeBlocks>

    ```typescript
    import Vapi from '@vapi-ai/web';

    const vapi = new Vapi('YOUR_PUBLIC_API_KEY');

    // Start voice conversation
    vapi.start('YOUR_ASSISTANT_ID');

    // Listen for events
    vapi.on('call-start', () => console.log('Call started'));
    vapi.on('call-end', () => console.log('Call ended'));
    vapi.on('message', (message) => {
      if (message.type === 'transcript') {
        console.log(`${message.role}: ${message.transcript}`);
      }
    });
    ```

  </Tab>

  <Tab title="React Native">
    Build voice-enabled mobile apps:

    ```bash
    npm install @vapi-ai/react-native
    ```

    ```jsx
    import { VapiProvider, useVapi } from '@vapi-ai/react-native';

    const VoiceApp = () => {
      const { start, stop, isConnected } = useVapi();

      return (
        <View>
          <Button
            title={isConnected ? "End Call" : "Start Call"}
            onPress={() => isConnected ? stop() : start('ASSISTANT_ID')}
          />
        </View>
      );
    };

    export default () => (
      <VapiProvider apiKey="YOUR_PUBLIC_API_KEY">
        <VoiceApp />
      </VapiProvider>
    );
    ```

  </Tab>

  <Tab title="Flutter">
    Create voice apps with Flutter:

    ```yaml
    dependencies:
      vapi_flutter: ^1.0.0
    ```

    ```dart
    import 'package:vapi_flutter/vapi_flutter.dart';

    class VoiceWidget extends StatefulWidget {
      @override
      _VoiceWidgetState createState() => _VoiceWidgetState();
    }

    class _VoiceWidgetState extends State<VoiceWidget> {
      final VapiClient _vapi = VapiClient('YOUR_PUBLIC_API_KEY');
      bool _isConnected = false;

      @override
      Widget build(BuildContext context) {
        return ElevatedButton(
          onPressed: () {
            if (_isConnected) {
              _vapi.stop();
            } else {
              _vapi.start('YOUR_ASSISTANT_ID');
            }
          },
          child: Text(_isConnected ? 'End Call' : 'Start Call'),
        );
      }
    }
    ```

  </Tab>

  <Tab title="iOS">
    Build native iOS voice apps:

    ```swift
    import VapiSDK

    class VoiceViewController: UIViewController {
        private let vapi = VapiClient(apiKey: "YOUR_PUBLIC_API_KEY")

        @IBAction func startCallTapped(_ sender: UIButton) {
            vapi.start(assistantId: "YOUR_ASSISTANT_ID")
        }

        override func viewDidLoad() {
            super.viewDidLoad()
            vapi.delegate = self
        }
    }

    extension VoiceViewController: VapiClientDelegate {
        func vapiCallDidStart() {
            print("Call started")
        }

        func vapiCallDidEnd() {
            print("Call ended")
        }
    }
    ```

  </Tab>
</Tabs>

### Voice widget implementation

Create a voice widget for your website:

<Tabs>
  <Tab title="HTML Script Tag">
    The fastest way to get started. Copy this snippet into your website:

    ```html
    <script>
      var vapiInstance = null;
      const assistant = "assistant_id"; // Substitute with your assistant ID
      const apiKey = "your_public_api_key"; // Substitute with your Public key from Vapi Dashboard.
      const buttonConfig = {}; // Modify this as required

      (function (d, t) {
        var g = document.createElement(t),
          s = d.getElementsByTagName(t)[0];
        g.src =
          "https://cdn.jsdelivr.net/gh/VapiAI/html-script-tag@latest/dist/assets/index.js";
        g.defer = true;
        g.async = true;
        s.parentNode.insertBefore(g, s);

        g.onload = function () {
          vapiInstance = window.vapiSDK.run({
            apiKey: apiKey, // mandatory
            assistant: assistant, // mandatory
            config: buttonConfig, // optional
          });
        };
      })(document, "script");
    </script>
    ```

  </Tab>

  <Tab title="React/TypeScript">
    Build a complete React voice widget:

    ```tsx
    import React, { useState, useEffect } from 'react';
    import Vapi from '@vapi-ai/web';

    interface VapiWidgetProps {
      apiKey: string;
      assistantId: string;
      config?: Record<string, unknown>;
    }

    const VapiWidget: React.FC<VapiWidgetProps> = ({
      apiKey,
      assistantId,
      config = {}
    }) => {
      const [vapi, setVapi] = useState<Vapi | null>(null);
      const [isConnected, setIsConnected] = useState(false);
      const [isSpeaking, setIsSpeaking] = useState(false);
      const [transcript, setTranscript] = useState<Array<{role: string, text: string}>>([]);

      useEffect(() => {
        const vapiInstance = new Vapi(apiKey);
        setVapi(vapiInstance);

        // Event listeners
        vapiInstance.on('call-start', () => {
          console.log('Call started');
          setIsConnected(true);
        });

        vapiInstance.on('call-end', () => {
          console.log('Call ended');
          setIsConnected(false);
          setIsSpeaking(false);
        });

        vapiInstance.on('speech-start', () => {
          console.log('Assistant started speaking');
          setIsSpeaking(true);
        });

        vapiInstance.on('speech-end', () => {
          console.log('Assistant stopped speaking');
          setIsSpeaking(false);
        });

        vapiInstance.on('message', (message) => {
          if (message.type === 'transcript') {
            setTranscript(prev => [...prev, {
              role: message.role,
              text: message.transcript
            }]);
          }
        });

        vapiInstance.on('error', (error) => {
          console.error('Vapi error:', error);
        });

        return () => {
          vapiInstance?.stop();
        };
      }, [apiKey]);

      const startCall = () => {
        if (vapi) {
          vapi.start(assistantId);
        }
      };

      const endCall = () => {
        if (vapi) {
          vapi.stop();
        }
      };

      return (
        <div style={{
          position: 'fixed',
          bottom: '24px',
          right: '24px',
          zIndex: 1000,
          fontFamily: 'Arial, sans-serif'
        }}>
          {!isConnected ? (
            <button
              onClick={startCall}
              style={{
                background: '#12A594',
                color: '#fff',
                border: 'none',
                borderRadius: '50px',
                padding: '16px 24px',
                fontSize: '16px',
                fontWeight: 'bold',
                cursor: 'pointer',
                boxShadow: '0 4px 12px rgba(18, 165, 148, 0.3)',
                transition: 'all 0.3s ease',
              }}
              onMouseOver={(e) => {
                e.currentTarget.style.transform = 'translateY(-2px)';
                e.currentTarget.style.boxShadow = '0 6px 16px rgba(18, 165, 148, 0.4)';
              }}
              onMouseOut={(e) => {
                e.currentTarget.style.transform = 'translateY(0)';
                e.currentTarget.style.boxShadow = '0 4px 12px rgba(18, 165, 148, 0.3)';
              }}
            >
              🎤 Talk to Assistant
            </button>
          ) : (
            <div style={{
              background: '#fff',
              borderRadius: '12px',
              padding: '20px',
              width: '320px',
              boxShadow: '0 8px 32px rgba(0, 0, 0, 0.12)',
              border: '1px solid #e1e5e9'
            }}>
              <div style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                marginBottom: '16px'
              }}>
                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px'
                }}>
                  <div style={{
                    width: '12px',
                    height: '12px',
                    borderRadius: '50%',
                    background: isSpeaking ? '#ff4444' : '#12A594',
                    animation: isSpeaking ? 'pulse 1s infinite' : 'none'
                  }}></div>
                  <span style={{ fontWeight: 'bold', color: '#333' }}>
                    {isSpeaking ? 'Assistant Speaking...' : 'Listening...'}
                  </span>
                </div>
                <button
                  onClick={endCall}
                  style={{
                    background: '#ff4444',
                    color: '#fff',
                    border: 'none',
                    borderRadius: '6px',
                    padding: '6px 12px',
                    fontSize: '12px',
                    cursor: 'pointer'
                  }}
                >
                  End Call
                </button>
              </div>

              <div style={{
                maxHeight: '200px',
                overflowY: 'auto',
                marginBottom: '12px',
                padding: '8px',
                background: '#f8f9fa',
                borderRadius: '8px'
              }}>
                {transcript.length === 0 ? (
                  <p style={{ color: '#666', fontSize: '14px', margin: 0 }}>
                    Conversation will appear here...
                  </p>
                ) : (
                  transcript.map((msg, i) => (
                    <div
                      key={i}
                      style={{
                        marginBottom: '8px',
                        textAlign: msg.role === 'user' ? 'right' : 'left'
                      }}
                    >
                      <span style={{
                        background: msg.role === 'user' ? '#12A594' : '#333',
                        color: '#fff',
                        padding: '8px 12px',
                        borderRadius: '12px',
                        display: 'inline-block',
                        fontSize: '14px',
                        maxWidth: '80%'
                      }}>
                        {msg.text}
                      </span>
                    </div>
                  ))
                )}
              </div>
            </div>
          )}

          <style>{`
            @keyframes pulse {
              0% { opacity: 1; }
              50% { opacity: 0.5; }
              100% { opacity: 1; }
            }
          `}</style>
        </div>
      );
    };

    export default VapiWidget;

    // Usage in your app:
    // <VapiWidget
    //   apiKey="your_public_api_key"
    //   assistantId="your_assistant_id"
    // />
    ```

  </Tab>
</Tabs>

## Server-side call management

Automate outbound calls and handle inbound call processing with server-side SDKs.

### Installation and setup

<Tabs>
  <Tab title="TypeScript">
    Install the TypeScript Server SDK:

    <CodeBlocks>
    ```bash title="npm"
    npm install @vapi-ai/server-sdk
    ```

    ```bash title="yarn"
    yarn add @vapi-ai/server-sdk
    ```

    ```bash title="pnpm"
    pnpm add @vapi-ai/server-sdk
    ```

    ```bash title="bun"
    bun add @vapi-ai/server-sdk
    ```
    </CodeBlocks>

    ```typescript
    import { VapiClient } from "@vapi-ai/server-sdk";

    const vapi = new VapiClient({
      token: process.env.VAPI_API_KEY!
    });

    // Create an outbound call
    const call = await vapi.calls.create({
      phoneNumberId: "YOUR_PHONE_NUMBER_ID",
      customer: { number: "+1234567890" },
      assistantId: "YOUR_ASSISTANT_ID"
    });

    console.log(`Call created: ${call.id}`);
    ```

  </Tab>

  <Tab title="Python">
    Install the Python Server SDK:

    ```bash
    pip install vapi_server_sdk
    ```

    ```python
    from vapi import Vapi

    vapi = Vapi(token=os.getenv("VAPI_API_KEY"))

    # Create an outbound call
    call = vapi.calls.create(
        phone_number_id="YOUR_PHONE_NUMBER_ID",
        customer={"number": "+1234567890"},
        assistant_id="YOUR_ASSISTANT_ID"
    )

    print(f"Call created: {call.id}")
    ```

  </Tab>

  <Tab title="Java">
    Add the Java SDK to your project:

    ```xml
    <dependency>
        <groupId>ai.vapi</groupId>
        <artifactId>server-sdk</artifactId>
        <version>1.0.0</version>
    </dependency>
    ```

    ```java
    import ai.vapi.VapiClient;
    import ai.vapi.models.Call;

    VapiClient vapi = VapiClient.builder()
        .apiKey(System.getenv("VAPI_API_KEY"))
        .build();

    // Create an outbound call
    Call call = vapi.calls().create(CreateCallRequest.builder()
        .phoneNumberId("YOUR_PHONE_NUMBER_ID")
        .customer(Customer.builder().number("+1234567890").build())
        .assistantId("YOUR_ASSISTANT_ID")
        .build());

    System.out.println("Call created: " + call.getId());
    ```

  </Tab>

  <Tab title="Ruby">
    Install the Ruby Server SDK:

    ```bash
    gem install vapi-server-sdk
    ```

    ```ruby
    require 'vapi'

    vapi = Vapi::Client.new(api_key: ENV['VAPI_API_KEY'])

    # Create an outbound call
    call = vapi.calls.create(
      phone_number_id: "YOUR_PHONE_NUMBER_ID",
      customer: { number: "+1234567890" },
      assistant_id: "YOUR_ASSISTANT_ID"
    )

    puts "Call created: #{call.id}"
    ```

  </Tab>

  <Tab title="C#">
    Install the C# Server SDK:

    ```bash
    dotnet add package Vapi.ServerSDK
    ```

    ```csharp
    using Vapi;

    var vapi = new VapiClient(Environment.GetEnvironmentVariable("VAPI_API_KEY"));

    // Create an outbound call
    var call = await vapi.Calls.CreateAsync(new CreateCallRequest
    {
        PhoneNumberId = "YOUR_PHONE_NUMBER_ID",
        Customer = new Customer { Number = "+1234567890" },
        AssistantId = "YOUR_ASSISTANT_ID"
    });

    Console.WriteLine($"Call created: {call.Id}");
    ```

  </Tab>

  <Tab title="Go">
    Install the Go Server SDK:

    ```bash
    go get github.com/VapiAI/server-sdk-go
    ```

    ```go
    package main

    import (
        "fmt"
        "os"
        "github.com/VapiAI/server-sdk-go"
    )

    func main() {
        client := vapi.NewClient(os.Getenv("VAPI_API_KEY"))

        // Create an outbound call
        call, err := client.Calls.Create(&vapi.CreateCallRequest{
            PhoneNumberID: "YOUR_PHONE_NUMBER_ID",
            Customer: &vapi.Customer{
                Number: "+1234567890",
            },
            AssistantID: "YOUR_ASSISTANT_ID",
        })

        if err != nil {
            panic(err)
        }

        fmt.Printf("Call created: %s\n", call.ID)
    }
    ```

  </Tab>
</Tabs>

### Creating assistants

<Tabs>
  <Tab title="TypeScript">
    ```typescript
    const assistant = await vapi.assistants.create({
      name: "Sales Assistant",
      firstMessage: "Hi! I'm calling about your interest in our software solutions.",
      model: {
        provider: "openai",
        model: "gpt-4o",
        temperature: 0.7,
        messages: [{
          role: "system",
          content: "You are a friendly sales representative. Keep responses under 30 words."
        }]
      },
      voice: {
        provider: "11labs",
        voiceId: "21m00Tcm4TlvDq8ikWAM"
      }
    });
    ```
  </Tab>

  <Tab title="Python">
    ```python
    assistant = vapi.assistants.create(
        name="Sales Assistant",
        first_message="Hi! I'm calling about your interest in our software solutions.",
        model={
            "provider": "openai",
            "model": "gpt-4o",
            "temperature": 0.7,
            "messages": [{
                "role": "system",
                "content": "You are a friendly sales representative. Keep responses under 30 words."
            }]
        },
        voice={
            "provider": "11labs",
            "voice_id": "21m00Tcm4TlvDq8ikWAM"
        }
    )
    ```
  </Tab>

  <Tab title="Java">
    ```java
    Assistant assistant = vapi.assistants().create(CreateAssistantRequest.builder()
        .name("Sales Assistant")
        .firstMessage("Hi! I'm calling about your interest in our software solutions.")
        .model(Model.builder()
            .provider("openai")
            .model("gpt-4o")
            .temperature(0.7)
            .messages(List.of(Message.builder()
                .role("system")
                .content("You are a friendly sales representative. Keep responses under 30 words.")
                .build()))
            .build())
        .voice(Voice.builder()
            .provider("11labs")
            .voiceId("21m00Tcm4TlvDq8ikWAM")
            .build())
        .build());
    ```
  </Tab>

  <Tab title="Ruby">
    ```ruby
    assistant = vapi.assistants.create(
      name: "Sales Assistant",
      first_message: "Hi! I'm calling about your interest in our software solutions.",
      model: {
        provider: "openai",
        model: "gpt-4o",
        temperature: 0.7,
        messages: [{
          role: "system",
          content: "You are a friendly sales representative. Keep responses under 30 words."
        }]
      },
      voice: {
        provider: "11labs",
        voice_id: "21m00Tcm4TlvDq8ikWAM"
      }
    )
    ```
  </Tab>

  <Tab title="C#">
    ```csharp
    var assistant = await vapi.Assistants.CreateAsync(new CreateAssistantRequest
    {
        Name = "Sales Assistant",
        FirstMessage = "Hi! I'm calling about your interest in our software solutions.",
        Model = new Model
        {
            Provider = "openai",
            ModelName = "gpt-4o",
            Temperature = 0.7,
            Messages = new List<Message>
            {
                new Message
                {
                    Role = "system",
                    Content = "You are a friendly sales representative. Keep responses under 30 words."
                }
            }
        },
        Voice = new Voice
        {
            Provider = "11labs",
            VoiceId = "21m00Tcm4TlvDq8ikWAM"
        }
    });
    ```
  </Tab>

  <Tab title="Go">
    ```go
    assistant, err := client.Assistants.Create(&vapi.CreateAssistantRequest{
        Name:         "Sales Assistant",
        FirstMessage: "Hi! I'm calling about your interest in our software solutions.",
        Model: &vapi.Model{
            Provider:    "openai",
            Model:       "gpt-4o",
            Temperature: 0.7,
            Messages: []vapi.Message{
                {
                    Role:    "system",
                    Content: "You are a friendly sales representative. Keep responses under 30 words.",
                },
            },
        },
        Voice: &vapi.Voice{
            Provider: "11labs",
            VoiceID:  "21m00Tcm4TlvDq8ikWAM",
        },
    })
    ```
  </Tab>
</Tabs>

### Bulk operations

Run automated call campaigns for sales, surveys, or notifications:

<Tabs>
  <Tab title="TypeScript">
    ```typescript
    async function runBulkCallCampaign(assistantId: string, phoneNumberId: string) {
      const prospects = [
        { number: "+1234567890", name: "John Smith" },
        { number: "+1234567891", name: "Jane Doe" },
        // ... more prospects
      ];

      const calls = [];
      for (const prospect of prospects) {
        const call = await vapi.calls.create({
          assistantId,
          phoneNumberId,
          customer: prospect,
          metadata: { campaign: "Q1_Sales" }
        });
        calls.push(call);

        // Rate limiting
        await new Promise(resolve => setTimeout(resolve, 2000));
      }

      return calls;
    }
    ```

  </Tab>

  <Tab title="Python">
    ```python
    import time

    def run_bulk_call_campaign(assistant_id: str, phone_number_id: str):
        prospects = [
            {"number": "+1234567890", "name": "John Smith"},
            {"number": "+1234567891", "name": "Jane Doe"},
            # ... more prospects
        ]

        calls = []
        for prospect in prospects:
            call = vapi.calls.create(
                assistant_id=assistant_id,
                phone_number_id=phone_number_id,
                customer=prospect,
                metadata={"campaign": "Q1_Sales"}
            )
            calls.append(call)

            # Rate limiting
            time.sleep(2)

        return calls
    ```

  </Tab>

  <Tab title="Java">
    ```java
    public List<Call> runBulkCallCampaign(String assistantId, String phoneNumberId) {
        List<Customer> prospects = Arrays.asList(
            Customer.builder().number("+1234567890").name("John Smith").build(),
            Customer.builder().number("+1234567891").name("Jane Doe").build()
            // ... more prospects
        );

        List<Call> calls = new ArrayList<>();
        for (Customer prospect : prospects) {
            Call call = vapi.calls().create(CreateCallRequest.builder()
                .assistantId(assistantId)
                .phoneNumberId(phoneNumberId)
                .customer(prospect)
                .metadata(Map.of("campaign", "Q1_Sales"))
                .build());
            calls.add(call);

            // Rate limiting
            Thread.sleep(2000);
        }

        return calls;
    }
    ```

  </Tab>

  <Tab title="Ruby">
    ```ruby
    def run_bulk_call_campaign(assistant_id, phone_number_id)
      prospects = [
        { number: "+1234567890", name: "John Smith" },
        { number: "+1234567891", name: "Jane Doe" },
        # ... more prospects
      ]

      calls = []
      prospects.each do |prospect|
        call = vapi.calls.create(
          assistant_id: assistant_id,
          phone_number_id: phone_number_id,
          customer: prospect,
          metadata: { campaign: "Q1_Sales" }
        )
        calls << call

        # Rate limiting
        sleep(2)
      end

      calls
    end
    ```

  </Tab>

  <Tab title="C#">
    ```csharp
    public async Task<List<Call>> RunBulkCallCampaign(string assistantId, string phoneNumberId)
    {
        var prospects = new List<Customer>
        {
            new Customer { Number = "+1234567890", Name = "John Smith" },
            new Customer { Number = "+1234567891", Name = "Jane Doe" },
            // ... more prospects
        };

        var calls = new List<Call>();
        foreach (var prospect in prospects)
        {
            var call = await vapi.Calls.CreateAsync(new CreateCallRequest
            {
                AssistantId = assistantId,
                PhoneNumberId = phoneNumberId,
                Customer = prospect,
                Metadata = new Dictionary<string, object> { ["campaign"] = "Q1_Sales" }
            });
            calls.Add(call);

            // Rate limiting
            await Task.Delay(2000);
        }

        return calls;
    }
    ```

  </Tab>

  <Tab title="Go">
    ```go
    func runBulkCallCampaign(client *vapi.Client, assistantID, phoneNumberID string) ([]*vapi.Call, error) {
        prospects := []*vapi.Customer{
            {Number: "+1234567890", Name: "John Smith"},
            {Number: "+1234567891", Name: "Jane Doe"},
            // ... more prospects
        }

        var calls []*vapi.Call
        for _, prospect := range prospects {
            call, err := client.Calls.Create(&vapi.CreateCallRequest{
                AssistantID:   assistantID,
                PhoneNumberID: phoneNumberID,
                Customer:      prospect,
                Metadata:      map[string]interface{}{"campaign": "Q1_Sales"},
            })
            if err != nil {
                return nil, err
            }
            calls = append(calls, call)

            // Rate limiting
            time.Sleep(2 * time.Second)
        }

        return calls, nil
    }
    ```

  </Tab>
</Tabs>

## Webhook integration

Handle real-time events for both client and server applications:

<Tabs>
  <Tab title="TypeScript">
    ```typescript
    import express from 'express';

    const app = express();
    app.use(express.json());

    app.post('/webhook/vapi', async (req, res) => {
      const { message } = req.body;

      switch (message.type) {
        case 'status-update':
          console.log(`Call ${message.call.id}: ${message.call.status}`);
          break;
        case 'transcript':
          console.log(`${message.role}: ${message.transcript}`);
          break;
        case 'function-call':
          return handleFunctionCall(message, res);
      }

      res.status(200).json({ received: true });
    });

    function handleFunctionCall(message: any, res: express.Response) {
      const { functionCall } = message;

      switch (functionCall.name) {
        case 'lookup_order':
          const orderData = { orderId: functionCall.parameters.orderId, status: 'shipped' };
          return res.json({ result: orderData });
        default:
          return res.status(400).json({ error: 'Unknown function' });
      }
    }

    app.listen(3000, () => console.log('Webhook server running on port 3000'));
    ```

  </Tab>

  <Tab title="Python">
    ```python
    from flask import Flask, request, jsonify

    app = Flask(__name__)

    @app.route('/webhook/vapi', methods=['POST'])
    def handle_vapi_webhook():
        payload = request.get_json()
        message = payload.get('message', {})

        if message.get('type') == 'status-update':
            call = message.get('call', {})
            print(f"Call {call.get('id')}: {call.get('status')}")

        elif message.get('type') == 'transcript':
            print(f"{message.get('role')}: {message.get('transcript')}")

        elif message.get('type') == 'function-call':
            return handle_function_call(message)

        return jsonify({"received": True}), 200

    def handle_function_call(message):
        function_call = message.get('functionCall', {})
        function_name = function_call.get('name')

        if function_name == 'lookup_order':
            order_data = {
                "orderId": function_call.get('parameters', {}).get('orderId'),
                "status": "shipped"
            }
            return jsonify({"result": order_data})

        return jsonify({"error": "Unknown function"}), 400

    if __name__ == '__main__':
        app.run(port=5000)
    ```

  </Tab>

  <Tab title="Java">
    ```java
    @RestController
    @RequestMapping("/webhook")
    public class VapiWebhookController {

        @PostMapping("/vapi")
        public ResponseEntity<?> handleVapiWebhook(@RequestBody Map<String, Object> payload) {
            Map<String, Object> message = (Map<String, Object>) payload.get("message");
            String type = (String) message.get("type");

            switch (type) {
                case "status-update":
                    Map<String, Object> call = (Map<String, Object>) message.get("call");
                    System.out.println("Call " + call.get("id") + ": " + call.get("status"));
                    break;
                case "transcript":
                    System.out.println(message.get("role") + ": " + message.get("transcript"));
                    break;
                case "function-call":
                    return handleFunctionCall(message);
            }

            return ResponseEntity.ok(Map.of("received", true));
        }

        private ResponseEntity<?> handleFunctionCall(Map<String, Object> message) {
            Map<String, Object> functionCall = (Map<String, Object>) message.get("functionCall");
            String functionName = (String) functionCall.get("name");

            if ("lookup_order".equals(functionName)) {
                Map<String, Object> parameters = (Map<String, Object>) functionCall.get("parameters");
                Map<String, Object> orderData = Map.of(
                    "orderId", parameters.get("orderId"),
                    "status", "shipped"
                );
                return ResponseEntity.ok(Map.of("result", orderData));
            }

            return ResponseEntity.badRequest().body(Map.of("error", "Unknown function"));
        }
    }
    ```

  </Tab>

  <Tab title="Ruby">
    ```ruby
    require 'sinatra'
    require 'json'

    post '/webhook/vapi' do
      payload = JSON.parse(request.body.read)
      message = payload['message']

      case message['type']
      when 'status-update'
        call = message['call']
        puts "Call #{call['id']}: #{call['status']}"
      when 'transcript'
        puts "#{message['role']}: #{message['transcript']}"
      when 'function-call'
        return handle_function_call(message)
      end

      content_type :json
      { received: true }.to_json
    end

    def handle_function_call(message)
      function_call = message['functionCall']
      function_name = function_call['name']

      case function_name
      when 'lookup_order'
        order_data = {
          orderId: function_call['parameters']['orderId'],
          status: 'shipped'
        }
        content_type :json
        { result: order_data }.to_json
      else
        status 400
        content_type :json
        { error: 'Unknown function' }.to_json
      end
    end
    ```

  </Tab>

  <Tab title="C#">
    ```csharp
    [ApiController]
    [Route("webhook")]
    public class VapiWebhookController : ControllerBase
    {
        [HttpPost("vapi")]
        public IActionResult HandleVapiWebhook([FromBody] WebhookPayload payload)
        {
            var message = payload.Message;

            switch (message.Type)
            {
                case "status-update":
                    Console.WriteLine($"Call {message.Call.Id}: {message.Call.Status}");
                    break;
                case "transcript":
                    Console.WriteLine($"{message.Role}: {message.Transcript}");
                    break;
                case "function-call":
                    return HandleFunctionCall(message);
            }

            return Ok(new { received = true });
        }

        private IActionResult HandleFunctionCall(WebhookMessage message)
        {
            var functionCall = message.FunctionCall;

            switch (functionCall.Name)
            {
                case "lookup_order":
                    var orderData = new
                    {
                        orderId = functionCall.Parameters["orderId"],
                        status = "shipped"
                    };
                    return Ok(new { result = orderData });
                default:
                    return BadRequest(new { error = "Unknown function" });
            }
        }
    }
    ```

  </Tab>

  <Tab title="Go">
    ```go
    package main

    import (
        "encoding/json"
        "fmt"
        "net/http"
    )

    type WebhookPayload struct {
        Message WebhookMessage `json:"message"`
    }

    type WebhookMessage struct {
        Type         string                 `json:"type"`
        Call         *Call                  `json:"call,omitempty"`
        Role         string                 `json:"role,omitempty"`
        Transcript   string                 `json:"transcript,omitempty"`
        FunctionCall *FunctionCall          `json:"functionCall,omitempty"`
    }

    func handleVapiWebhook(w http.ResponseWriter, r *http.Request) {
        var payload WebhookPayload
        if err := json.NewDecoder(r.Body).Decode(&payload); err != nil {
            http.Error(w, err.Error(), http.StatusBadRequest)
            return
        }

        message := payload.Message

        switch message.Type {
        case "status-update":
            fmt.Printf("Call %s: %s\n", message.Call.ID, message.Call.Status)
        case "transcript":
            fmt.Printf("%s: %s\n", message.Role, message.Transcript)
        case "function-call":
            handleFunctionCall(w, message)
            return
        }

        w.Header().Set("Content-Type", "application/json")
        json.NewEncoder(w).Encode(map[string]bool{"received": true})
    }

    func handleFunctionCall(w http.ResponseWriter, message WebhookMessage) {
        functionCall := message.FunctionCall

        switch functionCall.Name {
        case "lookup_order":
            orderData := map[string]interface{}{
                "orderId": functionCall.Parameters["orderId"],
                "status":  "shipped",
            }
            w.Header().Set("Content-Type", "application/json")
            json.NewEncoder(w).Encode(map[string]interface{}{"result": orderData})
        default:
            http.Error(w, `{"error": "Unknown function"}`, http.StatusBadRequest)
        }
    }

    func main() {
        http.HandleFunc("/webhook/vapi", handleVapiWebhook)
        fmt.Println("Webhook server running on port 8080")
        http.ListenAndServe(":8080", nil)
    }
    ```

  </Tab>
</Tabs>

## Next steps

Now that you understand both client and server SDK capabilities:

- **Explore use cases:** Check out our [examples section](/assistants/examples/inbound-support) for complete implementations
- **Add tools:** Connect your voice agents to external APIs and databases with [custom tools](/tools/custom-tools)
- **Configure models:** Try different [speech and language models](/assistants/speech-configuration) for better performance
- **Scale with workflows:** Use [Vapi workflows](/workflows/quickstart) for complex multi-step processes

## Resources

**Client SDKs:**

- [Web SDK GitHub](https://github.com/VapiAI/web)
- [React Native SDK GitHub](https://github.com/VapiAI/react-native)
- [Flutter SDK GitHub](https://github.com/VapiAI/flutter)
- [iOS SDK GitHub](https://github.com/VapiAI/ios)
- [Python Client GitHub](https://github.com/VapiAI/python)

**Server SDKs:**

- [TypeScript SDK GitHub](https://github.com/VapiAI/server-sdk-typescript)
- [Python SDK GitHub](https://github.com/VapiAI/server-sdk-python)
- [Java SDK GitHub](https://github.com/VapiAI/server-sdk-java)
- [Ruby SDK GitHub](https://github.com/VapiAI/server-sdk-ruby)
- [C# SDK GitHub](https://github.com/VapiAI/server-sdk-csharp)
- [Go SDK GitHub](https://github.com/VapiAI/server-sdk-go)

**Documentation:**

- [API Reference](/api-reference)
- [Discord Community](https://discord.gg/pUFNcf2WmH)

---

title: Guides
subtitle: >-
Explore real-world, cloneable examples to build voice agents with Vapi. Now
including new Workflow-based guides!
slug: guides

---

<Frame>
  <img src="file:6bfb5d2f-3b24-4a00-bc21-1384a94c028b" alt="Vapi Guides" />
</Frame>

<CardGroup cols={2}>
  <Card title="Appointment Scheduling" icon="calendar-check" href="/workflows/examples/appointment-scheduling">
    <div className='absolute top-4 right-4'>
      <Icon icon="arrow-up-right-from-square" />
    </div>
    <div class="vapi-badge vapi-badge-workflow">Built with Workflows</div>
    <br />
    Build an appointment scheduling assistant that can schedule appointments for a barbershop
  </Card>
  <Card title="Medical Triage & Scheduling" icon="stethoscope" href="/workflows/examples/clinic-triage-scheduling">
    <div className='absolute top-4 right-4'>
      <Icon icon="arrow-up-right-from-square" />
    </div>
    <div class="vapi-badge vapi-badge-workflow">Built with Workflows</div>
    <br />
    Build a medical triage and scheduling assistant that can triage patients and schedule appointments for a clinic
  </Card>
  <Card title="Ecommerce Order Management" icon="shopping-cart" href="/workflows/examples/ecommerce-order-management">
    <div className='absolute top-4 right-4'>
      <Icon icon="arrow-up-right-from-square" />
    </div>
    <div class="vapi-badge vapi-badge-workflow">Built with Workflows</div>
    <br />
    Build an ecommerce order management assistant that can track orders and process returns
  </Card>
  <Card title="Property Management" icon="building" href="/workflows/examples/property-management">
    <div className='absolute top-4 right-4'>
      <Icon icon="arrow-up-right-from-square" />
    </div>
    <div class="vapi-badge vapi-badge-workflow">Built with Workflows</div>
    <br />
    Build a call routing workflow that dynamically routes tenant calls based on verification and inquiry type
  </Card>
  <Card title="Lead Qualification" icon="phone" href="/workflows/examples/lead-qualification">
    <div className='absolute top-4 right-4'>
      <Icon icon="arrow-up-right-from-square" />
    </div>
    <div class="vapi-badge vapi-badge-workflow">Built with Workflows</div>
    <br />
    Create an outbound sales agent that can schedule appointments automatically
  </Card>
    <Card title="Multilingual Support Workflow" icon="globe" href="/workflows/examples/multilingual-support">
    <div className='absolute top-4 right-4'>
      <Icon icon="arrow-up-right-from-square" />
    </div>
    <div class="vapi-badge vapi-badge-workflow">Built with Workflows</div>
    <br />
    Build a structured multilingual support workflow with language selection and dedicated conversation paths
  </Card>
  <Card title="Dynamic Multilingual Agent" icon="language" href="/assistants/examples/multilingual-agent">
    <div className='absolute top-4 right-4'>
      <Icon icon="arrow-up-right-from-square" />
    </div>
    <div class="vapi-badge vapi-badge-assistant">Built with Assistants</div>
    <br />
    Build a dynamic agent with automatic language detection and real-time language switching
  </Card>
  <Card title="Support Escalation" icon="headset" href="/assistants/examples/support-escalation">
    <div className='absolute top-4 right-4'>
      <Icon icon="arrow-up-right-from-square" />
    </div>
    <div class="vapi-badge vapi-badge-assistant">Built with Assistants</div>
    <br />
    Build an intelligent support escalation system with dynamic routing based on customer tier and issue complexity
  </Card>
  <Card title="Docs Agent" icon="book-open" href="/assistants/examples/docs-agent">
    <div className='absolute top-4 right-4'>
      <Icon icon="arrow-up-right-from-square" />
    </div>
    <div class="vapi-badge vapi-badge-assistant">Built with Assistants</div>
    <br />
    Build a docs agent that can answer questions about your documentation
  </Card>
  <Card title="Inbound Support" icon="headset" href="/assistants/examples/inbound-support">
    <div className='absolute top-4 right-4'>
      <Icon icon="arrow-up-right-from-square" />
    </div>
    <div class="vapi-badge vapi-badge-assistant">Built with Assistants</div>
    <br />
    Build a technical support assistant that remembers where you left off between calls
  </Card>
  <Card title="Voice Widget" icon="microphone" href="/assistants/examples/voice-widget">
    <div className='absolute top-4 right-4'>
      <Icon icon="arrow-up-right-from-square" />
    </div>
    <div class="vapi-badge vapi-badge-assistant">Built with Assistants</div>
    <br />
    Easily integrate the Vapi Voice Widget into your website for enhanced user interaction
  </Card>
  <Card title="Vapi CLI" icon="terminal" href="/cli">
    <div className='absolute top-4 right-4'>
      <Icon icon="arrow-up-right-from-square" />
    </div>
    <div class="vapi-badge" style="background-color: #0e0e13; color: #12a594;">Developer Tool</div>
    <br />
    Build voice AI agents faster with the Vapi CLI - project integration, local testing, and IDE enhancement
  </Card>

</CardGroup>

---

title: Vapi CLI
description: Command-line interface for building voice AI applications faster
slug: cli

---

## Overview

The Vapi CLI is the official command-line interface that brings world-class developer experience to your terminal and IDE. Build, test, and deploy voice AI applications without leaving your development environment.

**In this guide, you'll learn to:**

- Install and authenticate with the Vapi CLI
- Initialize Vapi in existing projects
- Manage assistants, phone numbers, and workflows from your terminal
- Forward webhooks to your local development server
- Turn your IDE into a Vapi expert with MCP integration

## Installation

Install the Vapi CLI in seconds with our automated scripts:

<Tabs>
  <Tab title="macOS/Linux">
    ```bash
    curl -sSL https://vapi.ai/install.sh | bash
    ```
  </Tab>
  <Tab title="Windows">
    ```powershell
    iex ((New-Object System.Net.WebClient).DownloadString('https://vapi.ai/install.ps1'))
    ```
  </Tab>
  <Tab title="Docker">
    ```bash
    docker run -it ghcr.io/vapiai/cli:latest --help
    ```
  </Tab>
</Tabs>

## Quick start

<Steps>
  <Step title="Authenticate">
    Connect your Vapi account:
    ```bash
    vapi login
    ```
    This opens your browser for secure OAuth authentication.
  </Step>
  
  <Step title="Initialize your project">
    Add Vapi to an existing project:
    ```bash
    vapi init
    ```
    The CLI auto-detects your tech stack and sets up everything you need.
  </Step>
  
  <Step title="Create your first assistant">
    Build a voice assistant:
    ```bash
    vapi assistant create
    ```
    Follow the interactive prompts to configure your assistant.
  </Step>
</Steps>

## Key features

### 🚀 Project integration

Drop Vapi into any existing codebase with intelligent auto-detection:

```bash
vapi init
# Detected: Next.js application
# ✓ Installed @vapi-ai/web SDK
# ✓ Generated components/VapiButton.tsx
# ✓ Created pages/api/vapi/webhook.ts
# ✓ Added environment template
```

Supports React, Vue, Next.js, Python, Go, Flutter, React Native, and dozens more frameworks.

### 🤖 MCP integration

Turn your IDE into a Vapi expert with Model Context Protocol:

```bash
vapi mcp setup
```

Your IDE's AI assistant (Cursor, Windsurf, VSCode) gains complete, accurate knowledge of Vapi's APIs and best practices. No more hallucinated code or outdated examples.

### 🔗 Local webhook testing

Forward webhooks to your local server for debugging:

```bash
# Terminal 1: Create tunnel (e.g., with ngrok)
ngrok http 4242

# Terminal 2: Forward webhooks
vapi listen --forward-to localhost:3000/webhook
```

<Note>
**Important:** `vapi listen` is a local forwarder only - it does NOT provide a public URL. You need a separate tunneling service (like ngrok) to expose the CLI's port to the internet. Update your webhook URLs in Vapi to use the tunnel's public URL.
</Note>

### 🔐 Multi-account management

Switch between organizations and environments seamlessly:

```bash
# List all authenticated accounts
vapi auth status

# Switch between accounts
vapi auth switch production

# Add another account
vapi auth login
```

### 📱 Complete feature parity

Everything you can do in the dashboard, now in your terminal:

- **Assistants**: Create, update, list, and delete voice assistants
- **Phone numbers**: Purchase, configure, and manage phone numbers
- **Calls**: Make outbound calls and view call history
- **Workflows**: Manage conversation flows (visual editing in dashboard)
- **Campaigns**: Create and manage AI phone campaigns at scale
- **Tools**: Configure custom functions and integrations
- **Webhooks**: Set up and test event delivery
- **Logs**: View system logs, call logs, and debug issues

## Common commands

<AccordionGroup>
  <Accordion title="Assistant management">
    ```bash
    # List all assistants
    vapi assistant list
    
    # Create a new assistant
    vapi assistant create
    
    # Get assistant details
    vapi assistant get <assistant-id>
    
    # Update an assistant
    vapi assistant update <assistant-id>
    
    # Delete an assistant
    vapi assistant delete <assistant-id>
    ```
  </Accordion>
  
  <Accordion title="Phone number management">
    ```bash
    # List your phone numbers
    vapi phone list
    
    # Purchase a new number
    vapi phone create
    
    # Update number configuration
    vapi phone update <phone-number-id>
    
    # Release a number
    vapi phone delete <phone-number-id>
    ```
  </Accordion>
  
  <Accordion title="Call operations">
    ```bash
    # List recent calls
    vapi call list
    
    # Make an outbound call
    vapi call create
    
    # Get call details
    vapi call get <call-id>
    
    # End an active call
    vapi call end <call-id>
    ```
  </Accordion>
  
  <Accordion title="Debugging and logs">
    ```bash
    # View system logs
    vapi logs list
    
    # View call-specific logs
    vapi logs calls <call-id>
    
    # View error logs
    vapi logs errors
    
    # View webhook logs
    vapi logs webhooks
    ```
  </Accordion>
</AccordionGroup>

## Configuration

The CLI stores configuration in `~/.vapi-cli.yaml`. You can also use environment variables:

```bash
# Set API key via environment
export VAPI_API_KEY=your-api-key

# View current configuration
vapi config get

# Update configuration
vapi config set <key> <value>

# Manage analytics preferences
vapi config analytics disable
```

## Auto-updates

The CLI automatically checks for updates and notifies you when new versions are available:

```bash
# Check for updates manually
vapi update check

# Update to latest version
vapi update
```

## Next steps

Now that you have the Vapi CLI installed:

- **[Initialize a project](/cli/init):** Add Vapi to your existing codebase
- **[Set up MCP](/cli/mcp):** Enhance your IDE with Vapi intelligence
- **[Test webhooks locally](/cli/webhook):** Debug webhooks with tunneling services
- **[Manage authentication](/cli/auth):** Work with multiple accounts

---

**Resources:**

- [GitHub Repository](https://github.com/VapiAI/cli)
- [Report Issues](https://github.com/VapiAI/cli/issues)
- [Discord Community](https://discord.gg/vapi)

---

title: Transient vs permanent configurations
subtitle: Learn to choose between inline and stored assistant configurations
slug: assistants/concepts/transient-vs-permanent-configurations

---

## Overview

Choose between **transient** (inline) and **permanent** (stored) configurations to optimize your Vapi implementation for flexibility, reusability, and management needs.

**In this guide, you'll learn to:**

- Understand when to use transient vs permanent configurations
- Implement both approaches with practical examples
- Apply best practices for each configuration type

## Key differences

| Aspect               | Transient                       | Permanent                            |
| -------------------- | ------------------------------- | ------------------------------------ |
| **Definition**       | Complete JSON in API request    | ID reference to stored configuration |
| **Storage**          | Exists only during API call     | Stored on Vapi servers               |
| **Reusability**      | Defined per request             | Reusable across multiple calls       |
| **Dashboard access** | Not visible                     | Visible and manageable               |
| **Best for**         | Dynamic, personalized scenarios | Shared, reusable setups              |

## Transient configurations

Use **transient configurations** when you need dynamic, call-specific behavior without pre-creating stored configurations.

### When to use transient

<CardGroup cols={2}>
  <Card title="Dynamic personalization" icon="user">
    **Best for:** Customer-specific data Embed user information directly in
    system messages
  </Card>
  <Card title="A/B testing" icon="flask">
    **Best for:** Configuration experiments Test different setups without
    permanent storage
  </Card>
  <Card title="Temporary campaigns" icon="calendar">
    **Best for:** Short-term promotions Event-specific assistants that don't
    need persistence
  </Card>
  <Card title="Development testing" icon="code">
    **Best for:** Rapid prototyping Iterate quickly without managing stored
    configs
  </Card>
</CardGroup>

### Customer service with pre-filled data

<CodeBlocks>
```json title="Transient assistant"
{
  "assistant": {
    "name": "Customer Service Agent",
    "model": {
      "provider": "openai",
      "model": "gpt-4o",
      "messages": [
        {
          "role": "system",
          "content": "You are a customer service representative for Acme Corp. The customer's name is John Smith and their account status is premium. Provide personalized assistance based on their business account history."
        }
      ],
      "temperature": 0.7
    },
    "voice": {
      "provider": "11labs",
      "voiceId": "N2lVS1w4EtoT3dr4eOWO"
    },
    "firstMessage": "Hello John, I see you're calling about your business account. How can I help you today?"
  }
}
```
```bash title="Create call with transient assistant"
curl -X POST "https://api.vapi.ai/call" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "phoneNumberId": "your-phone-number-id",
    "customer": {
      "number": "+1234567890"
    },
    "assistant": {
      "name": "Personalized Sales Agent",
      "model": {
        "provider": "openai",
        "model": "gpt-4",
        "messages": [
          {
            "role": "system",
            "content": "You are calling John about their interest in Enterprise Solution. Their budget is $5000."
          }
        ]
      },
      "voice": {
        "provider": "11labs",
        "voiceId": "N2lVS1w4EtoT3dr4eOWO"
      },
      "firstMessage": "Hi John, this is Sarah from Acme Corp calling about Enterprise Solution. Do you have a moment to chat?"
    }
  }'
```
</CodeBlocks>

### A/B testing scenario

<CodeBlocks>
```json title="Variant A - Enthusiastic approach"
{
  "assistant": {
    "name": "A/B Test Assistant - Variant A",
    "model": {
      "provider": "openai",
      "model": "gpt-4",
      "messages": [
        {
          "role": "system",
          "content": "You are an enthusiastic sales representative. Use upbeat language and emphasize benefits."
        }
      ],
      "temperature": 0.9
    },
    "voice": {
      "provider": "11labs",
      "voiceId": "energetic-voice-id"
    },
    "firstMessage": "Hey there! Exciting news - I'd love to tell you about our amazing new features!",
    "analysisPlan": {
      "summaryPrompt": "Rate the customer's engagement level and interest in the product on a scale of 1-10.",
      "structuredDataPlan": {
        "enabled": true,
        "schema": {
          "type": "object",
          "properties": {
            "engagement_score": { "type": "number" },
            "interest_level": {
              "type": "string",
              "enum": ["high", "medium", "low"]
            },
            "conversion_likelihood": { "type": "number" }
          }
        }
      }
    }
  }
}
```
```json title="Variant B - Professional approach"
{
  "assistant": {
    "name": "A/B Test Assistant - Variant B",
    "model": {
      "provider": "openai",
      "model": "gpt-4",
      "messages": [
        {
          "role": "system",
          "content": "You are a professional sales consultant. Use formal language and focus on business value."
        }
      ],
      "temperature": 0.3
    },
    "voice": {
      "provider": "11labs",
      "voiceId": "professional-voice-id"
    },
    "firstMessage": "Good afternoon. I'm calling to discuss how our enterprise solutions can benefit your organization.",
    "analysisPlan": {
      "summaryPrompt": "Rate the customer's engagement level and interest in the product on a scale of 1-10.",
      "structuredDataPlan": {
        "enabled": true,
        "schema": {
          "type": "object",
          "properties": {
            "engagement_score": { "type": "number" },
            "interest_level": {
              "type": "string",
              "enum": ["high", "medium", "low"]
            },
            "conversion_likelihood": { "type": "number" }
          }
        }
      }
    }
  }
}
```
</CodeBlocks>

### Transient tools

Create custom tools for specific integrations or workflows:

<CodeBlocks>
```json title="Customer-specific function tool"
{
  "tools": [
    {
      "type": "function",
      "name": "check_inventory",
      "description": "Check product inventory for the customer's specific region",
      "parameters": {
        "type": "object",
        "properties": {
          "productId": {
            "type": "string",
            "description": "The product ID to check"
          },
          "region": {
            "type": "string",
            "description": "Customer's region code"
          }
        },
        "required": ["productId", "region"]
      },
      "server": {
        "url": "https://api.customer-integration.com/inventory",
        "secret": "customer-webhook-secret",
        "timeoutSeconds": 30
      }
    }
  ]
}
```
```json title="Context-specific transfer tool"
{
  "tools": [
    {
      "type": "transferCall",
      "destinations": [
        {
          "type": "assistant",
          "assistantName": "technical-support",
          "description": "Transfer to technical support specialist",
          "message": "Let me connect you with our technical team who can better assist with your technical question."
        },
        {
          "type": "number",
          "number": "+1234567890",
          "description": "Emergency escalation line",
          "message": "Transferring you to our priority support team."
        }
      ]
    }
  ]
}
```
</CodeBlocks>

<Warning>
  **Transient limitations:** Configurations exist only during the API call and
  cannot be managed through the dashboard or reused across calls.
</Warning>

## Permanent configurations

Use **permanent configurations** for reusable setups that multiple teams can access and manage through the dashboard.

### When to use permanent

<CardGroup cols={2}>
  <Card title="Shared resources" icon="users">
    **Best for:** Team collaboration Assistants used across multiple departments
  </Card>
  <Card title="Dashboard management" icon="cog">
    **Best for:** Non-technical users Visual configuration management
  </Card>
  <Card title="Reusable setups" icon="refresh">
    **Best for:** Standard workflows Consistent configurations across calls
  </Card>
  <Card title="Version control" icon="git-branch">
    **Best for:** Change tracking Maintain configuration history
  </Card>
</CardGroup>

### Creating permanent configurations

<Steps>
  <Step title="Create the assistant">
    Store your assistant configuration on Vapi servers
  </Step>
  <Step title="Get the assistant ID">
    Use the returned UUID to reference the assistant
  </Step>
  <Step title="Reference in API calls">
    Use the ID instead of inline configuration
  </Step>
</Steps>

<CodeBlocks>
```bash title="Create permanent assistant"
curl -X POST "https://api.vapi.ai/assistant" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "General Support Assistant",
    "model": {
      "provider": "openai",
      "model": "gpt-4",
      "messages": [
        {
          "role": "system",
          "content": "You are a helpful customer service representative for Acme Corp. Provide accurate information about our products and services."
        }
      ]
    },
    "voice": {
      "provider": "11labs",
      "voiceId": "N2lVS1w4EtoT3dr4eOWO"
    },
    "firstMessage": "Hello! Thank you for calling Acme Corp. How can I assist you today?"
  }'
```
```bash title="Create permanent tool"
curl -X POST "https://api.vapi.ai/tool" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "function",
    "name": "update_crm_contact",
    "description": "Update contact information in the CRM system",
    "parameters": {
      "type": "object",
      "properties": {
        "contactId": {
          "type": "string",
          "description": "CRM contact ID"
        },
        "updates": {
          "type": "object",
          "description": "Fields to update"
        }
      },
      "required": ["contactId", "updates"]
    },
    "server": {
      "url": "https://api.yourcrm.com/contacts/update",
      "secret": "your-webhook-secret"
    }
  }'
```
```bash title="Use permanent configurations"
curl -X POST "https://api.vapi.ai/call" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "phoneNumberId": "your-phone-number-id",
    "customer": {
      "number": "+1234567890"
    },
    "assistantId": "your-assistant-id",
    "assistantOverrides": {
      "toolIds": ["tool-id-1", "tool-id-2"],
      "variableValues": {
        "customerName": "John Smith",
        "accountId": "ACC123456"
      }
    }
  }'
```
</CodeBlocks>

## Mixed configurations

Combine transient and permanent configurations for maximum flexibility:

<CodeBlocks>
```json title="Squad with mixed configurations"
{
  "squad": [
    {
      "assistantId": "permanent-receptionist-assistant-id",
      "assistantDestinations": [
        {
          "type": "assistant",
          "assistantName": "technical-support"
        }
      ]
    },
    {
      "assistant": {
        "name": "technical-support",
        "model": {
          "provider": "openai",
          "model": "gpt-4",
          "messages": [
            {
              "role": "system",
              "content": "You are a technical support specialist for Enterprise Software. The customer has high priority issue."
            }
          ]
        },
        "voice": {
          "provider": "11labs",
          "voiceId": "technical-voice-id"
        }
      },
      "assistantDestinations": []
    }
  ]
}
```
```json title="Server message with transient assistant"
{
  "assistant": {
    "name": "Dynamic Inbound Handler",
    "model": {
      "provider": "openai",
      "model": "gpt-4",
      "messages": [
        {
          "role": "system",
          "content": "The caller is from West Coast calling during business hours. Adjust your approach accordingly."
        }
      ]
    },
    "voice": {
      "provider": "11labs",
      "voiceId": "appropriate-voice-for-region"
    },
    "firstMessage": "Hello! I see you're calling from West Coast. How can I help you today?"
  }
}
```
</CodeBlocks>

## Best practices

<AccordionGroup>
  <Accordion title="Choosing the right approach">
    **Use transient when:**
    - Customer data needs to be embedded in system messages
    - Testing different configurations temporarily
    - Creating user-specific personalizations
    - Rapid prototyping and development

    **Use permanent when:**
    - Multiple teams need access to the same configuration
    - Non-technical users manage configurations via dashboard
    - Consistency across multiple API calls is required
    - Version control and change tracking are important

  </Accordion>
  
  <Accordion title="Performance considerations">
    - **Transient:** Slightly larger request payloads but no additional API calls
    - **Permanent:** Smaller request payloads but requires initial creation calls
    - **Mixed:** Optimize by using permanent for stable configs, transient for dynamic parts
  </Accordion>
  
  <Accordion title="Security and access control">
    - **Transient:** Full configuration visible in API requests - avoid sensitive data
    - **Permanent:** Stored securely on Vapi servers with proper access controls
    - **Recommendation:** Use permanent configurations for sensitive integrations
  </Accordion>
</AccordionGroup>

## Limitations

<Tabs>
  <Tab title="Transient limitations">
    - **No persistence:** Cannot retrieve or reuse after API call - **No
    dashboard access:** Not visible in Vapi dashboard - **No version control:**
    Cannot track configuration changes - **Request size:** Larger payloads may
    impact performance
  </Tab>
  <Tab title="Permanent limitations">
    - **Setup overhead:** Requires separate creation API calls - **ID
    management:** Need to track and manage configuration UUIDs - **Update
    complexity:** Changes require additional API calls
  </Tab>
</Tabs>

## Next steps

Now that you understand transient vs permanent configurations:

- **[Assistant creation guide](/docs/assistants):** Learn to build and customize assistants
- **[Tool integration](/docs/tools):** Connect external services and functions
- **[Squad configuration](/docs/squads):** Set up multi-assistant workflows
- **[API reference](/fern/api-reference):** Explore all configuration options

---

title: Variables
subtitle: Personalize assistant messages with dynamic and default variables
slug: assistants/dynamic-variables

---

## Overview

Use dynamic variables in the system prompt or any message in the dashboard with double curly braces (e.g., `{{name}}`).

To set values, make a phone call request through the API and set `assistantOverrides`. You cannot set variable values directly in the dashboard.

For example, set the assistant's first message to "Hello, `{{name}}`!" and assign `name` to `John` by passing `assistantOverrides` with `variableValues`:

```json
{
  "variableValues": {
    "name": "John"
  }
}
```

## Using dynamic variables in a phone call

<Steps>

  <Step title="Prepare Your Request">

Create a JSON payload with these key-value pairs:

- **`assistantId`**: Replace `"your-assistant-id"` with your assistant's actual ID.
- **`assistantOverride`**: Customize your assistant's behavior.
  - **`variableValues`**: Include dynamic variables in the format `{ "variableName": "variableValue" }`. Example: `{ "name": "John" }`.
- **`customer`**: Represent the call recipient.
  - **`number`**: Replace `"+1xxxxxxxxxx"` with the recipient's phone number (E.164 format).
- **`phoneNumberId`**: Replace `"your-phone-id"` with your registered phone number's ID. Find it on the [Phone number](https://dashboard.vapi.ai/phone-numbers) page.

  </Step>

  <Step title="Send the Request">

Send the JSON payload to the `/call/phone` endpoint using your preferred method (e.g., HTTP POST request).

```json
{
  "assistantId": "your-assistant-id",
  "assistantOverrides": {
    "variableValues": {
      "name": "John"
    }
  },
  "customer": {
    "number": "+1xxxxxxxxxx"
  },
  "phoneNumberId": "your-phone-id"
}
```

  </Step>

</Steps>

<Note>
  Ensure `{{variableName}}` is included in all prompts where needed.
</Note>

## Default Variables

These variables are automatically filled based on the current (UTC) time, so you don't need to set them manually in `variableValues`:

| Variable              | Description                 | Example              |
| --------------------- | --------------------------- | -------------------- |
| `{{now}}`             | Current date and time (UTC) | Jan 1, 2024 12:00 PM |
| `{{date}}`            | Current date (UTC)          | Jan 1, 2024          |
| `{{time}}`            | Current time (UTC)          | 12:00 PM             |
| `{{month}}`           | Current month (UTC)         | January              |
| `{{day}}`             | Current day of month (UTC)  | 1                    |
| `{{year}}`            | Current year (UTC)          | 2024                 |
| `{{customer.number}}` | Customer's phone number     | +1xxxxxxxxxx         |
| `{{customer.X}}`      | Any other customer property |                      |

## Advanced date and time usage

You can use advanced date and time formatting in any prompt or message that supports dynamic variables in the dashboard or API. We use [LiquidJS](https://liquidjs.com/) for formatting - see their docs for details.

Format a date or time using the LiquidJS `date` filter:

```liquid
{{"now" | date: "%A, %B %d, %Y, %I:%M %p", "America/Los_Angeles"}}
```

Outputs: `Monday, January 01, 2024, 03:45 PM`

**Examples:**

- 24-hour time:
  ```liquid
  {{"now" | date: "%H:%M", "Europe/London"}}
  ```
  → `17:30`
- Day of week:
  ```liquid
  {{"now" | date: "%A"}}
  ```
  → `Tuesday`
- With customer number:
  ```liquid
  Hello, your number is {{customer.number}} and the time is {{"now" | date: "%I:%M %p", "America/New_York"}}
  ```

**Common formats:**

| Format String | Output       | Description       |
| ------------- | ------------ | ----------------- |
| `%Y-%m-%d`    | 2024-01-01   | Year-Month-Day    |
| `%I:%M %p`    | 03:45 PM     | Hour:Minute AM/PM |
| `%H:%M`       | 15:45        | 24-hour time      |
| `%A`          | Monday       | Day of week       |
| `%b %d, %Y`   | Jan 01, 2024 | Abbrev. Month Day |

```

## Using dynamic variables in the dashboard

To use dynamic variables in the dashboard, include them in your prompts or messages using double curly braces. For example:

```

Hello, {{name}}!

````

When you start a call, you must provide a value for each variable (like `name`) in the call configuration or via the API/SDK.

<Note>
Always use double curly braces (`{{variableName}}`) to reference dynamic variables in your prompts and messages.
</Note>
</rewritten_file>


---
title: Multilingual support
subtitle: Enable voice assistants to speak multiple languages fluently
slug: customization/multilingual
description: >-
  Configure multilingual voice AI agents with automatic language detection,
  cross-language conversation, and localized voices
---

## Overview

Configure your voice assistant to communicate in multiple languages with automatic language detection, native voice quality, and cultural context awareness.

**In this guide, you'll learn to:**
- Set up automatic language detection for speech recognition
- Configure multilingual voice synthesis
- Design language-aware system prompts
- Test and optimize multilingual performance

<Note>
**Multilingual Support:** Multiple providers support automatic language detection. **Deepgram** (Nova 2, Nova 3 with "Multi" setting) and **Google STT** (with "Multilingual" setting) both offer automatic language detection for seamless multilingual conversations.
</Note>

## Configure automatic language detection

Set up your transcriber to automatically detect and process multiple languages.

<Tabs>
  <Tab title="Dashboard">
    1. Navigate to **Assistants** in your [Vapi Dashboard](https://dashboard.vapi.ai/)
    2. Create a new assistant or edit an existing one
    3. In the **Transcriber** section:
       - **Provider**: Select `Deepgram` (recommended) or `Google`
       - **Model**: For Deepgram, choose `Nova 2` or `Nova 3`; for Google, choose `Latest`
       - **Language**: Set to `Multi` (Deepgram) or `Multilingual` (Google)
    4. **Other providers**: Single language only, no automatic detection
    5. Click **Save** to apply the configuration
  </Tab>
  <Tab title="TypeScript (Server SDK)">
    ```typescript
    import { VapiClient } from "@vapi-ai/server-sdk";

    const vapi = new VapiClient({ token: "YOUR_VAPI_API_KEY" });

    // Recommended: Deepgram for multilingual support
    const assistant = await vapi.assistants.create({
      name: "Multilingual Assistant",
      transcriber: {
        provider: "deepgram",
        model: "nova-2", // or "nova-3"
        language: "multi"
      }
    });

    // Alternative: Google for multilingual support
    const googleMultilingual = {
      provider: "google",
      model: "latest",
      language: "multilingual"
    };
    ```
  </Tab>
  <Tab title="Python (Server SDK)">
    ```python
    from vapi import Vapi
    import os

    client = Vapi(token=os.getenv("VAPI_API_KEY"))

    # Recommended: Deepgram for multilingual support
    assistant = client.assistants.create(
        name="Multilingual Assistant",
        transcriber={
            "provider": "deepgram",
            "model": "nova-2",  # or "nova-3"
            "language": "multi"
        }
    )

    # Alternative: Google for multilingual support
    google_multilingual = {
        "provider": "google",
        "model": "latest",
        "language": "multilingual"
    }
    ```
  </Tab>
  <Tab title="cURL">
    ```bash
    # Recommended: Deepgram for multilingual support
    curl -X POST "https://api.vapi.ai/assistant" \
         -H "Authorization: Bearer $VAPI_API_KEY" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Multilingual Assistant",
           "transcriber": {
             "provider": "deepgram",
             "model": "nova-2",
             "language": "multi"
           }
         }'

    # Alternative: Google for multilingual support
    curl -X POST "https://api.vapi.ai/assistant" \
         -H "Authorization: Bearer $VAPI_API_KEY" \
         -H "Content-Type: application/json" \
         -d '{
           "transcriber": {
             "provider": "google",
             "model": "latest",
             "language": "multilingual"
           }
         }'
    ```
  </Tab>
</Tabs>

<Note>
**Provider Performance:** **Deepgram** offers the best balance of speed and multilingual accuracy. **Google** provides broader language support but may be slower. Both providers support automatic language detection within conversations.
</Note>

## Set up multilingual voices

Configure your assistant to use appropriate voices for each detected language.

<Tabs>
  <Tab title="Dashboard">
    1. In the **Voice** section of your assistant:
       - **Provider**: Select `Azure` (best multilingual coverage)
       - **Voice**: Choose `multilingual-auto` for automatic voice selection
    2. **Alternative**: Configure specific voices for each language:
       - Select a primary voice (e.g., `en-US-AriaNeural`)
       - Click **Add Fallback Voices**
       - Add voices for other languages:
         - Spanish: `es-ES-ElviraNeural`
         - French: `fr-FR-DeniseNeural`
         - German: `de-DE-KatjaNeural`
    3. Click **Save** to apply the voice configuration
  </Tab>
  <Tab title="TypeScript (Server SDK)">
    ```typescript
    // Option 1: Automatic voice selection (recommended)
    const voice = {
      provider: "azure",
      voiceId: "multilingual-auto"
    };

    // Option 2: Specific voices with fallbacks
    const voiceWithFallbacks = {
      provider: "azure",
      voiceId: "en-US-AriaNeural", // Primary voice
      fallbackPlan: {
        voices: [
          { provider: "azure", voiceId: "es-ES-ElviraNeural" },
          { provider: "azure", voiceId: "fr-FR-DeniseNeural" },
          { provider: "azure", voiceId: "de-DE-KatjaNeural" }
        ]
      }
    };

    await vapi.assistants.update(assistantId, { voice });
    ```
  </Tab>
  <Tab title="Python (Server SDK)">
    ```python
    # Option 1: Automatic voice selection (recommended)
    voice = {
        "provider": "azure",
        "voiceId": "multilingual-auto"
    }

    # Option 2: Specific voices with fallbacks
    voice_with_fallbacks = {
        "provider": "azure",
        "voiceId": "en-US-AriaNeural",  # Primary voice
        "fallbackPlan": {
            "voices": [
                {"provider": "azure", "voiceId": "es-ES-ElviraNeural"},
                {"provider": "azure", "voiceId": "fr-FR-DeniseNeural"},
                {"provider": "azure", "voiceId": "de-DE-KatjaNeural"}
            ]
        }
    }

    client.assistants.update(assistant_id, voice=voice)
    ```
  </Tab>
  <Tab title="cURL">
    ```bash
    curl -X PATCH "https://api.vapi.ai/assistant/YOUR_ASSISTANT_ID" \
         -H "Authorization: Bearer $VAPI_API_KEY" \
         -H "Content-Type: application/json" \
         -d '{
           "voice": {
             "provider": "azure",
             "voiceId": "multilingual-auto"
           }
         }'
    ```
  </Tab>
</Tabs>

<Note>
**Voice Provider Support:** Unlike transcription, all major voice providers (Azure, ElevenLabs, OpenAI, etc.) support multiple languages. Azure offers the most comprehensive coverage with 400+ voices across 140+ languages.
</Note>

## Configure language-aware prompts

Create system prompts that explicitly list supported languages and handle multiple languages gracefully.

<Tabs>
  <Tab title="Dashboard">
    1. In the **Model** section, update your system prompt to explicitly list supported languages:
    ```
    You are a helpful assistant that can communicate in English, Spanish, and French.

    Language Instructions:
    - You can speak and understand: English, Spanish, and French
    - Automatically detect and respond in the user's language
    - Switch languages seamlessly when the user changes languages
    - Maintain consistent personality across all languages
    - Use culturally appropriate greetings and formality levels

    If a user speaks a language other than English, Spanish, or French, politely explain that you only support these three languages and ask them to continue in one of them.
    ```
    2. Click **Save** to apply the prompt changes
  </Tab>
  <Tab title="TypeScript (Server SDK)">
    ```typescript
    const systemPrompt = `You are a helpful assistant that can communicate in English, Spanish, and French.

Language Instructions:
- You can speak and understand: English, Spanish, and French
- Automatically detect and respond in the user's language
- Switch languages seamlessly when the user changes languages
- Maintain consistent personality across all languages
- Use culturally appropriate greetings and formality levels

If a user speaks a language other than English, Spanish, or French, politely explain that you only support these three languages and ask them to continue in one of them.`;

    const model = {
      provider: "openai",
      model: "gpt-4",
      messages: [
        {
          role: "system",
          content: systemPrompt
        }
      ]
    };

    await vapi.assistants.update(assistantId, { model });
    ```
  </Tab>
  <Tab title="Python (Server SDK)">
    ```python
    system_prompt = """You are a helpful assistant that can communicate in English, Spanish, and French.

Language Instructions:
- You can speak and understand: English, Spanish, and French
- Automatically detect and respond in the user's language
- Switch languages seamlessly when the user changes languages
- Maintain consistent personality across all languages
- Use culturally appropriate greetings and formality levels

If a user speaks a language other than English, Spanish, or French, politely explain that you only support these three languages and ask them to continue in one of them."""

    model = {
        "provider": "openai",
        "model": "gpt-4",
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            }
        ]
    }

    client.assistants.update(assistant_id, model=model)
    ```
  </Tab>
  <Tab title="cURL">
    ```bash
    curl -X PATCH "https://api.vapi.ai/assistant/YOUR_ASSISTANT_ID" \
         -H "Authorization: Bearer $VAPI_API_KEY" \
         -H "Content-Type: application/json" \
         -d '{
           "model": {
             "provider": "openai",
             "model": "gpt-4",
             "messages": [
               {
                 "role": "system",
                 "content": "You are a helpful assistant that can communicate in English, Spanish, and French..."
               }
             ]
           }
         }'
    ```
  </Tab>
</Tabs>

<Warning>
**Critical for Multilingual Success:** You must explicitly list the supported languages in your system prompt. Assistants struggle to understand they can speak multiple languages without this explicit instruction.
</Warning>

## Add multilingual greetings

Configure greeting messages that work across multiple languages.

<Tabs>
  <Tab title="Dashboard">
    1. In the **First Message** field, enter a multilingual greeting:
    ```
    Hello! I can assist you in English, Spanish, or French. How can I help you today?
    ```
    2. **Optional**: For more personalized greetings, use the **Advanced Message Configuration**:
       - Enable **Language-Specific Messages**
       - Add greetings for each target language
    3. Click **Save** to apply the greeting
  </Tab>
  <Tab title="TypeScript (Server SDK)">
    ```typescript
    // Simple multilingual greeting
    const firstMessage = "Hello! I can assist you in English, Spanish, or French. How can I help you today?";

    // Language-specific greetings (advanced)
    const multilingualGreeting = {
      contents: [
        {
          type: "text",
          text: "Hello! How can I help you today?",
          language: "en"
        },
        {
          type: "text",
          text: "¡Hola! ¿Cómo puedo ayudarte hoy?",
          language: "es"
        },
        {
          type: "text",
          text: "Bonjour! Comment puis-je vous aider?",
          language: "fr"
        }
      ]
    };

    await vapi.assistants.update(assistantId, { firstMessage });
    ```
  </Tab>
  <Tab title="Python (Server SDK)">
    ```python
    # Simple multilingual greeting
    first_message = "Hello! I can assist you in English, Spanish, or French. How can I help you today?"

    # Language-specific greetings (advanced)
    multilingual_greeting = {
        "contents": [
            {
                "type": "text",
                "text": "Hello! How can I help you today?",
                "language": "en"
            },
            {
                "type": "text",
                "text": "¡Hola! ¿Cómo puedo ayudarte hoy?",
                "language": "es"
            },
            {
                "type": "text",
                "text": "Bonjour! Comment puis-je vous aider?",
                "language": "fr"
            }
        ]
    }

    client.assistants.update(assistant_id, first_message=first_message)
    ```
  </Tab>
  <Tab title="cURL">
    ```bash
    curl -X PATCH "https://api.vapi.ai/assistant/YOUR_ASSISTANT_ID" \
         -H "Authorization: Bearer $VAPI_API_KEY" \
         -H "Content-Type: application/json" \
         -d '{
           "firstMessage": "Hello! I can assist you in English, Spanish, or French. How can I help you today?"
         }'
    ```
  </Tab>
</Tabs>

## Test your multilingual assistant

Validate your configuration with different languages and scenarios.

<Tabs>
  <Tab title="Dashboard">
    1. Use the **Test Assistant** feature in your dashboard
    2. Test these scenarios:
       - Start conversations in different languages
       - Switch languages mid-conversation
       - Use mixed-language input
    3. Monitor the **Call Analytics** for:
       - Language detection accuracy
       - Voice quality consistency
       - Response appropriateness
    4. Adjust configuration based on test results
  </Tab>
  <Tab title="TypeScript (Server SDK)">
    ```typescript
    // Create test call
    const testCall = await vapi.calls.create({
      assistantId: "your-multilingual-assistant-id",
      customer: {
        number: "+1234567890"
      }
    });

    // Monitor call events
    vapi.on('call-end', (event) => {
      console.log('Language detection results:', event.transcript);
      console.log('Call summary:', event.summary);
    });
    ```
  </Tab>
  <Tab title="Python (Server SDK)">
    ```python
    # Create test call
    test_call = client.calls.create(
        assistant_id="your-multilingual-assistant-id",
        customer={
            "number": "+1234567890"
        }
    )

    # Retrieve call details for analysis
    call_details = client.calls.get(test_call.id)
    print(f"Language detection: {call_details.transcript}")
    ```
  </Tab>
  <Tab title="cURL">
    ```bash
    # Create test call
    curl -X POST "https://api.vapi.ai/call" \
         -H "Authorization: Bearer $VAPI_API_KEY" \
         -H "Content-Type: application/json" \
         -d '{
           "assistantId": "your-multilingual-assistant-id",
           "customer": {
             "number": "+1234567890"
           }
         }'
    ```
  </Tab>
</Tabs>

## Provider capabilities (Accurate as of testing)

### Speech Recognition (Transcription)

| Provider | Multilingual Support | Languages | Notes |
|----------|---------------------|-----------|-------|
| **Deepgram** | ✅ Full auto-detection | 100+ | **Recommended**: Nova 2/Nova 3 with "Multi" language setting |
| **Google STT** | ✅ Full auto-detection | 125+ | Latest models with "Multilingual" language setting |
| **Assembly AI** | ❌ English only | English | No multilingual support |
| **Azure STT** | ❌ Single language | 100+ | Many languages, but no auto-detection |
| **OpenAI Whisper** | ❌ Single language | 90+ | Many languages, but no auto-detection |
| **Gladia** | ❌ Single language | 80+ | Many languages, but no auto-detection |
| **Speechmatics** | ❌ Single language | 50+ | Many languages, but no auto-detection |
| **Talkscriber** | ❌ Single language | 40+ | Many languages, but no auto-detection |

### Voice Synthesis (Text-to-Speech)

| Provider | Languages | Multilingual Voice Selection | Best For |
|----------|-----------|------------------------------|----------|
| **Azure** | 140+ | ✅ Automatic | Maximum language coverage |
| **ElevenLabs** | 30+ | ✅ Automatic | Premium voice quality |
| **OpenAI TTS** | 50+ | ✅ Automatic | Consistent quality across languages |
| **PlayHT** | 80+ | ✅ Automatic | Cost-effective scaling |

## Common challenges and solutions

<AccordionGroup>
  <Accordion title="Language detection is inaccurate">
    **Solutions:**
    - Use Deepgram (Nova 2/Nova 3 with "Multi") or Google STT (with "Multilingual")
    - Ensure high-quality audio input for better detection accuracy
    - Test with native speakers of target languages
    - Consider provider-specific language combinations for optimal results
  </Accordion>

  <Accordion title="Assistant doesn't realize it can speak multiple languages">
    **Solutions:**
    - **Explicitly list all supported languages** in your system prompt
    - Include language capabilities in the assistant's instructions
    - Test the prompt with multilingual conversations
    - Avoid generic "multilingual" statements without specifics
  </Accordion>

  <Accordion title="Transcription is too slow">
    **Solutions:**
    - Use Deepgram Nova 2/Nova 3 for optimal speed and multilingual support
    - For Google STT, use latest models for better performance
    - Consider the speed vs accuracy tradeoff for your use case
    - Optimize audio quality and format to improve processing speed
  </Accordion>

  <Accordion title="Voice quality varies between languages">
    **Solutions:**
    - Test different voice providers for each language
    - Use Azure for maximum language coverage
    - Configure fallback voices as backup options
    - Consider premium providers for key languages
  </Accordion>
</AccordionGroup>

## Next steps

Now that you have multilingual support configured:

- **[Build a complete multilingual agent](../assistants/examples/multilingual-agent):** Follow our step-by-step implementation guide
- **[Custom voices](custom-voices/custom-voice):** Set up region-specific custom voices
- **[System prompting](../prompting-guide):** Design effective multilingual prompts
- **[Call analysis](../call-analysis):** Monitor language performance and usage


---
title: Personalization with user information
subtitle: Add customer-specific information to your voice assistant conversations
slug: assistants/personalization
---

## Overview

Personalization lets you include customer-specific information in your voice assistant conversations. When a customer calls, your server can provide data about that customer, which is then used to tailor the conversation in real time.

This approach is ideal for use cases like customer support, account management, or any scenario where the assistant should reference details unique to the caller.

## How Personalization Works

<Steps>
  <Step title="Customer Calls Your Number">
    When a call comes in, Vapi sends a request to your server instead of using a fixed assistant configuration.
  </Step>

  <Step title="Your Server Looks Up the Caller">
    Your server receives the request, identifies the caller (for example, by phone number), and fetches relevant customer data from your database or CRM.
  </Step>

  <Step title="Your Server Responds with Assistant Details">
    Your server responds to Vapi with either:
    - An existing assistant ID and a set of dynamic variables to personalize the conversation, or
    - A complete assistant configuration, with customer data embedded directly in the prompts or instructions.
  </Step>

  <Step title="Vapi Handles the Call">
    Vapi uses the personalized assistant configuration or variables to guide the conversation, referencing the customer's information as needed.
  </Step>
</Steps>

## Prerequisites

- A Vapi phone number
- A created Vapi Assistant
- A server endpoint to receive Vapi's requests

## Implementation

<Steps>
  <Step title="Add Dynamic Variables to Your Assistant">
    Use variable placeholders in your assistant's instructions or messages with the `{{variable_name}}` syntax.

    Example:
    `"Hello {{customerName}}! I see you've been a {{accountType}} customer since {{joinDate}}."`
  </Step>

  <Step title="Configure Your Phone Number to Use Your Server">
    Update your phone number so that Vapi sends incoming call events to your server, rather than using a static assistant.

    ```json
    PATCH /phone-number/{id}
    {
      "assistantId": null,
      "squadId": null,
      "server": {
        "url": "https://your-server.com/api/assistant-selector"
      }
    }
    ```

    <Note>
      Your server must respond within 7.5 seconds, or the call will fail.
    </Note>
  </Step>

  <Step title="Implement Your Server Endpoint">
    Your server should handle POST requests from Vapi and return either:

    **Option 1: Use an Existing Assistant with Dynamic Variables**

    ```javascript
    app.post("/api/assistant-selector", async (req, res) => {
      if (req.body.message?.type === "assistant-request") {
        const phoneNumber = req.body.call.from.phoneNumber;
        const customer = await crmAPI.getCustomerByPhone(phoneNumber);

        res.json({
          assistantId: "asst_customersupport",
          assistantOverrides: {
            variableValues: {
              customerName: customer.name,
              accountType: customer.tier,
              joinDate: customer.createdAt
            }
          }
        });
      }
    });
    ```

    **Option 2: Return a Complete Assistant Configuration**

    ```javascript
    app.post("/api/assistant-selector", async (req, res) => {
      if (req.body.message?.type === "assistant-request") {
        const phoneNumber = req.body.call.from.phoneNumber;
        const customer = await crmAPI.getCustomerByPhone(phoneNumber);

        res.json({
          assistant: {
            name: "Dynamic Customer Support Assistant",
            model: {
              provider: "openai",
              model: "gpt-4o",
              messages: [{
                role: "system",
                content: `You are helping ${customer.name}, a ${customer.tier} member since ${customer.createdAt}.`
              }]
            },
            voice: {
              provider: "11labs",
              voiceId: "shimmer"
            }
          }
        });
      }
    });
    ```
  </Step>
</Steps>

## Error Handling

If your server encounters an error or cannot find the customer, return a response like this to end the call with a spoken message:

```json
{
  "error": "Unable to find customer record. Please try again later."
}
````

## Common Issues

<Note>
- Use the exact `{{variable_name}}` syntax for variables in your assistant configuration.
- Your server must respond within 7.5 seconds.
- Implement fallbacks for missing or incomplete customer data.
- Ensure your endpoint is highly available to avoid missed calls.
</Note>

---

title: Voice formatting plan
subtitle: Format LLM output for natural-sounding speech
slug: assistants/voice-formatting-plan

---

## Overview

Voice formatting automatically transforms raw text from your language model (LLM) into a format that sounds natural when spoken by a text-to-speech (TTS) provider. This process—called **Voice Input Formatted**—is enabled by default for all assistants.

Formatting helps with things like:

- Expanding numbers and currency (e.g., `$42.50` → "forty two dollars and fifty cents")
- Expanding abbreviations (e.g., `ST` → "STREET")
- Spacing out phone numbers (e.g., `123-456-7890` → "1 2 3 4 5 6 7 8 9 0")

You can turn off formatting if you want the TTS to read the raw LLM output.

## How voice input formatting works

When enabled, the formatter runs a series of transformations on your text, each handled by a specific function. Here's the order and what each function does:

| **Step** | **Function Name**                                                           | **Description**                                                                                                           | **Before**                            | **After**                                                                 | **Default** | **Precedence** |
| :------- | :-------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------ | :------------------------------------ | :------------------------------------------------------------------------ | :---------- | :------------- |
| 1        | `removeAngleBracketContent`                                                 | Removes anything within `<...>`, except for `<break>`, `<spell>`, or double angle brackets `<< >>`.                       | `Hello <tag> world`                   | `Hello  world`                                                            | ✅          | -              |
| 2        | `removeMarkdownSymbols`                                                     | Removes markdown symbols like `_`, `` ` ``, and `~`. Asterisks (`*`) are preserved in this step.                          | `**Wanted** to say *hi*`              | `**Wanted** to say *hi*`                                                  | ✅          | 0              |
| 3        | `removePhrasesInAsterisks`                                                  | Removes text surrounded by single or double asterisks.                                                                    | `**Wanted** to say *hi*`              | ` to say`                                                                 | ❌          | 0              |
| 4        | `replaceNewLinesWithPeriods`                                                | Converts new lines (`\n`) to periods for smoother speech.                                                                 | `Hello  world\n to say\nWe have NASA` | `Hello  world .  to say . We have NASA`                                   | ✅          | 0              |
| 5        | `replaceColonsWithPeriods`                                                  | Replaces `:` with `.` for better phrasing.                                                                                | `price: $42.50`                       | `price. $42.50`                                                           | ✅          | 0              |
| 6        | `formatAcronyms`                                                            | Converts known acronyms to lowercase (e.g., NASA → nasa) or spaces out unknown all-caps words unless they contain vowels. | `NASA and .NET`                       | `nasa and .net`                                                           | ✅          | 0              |
| 7        | `formatDollarAmounts`                                                       | Converts currency amounts to spoken words.                                                                                | `$42.50`                              | `forty two dollars and fifty cents`                                       | ✅          | 0              |
| 8        | `formatEmails`                                                              | Replaces `@` with "at" and `.` with "dot" in emails.                                                                      | `JOHN.DOE@example.COM`                | `JOHN dot DOE at example dot COM`                                         | ✅          | 0              |
| 9        | `formatDates`                                                               | Converts date strings into spoken date format.                                                                            | `2023 05 10`                          | `Wednesday, May 10, 2023`                                                 | ✅          | 0              |
| 10       | `formatTimes`                                                               | Expands or simplifies time expressions.                                                                                   | `14:00`                               | `14`                                                                      | ✅          | 0              |
| 11       | `formatDistances`, `formatUnits`, `formatPercentages`, `formatPhoneNumbers` | Converts units, distances, percentages, and phone numbers into spoken words.                                              | `5km`, `43 lb`, `50%`, `123-456-7890` | `5 kilometers`, `forty three pounds`, `50 percent`, `1 2 3 4 5 6 7 8 9 0` | ✅          | 0              |
| 12       | `formatNumbers`                                                             | Formats general numbers: years read as digits, large numbers spelled out, negative and decimal numbers clarified.         | `-9`, `2.5`, `2023`                   | `minus nine`, `two point five`, `2023`                                    | ✅          | 0              |
| 13       | `removeAsterisks`                                                           | Removes all asterisk characters from the text.                                                                            | `**Bold** and *italic*`               | `Bold and italic`                                                         | ✅          | 1              |
| 14       | `Applying Replacements`                                                     | Applies user-defined final replacements like expanding street abbreviations.                                              | `320 ST 21 RD`                        | `320 STREET 21 ROAD`                                                      | ✅          | -              |

---

## Customizing the formatting plan

You can control some aspects of formatting:

### Enabled

Formatting is on by default. To disable, set:

```js
voice.chunkPlan.formatPlan.enabled = false;
```

### Number-to-digits cutoff

Controls when numbers are read as digits instead of words.

- **Default:** `2025` (current year)
- Example: With a cutoff of `2025`, numbers above this are read as digits.
- To spell out larger numbers, set the cutoff higher (e.g., `300000`).

### Replacements

Add exact or regex-based substitutions to customize output.

- **Example 1:** Replace `hello` with `hi`:
  ```js
  { type: 'exact', key: 'hello', value: 'hi' }
  ```
- **Example 2:** Replace words matching a pattern:
  ```js
  { type: 'regex', regex: '\b[a-zA-Z]{5}\b', value: 'hi' }
  ```

<Note>
Currently, only replacements and the number-to-digits cutoff are customizable. Other options are not exposed.
</Note>

---

## Turning formatting off

To disable all formatting and use raw LLM output, set either of these to `false`:

```js
voice.chunkPlan.enabled = false;
// or
voice.chunkPlan.formatPlan.enabled = false;
```

---

## Summary

- Voice input formatting improves clarity and naturalness for TTS.
- Each transformation step targets a specific pattern for better speech output.
- You can customize or disable formatting as needed.

---

title: Flush syntax
subtitle: Control voice transmission timing for responsive conversations
slug: assistants/flush-syntax
description: >-
Force immediate voice transmission with VAPI's flush syntax for real-time
interactions

---

## Overview

The flush syntax is a VAPI audio control token that forces immediate transmission of LLM output to voice providers, eliminating buffering delays for real-time voice interactions.

**When to use flush syntax:**

- Acknowledge user requests immediately during processing
- Provide feedback during long-running tool executions
- Create natural conversation pauses
- Support custom LLM integrations with processing delays

<Tip>
  Use flush strategically—overuse can cause audio fragmentation and degrade
  conversation quality.
</Tip>

## How it works

The flush syntax bypasses normal buffering to provide immediate audio feedback:

1. **Detection**: VAPI scans LLM output for flush syntax using regex pattern
2. **Split**: Text is divided at the flush position
3. **Immediate Send**: Content before flush is sent instantly to voice provider
4. **Continue**: Remaining text follows normal buffering

<CodeBlocks>
```typescript title="Processing Example"
const { sendToTTS, flush, remainingBuffer } = ttsBuffer(buffer, voice);
if (sendToTTS.length > 0) {
  pushBuffer(sendToTTS, flush); // flush=true triggers immediate send
  buffer = remainingBuffer;
}
```
```python title="Conceptual Flow"
# 1. LLM generates: "I'm processing your request... <flush /> Here's the result"
# 2. VAPI detects flush syntax
# 3. Sends "I'm processing your request..." immediately to voice
# 4. Continues with "Here's the result" using normal buffering
```
</CodeBlocks>

## Syntax formats

VAPI supports three flush formats with case-insensitive matching:

<CodeBlocks>
  ```html title="Self-closing (Recommended)"
  <flush />
  ``` ```html title="Opening tag"
  <flush>``` ```html title="Closing tag"</flush>
  ```
</CodeBlocks>

<Note>
All formats use regex pattern `/<\s*flush\s*\/?>|<\s*\/\s*flush\s*>/i` allowing whitespace variations.
</Note>

## Configuration requirements

Flush syntax requires proper voice configuration:

<CodeBlocks>
```json title="Assistant Configuration"
{
  "voice": {
    "chunkPlan": {
      "enabled": true  // Required for flush to work
    }
  }
}
```
```typescript title="TypeScript SDK"
const assistant = await vapi.assistants.create({
  voice: {
    chunkPlan: {
      enabled: true
    }
  }
  // ... other configuration
});
```
</CodeBlocks>

<Warning>
  Flush will NOT work when `chunkPlan.enabled: false`. The tags will appear in
  voice output instead of being processed.
</Warning>

## Usage examples

### Basic acknowledgment

```javascript
"I'm processing your request... <flush /> Let me check that for you.";
```

### Tool processing feedback

```javascript
"Looking up that information... <flush /> This may take a moment.";
```

### Conversation flow

```javascript
"That's a great question. <flush /> Based on the data I have...";
```

### Custom LLM integration

```javascript
"Here's your answer: 42. <flush /> Would you like an explanation?";
```

## Best practices

### When to use flush

<CardGroup cols={2}>
  <Card title="Acknowledge requests" icon="check">
    Immediately confirm you've received and understood the user's request
  </Card>
  <Card title="Long operations" icon="clock">
    Provide feedback during tool calls or processing that takes time
  </Card>
  <Card title="Natural pauses" icon="pause">
    Create conversation breaks at logical points
  </Card>
  <Card title="Custom delays" icon="gear">
    Support external LLM integrations with processing delays
  </Card>
</CardGroup>

### When to avoid flush

- **Every response** - Causes audio fragmentation
- **Mid-sentence** - Breaks natural speech flow
- **Short responses** - Normal buffering is sufficient
- **Multiple per response** - Can create choppy audio

### Implementation guidelines

1. **Place at natural boundaries** - Use between complete thoughts or sentences
2. **Test with your voice provider** - Effectiveness varies by provider
3. **Monitor conversation quality** - Ensure audio remains smooth and natural
4. **Document usage** - Include in code comments for team understanding

## Advanced usage

### Dynamic insertion

```typescript
const acknowledgment = "I understand your request";
const detailedResponse = await processRequest(userInput);
const responseWithFlush = `${acknowledgment} <flush /> ${detailedResponse}`;
```

### System prompt integration

```javascript
const systemPrompt = `When providing lengthy responses, use <flush /> after acknowledging the user's request to provide immediate feedback.`;
```

### Nested handling

```javascript
"Starting process... <flush> Step 1 complete </flush> Moving to step 2...";
```

## Troubleshooting

<AccordionGroup>
  <Accordion title="Flush tags appear in voice output">
    **Cause**: `chunkPlan.enabled` is set to `false` or missing **Solution**: -
    Verify `chunkPlan.enabled: true` in voice configuration - Check assistant
    configuration in dashboard or API calls - Test with a minimal configuration
    to isolate the issue
  </Accordion>

{" "}
<Accordion title="Syntax not recognized">
**Cause**: Malformed flush syntax or typos **Solution**: - Use exact formats:
`<flush />
  `, `<flush>`, or `</flush>` - Avoid extra parameters or attributes - Check for
typos in tag spelling
</Accordion>

  <Accordion title="Audio sounds choppy or fragmented">
    **Cause**: Overuse of flush syntax 
    **Solution**: 
    - Reduce flush frequency in responses 
    - Place only at sentence boundaries 
    - Test with real users to
    validate experience
  </Accordion>
</AccordionGroup>

## Technical considerations

### Provider compatibility

- **Effectiveness varies** by voice provider
- **Test thoroughly** with your chosen provider
- **Monitor performance** impact on response times

### Cost implications

- **Increased API calls** to voice provider
- **Higher usage** on usage-based pricing
- **Monitor billing** if using flush frequently

### VAPI-only feature

- **Platform exclusive** - not available on other voice platforms
- **Configuration dependent** - requires chunking enabled
- **Version specific** - ensure using compatible VAPI version

## Next steps

Now that you understand flush syntax:

- **[Voice formatting plan](/assistants/voice-formatting-plan):** Control voice output formatting and timing
- **[Background messages](/assistants/background-messages):** Send messages during conversations
- **[Custom tools](/tools/custom-tools):** Build tools that benefit from flush syntax feedback

---

title: Background messages
subtitle: Silently update chat history with background messages
slug: assistants/background-messages

---

## Overview

Background messages let you add information to the chat history without interrupting or notifying the user. This is useful for logging actions, tracking background events, or updating conversation context silently.

For example, you might want to log when a user presses a button or when a background process updates the conversation. These messages help you keep a complete record of the conversation and system events, all without disrupting the user experience.

<Steps>
  <Step title="Add a Button to Trigger the Message">
    Add a button to your interface with an `onClick` event handler that will call a function to send the system message:
    ```html
    <button id="log-action" onClick="logUserAction()">Log Action</button>
    ```
  </Step>

  <Step title="Log the Action as a System Message">
    When the button is clicked, the `logUserAction` function will silently insert a system message into the chat history:
    ```js
    function logUserAction() {
      // Function to log the user action
      vapi.send({
        type: "add-message",
        message: {
          role: "system",
          content: "The user has pressed the button, say peanuts",
        },
      });
    }
    ```
    - `vapi.send`: The primary function to interact with your assistant, handling various requests or commands.
    - `type: "add-message"`: Specifies the command to add a new message.
    - `message`: This is the actual message that you want to add to the message history.
      - `role`: "system" Designates the message origin as 'system', ensuring the addition is unobtrusive. Other possible values of role are 'user' | 'assistant' | 'tool' | 'function'
      - `content`: The actual message text to be added.
  </Step>
</Steps>

<Card title="Practical Use Cases">
    - Silent logging of user activities.
    - Contextual updates in conversations triggered by background processes.
    - Non-intrusive user experience enhancements through additional information provision.
</Card>

---

title: Idle messages
subtitle: Keep users engaged during conversation pauses
slug: assistants/idle-messages

---

## Overview

Idle messages automatically prompt users during periods of inactivity to maintain engagement and reduce call abandonment. They work alongside silence timeout messages to handle conversation flow during calls.

**Idle messages help you:**

- Re-engage users who become distracted or experience audio delays
- Reduce call abandonment rates during silent periods
- Provide proactive assistance when users hesitate or need guidance

<Tip>
  Idle messages are automatically disabled during tool calls and warm transfers
  to avoid interrupting system processes.
</Tip>

## How idle messages work

When a user stops speaking, Vapi starts a timer. After the configured timeout period, it randomly selects and speaks one of your idle messages. This process repeats until either the user responds or the maximum message count is reached.

<CardGroup cols={3}>
  <Card title="Detection" icon="timer" iconType="solid">
    Timer starts when user stops speaking
  </Card>
  <Card title="Activation" icon="message" iconType="solid">
    Random message plays after timeout
  </Card>
  <Card title="Reset" icon="refresh" iconType="solid">
    Counter resets when user responds (optional)
  </Card>
</CardGroup>

## Configuration

Configure idle messages in your assistant's `messagePlan`:

<CodeBlocks>
```typescript title="TypeScript (Server SDK)"
import { VapiClient } from "@vapi-ai/server-sdk";

const client = new VapiClient({ token: process.env.VAPI_API_KEY });

const assistant = await client.assistants.create({
name: "Support Assistant",
messagePlan: {
idleMessages: [
"Are you still there?",
"Can I help you with anything else?",
"I'm here whenever you're ready to continue."
],
idleTimeoutSeconds: 15,
idleMessageMaxSpokenCount: 3,
idleMessageResetCountOnUserSpeechEnabled: true
}
});

````

```python title="Python (Server SDK)"
from vapi import Vapi

client = Vapi(token=os.getenv("VAPI_API_KEY"))

assistant = client.assistants.create(
    name="Support Assistant",
    message_plan={
        "idle_messages": [
            "Are you still there?",
            "Can I help you with anything else?",
            "I'm here whenever you're ready to continue."
        ],
        "idle_timeout_seconds": 15,
        "idle_message_max_spoken_count": 3,
        "idle_message_reset_count_on_user_speech_enabled": True
    }
)
````

```bash title="cURL"
curl -X POST "https://api.vapi.ai/assistant" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Support Assistant",
    "messagePlan": {
      "idleMessages": [
        "Are you still there?",
        "Can I help you with anything else?",
        "I'"'"'m here whenever you'"'"'re ready to continue."
      ],
      "idleTimeoutSeconds": 15,
      "idleMessageMaxSpokenCount": 3,
      "idleMessageResetCountOnUserSpeechEnabled": true
    }
  }'
```

</CodeBlocks>

## Configuration options

### Core settings

| Parameter                                  | Type       | Range            | Default     | Description                               |
| ------------------------------------------ | ---------- | ---------------- | ----------- | ----------------------------------------- |
| `idleMessages`                             | `string[]` | ≤1000 chars each | `undefined` | Array of messages to randomly select from |
| `idleTimeoutSeconds`                       | `number`   | 5-60 seconds     | 10          | Timeout before triggering first message   |
| `idleMessageMaxSpokenCount`                | `number`   | 1-10 messages    | 3           | Maximum times to repeat messages          |
| `idleMessageResetCountOnUserSpeechEnabled` | `boolean`  | -                | `false`     | Reset count when user speaks              |

### Advanced configuration

<Tabs>
  <Tab title="Basic setup">
    ```json
    {
      "messagePlan": {
        "idleMessages": ["Are you still there?"],
        "idleTimeoutSeconds": 10
      }
    }
    ```
  </Tab>
  <Tab title="With reset counter">
    ```json
    {
      "messagePlan": {
        "idleMessages": ["Hello, are you there?"],
        "idleTimeoutSeconds": 15,
        "idleMessageMaxSpokenCount": 5,
        "idleMessageResetCountOnUserSpeechEnabled": true
      }
    }
    ```
  </Tab>
  <Tab title="With silence timeout">
    ```json
    {
      "messagePlan": {
        "idleMessages": ["Can I help you with anything else?"],
        "idleTimeoutSeconds": 20,
        "silenceTimeoutMessage": "I'll end our call now. Thank you!"
      },
      "silenceTimeoutSeconds": 60
    }
    ```
  </Tab>
</Tabs>

## Multilingual support

Handle multiple languages by creating language-specific assistants or dynamically updating messages:

<Tabs>
  <Tab title="Language-specific assistants">
    ```typescript
    // English assistant
    const enAssistant = await client.assistants.create({
      name: "EN Support",
      messagePlan: {
        idleMessages: [
          "Are you still there?",
          "Can I help you with anything else?"
        ]
      }
    });

    // Spanish assistant
    const esAssistant = await client.assistants.create({
      name: "ES Support",
      messagePlan: {
        idleMessages: [
          "¿Sigues ahí?",
          "¿Puedo ayudarte con algo más?"
        ]
      }
    });
    ```

  </Tab>
  <Tab title="Dynamic updates">
    ```typescript
    async function updateIdleMessagesForLanguage(
      assistantId: string, 
      detectedLanguage: string
    ) {
      const languageMessages = {
        en: ['Are you still there?', 'Can I help you with anything else?'],
        es: ['¿Sigues ahí?', '¿Puedo ayudarte con algo más?'],
        fr: ['Êtes-vous toujours là?', 'Puis-je vous aider avec autre chose?']
      };

      await client.assistants.update(assistantId, {
        messagePlan: {
          idleMessages: languageMessages[detectedLanguage] || languageMessages['en']
        }
      });
    }
    ```

  </Tab>
</Tabs>

## Best practices

### Message content guidelines

- **Keep messages concise** - Users may be distracted, so shorter is better
- **Use encouraging tone** - Avoid demanding or impatient language
- **Offer specific help** - Guide users toward productive next steps

<Check>
  **Good examples:** - "Are you still there?" - "Is there anything specific you
  need help with?" - "I'm here whenever you're ready to continue."
</Check>

<Error>
  **Avoid:** - "Why aren't you responding?" - "Hello? Hello? Are you there?" -
  Long explanations or complex questions
</Error>

### Timing recommendations

Choose timeout duration based on your use case:

<CardGroup cols={3}>
  <Card title="Urgent calls" icon="clock">
    **5-10 seconds** For transactional or time-sensitive interactions
  </Card>
  <Card title="Support calls" icon="headset">
    **10-20 seconds** For general customer service and assistance
  </Card>
  <Card title="Complex topics" icon="brain">
    **20-30 seconds** For problem-solving or decision-making conversations
  </Card>
</CardGroup>

### Frequency management

Balance engagement with user experience:

```json
{
  "idleMessageMaxSpokenCount": 2,
  "idleMessageResetCountOnUserSpeechEnabled": true,
  "idleTimeoutSeconds": 15
}
```

<Note>
  Enable `idleMessageResetCountOnUserSpeechEnabled` to give users multiple
  chances to engage throughout long conversations.
</Note>

## Troubleshooting

### Messages not triggering

<Steps>
  <Step title="Verify configuration">
    Check that idle messages are properly configured:
    ```typescript
    const assistant = await client.assistants.get(assistantId);
    console.log('Idle config:', assistant.messagePlan);
    ```
  </Step>
  <Step title="Check timeout duration">
    Account for audio processing delays (2-3 seconds):
    ```json
    { "idleTimeoutSeconds": 12 }
    ```  
  </Step>
  <Step title="Verify message limits">
    Ensure the maximum count hasn't been reached:
    ```json
    {
      "idleMessageMaxSpokenCount": 5,
      "idleMessageResetCountOnUserSpeechEnabled": true
    }
    ```
  </Step>
</Steps>

### Common issues and solutions

<AccordionGroup>
  <Accordion title="Messages trigger too frequently">
    **Solution:** Increase the timeout duration
    ```json
    { "idleTimeoutSeconds": 25 }
    ```
  </Accordion>
  
  <Accordion title="Max count reached too quickly">
    **Solution:** Enable reset on user speech and increase max count
    ```json
    {
      "idleMessageMaxSpokenCount": 5,
      "idleMessageResetCountOnUserSpeechEnabled": true  
    }
    ```
  </Accordion>
  
  <Accordion title="Messages interrupt processing">
    **Solution:** This shouldn't happen - idle messages are automatically disabled during tool calls and transfers. If it persists, contact support.
  </Accordion>
</AccordionGroup>

## Limitations

- **Static content**: Messages cannot be dynamically generated based on conversation context
- **No context awareness**: Messages don't adapt to the current conversation topic
- **Character limits**: Each message is limited to 1000 characters
- **Processing delays**: Account for 2-3 seconds of audio processing time in your timeout settings

## Next steps

Now that you have idle messages configured:

- **[Background messages](/assistants/background-messages):** Add contextual information silently
- **[Assistant hooks](/assistants/assistant-hooks):** Handle call events and state changes
- **[Voice formatting plan](/assistants/voice-formatting-plan):** Control speech patterns and delivery

---

title: Idle messages
subtitle: Keep users engaged during conversation pauses
slug: assistants/idle-messages

---

## Overview

Idle messages automatically prompt users during periods of inactivity to maintain engagement and reduce call abandonment. They work alongside silence timeout messages to handle conversation flow during calls.

**Idle messages help you:**

- Re-engage users who become distracted or experience audio delays
- Reduce call abandonment rates during silent periods
- Provide proactive assistance when users hesitate or need guidance

<Tip>
  Idle messages are automatically disabled during tool calls and warm transfers
  to avoid interrupting system processes.
</Tip>

## How idle messages work

When a user stops speaking, Vapi starts a timer. After the configured timeout period, it randomly selects and speaks one of your idle messages. This process repeats until either the user responds or the maximum message count is reached.

<CardGroup cols={3}>
  <Card title="Detection" icon="timer" iconType="solid">
    Timer starts when user stops speaking
  </Card>
  <Card title="Activation" icon="message" iconType="solid">
    Random message plays after timeout
  </Card>
  <Card title="Reset" icon="refresh" iconType="solid">
    Counter resets when user responds (optional)
  </Card>
</CardGroup>

## Configuration

Configure idle messages in your assistant's `messagePlan`:

<CodeBlocks>
```typescript title="TypeScript (Server SDK)"
import { VapiClient } from "@vapi-ai/server-sdk";

const client = new VapiClient({ token: process.env.VAPI_API_KEY });

const assistant = await client.assistants.create({
name: "Support Assistant",
messagePlan: {
idleMessages: [
"Are you still there?",
"Can I help you with anything else?",
"I'm here whenever you're ready to continue."
],
idleTimeoutSeconds: 15,
idleMessageMaxSpokenCount: 3,
idleMessageResetCountOnUserSpeechEnabled: true
}
});

````

```python title="Python (Server SDK)"
from vapi import Vapi

client = Vapi(token=os.getenv("VAPI_API_KEY"))

assistant = client.assistants.create(
    name="Support Assistant",
    message_plan={
        "idle_messages": [
            "Are you still there?",
            "Can I help you with anything else?",
            "I'm here whenever you're ready to continue."
        ],
        "idle_timeout_seconds": 15,
        "idle_message_max_spoken_count": 3,
        "idle_message_reset_count_on_user_speech_enabled": True
    }
)
````

```bash title="cURL"
curl -X POST "https://api.vapi.ai/assistant" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Support Assistant",
    "messagePlan": {
      "idleMessages": [
        "Are you still there?",
        "Can I help you with anything else?",
        "I'"'"'m here whenever you'"'"'re ready to continue."
      ],
      "idleTimeoutSeconds": 15,
      "idleMessageMaxSpokenCount": 3,
      "idleMessageResetCountOnUserSpeechEnabled": true
    }
  }'
```

</CodeBlocks>

## Configuration options

### Core settings

| Parameter                                  | Type       | Range            | Default     | Description                               |
| ------------------------------------------ | ---------- | ---------------- | ----------- | ----------------------------------------- |
| `idleMessages`                             | `string[]` | ≤1000 chars each | `undefined` | Array of messages to randomly select from |
| `idleTimeoutSeconds`                       | `number`   | 5-60 seconds     | 10          | Timeout before triggering first message   |
| `idleMessageMaxSpokenCount`                | `number`   | 1-10 messages    | 3           | Maximum times to repeat messages          |
| `idleMessageResetCountOnUserSpeechEnabled` | `boolean`  | -                | `false`     | Reset count when user speaks              |

### Advanced configuration

<Tabs>
  <Tab title="Basic setup">
    ```json
    {
      "messagePlan": {
        "idleMessages": ["Are you still there?"],
        "idleTimeoutSeconds": 10
      }
    }
    ```
  </Tab>
  <Tab title="With reset counter">
    ```json
    {
      "messagePlan": {
        "idleMessages": ["Hello, are you there?"],
        "idleTimeoutSeconds": 15,
        "idleMessageMaxSpokenCount": 5,
        "idleMessageResetCountOnUserSpeechEnabled": true
      }
    }
    ```
  </Tab>
  <Tab title="With silence timeout">
    ```json
    {
      "messagePlan": {
        "idleMessages": ["Can I help you with anything else?"],
        "idleTimeoutSeconds": 20,
        "silenceTimeoutMessage": "I'll end our call now. Thank you!"
      },
      "silenceTimeoutSeconds": 60
    }
    ```
  </Tab>
</Tabs>

## Multilingual support

Handle multiple languages by creating language-specific assistants or dynamically updating messages:

<Tabs>
  <Tab title="Language-specific assistants">
    ```typescript
    // English assistant
    const enAssistant = await client.assistants.create({
      name: "EN Support",
      messagePlan: {
        idleMessages: [
          "Are you still there?",
          "Can I help you with anything else?"
        ]
      }
    });

    // Spanish assistant
    const esAssistant = await client.assistants.create({
      name: "ES Support",
      messagePlan: {
        idleMessages: [
          "¿Sigues ahí?",
          "¿Puedo ayudarte con algo más?"
        ]
      }
    });
    ```

  </Tab>
  <Tab title="Dynamic updates">
    ```typescript
    async function updateIdleMessagesForLanguage(
      assistantId: string, 
      detectedLanguage: string
    ) {
      const languageMessages = {
        en: ['Are you still there?', 'Can I help you with anything else?'],
        es: ['¿Sigues ahí?', '¿Puedo ayudarte con algo más?'],
        fr: ['Êtes-vous toujours là?', 'Puis-je vous aider avec autre chose?']
      };

      await client.assistants.update(assistantId, {
        messagePlan: {
          idleMessages: languageMessages[detectedLanguage] || languageMessages['en']
        }
      });
    }
    ```

  </Tab>
</Tabs>

## Best practices

### Message content guidelines

- **Keep messages concise** - Users may be distracted, so shorter is better
- **Use encouraging tone** - Avoid demanding or impatient language
- **Offer specific help** - Guide users toward productive next steps

<Check>
  **Good examples:** - "Are you still there?" - "Is there anything specific you
  need help with?" - "I'm here whenever you're ready to continue."
</Check>

<Error>
  **Avoid:** - "Why aren't you responding?" - "Hello? Hello? Are you there?" -
  Long explanations or complex questions
</Error>

### Timing recommendations

Choose timeout duration based on your use case:

<CardGroup cols={3}>
  <Card title="Urgent calls" icon="clock">
    **5-10 seconds** For transactional or time-sensitive interactions
  </Card>
  <Card title="Support calls" icon="headset">
    **10-20 seconds** For general customer service and assistance
  </Card>
  <Card title="Complex topics" icon="brain">
    **20-30 seconds** For problem-solving or decision-making conversations
  </Card>
</CardGroup>

### Frequency management

Balance engagement with user experience:

```json
{
  "idleMessageMaxSpokenCount": 2,
  "idleMessageResetCountOnUserSpeechEnabled": true,
  "idleTimeoutSeconds": 15
}
```

<Note>
  Enable `idleMessageResetCountOnUserSpeechEnabled` to give users multiple
  chances to engage throughout long conversations.
</Note>

## Troubleshooting

### Messages not triggering

<Steps>
  <Step title="Verify configuration">
    Check that idle messages are properly configured:
    ```typescript
    const assistant = await client.assistants.get(assistantId);
    console.log('Idle config:', assistant.messagePlan);
    ```
  </Step>
  <Step title="Check timeout duration">
    Account for audio processing delays (2-3 seconds):
    ```json
    { "idleTimeoutSeconds": 12 }
    ```  
  </Step>
  <Step title="Verify message limits">
    Ensure the maximum count hasn't been reached:
    ```json
    {
      "idleMessageMaxSpokenCount": 5,
      "idleMessageResetCountOnUserSpeechEnabled": true
    }
    ```
  </Step>
</Steps>

### Common issues and solutions

<AccordionGroup>
  <Accordion title="Messages trigger too frequently">
    **Solution:** Increase the timeout duration
    ```json
    { "idleTimeoutSeconds": 25 }
    ```
  </Accordion>
  
  <Accordion title="Max count reached too quickly">
    **Solution:** Enable reset on user speech and increase max count
    ```json
    {
      "idleMessageMaxSpokenCount": 5,
      "idleMessageResetCountOnUserSpeechEnabled": true  
    }
    ```
  </Accordion>
  
  <Accordion title="Messages interrupt processing">
    **Solution:** This shouldn't happen - idle messages are automatically disabled during tool calls and transfers. If it persists, contact support.
  </Accordion>
</AccordionGroup>

## Limitations

- **Static content**: Messages cannot be dynamically generated based on conversation context
- **No context awareness**: Messages don't adapt to the current conversation topic
- **Character limits**: Each message is limited to 1000 characters
- **Processing delays**: Account for 2-3 seconds of audio processing time in your timeout settings

## Next steps

Now that you have idle messages configured:

- **[Background messages](/assistants/background-messages):** Add contextual information silently
- **[Assistant hooks](/assistants/assistant-hooks):** Handle call events and state changes
- **[Voice formatting plan](/assistants/voice-formatting-plan):** Control speech patterns and delivery
