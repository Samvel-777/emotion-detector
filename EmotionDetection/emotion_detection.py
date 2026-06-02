"""Emotion detection logic for the EmotionDetector project."""
import os
import re

try:
    from ibm_watson import NaturalLanguageUnderstandingV1
    from ibm_watson.natural_language_understanding_v1 import Features, EmotionOptions
    from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
    WATSON_AVAILABLE = True
except ImportError:
    WATSON_AVAILABLE = False


def _fallback_emotion_scores(text):
    normalized = text.strip().lower()
    scores = {
        "joy": 0.0,
        "sadness": 0.0,
        "anger": 0.0,
        "fear": 0.0,
        "disgust": 0.0,
    }
    if not normalized:
        return scores

    positive_keywords = ["happy", "joy", "love", "great", "good", "awesome", "excellent"]
    negative_keywords = ["sad", "anger", "angry", "hate", "terrible", "bad", "worst"]
    fear_keywords = ["scared", "afraid", "fear", "nervous", "worried"]
    disgust_keywords = ["disgust", "gross", "nausea", "sick", "hate"]

    for keyword in positive_keywords:
        if keyword in normalized:
            scores["joy"] += 0.2

    for keyword in negative_keywords:
        if keyword in normalized:
            scores["sadness"] += 0.2
            scores["anger"] += 0.2

    for keyword in fear_keywords:
        if keyword in normalized:
            scores["fear"] += 0.3

    for keyword in disgust_keywords:
        if keyword in normalized:
            scores["disgust"] += 0.3

    if scores == {key: 0.0 for key in scores}:
        scores["joy"] = 0.5
        scores["sadness"] = 0.2

    total = sum(scores.values())
    if total > 0:
        scores = {emotion: round(score / total, 2) for emotion, score in scores.items()}
    return scores


def _analyze_with_watson(text):
    if not WATSON_AVAILABLE:
        raise RuntimeError("IBM Watson SDK is not available")

    api_key = os.getenv("WATSON_NLU_APIKEY")
    service_url = os.getenv("WATSON_NLU_URL")
    if not api_key or not service_url:
        raise RuntimeError("Watson NLU credentials are not configured in the environment")

    authenticator = IAMAuthenticator(api_key)
    nlu = NaturalLanguageUnderstandingV1(version="2021-08-01", authenticator=authenticator)
    nlu.set_service_url(service_url)
    analysis = nlu.analyze(text=text, features=Features(emotion=EmotionOptions())).get_result()
    emotion_scores = analysis.get("emotion", {}).get("document", {}).get("emotion", {})

    if not emotion_scores:
        raise RuntimeError("Watson NLU returned no emotion scores")

    return {emotion: round(float(score), 2) for emotion, score in emotion_scores.items()}


def emotion_detector(text):
    """Analyze emotion from a text input and return a formatted response."""
    if text is None or not isinstance(text, str) or not text.strip():
        return {
            "status_code": 400,
            "error": "Text input cannot be blank.",
            "text": text,
        }

    try:
        emotion_scores = _analyze_with_watson(text)
    except Exception:
        emotion_scores = _fallback_emotion_scores(text)

    top_emotion = max(emotion_scores, key=emotion_scores.get)
    confidence = emotion_scores.get(top_emotion, 0.0)

    formatted = {
        "status_code": 200,
        "text": text,
        "emotion": top_emotion,
        "confidence": confidence,
        "emotions": [
            {"label": label, "score": score}
            for label, score in sorted(emotion_scores.items(), key=lambda item: item[1], reverse=True)
        ],
    }
    return formatted
