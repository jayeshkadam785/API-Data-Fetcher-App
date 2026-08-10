from flask import Flask, render_template_string
import requests

app = Flask(__name__)

PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Random Joke Fetcher</title>
<style>
  * { box-sizing: border-box; }
  body {
    font-family: 'Segoe UI', Arial, sans-serif;
    background: #0d1117;
    color: #e6edf3;
    display: flex;
    justify-content: center;
    padding: 40px 15px;
    margin: 0;
  }
  .card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 30px;
    width: 100%;
    max-width: 420px;
    text-align: center;
  }
  h1 { font-size: 22px; color: #58a6ff; margin-bottom: 25px; }
  .joke-box {
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 20px;
    margin-top: 20px;
    text-align: left;
    min-height: 80px;
  }
  .joke-box p { margin: 6px 0; line-height: 1.5; font-size: 15px; }
  .setup { color: #8b949e; }
  .punchline { color: #58a6ff; font-weight: bold; margin-top: 10px; }
  a.button {
    display: inline-block;
    margin-top: 20px;
    padding: 12px 24px;
    background: #238636;
    color: #fff;
    text-decoration: none;
    border-radius: 6px;
    font-size: 15px;
  }
  a.button:hover { background: #2ea043; }
  .error { color: #f85149; margin-top: 12px; font-size: 14px; }
</style>
</head>
<body>
  <div class="card">
    <h1>🎭 Random Joke Fetcher</h1>

    {% if error %}
      <div class="error">{{ error }}</div>
    {% else %}
      <div class="joke-box">
        {% if joke_type == 'single' %}
          <p>{{ joke }}</p>
        {% else %}
          <p class="setup">{{ setup }}</p>
          <p class="punchline">{{ delivery }}</p>
        {% endif %}
      </div>
    {% endif %}

    <a class="button" href="/">Get Another Joke</a>
  </div>
</body>
</html>
"""


def fetch_joke():
    url = "https://v2.jokeapi.dev/joke/Any?safe-mode"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


@app.route("/")
def index():
    try:
        data = fetch_joke()
        if data.get("type") == "single":
            return render_template_string(
                PAGE, error=None, joke_type="single", joke=data.get("joke", "")
            )
        else:
            return render_template_string(
                PAGE, error=None, joke_type="twopart",
                setup=data.get("setup", ""), delivery=data.get("delivery", "")
            )
    except Exception:
        return render_template_string(
            PAGE, error="Could not fetch a joke right now. Please try again.",
            joke_type=None, joke=None, setup=None, delivery=None
        )


if __name__ == "__main__":
    app.run(debug=True)
