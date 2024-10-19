import subprocess
import whisper
import os
import sys
import yt_dlp


def download_audio(video_url):
    try:
        # Command to download audio and convert to MP3 using yt-dlp
        command = [
            sys.executable, '-m', 'yt_dlp', 
            '-f', 'bestaudio', 
            '--extract-audio', '--audio-format', 'mp3', 
            video_url
        ]

        # Run the command
        subprocess.run(command, check=True)
        print(f"Audio successfully downloaded from: {video_url}")
        
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")

def transcribe_audio_whisper(audio_path):
    # Load Whisper model (base or small moor fasdel fter performance)
    model = whisper.load_model("base")
    
    result = model.transcribe(audio_path)
    
    return result['text']
# # Example usage
# audio_path = '/workspaces/GenAIProject/What is Biology？ [6v8djXa-IPQ].mp3'
# transcript = transcribe_audio_whisper(audio_path)
# print(transcript)

