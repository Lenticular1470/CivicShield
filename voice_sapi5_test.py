import pyttsx3

print("Testing voice engine...")

try:
    engine = pyttsx3.init('sapi5')
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    
    print("✅ Engine initialized")
    
    # Test messages
    engine.say("person detected")
    engine.runAndWait()
    
    engine.say("mobile phone detected")
    engine.runAndWait()
    
    engine.say("bottle detected")
    engine.runAndWait()
    
    print("✅ All tests completed!")
    
except Exception as e:
    print(f"❌ Error: {e}")
