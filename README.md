🤖 AI-Powered Voice Agent for Lead Qualification
This project is a sophisticated, voice-enabled AI assistant designed to automate the initial stages of the sales pipeline. The agent engages potential leads in a natural conversation, asks a series of qualifying questions, and seamlessly logs their responses in a Google Sheet for a sales team to review.

The goal was to build a complete, end-to-end application that integrates cutting-edge AI with practical business automation, showcasing skills in full-stack development, cloud services, and AI engineering.

🚀 Key Features
🧠 Conversational AI Engine: Utilizes Google's Gemini 1.0 Pro model to understand user input and generate natural, human-like responses.

🎤 Voice-Enabled Interface: Supports both text and voice input. The agent features speech-to-text transcription and text-to-speech (TTS) responses for a hands-free, conversational experience.

💾 Automated Data Entry: All qualified lead data (name, budget, timeline, notes) is automatically and instantly saved to a designated Google Sheet.

🐍 Python Flask Backend: A robust and scalable backend built with Flask to handle API requests, business logic, and serve the frontend.

🌐 Modern Frontend: A clean and simple user interface built with HTML, CSS, and vanilla JavaScript using the Fetch API for seamless communication with the backend.

🛠️ How It Works: The Architecture
The application follows a straightforward but powerful architecture:

Frontend (UI): The user interacts with the chat interface in their browser. Voice input is captured as a .webm audio blob, and text is sent as a JSON object.

Flask Backend: A Flask server listens for requests on the /chat (for text) and /voice (for audio) endpoints.

Audio Processing: For voice input, the backend first uses pydub and FFmpeg to convert the .webm audio file into a .wav file.

Speech-to-Text: The .wav file is then passed to the SpeechRecognition library, which uses Google's Web Speech API to transcribe the audio into text.

Gemini AI Core: The user's message (whether typed or transcribed) is sent to the Google Gemini API. The AI model, guided by a system prompt, processes the conversation history and generates the next appropriate question.

Text-to-Speech: The AI's text response is converted back into speech using the gTTS library, generating an MP3 file that is sent back to the frontend to be played.

Google Sheets Integration: Once the final question is answered, the backend uses the gspread library and a Google Service Account to authenticate and write the complete lead profile as a new row in the "Leads" Google Sheet.

💻 Tech Stack
Backend: Python, Flask

Frontend: HTML5, CSS3, JavaScript (Vanilla)

AI Model: Google Gemini 1.0 Pro

Database: Google Sheets

Voice Processing:

SpeechRecognition (Speech-to-Text)

gTTS (Text-to-Speech)

pydub & FFmpeg (Audio Conversion)

Deployment: Local Flask Development Server

🔧 Setup and Installation
Follow these steps carefully to get the application running locally.

Step 1: Install FFmpeg
This is a critical dependency for processing voice input.

macOS (Homebrew): brew install ffmpeg

Debian/Ubuntu: sudo apt update && sudo apt install ffmpeg

Windows: Download from the official site and add the bin directory to your system's PATH.

Step 2: Clone & Set Up Environment
Clone this repository and set up a Python virtual environment.

git clone <your-repo-url>
cd lead-agent
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

Step 3: Configure Google APIs
You will need credentials for both the Gemini API and the Sheets API.

Google Gemini API Key:

Create a key in Google AI Studio.

Open gemini_config.py and replace "YOUR_NEW_GEMINI_API_KEY" with your key. (For production, use environment variables.)

Google Sheets API Credentials:

Create a new project in the Google Cloud Console.

Enable the Google Drive API and Google Sheets API.

Create a Service Account with the "Editor" role.

Create a JSON key for this service account, download it, and rename the file to credentials.json in the project's root directory.

Create a new Google Sheet named "Leads".

Share this sheet with the client_email found inside your credentials.json file, giving it "Editor" permissions.

Step 4: Run the Application
Launch the Flask development server.

python app.py

Open your browser and navigate to http://127.0.0.1:5000.

🧠 Project Learnings & Challenges
Building this agent was a fantastic learning experience. Here are some key takeaways:

The Challenge of Audio Formats: A major hurdle was discovering that browsers record audio in .webm format, while most Python speech recognition libraries expect .wav. The solution was to implement a conversion step using pydub and FFmpeg, which taught me a valuable lesson in data preprocessing and the importance of understanding media codecs.

AI Prompt Engineering: Crafting the SYSTEM_PROMPT was an iterative process. It was crucial to be very specific in the instructions to keep the AI focused on its script and prevent it from asking multiple questions at once or deviating from its role.

Secure API Key Management: This project underscored the importance of not hard-coding API keys. The code is set up to use environment variables, which is a security best practice for any production-level application.

🔮 Future Enhancements
Calendar Integration: Connect to Google Calendar to allow the agent to book a follow-up call directly after qualifying a lead.

CRM Integration: Instead of a Google Sheet, push lead data directly into a CRM like HubSpot or Salesforce for a more robust sales workflow.

Dynamic Conversations: Allow the Gemini model more freedom to ask follow-up questions based on user responses, rather than sticking to a rigid script.