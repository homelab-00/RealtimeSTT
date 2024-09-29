from RealtimeSTT import AudioToTextRecorder
from colorama import Fore, Back, Style
import colorama
import os
import pyautogui
import keyboard

# Global variables for controlling microphone state
mic_muted = True
full_sentences = []
displayed_text = ""

def clear_console():
    os.system('clear' if os.name == 'posix' else 'cls')

def unmute_mic():
    global mic_muted
    mic_muted = False
    print("Microphone Unmuted")

def mute_mic():
    global mic_muted
    mic_muted = True
    print("Microphone Muted")

def text_detected(text):
    global displayed_text, mic_muted
    sentences_with_style = [
        f"{Fore.YELLOW + sentence + Style.RESET_ALL if i % 2 == 0 else Fore.CYAN + sentence + Style.RESET_ALL} "
        for i, sentence in enumerate(full_sentences)
    ]
    new_text = "".join(sentences_with_style).strip() + " " + text if len(sentences_with_style) > 0 else text

    if new_text != displayed_text and not mic_muted:
        displayed_text = new_text
        clear_console()
        print(f"Language: {recorder.detected_language} (realtime: {recorder.detected_realtime_language})")
        print(displayed_text, end="", flush=True)

        # Send the text to Notepad
        pyautogui.click()  # Ensure the window is active (you may need to adapt this part)
        pyautogui.typewrite(displayed_text)

def process_text(text):
    full_sentences.append(text)
    text_detected("")

recorder_config = {
    'spinner': False,
    'model': 'tiny',
    'silero_sensitivity': 0.4,
    'webrtc_sensitivity': 2,
    'post_speech_silence_duration': 0.4,
    'min_length_of_recording': 0,
    'min_gap_between_recordings': 0,
    'enable_realtime_transcription': True,
    'realtime_processing_pause': 0.2,
    'realtime_model_type': 'tiny',
    'on_realtime_transcription_update': text_detected, 
    'silero_deactivity_detection': True,
}

if __name__ == '__main__':
    colorama.init()

    # Register global hotkeys
    keyboard.add_hotkey('ctrl+1', unmute_mic, suppress=True)
    keyboard.add_hotkey('ctrl+2', mute_mic, suppress=True)

    clear_console()
    print("Say something...", end="", flush=True)

    recorder = AudioToTextRecorder(**recorder_config)

    while True:
        if not mic_muted:
            recorder.text(process_text)