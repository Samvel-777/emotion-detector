"""Unit tests for the Emotion Detector application."""
import unittest

from EmotionDetection import emotion_detector


class TestEmotionDetection(unittest.TestCase):

    def test_emotion_detector_returns_formatted_output(self):
        result = emotion_detector("I love this product and I feel great")
        self.assertEqual(result["status_code"], 200)
        self.assertIn("emotion", result)
        self.assertIn("confidence", result)
        self.assertEqual(result["text"], "I love this product and I feel great")
        self.assertIsInstance(result["emotions"], list)
        self.assertGreaterEqual(result["confidence"], 0.0)

    def test_emotion_detector_blank_input_returns_400(self):
        result = emotion_detector("   ")
        self.assertEqual(result["status_code"], 400)
        self.assertEqual(result["error"], "Text input cannot be blank.")

    def test_package_imports_successfully(self):
        self.assertTrue(hasattr(emotion_detector, "__call__") or callable(emotion_detector))


if __name__ == "__main__":
    unittest.main()
