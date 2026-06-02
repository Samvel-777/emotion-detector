"""Flask web deployment for the Emotion Detector application."""
from flask import Flask, render_template_string, request

from EmotionDetection import emotion_detector

app = Flask(__name__)

HOME_PAGE = """
<!doctype html>
<title>Emotion Detector</title>
<h1>Emotion Detector</h1>
<form action="/analyze" method="post">
  <label for="text">Enter text to analyze:</label><br>
  <textarea id="text" name="text" rows="4" cols="50"></textarea><br>
  <button type="submit">Analyze Emotion</button>
</form>
{% if error %}
  <p style="color:red;">{{ error }}</p>
{% endif %}
{% if result %}
  <h2>Result</h2>
  <pre>{{ result }}</pre>
{% endif %}
"""


@app.route("/", methods=["GET"])
def home():
    """Render the homepage for emotion detection input."""
    return render_template_string(HOME_PAGE, error=None, result=None)


@app.route("/analyze", methods=["POST"])
def analyze():
    """Analyze submitted text and render the result page."""
    text = request.form.get("text", "")
    if not text.strip():
        return (
            render_template_string(
                HOME_PAGE,
                error="Input text cannot be blank.",
                result=None,
            ),
            400,
        )

    result = emotion_detector(text)
    return render_template_string(HOME_PAGE, error=None, result=result)


def static_code_analysis_command():
    """Return the static analysis command used for this server module."""
    return "python -m pylint server.py"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
