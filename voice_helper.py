import speech_recognition as sr
from gtts import gTTS
import os
import uuid
from pydub import AudioSegment

# --- CONFIGURATION ---
# Directory to save the generated TTS audio files
AUDIO_DIR = 'static/audio'
# Ensure the directory exists
os.makedirs(AUDIO_DIR, exist_ok=True)

def transcribe_audio(webm_path):
    """
    Transcribes spoken words from a WebM audio file to text.
    It first converts the WebM file to WAV format, which is required
    by the speech_recognition library.
    
    Args:
        webm_path (str): The file path of the audio to transcribe.
        
    Returns:
        str or None: The transcribed text, or None if transcription fails.
    """
    recognizer = sr.Recognizer()
    
    # Define the path for the converted WAV file
    wav_path = webm_path.replace(".webm", ".wav")

    try:
        # Convert WebM to WAV using pydub
        print(f"Converting {webm_path} to {wav_path}...")
        audio = AudioSegment.from_file(webm_path, format="webm")
        audio.export(wav_path, format="wav")
        print("Conversion successful.")

        # Transcribe the WAV file
        with sr.AudioFile(wav_path) as source:
            print("Processing audio for transcription...")
            audio_data = recognizer.record(source)
            try:
                # Recognize speech using Google Web Speech API
                text = recognizer.recognize_google(audio_data)
                print(f"Transcription successful: '{text}'")
                return text
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio.")
                return None
            except sr.RequestError as e:
                print(f"Could not request results from Google service; {e}")
                return None

    except FileNotFoundError:
        print(f"Error: FFmpeg not found. Please install FFmpeg and ensure it's in your system's PATH.")
        return None
    except Exception as e:
        print(f"An error occurred during transcription: {e}")
        return None
    finally:
        # Clean up the temporary files
        if os.path.exists(webm_path):
            os.remove(webm_path)
        if os.path.exists(wav_path):
            os.remove(wav_path)


def text_to_speech(text):
    """
    Converts a string of text into a spoken audio file using Google Text-to-Speech (gTTS).
    
    Args:
        text (str): The text to be converted to speech.
        
    Returns:
        str: The relative file path to the generated audio file.
    """
    try:
        tts = gTTS(text=text, lang='en')
        # Generate a unique filename to avoid browser caching issues
        filename = f"response_{uuid.uuid4()}.mp3"
        filepath = os.path.join(AUDIO_DIR, filename)
        
        tts.save(filepath)
        print(f"TTS audio saved to: {filepath}")
        
        # Return a path that's accessible from the web (e.g., /static/audio/filename.mp3)
        web_path = os.path.join(AUDIO_DIR, filename).replace("\\", "/")
        return web_path
    except Exception as e:
        print(f"An error occurred during text-to-speech conversion: {e}")
        return None

if __name__ == '__main__':
    # Example usage for testing the module directly
    print("Testing Voice Helper...")
    
    # --- Test Text-to-Speech ---
    print("\n--- Testing TTS ---")
    tts_path = text_to_speech("Hello, this is a test of the text-to-speech functionality.")
    if tts_path:
        print(f"TTS audio file generated at: {tts_path}")
    else:
        print("TTS generation failed.")
        
    # --- Test Transcription ---
    print("\n--- Testing Transcription ---")
    print("Skipping transcription test in standalone mode as it requires FFmpeg and a sample file.")

