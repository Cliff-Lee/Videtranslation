Whisper Translator GUI

A simple graphical user interface (GUI) for OpenAI Whisper that allows you to transcribe and translate audio or video files. This application supports choosing an input language (the language spoken in the media file) and an output language for the subtitles (SRT file). For translation, it uses Whisper’s built‑in translation when output is English or the [googletrans](https://pypi.org/project/googletrans/) library for other language pairs.

Features

- File Browsing: Easily select your video or audio file.
- Input & Output Language Selection: Choose any supported input language and your desired output language.
- Transcription & Translation: 
  - If the output language is English, the built‑in Whisper translation is used.
  - Otherwise, the tool first transcribes the audio and then translates the text using googletrans.
- Duplicate Filtering: Consecutive duplicate segments are filtered out.
- SRT File Output: Save the resulting transcription/translation as an SRT file.

Prerequisites

- Python 3.7+
- FFmpeg: Whisper uses FFmpeg for audio extraction.  

  Install it on Ubuntu with:

  sudo apt update
  sudo apt install ffmpeg
