from flask import Flask, request, abort, render_template
import hmac
import hashlib
import os

app = Flask(__name__)

# SECRET = le même que tu mettras dans GitHub Webhook
SECRET = os.environ.get("GITHUB_SECRET", "ton_secret")

def verify_signature(payload, signature):
    mac = hmac.new(SECRET.encode(), msg=payload, digestmod=hashlib.sha256)
    expected_signature = 'sha256=' + mac.hexdigest()
    return hmac.compare_digest(expected_signature, signature)

@app.route("/page")
def mypage():
    return render_template('page.html')  # Assure-toi que page.html est dans un dossier /templates

@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers.get('X-Hub-Signature-256')
    if signature is None or not verify_signature(request.data, signature):
        abort(400, "Signature invalide")

    # Pull automatique depuis GitHub
    os.system("cd /home/bio220EU/test_webhooks && git pull origin main")
    return "OK", 200

@app.route("/")
def home():
    return "<h1>Serveur en ligne !</h1>"

if __name__ == "__main__":
    app.run()

