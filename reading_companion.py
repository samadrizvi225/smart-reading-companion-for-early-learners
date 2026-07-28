import os
import tkinter as tk
from tkinter import messagebox
import sounddevice as sd
from scipy.io.wavfile import write
from groq import Groq
from Levenshtein import ratio

API_KEY = "PASTE_YOUR_GROQ_API_KEY_HERE"

try:
    SCRIPT_DIR = os.path.dirname(__file__)
except NameError:
    SCRIPT_DIR = os.getcwd()

AUDIO_FILE = os.path.join(SCRIPT_DIR, "voice.wav")

RECORD_SECONDS = 5
SAMPLE_RATE = 44100

BG_COLOR = "#0F172A"
CARD_COLOR = "#1E293B"
BTN_COLOR = "#2563EB"
BTN_HOVER = "#1D4ED8"

TEXT_COLOR = "#F8FAFC"
ACCENT_COLOR = "#38BDF8"

TITLE_FONT = ("Segoe UI", 32, "bold")
TEXT_FONT = ("Segoe UI", 18)
BUTTON_FONT = ("Segoe UI", 16, "bold")
RESULT_FONT = ("Segoe UI", 20)

def record_audio():

    try:

        messagebox.showinfo(
            "Recording",
            f"Recording will start for {RECORD_SECONDS} seconds.\nSpeak clearly!"
        )

        recording = sd.rec(
            int(RECORD_SECONDS * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype='int16'
        )

        sd.wait()

        write(AUDIO_FILE, SAMPLE_RATE, recording)

        return True, None

    except Exception as e:
        return False, str(e)

def transcribe_audio():

    if not API_KEY or API_KEY.startswith("PASTE"):
        return None, "Please enter your Groq API Key."

    try:

        client = Groq(api_key=API_KEY)

        with open(AUDIO_FILE, "rb") as f:
            audio_bytes = f.read()

        result = client.audio.transcriptions.create(
            file=(os.path.basename(AUDIO_FILE), audio_bytes),
            model="whisper-large-v3"
        )

        if hasattr(result, "text"):
            return result.text, None

        if isinstance(result, dict) and "text" in result:
            return result["text"], None

        return str(result), None

    except Exception as e:
        return None, str(e)

def calculate_wpm(text):

    words = text.split()

    if not words:
        return 0

    minutes = RECORD_SECONDS / 60.0

    return round(len(words) / minutes, 2)

root = tk.Tk()

root.title("SMART READING COMPANION")
root.geometry("1400x800")
root.configure(bg=BG_COLOR)

root.state("zoomed")

typed_text = ""

def hover_on(e):
    e.widget["bg"] = BTN_HOVER

def hover_off(e):
    e.widget["bg"] = BTN_COLOR

def create_button(parent, text, command, width=15):

    btn = tk.Button(
        parent,
        text=text,
        command=command,
        font=BUTTON_FONT,
        bg=BTN_COLOR,
        fg="white",
        activebackground=BTN_HOVER,
        activeforeground="white",
        relief="flat",
        padx=12,
        pady=10,
        cursor="hand2",
        width=width
    )

    btn.bind("<Enter>", hover_on)
    btn.bind("<Leave>", hover_off)

    return btn

slide1 = tk.Frame(root, bg=BG_COLOR)
slide2 = tk.Frame(root, bg=BG_COLOR)
slide3 = tk.Frame(root, bg=BG_COLOR)
slide4 = tk.Frame(root, bg=BG_COLOR)

for slide in (slide1, slide2, slide3, slide4):
    slide.place(relwidth=1, relheight=1)

def show(frame):
    frame.tkraise()

card1 = tk.Frame(slide1, bg=CARD_COLOR)

card1.place(
    relx=0.5,
    rely=0.5,
    anchor="center",
    relwidth=0.75,
    relheight=0.75
)

tk.Label(
    card1,
    text="SMART READING\nCOMPANION FOR EARLY LEARNERS",
    font=TITLE_FONT,
    fg=ACCENT_COLOR,
    bg=CARD_COLOR,
    pady=100,
    justify="center"
).pack()

create_button(
    card1,
    "Start",
    lambda: show(slide2),
    width=20
).pack(pady=20)

create_button(
    card1,
    "Exit",
    root.destroy,
    width=20
).pack()

card2 = tk.Frame(slide2, bg=CARD_COLOR)

card2.place(
    relx=0.5,
    rely=0.5,
    anchor="center",
    relwidth=0.75,
    relheight=0.75
)

tk.Label(
    card2,
    text="Write the sentence you want to speak",
    font=("Segoe UI", 24, "bold"),
    fg=ACCENT_COLOR,
    bg=CARD_COLOR,
    pady=30
).pack()

entry_text = tk.Text(
    card2,
    height=5,
    width=60,
    font=("Segoe UI", 18),
    bg="#334155",
    fg="white",
    insertbackground="white",
    relief="flat"
)

entry_text.pack(pady=20)

def on_next_to_speak():

    global typed_text

    typed_text = entry_text.get("1.0", "end").strip()

    if not typed_text:

        messagebox.showwarning(
            "Input Required",
            "Please write something first."
        )

        return

    label_to_speak.config(
        text=f'Now try to speak:\n\n"{typed_text}"'
    )

    show(slide3)

btn_frame = tk.Frame(card2, bg=CARD_COLOR)
btn_frame.pack(pady=20)

create_button(
    btn_frame,
    "Next",
    on_next_to_speak
).grid(row=0, column=0, padx=10)

create_button(
    btn_frame,
    "Back",
    lambda: show(slide1)
).grid(row=0, column=1, padx=10)

card3 = tk.Frame(slide3, bg=CARD_COLOR)

card3.place(
    relx=0.5,
    rely=0.5,
    anchor="center",
    relwidth=0.75,
    relheight=0.75
)

label_to_speak = tk.Label(
    card3,
    text="",
    font=("Segoe UI", 24, "bold"),
    fg=TEXT_COLOR,
    bg=CARD_COLOR,
    wraplength=1000,
    pady=50
)

label_to_speak.pack()

status_label = tk.Label(
    card3,
    text="",
    font=TEXT_FONT,
    fg=ACCENT_COLOR,
    bg=CARD_COLOR
)

status_label.pack(pady=20)

def on_speak_click():

    status_label.config(text="🎤 Recording...")
    root.update()

    ok, err = record_audio()

    if not ok:
        status_label.config(text=f"Recording Error : {err}")
        return

    status_label.config(text="🧠 Transcribing...")
    root.update()

    transcription, terr = transcribe_audio()

    if terr:
        status_label.config(text=f"Transcription Error : {terr}")
        return

    accuracy = round(
        ratio(
            typed_text.lower(),
            transcription.lower()
        ) * 100,
        2
    )

    wpm = calculate_wpm(transcription)

    if accuracy >= 70:
        feedback = "🌟 Excellent! Keep it up"
    else:
        feedback = "😊 Try Again"

    if wpm < 80:
        speed_msg = "Your speed is slow"
    elif 80 <= wpm <= 150:
        speed_msg = "Good speaking speed"
    else:
        speed_msg = "Too fast! Slow down"

    written_label.config(
        text=f"Written Text:\n{typed_text}"
    )

    trans_label.config(
        text=f"Recognized Speech:\n{transcription}"
    )

    grade_label.config(
        text=f"Accuracy : {accuracy}%"
    )

    speed_label.config(
        text=f"Voice Speed : {wpm} WPM\n{speed_msg}"
    )

    feedback_label.config(
        text=feedback
    )

    status_label.config(text="✅ Completed")

    show(slide4)

create_button(
    card3,
    "Speak",
    on_speak_click,
    width=20
).pack(pady=20)

create_button(
    card3,
    "Back",
    lambda: show(slide2),
    width=20
).pack()

card4 = tk.Frame(slide4, bg=CARD_COLOR)

card4.place(
    relx=0.5,
    rely=0.5,
    anchor="center",
    relwidth=0.80,
    relheight=0.85
)

tk.Label(
    card4,
    text="RESULTS",
    font=("Segoe UI", 30, "bold"),
    fg=ACCENT_COLOR,
    bg=CARD_COLOR,
    pady=20
).pack()

written_label = tk.Label(
    card4,
    text="",
    font=RESULT_FONT,
    fg=TEXT_COLOR,
    bg=CARD_COLOR,
    wraplength=1000,
    justify="center"
)

written_label.pack(pady=15)

trans_label = tk.Label(
    card4,
    text="",
    font=RESULT_FONT,
    fg=TEXT_COLOR,
    bg=CARD_COLOR,
    wraplength=1000,
    justify="center"
)

trans_label.pack(pady=15)

grade_label = tk.Label(
    card4,
    text="",
    font=("Segoe UI", 22, "bold"),
    fg="#22C55E",
    bg=CARD_COLOR
)

grade_label.pack(pady=10)

speed_label = tk.Label(
    card4,
    text="",
    font=("Segoe UI", 20),
    fg="#FACC15",
    bg=CARD_COLOR
)

speed_label.pack(pady=10)

feedback_label = tk.Label(
    card4,
    text="",
    font=("Segoe UI", 24, "bold"),
    fg="#38BDF8",
    bg=CARD_COLOR
)

feedback_label.pack(pady=25)

create_button(
    card4,
    "Try Again",
    lambda: show(slide1),
    width=20
).pack(pady=20)

show(slide1)

root.mainloop()