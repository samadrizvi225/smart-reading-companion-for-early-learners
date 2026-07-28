# Smart Reading Companion for Early Learners

An AI-powered Python application designed to help early learners improve reading skills by analyzing speech, pronunciation accuracy, and speaking speed.

## Project Overview

Smart Reading Companion is a speech analysis system that allows users to enter a sentence, speak it aloud, and receive feedback based on their pronunciation accuracy and speaking speed.

The application uses AI-based speech transcription to convert voice into text and compares it with the user's written sentence to evaluate performance.

## Features

- Real-time voice recording
- AI-based speech transcription using Groq Whisper API
- Pronunciation accuracy evaluation using text similarity analysis
- Speaking speed calculation (Words Per Minute)
- Performance feedback based on accuracy and speed
- User-friendly graphical interface using Tkinter

## Technologies Used

- Python
- Tkinter (GUI)
- Groq Whisper API
- Speech Processing
- SoundDevice
- Levenshtein Similarity Algorithm

## How It Works

1. User enters a sentence in the application.
2. The user speaks the same sentence.
3. The recorded audio is converted into text using AI speech recognition.
4. The system compares the spoken text with the written text.
5. The application displays accuracy score, speaking speed, and feedback.

## Installation

1. Download the required libraries :

    ```bash
   pip install -r requirements.txt
   ```
2. Add your Groq API Key before running the application. 
