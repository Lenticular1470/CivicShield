import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 150)

# Test different messages
messages = [
    "person detected",
    "cell phone detected",
    "bottle detected",
    "laptop detected"
]

for msg in messages:
    print(f"Speaking: {msg}")
    engine.say(msg)
    engine.runAndWait()
    
print("✅ Voice test complete!")
