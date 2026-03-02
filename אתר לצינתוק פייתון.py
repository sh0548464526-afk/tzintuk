from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="he">
<head>
    <meta charset="UTF-8">
    <title>שליחת צינתוק</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f7f9fc;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 50px;
        }
        h1 {
            color: #333;
        }
        button {
            background-color: #4CAF50;
            color: white;
            font-size: 18px;
            padding: 15px 30px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: background 0.3s, transform 0.2s;
            position: relative;
            overflow: hidden;
        }
        button:hover {
            background-color: #45a049;
        }
        button:active {
            transform: scale(0.95);
        }
        .spinner {
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255,255,255,0.3);
            border-top-color: white;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            position: absolute;
            left: 10px;
            top: 50%;
            transform: translateY(-50%);
            display: none;
        }
        @keyframes spin {
            0% { transform: translateY(-50%) rotate(0deg); }
            100% { transform: translateY(-50%) rotate(360deg); }
        }
        .status {
            margin-top: 30px;
            padding: 20px;
            border-radius: 8px;
            background: #e0f7e0;
            color: #2f6627;
            max-width: 600px;
            word-wrap: break-word;
        }
        .error {
            background: #f8d7da;
            color: #842029;
        }
    </style>
</head>
<body>
    <h1>שליחת צינתוק לחבורה</h1>

    <form method="post" onsubmit="startLoading()">
        <button type="submit" name="send">
            <div class="spinner" id="spinner"></div>
            שלח צינתוק
        </button>
    </form>

    {% if sent %}
        <div class="status {% if http_code != 200 %}error{% endif %}">
            {% if http_code == 200 %}
                נשלח בהצלחה!<br>
                תשובת השרת:
                <pre>{{ response }}</pre>
            {% else %}
                שגיאה בשליחה, קוד HTTP: {{ http_code }}<br>
                תשובת השרת:
                <pre>{{ response }}</pre>
            {% endif %}
        </div>
    {% endif %}

    <script>
        function startLoading() {
            const spinner = document.getElementById('spinner');
            spinner.style.display = 'inline-block';
        }
    </script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    sent = False
    response_text = ""
    http_code = None

    if request.method == "POST" and "send" in request.form:
        url = "https://www.call2all.co.il/ym/api/RunTzintuk?token=WU1BUElL.apik_ZShiuO21zrq-HjlhwgD2cw.us6C00wSBgKBzX5wzE_z-VDb8TJWQx1kIrzyQO2J5kI"
        try:
            r = requests.post(url, data="")
            response_text = r.text
            http_code = r.status_code
        except Exception as e:
            response_text = str(e)
            http_code = 500

        sent = True

    return render_template_string(
        HTML_TEMPLATE,
        sent=sent,
        response=response_text,
        http_code=http_code
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)