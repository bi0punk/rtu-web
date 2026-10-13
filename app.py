import logging
import os
import re
import shlex

import paramiko
from dotenv import load_dotenv
from flask import Flask, abort, jsonify, render_template, request

load_dotenv()

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

SSH_HOST = os.environ.get("SSH_HOST")
SSH_USER = os.environ.get("SSH_USER")
SSH_PASSWORD = os.environ.get("SSH_PASSWORD")
API_TOKEN = os.environ.get("API_TOKEN")

if not all([SSH_HOST, SSH_USER, SSH_PASSWORD, API_TOKEN]):
    raise RuntimeError(
        "SSH_HOST, SSH_USER, SSH_PASSWORD and API_TOKEN must be set in environment or .env file"
    )


def execute_ssh_command(command):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.RejectPolicy())
    try:
        client.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode()
        return output
    except Exception as e:
        app.logger.error("SSH command failed: %s", e)
        return None
    finally:
        client.close()


def require_auth():
    token = request.headers.get("X-API-Token")
    if not token or token != API_TOKEN:
        abort(401, description="Unauthorized")


@app.route("/")
def index():
    return render_template("index.html", api_token=API_TOKEN)


@app.route("/messages", methods=["GET"])
def get_messages():
    require_auth()
    messages = execute_ssh_command("termux-sms-list")
    if messages is None:
        return jsonify({"error": "SSH command failed"}), 502
    return jsonify({"messages": messages})


@app.route("/send", methods=["POST"])
def send_message():
    require_auth()
    data = request.json
    number = data.get("number")
    text = data.get("text")
    if not number or not text:
        return jsonify({"error": "Número y texto son requeridos"}), 400
    if not re.match(r"^\+?\d{7,15}$", number):
        return jsonify({"error": "Número inválido"}), 400
    if len(text) > 1600:
        return jsonify({"error": "Texto demasiado largo (máx 1600 caracteres)"}), 400
    command = f"termux-sms-send -n {shlex.quote(number)} {shlex.quote(text)}"
    response = execute_ssh_command(command)
    if response is None:
        return jsonify({"error": "SSH command failed"}), 502
    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
