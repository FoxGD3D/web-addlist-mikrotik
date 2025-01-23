from flask import Flask, request, jsonify
from flask_cors import CORS
import paramiko

app = Flask(__name__)
CORS(app)  # Allowing CORS requests

# Конфигурация MikroTik
MIKROTIK_HOST = "Enter Mikrotik IP"
MIKROTIK_USER = "Enter Mikrotik USER"
MIKROTIK_PASSWORD = "Enter Mikrotik PASS"
MIKROTIK_PORT = 22

@app.route('/api/unlock', methods=['POST'])
def unlock_domain():
    data = request.get_json()
    domain = data.get("domain")

    if not domain:
        return jsonify({"error": "Домен не указан"}), 400

    try:
        # Connecting to MikroTik via SSH
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(MIKROTIK_HOST, port=MIKROTIK_PORT, username=MIKROTIK_USER, password=MIKROTIK_PASSWORD)

        # Выполнение команды добавления в список
        command = f"/ip firewall address-list add list=rkn_wg address={domain} comment=AddFromApi"
        stdin, stdout, stderr = ssh.exec_command(command)

        # Проверка результата
        error = stderr.read().decode()
        if error:
            return jsonify({"error": f"Ошибка выполнения команды: {error}"}), 500

        ssh.close()
        return jsonify({"message": f"Домен {domain} успешно добавлен в rkn_wg"})

    except Exception as e:
        return jsonify({"error": f"Ошибка при подключении: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
