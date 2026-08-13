import os
import requests
from flask import Flask, request, render_template_string

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>إرسال ملفات</title>
<style>
body {
    font-family: Arial;
    text-align: center;
    padding: 40px 20px;
    background: #f5f5f5;
}
.box {
    max-width: 500px;
    margin: auto;
    background: white;
    padding: 30px;
    border-radius: 15px;
}
input, button {
    width: 100%;
    margin-top: 20px;
    padding: 15px;
    box-sizing: border-box;
}
button {
    background: #229ED9;
    color: white;
    border: 0;
    border-radius: 8px;
    font-size: 18px;
}
</style>
</head>
<body>
<div class="box">
<h2>إرسال الملفات</h2>
<p>اختر الصور أو الملفات التي تريد إرسالها</p>

<form method="POST" enctype="multipart/form-data">
<input type="file" name="files" multiple required>
<button type="submit">إرسال الملفات</button>
</form>

{% if message %}
<p>{{ message }}</p>
{% endif %}
</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
@app.route("/upload/<person>", methods=["GET", "POST"])
def upload(person="غير محدد"):

    message = ""

    if request.method == "POST":

        files = request.files.getlist("files")

        for file in files:

            if file.filename:

                caption = f"👤 الشخص: {person}\n📎 الملف: {file.filename}"

                url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"

                response = requests.post(
                    url,
                    data={
                        "chat_id": CHAT_ID,
                        "caption": caption
                    },
                    files={
                        "document": (
                            file.filename,
                            file.stream,
                            file.mimetype
                        )
                    },
                    timeout=120
                )

                if not response.ok:
                    return "حدث خطأ أثناء إرسال الملف"

        message = "✅ تم إرسال الملفات بنجاح"

    return render_template_string(
        HTML,
        message=message
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
