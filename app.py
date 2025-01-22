from flask import Flask, request, jsonify
from flask_cors import CORS
import paramiko

app = Flask(__name__)
CORS(app)  # Allowing CORS requests

# MikroTik configuration
MIKROTIK_HOST = "Enter Mikrotik IP"
MIKROTIK_USER = "Enter Mikrotik USER"
MIKROTIK_PASSWORD = "Enter Mikrotik PASS"
MIKROTIK_PORT = 22

@app.route('/api/unlock', methods=['POST'])
def unlock_domain():
    data = request.get_json()
    domain = data.get("domain")

    if not domain:
        return jsonify({"error": "Domain not specified"}), 400

    try:
        # Connecting to MikroTik via SSH
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(MIKROTIK_HOST, port=MIKROTIK_PORT, username=MIKROTIK_USER, password=MIKROTIK_PASSWORD)

        # Executing the command to add to the list
        command = f"/ip firewall address-list add list=rkn_wg address={domain} comment=AddFromApi"
        stdin, stdout, stderr = ssh.exec_command(command)

        # Checking the result
        error = stderr.read().decode()
        if error:
            return jsonify({"error": f"Command execution error: {error}"}), 500

        ssh.close()
        return jsonify({"message": f"Domain {domain} successfully added to rkn_wg"})

    except Exception as e:
        return jsonify({"error": f"Connection error: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
