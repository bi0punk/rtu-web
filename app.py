from flask import Flask, request, jsonify, render_template
import paramiko

app = Flask(__name__)

# Configuración SSH
HOST = "IP_DE_TU_TELEFONO"
USER = "usuario_termux"
PASSWORD = "contraseña"

def execute_ssh_command(command):
    """Ejecuta un comando en Termux vía SSH y devuelve la salida."""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(HOST, username=USER, password=PASSWORD)
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode()
        return output
    except Exception as e:
        return str(e)
    finally:
        client.close()

@app.route("/")
def index():
    """Página principal con interfaz web."""
    return render_template("index.html")

@app.route("/messages", methods=["GET"])
def get_messages():
    """Obtiene los mensajes SMS del teléfono."""
    messages = execute_ssh_command("termux-sms-list")
    return jsonify({"messages": messages})

@app.route("/send", methods=["POST"])
def send_message():
    """Envía un mensaje SMS desde el teléfono."""
    data = request.json
    number = data.get("number")
    text = data.get("text")
    if not number or not text:
        return jsonify({"error": "Número y texto son requeridos"}), 400
    command = f'termux-sms-send -n {number} "{text}"'
    response = execute_ssh_command(command)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
