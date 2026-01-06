from flask import Flask, request, abort
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
    return render_template('page.html') 




@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers.get('X-Hub-Signature-256')
    if signature is None or not verify_signature(request.data, signature):
        abort(400, "Signature invalide")

    # Ici tu peux lancer un script qui pull les changements
    os.system("cd /home/ton_username/ton_projet && git pull origin main")
    return "OK", 200

if __name__ == "__main__":
    app.run()
