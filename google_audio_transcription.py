from google.cloud import speech_v1p1beta1 as speech
import io
import tarfile
import os
import csv
import py7zr
from pydub import AudioSegment

def get_sample_rate(file_path):
    audio = AudioSegment.from_file(file_path)
    return audio.frame_rate

def extract_archive(file_path, extract_path, file_type='gz'):
    if file_type == 'gz':
        with tarfile.open(file_path, 'r:gz') as tar:
            tar.extractall(path=extract_path)
    elif file_type == '7z':
        with py7zr.SevenZipFile(file_path, mode='r') as z:
            z.extractall(path=extract_path)

    print(f"Extracted to {extract_path}")

def transcribe_audio(file_path):
    client = speech.SpeechClient()

    with io.open(file_path, "rb") as audio_file:
        content = audio_file.read()

    sample_rate = get_sample_rate(file_path)

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=sample_rate,
        language_code="en-US",
        speech_contexts=[
            speech.SpeechContext(
                phrases=[
                    "Walter Bytell",
                    "Russell Ahhnold"
                ]
            )
        ]
    )

    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        print(file_path)
        print("Transcript: {}".format(result.alternatives[0].transcript))

'''# Path to your TSV file
file_path = 'clip_durations.tsv'

transcriptions = 0

# Read the TSV file
with open(file_path, mode='r', newline='', encoding='utf-8') as file:
    tsv_reader = csv.DictReader(file, delimiter='\t')
    
    # Process each row as a dictionary
    for row in tsv_reader:        
        file_name = row['clip']        
        duration = int(row['duration[ms]'])        
        
        if duration > 10000:
            transcriptions += 1
            print(transcriptions)
            if transcriptions < 4:
                continue
            transcribe_audio(os.path.join('E:/audio/common_voice_delta_17/cv-corpus-17.0-delta-2024-03-15/en/clips', file_name))            

        if transcriptions > 9:
            break'''

transcribe_audio('E:/audio/common_voice_delta_17/cv-corpus-17.0-delta-2024-03-15/en/clips/common_voice_en_39630029.mp3')