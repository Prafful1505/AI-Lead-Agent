import os
import google.generativeai as genai

# --- CONFIGURATION ---
# IMPORTANT: Set your Gemini API key as an environment variable
# or replace 'YOUR_GEMINI_API_KEY' with your actual key.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyB9BpGB80JEe8iEwkHH6p-GY6I1wyU2JFI")

try:
    genai.configure(api_key=GEMINI_API_KEY)
    # Initialize the Gemini model
    model = genai.GenerativeModel('gemini-2.5-pro')
except Exception as e:
    print(f"Error configuring Gemini API: {e}")
    print("Please make sure you have set the GEMINI_API_KEY environment variable or replaced the placeholder in the script.")
    model = None

# Initial system prompt to guide the AI agent's behavior
SYSTEM_PROMPT = """
You are a friendly and professional AI assistant for a company called 'Innovate Inc.'.
Your role is to qualify new leads by asking a series of questions.
Be conversational, polite, and keep your responses concise.
Do not ask more than one question at a time.
Do not deviate from the script.
Start the conversation by introducing yourself and asking the first question: 'What is your name?'.
"""

def get_gemini_response(prompt):
    """
    Generates a response from the Gemini model based on a given prompt.

    Args:
        prompt (str): The user prompt to send to the model.

    Returns:
        str: The generated text response from the model, or a fallback message on error.
    """
    if not model:
        return "AI model is not available due to configuration error."
    try:
        # Prepending the system prompt to maintain context and persona
        full_prompt = f"{SYSTEM_PROMPT}\n\nUser Prompt: {prompt}"
        
        # Generate content
        response = model.generate_content(full_prompt)
        
        # Extract and return the text part of the response
        return response.text
    except Exception as e:
        print(f"An error occurred while calling the Gemini API: {e}")
        return "I'm sorry, I'm having trouble connecting to my brain right now. Please try again later."

if __name__ == '__main__':
    # Example usage for testing the module directly
    print("Testing Gemini Config...")
    initial_prompt = "Start the conversation by introducing yourself and asking for the user's name."
    response = get_gemini_response(initial_prompt)
    print(f"AI Response: {response}")
