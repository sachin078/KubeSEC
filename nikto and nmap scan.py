from flask import Flask, request
import subprocess

app = Flask(__name__)

# Function to run nmap scan
def run_nmap_scan(target):
    subprocess.run(["nmap", "-sV", target])

# Function to run nikto scan
def run_nikto_scan(target):
    subprocess.run(["nikto", "-h", target])

# API endpoint to run scans
@app.route('/scan', methods=['POST'])
def scan():
    target = request.json.get('target')
    scan_type = request.json.get('scan_type')

    if scan_type == 'nmap':
        run_nmap_scan(target)
    elif scan_type == 'nikto':
        run_nikto_scan(target)
    else:
        return "Invalid scan type. Please specify 'nmap' or 'nikto'.", 400

    return "Scan completed.", 200

if __name__ == '__main__':
    app.run(debug=True)
