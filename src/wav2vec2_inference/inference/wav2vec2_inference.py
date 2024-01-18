"""
Speech Transcription with finetuned wav2vec 2.0 models

Author: Aditya Parikh, CLST, Radboud University

Description:
This script uses a finetuned wav2vec 2.0 model to transcribe speech from an audio file.
It provides transcribed words, along with their corretsponding start and end times.

Usage:
Run the script with the following command:
   python wav2vec2_inference.py --model_id [finetuned_model_path or huggingface_model_id] --cache_dir [cache_directory_path] --audio_filepath [audio_file_path]

Arguments:
- --model_id: Finetuned model path of pretrained model identifier from Hugging Face Transformers.
- --cache_dir: Path to the cache directory for storing pretrained models.
- --audio_filepath: Path to the audio file for transcription.

Example:
   python your_script.py --model_id path/to/model/xls-r-300m-nl-v2_lm-5gram-os --cache_dir /path/to/cache_dir --audio_filepath /path/to/audio_file.wav
"""

import argparse
import warnings
import librosa
import torch
from transformers import AutoTokenizer, AutoProcessor, AutoModelForCTC

warnings.filterwarnings("ignore")

def transcribe_audio(model_id, cache_dir, audio_filepath):
    model_path = f"{model_id}/"
    model = AutoModelForCTC.from_pretrained(model_path, cache_dir=cache_dir)
    processor = AutoProcessor.from_pretrained(model_path, cache_dir=cache_dir)

    # Reading audio clip
    audio, rate = librosa.load(audio_filepath, sr=16000)

    # Processing input values
    input_values = processor(audio, sampling_rate=16_000, return_tensors="pt", padding="longest").input_values
    with torch.no_grad():
        logits = model(input_values).logits[0].cpu().numpy()
    outputs = processor.decode(logits, output_word_offsets=True)

    # Compute time offsets in seconds
    time_offset = model.config.inputs_to_logits_ratio / processor.feature_extractor.sampling_rate
    word_offsets = [
        {
            "word": d["word"],
            "start_time": round(d["start_offset"] * time_offset, 2),
            "end_time": round(d["end_offset"] * time_offset, 2),
        }
        for d in outputs.word_offsets
    ]
    
    return word_offsets

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcribe audio using a pretrained CTC model.")
    parser.add_argument("--model_id", required=True, help="Pretrained model identifier")
    parser.add_argument("--cache_dir", required=True, help="Path to cache directory for storing models")
    parser.add_argument("--audio_filepath", required=True, help="Path to the audio file for transcription")

    args = parser.parse_args()

    transcribed_words = transcribe_audio(args.model_id, args.cache_dir, args.audio_filepath)
    print(transcribed_words)
