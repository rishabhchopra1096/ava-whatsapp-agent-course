#!/usr/bin/env python3
"""
SIMPLE VAPI TEST - Basic syntax and structure validation

🎯 PURPOSE: Test our Vapi code syntax without requiring full dependencies
This verifies our code is structured correctly before deployment

🔗 REAL-WORLD ANALOGY: Like checking a blueprint before building - 
making sure all the plans are drawn correctly
"""

import ast
import os

def test_python_syntax(file_path):
    """Test if a Python file has valid syntax"""
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        
        # Try to parse the file as Python code
        ast.parse(content)
        return True, "Syntax OK"
    except SyntaxError as e:
        return False, f"Syntax Error: {e}"
    except Exception as e:
        return False, f"Error: {e}"

def main():
    print("🧪 SIMPLE VAPI SYNTAX TESTS")
    print("=" * 40)
    
    # Test our Vapi files
    vapi_files = [
        "src/ai_companion/interfaces/vapi/__init__.py",
        "src/ai_companion/interfaces/vapi/vapi_endpoints.py", 
        "src/ai_companion/interfaces/vapi/vapi_client.py",
        "src/ai_companion/interfaces/vapi/voice_context_manager.py"
    ]
    
    all_passed = True
    
    for file_path in vapi_files:
        if os.path.exists(file_path):
            success, message = test_python_syntax(file_path)
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"{status} - {os.path.basename(file_path)}: {message}")
            if not success:
                all_passed = False
        else:
            print(f"❌ FAIL - {os.path.basename(file_path)}: File not found")
            all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("🎉 ALL SYNTAX TESTS PASSED!")
        print("✅ Vapi code is ready for deployment")
        print("\n📋 NEXT STEPS:")
        print("1. Deploy to Railway")
        print("2. Test endpoints with real dependencies")
        print("3. Configure Vapi to use your Railway URL")
    else:
        print("⚠️  Some syntax errors found")
        print("Fix the errors above before deploying")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)