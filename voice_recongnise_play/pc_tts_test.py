import os
import subprocess
from aip import AipSpeech

APP_ID = '123362614'
API_KEY = '1Q06Oqho4OCCVAV6IX67dD6P'
SECRET_KEY = 'rcbHIf7tdYSjj7zeWZbZdl1gfFJpaej7'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

def synthesize_audio(text, output_file="tts_output.wav"):
    print(f"[*] Preparing to synthesize: '{text[:30]}...'")
    try:
        # aue: 6 requests WAV format. vol: 15 is MAX volume.
        result = client.synthesis(text, 'zh', 1, {
            'vol': 15, 
            'per': 4,
            'spd': 5,
            'aue': 6  
        })
        if not isinstance(result, dict):
            with open(output_file, 'wb') as f:
                f.write(result)
            print("[+] Synthesis successful (WAV format).")
            return True
        else:
            print(f"[-] Synthesis failed: {result}")
            return False
    except Exception as e:
        print(f"[-] Exception: {e}")
        return False

def play_audio(audio_file):
    print("[*] ?? Playing audio response...")
    
    # Ultimate player fallback sequence
    players = [
        # 1. ffplay: The most robust player (auto-converts sample rates)
        ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", audio_file],
        # 2. mplayer: Strong alternative
        ["mplayer", "-really-quiet", audio_file],
        # 3. paplay: PulseAudio native
        ["paplay", audio_file],
        # 4. aplay: Raw ALSA as absolute last resort
        ["aplay", "-q", audio_file]
    ]
    
    success = False
    for cmd in players:
        try:
            subprocess.run(cmd, check=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            print(f"[+] Playback finished using '{cmd[0]}'.")
            success = True
            break  # Exit loop if played successfully
        except (FileNotFoundError, subprocess.CalledProcessError):
            continue # Try the next player in the list
            
    if not success:
        print("[-] All playback methods failed. Please check your speaker connection and VNC volume settings.")
