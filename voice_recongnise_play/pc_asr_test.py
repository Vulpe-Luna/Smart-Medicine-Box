import os
import time
import subprocess
from scipy.io.wavfile import read, write
from scipy.signal import resample
from aip import AipSpeech
import numpy as np

APP_ID = '123362614'
API_KEY = '1Q06Oqho4OCCVAV6IX67dD6P'
SECRET_KEY = 'rcbHIf7tdYSjj7zeWZbZdl1gfFJpaej7'

AUDIO_FILE = "asr_input.wav"
AUDIO_16K = "asr_input_16k.wav"

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


ALSA_DEVICE = "plughw:3,0"  
RECORD_RATE = 48000

def record_audio(duration=5):
    print(f"\n[*] Get ready... Recording starts in 1 second (Device: {ALSA_DEVICE}).")
    time.sleep(1)
    print(f"[*] >>> RECORDING NOW <<< Please speak for {duration} seconds...")

    command = [
        "arecord",
        "-D", ALSA_DEVICE,
        "-f", "S16_LE",
        "-r", str(RECORD_RATE),
        "-c", "1",
        "-d", str(duration),
        "-q",
        AUDIO_FILE
    ]

    try:
        subprocess.run(command, check=True)
        print("[+] Recording finished successfully.")
        return AUDIO_FILE
    except subprocess.CalledProcessError as e:
        print(f"[-] 'arecord' failed. Error: {e}")
        return None
    except FileNotFoundError:
        print("[-] 'arecord' command not found.")
        return None

def resample_wav(input_file, output_file, target_fs=16000):
    rate, data = read(input_file)
    if rate == target_fs:
        write(output_file, target_fs, data)
        return output_file
    duration = len(data) / rate
    target_len = int(duration * target_fs)
    resampled_data = resample(data, target_len)
    resampled_data = np.int16(resampled_data)
    write(output_file, target_fs, resampled_data)
    return output_file

def recognize_audio(audio_path):
    print("[*] Processing audio and sending to Baidu API...")
    try:
        if os.path.exists(AUDIO_16K):
            os.remove(AUDIO_16K)
        resample_wav(audio_path, AUDIO_16K)
        with open(AUDIO_16K, 'rb') as f:
            audio_data = f.read()
        result = client.asr(audio_data, 'wav', 16000, {'dev_pid': 1537})
        if result.get('err_no') == 0:
            text = result['result'][0]
            if text.strip():
                print(f"[+] Recognition Success: {text}")
                return text
            else:
                print("[-] Audio was empty or silent.")
                return None
        else:
            print(f"[-] Recognition Failed. Error code: {result}")
            return None
    except Exception as e:
        print(f"[-] Exception occurred: {e}")
        return None
    finally:
        if os.path.exists(AUDIO_16K):
            os.remove(AUDIO_16K)
