from flask import Flask, request, render_template_string, jsonify
import requests
import os

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
    background:#f7f9fc;
    display:flex;
    flex-direction:column;
    align-items:center;
    padding:50px;
}
button{
    background:#4CAF50;
    color:white;
    font-size:18px;
    padding:15px 30px;
    border:none;
    border-radius:8px;
    cursor:pointer;
}
button:disabled{
    background:#999;
    cursor:not-allowed;
}
.status{
    margin-top:30px;
    padding:20px;
    border-radius:8px;
    max-width:600px;
    word-wrap:break-word;
}
.success{
    background:#e0f7e0;
    color:#2f6627;
}
.error{
    background:#f8d7da;
    color:#842029;
}
.spinner{
    width:18px;
    height:18px;
    border:3px solid rgba(255,255,255,0.3);
    border-top-color:white;
    border-radius:50%;
    display:none;
    animation:spin 1s linear infinite;
}
@keyframes spin{
0%{transform:rotate(0deg);}
100%{transform:rotate(360deg);}
}
</style>
</head>

<body>
<h1>שליחת צינתוק לחבורה</h1>

<button id="sendBtn" onclick="sendCall()">
<span id="btnText">שלח צינתוק</span>
<div class="spinner" id="spinner"></div>
</button>

<div id="status"></div>

<script>
async function sendCall(){
    const btn=document.getElementById("sendBtn")
    const spinner=document.getElementById("spinner")
    const text=document.getElementById("btnText")
    const status=document.getElementById("status")

    btn.disabled=true
    spinner.style.display="inline-block"
    text.innerText="שולח..."
    status.innerHTML=""

    try{
        let response=await fetch("/send",{method:"POST"})
        let data=await response.json()
        if(data.success){
            status.innerHTML='<div class="status success">נשלח בהצלחה!<pre>'+data.response+'</pre></div>'
        }else{
            status.innerHTML='<div class="status error">שגיאה:<pre>'+data.response+'</pre></div>'
        }
    }catch(e){
        status.innerHTML='<div class="status error">שגיאת שרת</div>'
    }

    spinner.style.display="none"
    text.innerText="שלח צינתוק"
    btn.disabled=false
}
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/send", methods=["POST"])
def send():
    url="https://www.call2all.co.il/ym/api/RunTzintuk"
    params={
        "token":"WU1BUElL.apik_ZShiuO21zrq-HjlhwgD2cw.yeElOoMFJHG0lVG84H3rM6kk2IisyREB-U3QHsF7aHE"
    }
    try:
        r=requests.get(url, params=params, timeout=10)
        return jsonify({"success":r.status_code==200, "response":r.text})
    except Exception as e:
        return jsonify({"success":False, "response":str(e)})

if __name__=="__main__":
    port=int(os.environ.get("PORT", 10000))  # Render נותן פורט בסביבה
    app.run(host="0.0.0.0", port=port)
