import os
import time
from pc_asr_test import record_audio, recognize_audio
from pc_tts_test import synthesize_audio, play_audio
from deepseek_api import ask_pillbox

def main():
    print("=" * 50)
    print("    Smart Medicine Box - Voice Health Assistant    ")
    print("=" * 50)
    print("Flow: Record -> Baidu ASR -> DeepSeek -> Baidu TTS -> Play")
    print("Press Ctrl+C to exit at any time.\n")

    while True:
        try:
            print("\n" + "-"*40)
            print("--- Step 1: Voice Input ---")
            audio_path = record_audio(duration=5)

            if not audio_path or not os.path.exists(audio_path):
                print("[-] Audio missing, retrying in 2 seconds...")
                time.sleep(2)
                continue

            print("\n--- Step 2: Speech to Text ---")
            symptom_text = recognize_audio(audio_path)
            if not symptom_text:
                print("[-] Could not hear clearly, retrying...")
                continue

            print(f"\n[You Asked]: {symptom_text}")

            print("\n--- Step 3: DeepSeek Analysis ---")
            answer = ask_pillbox(symptom_text)
            print(f"\n[AI Reply]:\n{answer}\n")

            print("\n--- Step 4: Text to Speech ---")
            if synthesize_audio(answer, "tts_output.wav"):
                play_audio("tts_output.wav")
                if os.path.exists("tts_output.wav"):
                    os.remove("tts_output.wav")
            else:
                print("[-] TTS Failed. Check logs above.")

            if os.path.exists(audio_path):
                os.remove(audio_path)

            print("\n" + "-"*40)
            user_input = input("Type 'q' to quit, or press ENTER to ask another question: ")
            if user_input.strip().lower() == 'q':
                print("[+] Goodbye!")
                break

        except KeyboardInterrupt:
            print("\n\n[+] System closed by user.")
            break
        except Exception as e:
            print(f"[-] Global Exception: {e}")
            time.sleep(2)

if __name__ == "__main__":
    main()
