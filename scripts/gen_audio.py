import os
import sys

def main():
    print("gen_audio.py: Skipping TTS generation to use Android native TTS fallback as per spec.")
    audio_dir = os.path.join(os.path.dirname(__file__), '..', 'content', 'audio')
    os.makedirs(os.path.join(audio_dir, 'hi'), exist_ok=True)
    os.makedirs(os.path.join(audio_dir, 'sat'), exist_ok=True)
    
if __name__ == '__main__':
    main()
