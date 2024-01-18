"""
Whisper ASR Audio Transcription Script

Author: Aditya Parikh, CLST, Radboud University

Description:
This script uses the Whisper ASR (Automatic Speech Recognition) system to transcribe audio files.
It reads a list of audio file paths from an input file, transcribes each file, and prints the
transcripts to the terminal.

Usage:
- Ensure you have the required dependencies installed (Whisper library).
- Run the script with the following command:
  python your_script.py input_file.txt model_download_folder --language [desired_language]

Arguments:
- input_file: Path to the file containing a list of audio file paths.
- model_download_folder: Path to the folder where Whisper models will be stored.
- --language (optional): Language for transcription (default: english).

Example:
  python your_script.py audio_paths.txt models --language spanish
"""



import argparse
import whisper
import json
import warnings
warnings.filterwarnings("ignore")


def transcribe_audio_files(input_file,model_download,language="english"):
    # Load the model
    model = whisper.load_model("large-v2", download_root=model_download, device="cpu")
    
    # Open the input file and read file paths
    with open(input_file, 'r') as file:
        file_paths = file.read().splitlines()

    for file_path in file_paths:
        try:
            # Extract filename from the file path
            filename = file_path.split("/")[-1]
            # Print filename and transcript to the terminal
            print(f"{filename}\n")
            # Transcribe the audio file with the specified language
            result = model.transcribe(file_path, verbose=True, language=language)

        except Exception as e:
            # Handle exceptions, e.g., if the file is not found or transcription fails
            print(f"Error processing {file_path}: {str(e)}\n")

    print("Transcription completed.")

if __name__ == "__main__":
    # Create ArgumentParser object
    parser = argparse.ArgumentParser(description="Transcribe audio files and print transcripts to the terminal")

    # Add arguments
    parser.add_argument("input_file", help="Path to the input file containing audio file paths")
    parser.add_argument("model_download", help="Path to the folder where you want to store Whisper models")
    parser.add_argument("--language", default="english", help="Language for transcription (default: english)")

    # Parse command-line arguments
    args = parser.parse_args()

    # Call the transcribe function with provided arguments
    transcribe_audio_files(args.input_file,args.model_download,language=args.language)
