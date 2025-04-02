Whisper Translator GUI
A simple Python-based GUI tool that leverages OpenAI’s Whisper model to transcribe and translate media files into SRT subtitle files. This application provides an easy-to-use interface for converting audio or video content into time-stamped subtitles, with support for multiple source languages.

Features
Media File Input:
Browse and select media files (e.g., MP4, MP3, MKV, WAV).

Language Selection:
Choose the source language from a pre-defined list (Chinese, English, Spanish, French, German, Japanese, Korean). The selected language is automatically converted to its corresponding language code for the Whisper model.

Transcription & Translation:
Utilizes the Whisper model (base version) to transcribe and translate the selected media file.

SRT Subtitle Generation:
Processes the transcription into SRT format, including:

Time formatting into HH:MM:SS,mmm

Filtering out consecutive duplicate subtitle segments

Allowing the user to specify the save location for the generated subtitle file

User-friendly Interface:
Built with Tkinter, providing a straightforward GUI with status updates and error messages.

Prerequisites
Python 3.7+
Ensure you have Python installed on your system.

Tkinter:
Typically included with standard Python installations. If not, install via your system package manager.

Whisper Library:
Install OpenAI’s Whisper via pip:


pip install openai-whisper
Note: Whisper may require additional dependencies like ffmpeg for processing audio/video files. Ensure ffmpeg is installed and properly configured on your system.

Other Python Libraries:
The script uses standard libraries (os) and Tkinter modules (tkinter, filedialog, messagebox, ttk).

Installation
Clone or Download the Repository:

git clone https://github.com/yourusername/whisper-translator-gui.git
cd whisper-translator-gui

Set Up a Virtual Environment (Optional but Recommended):
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

Install Required Packages:
pip install openai-whisper

Verify Dependencies:
Make sure ffmpeg is installed and accessible in your system’s PATH.

Usage
Run the Script:
python your_script.py

Replace your_script.py with the actual filename if different.

Using the GUI:
Input File: Click the Browse button to select your media file.

Source Language: Choose the language from the drop-down list. The default language is set to Chinese.

Start Translation: Click the Start Translation button to begin the transcription and translation process.

Save SRT File: When prompted, choose the location and filename to save the generated SRT subtitle file.

Status Updates: The status label at the bottom will update you on the current process (loading model, transcribing, etc.) or display error messages if something goes wrong.

Customization
Model Selection:
The script currently loads the "base" Whisper model. To use a different model, modify the following line:

python
model = whisper.load_model("base")
Replace "base" with your preferred model variant (e.g., "small", "medium", or "large").

Language Mapping:
The list of available languages and their corresponding codes is defined in the languages dictionary. Add or modify entries as needed.

Error Handling
The GUI displays error messages for missing inputs or issues during model loading, transcription, or file saving.

Ensure your media files are valid and that ffmpeg is correctly installed to avoid transcription errors.

Credits
OpenAI Whisper:
This project utilizes the Whisper model for advanced transcription and translation.

Tkinter:
Provides the GUI framework for the application.

Feel free to fork, contribute, or open issues if you encounter any problems or have suggestions for improvements.

License
Distributed under the MIT License. See LICENSE for more information.
