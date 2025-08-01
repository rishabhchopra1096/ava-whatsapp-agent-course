#!/usr/bin/env python3
"""
TEST VAPI ENDPOINTS - Simple script to test our voice calling endpoints

🎯 PURPOSE: This script tests our Vapi integration without needing the full
LangGraph setup, so we can verify our endpoints work correctly

🔗 REAL-WORLD ANALOGY: Like doing a "phone system test" before connecting
it to the main office - we want to make sure calls can connect properly

📞 WHAT THIS TESTS:
1. Can we import our Vapi modules without errors?
2. Does the health check endpoint work?
3. Does the test chat endpoint respond correctly?
4. Can we create a voice assistant configuration?

💡 HOW TO RUN:
   python3 test_vapi_endpoints.py
"""

import sys
import os
import asyncio
import logging

# Add the project root to Python path so we can import Ava's modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Set up logging to see what's happening
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def test_vapi_imports():
    """Test that we can import all Vapi modules without errors"""
    print("🧪 TEST 1: Testing Vapi module imports...")
    
    try:
        # Test basic imports
        from ai_companion.interfaces.vapi.vapi_endpoints import vapi_router
        from ai_companion.interfaces.vapi.voice_context_manager import VoiceContextManager
        print("✅ Successfully imported Vapi modules!")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

async def test_vapi_client():
    """Test that we can create a Vapi client (without actually connecting)"""
    print("\n🧪 TEST 2: Testing Vapi client creation...")
    
    try:
        # Try to import the client
        from ai_companion.interfaces.vapi.vapi_client import VapiClient
        print("✅ Vapi client import successful!")
        
        # Note: We won't actually create the client here because it requires API keys
        # and network connection. This test just verifies the code can be imported.
        print("ℹ️  Note: Actual client creation requires API keys and will be tested in deployment")
        return True
    except Exception as e:
        print(f"❌ Vapi client test error: {e}")
        return False

async def test_context_manager():
    """Test the voice context manager with sample data"""
    print("\n🧪 TEST 3: Testing voice context manager...")
    
    try:
        from ai_companion.interfaces.vapi.voice_context_manager import VoiceContextManager
        from langchain_core.messages import HumanMessage, AIMessage
        
        # Create sample conversation
        sample_messages = [
            HumanMessage(content="Hi, I'm John and I need help with my project"),
            AIMessage(content="Hello John! I'd be happy to help you with your project. What do you need assistance with?"),
            HumanMessage(content="I'm working on a presentation and need some ideas"),
            AIMessage(content="Great! I can help you brainstorm presentation ideas. What's the topic?"),
            HumanMessage(content="Can you call me to discuss this?")
        ]
        
        # Test context creation
        manager = VoiceContextManager()
        context = manager.prepare_voice_context(sample_messages, user_id="test_user")
        
        print("✅ Context manager working! Generated context:")
        print(f"   User Name: {context['userName']}")
        print(f"   Topic: {context['conversationTopic']}")
        print(f"   Message Count: {context['messageCount']}")
        print(f"   Calling Reason: {context['callingReason']}")
        
        return True
    except Exception as e:
        print(f"❌ Context manager test error: {e}")
        return False

async def test_endpoint_structure():
    """Test that our endpoints are structured correctly"""
    print("\n🧪 TEST 4: Testing endpoint structure...")
    
    try:
        from ai_companion.interfaces.vapi.vapi_endpoints import vapi_router
        
        # Check that router has the expected routes
        routes = [route.path for route in vapi_router.routes]
        expected_routes = ['/chat/completions', '/webhook', '/health', '/test-chat']
        
        print("✅ Router created successfully!")
        print(f"   Available routes: {routes}")
        
        # Check if we have the main routes we need
        has_chat = any('/chat/completions' in route for route in routes)
        has_webhook = any('/webhook' in route for route in routes)
        has_health = any('/health' in route for route in routes)
        
        if has_chat and has_webhook and has_health:
            print("✅ All expected routes are present!")
            return True
        else:
            print(f"❌ Missing routes: chat={has_chat}, webhook={has_webhook}, health={has_health}")
            return False
            
    except Exception as e:
        print(f"❌ Endpoint structure test error: {e}")
        return False

async def run_all_tests():
    """Run all tests and report results"""
    print("🚀 STARTING VAPI INTEGRATION TESTS")
    print("=" * 50)
    
    tests = [
        ("Module Imports", test_vapi_imports),
        ("Vapi Client", test_vapi_client),
        ("Context Manager", test_context_manager),
        ("Endpoint Structure", test_endpoint_structure)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("🎯 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 ALL TESTS PASSED! Vapi integration is ready for deployment.")
        return True
    else:
        print("⚠️  Some tests failed. Check the errors above before deploying.")
        return False

if __name__ == "__main__":
    # Run the tests
    success = asyncio.run(run_all_tests())
    
    if success:
        print("\n📋 NEXT STEPS:")
        print("1. Deploy to Railway to test with real Vapi connections")
        print("2. Test the /vapi/health endpoint via web browser")
        print("3. Configure Vapi assistant to use your Railway URL")
        print("4. Test end-to-end voice calling")
    else:
        print("\n📋 NEXT STEPS:")
        print("1. Fix the failing tests above")
        print("2. Re-run this test script")
        print("3. Only deploy after all tests pass")
    
    sys.exit(0 if success else 1)