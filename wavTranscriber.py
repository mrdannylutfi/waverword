import os
import wave
import json
import datetime
from vosk import Model, KaldiRecognizer
from docx import Document

def format_time(seconds):
    """Converts seconds (float) into a readable HH:MM:SS format."""
    td = datetime.timedelta(seconds=seconds)
    # Extract hours, minutes, and integer seconds
    return str(td).split(".")[0]

def transcribe_to_paragraphs(audio_path, model_path, output_docx_path, time_threshold=30.0, word_threshold=30):
    # 1. Verify audio file exists and is mono
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
    wf = wave.open(audio_path, "rb")
    if wf.getnchannels() != 1:
        raise ValueError("Vosk requires a MONO WAV file. Please convert it to mono first.")

    # 2. Load the Vosk model
    print("Loading Vosk model...")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model directory not found at: {model_path}")
    
    model = Model(model_path)
    
    # 3. Initialize the recognizer and enable word timestamps
    sample_rate = wf.getframerate()
    recognizer = KaldiRecognizer(model, sample_rate)
    recognizer.SetWords(True) 

    print("Transcribing audio and processing paragraphs...")
    all_words = []

    # Stream and process the audio file
    chunk_size = 4000
    while True:
        data = wf.readframes(chunk_size)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            result_json = json.loads(recognizer.Result())
            if "result" in result_json:
                all_words.extend(result_json["result"])

    final_result = json.loads(recognizer.FinalResult())
    if "result" in final_result:
        all_words.extend(final_result["result"])

    wf.close()
    print("Transcription complete!")

    # 4. Build the Word Document with Grouped Paragraphs
    print(f"Creating Word document: {output_docx_path}...")
    doc = Document()
    doc.add_heading('Audio Transcription (Paragraph Blocks)', level=1)
    
    if not all_words:
        doc.add_paragraph("No speech was recognized.")
        doc.save(output_docx_path)
        return

    current_paragraph_words = []
    paragraph_start_time = all_words[0].get("start", 0.0)
    word_count_in_para = 0

    # Function helper to commit a paragraph to the document
    def commit_paragraph(words_list, start_time):
        if not words_list:
            return
        p = doc.add_paragraph()
        # Add timestamp at the beginning of the paragraph
        timestamp_run = p.add_run(f"[{format_time(start_time)}] ")
        timestamp_run.bold = True
        # Add the text block
        p.add_run(" ".join(words_list))

    # 5. Segment words into paragraphs based on sentences and time limits
    for item in all_words:
        word = item.get("word", "")
        start_time = item.get("start", 0.0)
        
        # If this is the start of a completely fresh paragraph segment, update the time tracker
        if not current_paragraph_words:
            paragraph_start_time = start_time
            
        current_paragraph_words.append(word)
        word_count_in_para += 1
        
        # Check conditions to break into a new paragraph:
        # A) Natural punctuation sentence ends (. ! ?)
        is_sentence_end = word.endswith(('.', '!', '?'))
        
        # B) Time elapsed since current paragraph started exceeds threshold (e.g., 30 seconds)
        time_elapsed = start_time - paragraph_start_time
        is_time_limit = time_elapsed >= time_threshold
        
        # C) Word count limit reached (in case Vosk model provides no punctuation labels)
        is_word_limit = word_count_in_para >= word_threshold

        if is_sentence_end or is_time_limit or is_word_limit:
            commit_paragraph(current_paragraph_words, paragraph_start_time)
            # Reset paragraph state
            current_paragraph_words = []
            word_count_in_para = 0

    # Catch any remaining words at the end
    if current_paragraph_words:
        commit_paragraph(current_paragraph_words, paragraph_start_time)

    doc.save(output_docx_path)
    print("File saved successfully.")

# --- Configuration ---
if __name__ == "__main__":
    MODEL_DIR = "vosk-model-small-en-us-0.15"  # Your model directory
    AUDIO_FILE = "speech.wav"                  # Your MONO wav file
    OUTPUT_DOCX = "paragraph_transcription.docx"

    # You can customize time_threshold (seconds) or word_threshold (max words per paragraph)
    transcribe_to_paragraphs(AUDIO_FILE, MODEL_DIR, OUTPUT_DOCX, time_threshold=30.0, word_threshold=35)
