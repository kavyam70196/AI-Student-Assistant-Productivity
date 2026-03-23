import google.generativeai as genai

# Configure API
genai.configure(api_key='AIzaSyCKJfdOGsmrbcWbTOP1NgUtiTlPXB73WtU')

print("Available Gemini Models:")
print("-" * 50)

for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"✓ {model.name}")

print("-" * 50)
print("\nTrying to use a model...")

# Try different models
models_to_try = [
    'gemini-1.5-flash-latest',
    'gemini-1.5-pro-latest', 
    'gemini-1.5-flash',
    'gemini-1.5-pro',
    'gemini-pro',
    'models/gemini-pro',
    'models/gemini-1.5-flash',
]

for model_name in models_to_try:
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Say hello")
        print(f"\n✅ SUCCESS with model: {model_name}")
        print(f"Response: {response.text}")
        break
    except Exception as e:
        print(f"❌ Failed with {model_name}: {str(e)[:100]}")
