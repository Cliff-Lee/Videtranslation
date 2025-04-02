import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import whisper
import os

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

def start_transcription():
    input_file = file_entry.get()
    if not input_file:
        messagebox.showerror("Error", "Please select an input file.")
        return

    language = language_var.get()
    if language == "":
        messagebox.showerror("Error", "Please select the language.")
        return

    # Load the Whisper model (using the base model; adjust if needed)
    try:
        status_label.config(text="Loading model...")
        root.update_idletasks()
        model = whisper.load_model("base")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load model: {e}")
        return

    # Run transcription with translation; the selected language indicates the source language.
    try:
        status_label.config(text="Transcribing and translating...")
        root.update_idletasks()
        result = model.transcribe(input_file, task="translate", language=language)
    except Exception as e:
        messagebox.showerror("Error", f"Transcription failed: {e}")
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

# --- Language selection ---
tk.Label(root, text="Source Language:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
language_var = tk.StringVar()
language_combobox = ttk.Combobox(root, textvariable=language_var, state="readonly")
# Define a simple mapping of display names to language codes.
languages = {
    "Chinese": "zh",
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Japanese": "ja",
    "Korean": "ko"
}
language_combobox['values'] = list(languages.keys())
language_combobox.grid(row=1, column=1, padx=5, pady=5, sticky="w")
language_combobox.current(0)  # Default to "Chinese"

def get_language_code():
    """Convert human-readable language to language code."""
    selected = language_var.get()
    return languages.get(selected, selected)

# --- Start button ---
def start_transcription_wrapper():
    # Set language variable to code for Whisper
    lang_code = get_language_code()
    language_var.set(lang_code)
    start_transcription()

start_button = tk.Button(root, text="Start Translation", command=start_transcription_wrapper)
start_button.grid(row=2, column=1, padx=5, pady=15)

# --- Status label ---
status_label = tk.Label(root, text="Ready", fg="blue")
status_label.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

root.mainloop()
