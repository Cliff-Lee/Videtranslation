import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import whisper
import os

# For translation (if needed)
try:
    from googletrans import Translator
except ImportError:
    messagebox.showerror("Missing Dependency", "Please install googletrans using:\npip install googletrans==4.0.0rc1")
    raise

def format_time(seconds):
    """Convert seconds to SRT time format: HH:MM:SS,mmm"""
    msec = int((seconds - int(seconds)) * 1000)
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02d}:{m:02d}:{s:02d},{msec:03d}"

def browse_file():
    """Open a dialog to choose a media file."""
    filename = filedialog.askopenfilename(
        title="Select video or audio file",
        filetypes=[("Media files", "*.mp4 *.mp3 *.mkv *.wav"), ("All files", "*.*")]
    )
    if filename:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, filename)

def save_file_dialog():
    """Open a dialog to choose where to save the SRT file."""
    return filedialog.asksaveasfilename(
        defaultextension=".srt",
        filetypes=[("SRT files", "*.srt"), ("All files", "*.*")]
    )

def start_transcription(input_lang, output_lang):
    input_file = file_entry.get()
    if not input_file:
        messagebox.showerror("Error", "Please select an input file.")
        return

    # Load the Whisper model (using the base model; adjust if needed)
    try:
        status_label.config(text="Loading model...")
        root.update_idletasks()
        model = whisper.load_model("base")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load model: {e}")
        return

    # Determine whether to translate using Whisper or using googletrans
    # If input and output languages are the same, simply transcribe.
    # If output is English and input is not, use Whisper's built-in translate.
    # Otherwise, transcribe and then translate with googletrans.
    try:
        if input_lang == output_lang:
            status_label.config(text="Transcribing...")
            root.update_idletasks()
            result = model.transcribe(input_file, task="transcribe", language=input_lang)
        elif output_lang == "en":
            status_label.config(text="Translating to English using Whisper...")
            root.update_idletasks()
            result = model.transcribe(input_file, task="translate", language=input_lang)
        else:
            # First, transcribe in the input language.
            status_label.config(text="Transcribing...")
            root.update_idletasks()
            result = model.transcribe(input_file, task="transcribe", language=input_lang)
            # Then translate each segment using googletrans.
            translator = Translator()
            status_label.config(text="Translating segments...")
            root.update_idletasks()
            for segment in result["segments"]:
                original_text = segment["text"].strip()
                # Translate from input_lang to output_lang.
                translation = translator.translate(original_text, src=input_lang, dest=output_lang)
                segment["text"] = translation.text
    except Exception as e:
        messagebox.showerror("Error", f"Processing failed: {e}")
        return

    # Filter out consecutive duplicate segments
    filtered_segments = []
    prev_text = ""
    for segment in result["segments"]:
        current_text = segment["text"].strip()
        if current_text == prev_text:
            continue
        filtered_segments.append(segment)
        prev_text = current_text

    # Ask where to save the SRT file
    srt_file = save_file_dialog()
    if not srt_file:
        return

    # Write the SRT file using the filtered segments
    try:
        with open(srt_file, "w", encoding="utf-8") as f:
            for i, segment in enumerate(filtered_segments, start=1):
                start_time = format_time(segment["start"])
                end_time = format_time(segment["end"])
                text = segment["text"].strip()
                f.write(f"{i}\n{start_time} --> {end_time}\n{text}\n\n")
        status_label.config(text=f"Subtitle saved to {srt_file}")
        messagebox.showinfo("Success", f"Subtitle saved to:\n{srt_file}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save SRT file: {e}")

# Create the main window
root = tk.Tk()
root.title("Whisper Translator GUI")

# --- File selection ---
tk.Label(root, text="Input File:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
file_entry = tk.Entry(root, width=50)
file_entry.grid(row=0, column=1, padx=5, pady=5)
browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.grid(row=0, column=2, padx=5, pady=5)

# Define language mapping (display names to language codes)
languages = {
    "Chinese": "zh",
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Japanese": "ja",
    "Korean": "ko"
}

# --- Input Language selection ---
tk.Label(root, text="Input Language:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
input_language_var = tk.StringVar()
input_language_combobox = ttk.Combobox(root, textvariable=input_language_var, state="readonly")
input_language_combobox['values'] = list(languages.keys())
input_language_combobox.grid(row=1, column=1, padx=5, pady=5, sticky="w")
input_language_combobox.current(0)  # Default to "Chinese"

# --- Output Language selection ---
tk.Label(root, text="Output Language:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
output_language_var = tk.StringVar()
output_language_combobox = ttk.Combobox(root, textvariable=output_language_var, state="readonly")
output_language_combobox['values'] = list(languages.keys())
output_language_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="w")
# Default to English for output translation
output_language_combobox.set("English")

def get_language_code(display_name):
    """Convert human-readable language to language code."""
    return languages.get(display_name, display_name)

# --- Start button ---
def start_transcription_wrapper():
    # Get language codes from combobox selections
    input_lang_code = get_language_code(input_language_var.get())
    output_lang_code = get_language_code(output_language_var.get())
    start_transcription(input_lang_code, output_lang_code)

start_button = tk.Button(root, text="Start Processing", command=start_transcription_wrapper)
start_button.grid(row=3, column=1, padx=5, pady=15)

# --- Status label ---
status_label = tk.Label(root, text="Ready", fg="blue")
status_label.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

root.mainloop()

