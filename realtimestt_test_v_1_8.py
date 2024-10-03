import os
import time
import sys
import logging

from colorama import Fore, Style
import colorama
from rich.live import Live
from rich.console import Console
from rich.text import Text

# Ensure that imports needed for child processes are safe
# Import AudioToTextRecorder within the main guard

if os.name == "nt" and (3, 8) <= sys.version_info < (3, 99):
    from torchaudio._extension.utils import _init_dll_path
    _init_dll_path()

colorama.init()

# Initialize Rich Console and Live
console = Console()
live = Live(console=console, refresh_per_second=10, screen=False)

# Global variables
full_sentences = []
displayed_text = ""
prev_text = ""
rich_text_stored = ""
recorder = None

end_of_sentence_detection_pause = 0.4
unknown_sentence_detection_pause = 0.7
mid_sentence_detection_pause = 2.0

USE_MAIN_MODEL = False  # Set to False to use only real-time model

def clear_console():
    os.system('clear' if os.name == 'posix' else 'cls')

def text_detected(text):
    global displayed_text, prev_text, full_sentences, recorder, rich_text_stored
    sentence_end_marks = ['.', '!', '?', '。']
    if text.endswith("..."):
        recorder.post_speech_silence_duration = mid_sentence_detection_pause
    elif text and text[-1] in sentence_end_marks and prev_text and prev_text[-1] in sentence_end_marks:
        recorder.post_speech_silence_duration = end_of_sentence_detection_pause
    else:
        recorder.post_speech_silence_duration = unknown_sentence_detection_pause

    prev_text = text

    # Build Rich Text with alternating colors
    rich_text = Text()
    for i, sentence in enumerate(full_sentences):
        if i % 2 == 0:
            rich_text += Text(sentence, style="yellow") + Text(" ")
        else:
            rich_text += Text(sentence, style="cyan") + Text(" ")
    
    # If the current text is not a sentence-ending, display it in real-time
    if text:
        rich_text += Text(text, style="white")

    new_displayed_text = rich_text.plain

    if new_displayed_text != displayed_text:
        displayed_text = new_displayed_text
        live.update(rich_text)
        rich_text_stored = rich_text

def process_text(text):
    global recorder, full_sentences, prev_text
    recorder.post_speech_silence_duration = unknown_sentence_detection_pause
    full_sentences.append(text)
    prev_text = ""
    text_detected("")

if __name__ == '__main__':
    # Now that we are under the main guard, we can import modules that start processes
    sys.path.insert(0, './')  # This assumes audio_recorder.py is in the same directory
    from audio_recorder_v_1_3 import AudioToTextRecorder

    if os.name == "nt" and (3, 8) <= sys.version_info < (3, 99):
        from torchaudio._extension.utils import _init_dll_path
        _init_dll_path()

    print("Initializing RealtimeSTT test...")

    live.start()

    EXTENDED_LOGGING = True

    # Recorder configuration
    recorder_config = {
        'spinner': False,
        'model': 'large-v2',
        'input_device_index': 0,  # Uncomment and set if needed
        'realtime_model_type': 'tiny.en',
        'language': 'en',
        'silero_sensitivity': 0.05,
        'webrtc_sensitivity': 3,
        'post_speech_silence_duration': unknown_sentence_detection_pause,
        'min_length_of_recording': 0.7,
        'min_gap_between_recordings': 0,
        'enable_realtime_transcription': True,
        'use_main_model_for_realtime': False,
        'realtime_processing_pause': 0.1,
        # 'on_realtime_transcription_update': text_detected,  # Deprecated in favor of stabilized
        'on_realtime_transcription_stabilized': text_detected,
        'silero_deactivity_detection': True,
        'early_transcription_on_silence': 0,
        'beam_size': 5,
        'beam_size_realtime': 1,
        'no_log_file': False,
        'use_main_transcription_model': USE_MAIN_MODEL,  # Pass the toggle here
        'use_extended_logging': True
    }

    if EXTENDED_LOGGING:
        recorder_config['level'] = logging.DEBUG

    recorder = AudioToTextRecorder(**recorder_config)

    # Initial display message
    initial_text = Text("Say something...", style="green")
    live.update(initial_text)

    try:
        if USE_MAIN_MODEL:
            # Use both Real-Time and Main Models
            while True:
                transcription = recorder.text(process_text)
        else:
            # Use only the Real-Time Model
            while True:
                time.sleep(0.1)  # Keep the script running without invoking the main model
    except KeyboardInterrupt:
        live.stop()
        recorder.shutdown()
        print("\nExiting application due to keyboard interrupt")
