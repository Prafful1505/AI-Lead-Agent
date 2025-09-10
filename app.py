import os
from flask import Flask, render_template, request, jsonify, session, send_from_directory
from werkzeug.utils import secure_filename
import uuid

# Import helper modules
from gemini_config import get_gemini_response
from sheets_helper import save_lead
from voice_helper import transcribe_audio, text_to_speech

# Initialize the Flask application
app = Flask(__name__)
# A secret key is required for session management
app.secret_key = os.urandom(24) 
# Configure a directory to store temporary audio files
UPLOAD_FOLDER = 'static/audio'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Define the sequence of lead qualification questions
LEAD_QUALIFICATION_QUESTIONS = [
    "What is your name?",
    "What is your budget for this project?",
    "What is your ideal start date or timeline?",
    "Do you have any other specific requirements or notes for us?",
]

@app.route('/')
def index():
    """
    Renders the main chat interface.
    Initializes or resets the conversation state in the session.
    """
    # Initialize session variables for a new conversation
    session['question_index'] = 0
    session['lead_data'] = {}
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """
    Handles text-based chat interactions.
    Processes the user's message, manages conversation flow,
    and returns the AI's next response.
    """
    user_message = request.json['message']
    question_index = session.get('question_index', 0)
    
    # Process the user's answer and prepare the next question
    response_data = process_conversation(user_message, question_index)
    
    # Update the session with the new question index
    session['question_index'] = response_data['next_question_index']
    
    return jsonify({
        'response': response_data['ai_response'],
        'is_last_question': response_data['is_last_question']
    })

@app.route('/voice', methods=['POST'])
def voice():
    """
    Handles voice-based interactions.
    Receives an audio file, transcribes it, processes the conversation,
    generates a spoken response (TTS), and returns the audio file URL.
    """
    if 'audio_data' not in request.files:
        return jsonify({'error': 'No audio file found'}), 400

    audio_file = request.files['audio_data']
    filename = secure_filename(f"user_voice_{uuid.uuid4()}.webm")
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    audio_file.save(filepath)

    # 1. Transcribe the user's voice message
    transcribed_text = transcribe_audio(filepath)
    if not transcribed_text:
        # If transcription fails, provide a fallback response
        error_text = "I'm sorry, I couldn't understand what you said. Could you please type your response?"
        tts_audio_path = text_to_speech(error_text)
        tts_audio_url = request.host_url + tts_audio_path
        return jsonify({
            'user_message': 'Transcription failed.',
            'response': error_text,
            'audio_url': tts_audio_url,
            'is_last_question': False
        })
        
    # 2. Process the conversation logic with the transcribed text
    question_index = session.get('question_index', 0)
    response_data = process_conversation(transcribed_text, question_index)
    
    # Update session
    session['question_index'] = response_data['next_question_index']

    # 3. Generate Text-to-Speech for the AI's response
    tts_audio_path = text_to_speech(response_data['ai_response'])
    tts_audio_url = request.host_url + tts_audio_path

    return jsonify({
        'user_message': transcribed_text,
        'response': response_data['ai_response'],
        'audio_url': tts_audio_url,
        'is_last_question': response_data['is_last_question']
    })

def process_conversation(user_answer, current_index):
    """
    Core logic for managing the conversation flow.
    - Stores user's answer.
    - Determines the next question.
    - Saves lead data to Google Sheets when conversation is complete.

    Args:
        user_answer (str): The user's response to the current question.
        current_index (int): The index of the current question in the list.

    Returns:
        dict: A dictionary containing the AI response, the next question index,
              and a flag for the last question.
    """
    # Map question index to the corresponding data key
    data_keys = ['name', 'budget', 'timeline', 'notes']
    
    # Store the user's answer
    if current_index < len(data_keys):
        key = data_keys[current_index]
        session['lead_data'][key] = user_answer
        session.modified = True # Important: mark session as modified

    next_index = current_index + 1
    is_last = False
    
    if next_index < len(LEAD_QUALIFICATION_QUESTIONS):
        # If there are more questions, get the next one
        next_question = LEAD_QUALIFICATION_QUESTIONS[next_index]
        prompt = f"The user just answered saying: '{user_answer}'. Now, ask them the next question in a friendly and conversational way: '{next_question}'"
        ai_response = get_gemini_response(prompt)
    else:
        # If all questions are answered, finalize and save the lead
        is_last = True
        lead_data = session.get('lead_data', {})
        
        # Save the collected data to Google Sheets
        save_lead(list(lead_data.values()))
        
        prompt = f"The user has answered all qualification questions. Their final note was: '{user_answer}'. Thank them for their time, let them know their information has been received, and that a team member will be in touch shortly. Here is a summary of their info: Name: {lead_data.get('name')}, Budget: {lead_data.get('budget')}, Timeline: {lead_data.get('timeline')}."
        ai_response = get_gemini_response(prompt)
        
        # Reset for the next conversation
        session['question_index'] = 0
        session['lead_data'] = {}

    return {
        'ai_response': ai_response,
        'next_question_index': next_index,
        'is_last_question': is_last
    }

@app.route('/static/audio/<filename>')
def uploaded_file(filename):
    """Serves the generated audio files."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    # Running in debug mode is convenient for development
    app.run(debug=True)
