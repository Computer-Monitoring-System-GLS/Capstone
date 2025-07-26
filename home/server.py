from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Store client system info (IP → System Details)
client_data = {}

@app.route('/register_client', methods=['POST'])
def register_client():
    """
    Receives client system info and stores it using IP as key.
    """
    data = request.json
    client_ip = data.get("ip")
    
    if client_ip:
        client_data[client_ip] = data
        return jsonify({"message": "Client registered successfully", "data": data})
    else:
        return jsonify({"error": "Invalid data"}), 400

@app.route('/client-info')
def client_info():
    """
    Detects the client's IP and returns their stored system info.
    """
    client_ip = request.remote_addr  # Get the IP of the client visiting this page
    info = client_data.get(client_ip)

    if info:
        return render_template("client_info.html", info=info)
    else:
        return render_template("client_info.html", info={"error": "Client data not found"})

@app.route('/')
def home():
    return "Server is running. Visit /client-info to view client system details."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
