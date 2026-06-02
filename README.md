# Emotion Detector

This project implements an emotion detection application using a Watson-style NLP pipeline and a Flask web deployment.

Files included:
- `EmotionDetection/emotion_detection.py`: main emotion detection logic with Watson NLP compatibility and fallback analysis.
- `EmotionDetection/__init__.py`: package initializer for `EmotionDetection`.
- `server.py`: Flask web application with blank-input error handling.
- `test_emotion_detection.py`: unit tests for the emotion detector.
- `requirements.txt`: required Python dependencies.

## Usage

1. Install dependencies:
   `pip install -r requirements.txt`
2. Run tests:
   `python -m unittest test_emotion_detection.py`
3. Start Flask app:
   `python server.py`

## Notes

- The code includes a Watson NLP integration path via `ibm_watson` if available.
- Blank input returns a `400` result with a clear error message.
- Static analysis is performed using `pylint server.py`.
