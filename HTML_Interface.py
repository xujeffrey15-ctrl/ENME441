import http.server
import socketserver
import json
import time
import multiprocessing

# Import your Stitch motor control class
from Stich import Stepper_Motors   # <-- CHANGE THIS to match your actual filename

# --------------------------------------------------------------------------------------
# GPIO SIMULATOR / REAL MOTOR WRAPPER
# --------------------------------------------------------------------------------------

class GPIOSimulator:
    def __init__(self):
        self.pin_state = False

        # Use the REAL motor system from your Stitch file
        self.motors = Stepper_Motors()

        # For display values
        self.radius = 0
        self.theta = 0
        self.z = 0

    def toggle_pin(self):
        self.pin_state = not self.pin_state
        # (In real hardware, GPIO.output would go here)
        return self.pin_state

    def set_origin(self, radius, theta, z):
        self.radius = float(radius)
        self.theta = float(theta)
        self.z = float(z)

        # Use your real calibration method
        self.motors.Calibration(1)
        return True

    def get_status(self):
        return {
            'pin_state': 'ON' if self.pin_state else 'OFF',
            'radius': self.radius,
            'theta': self.theta,
            'z': self.z,
            'motor1_angle': self.motors.m1.angle,
            'motor2_angle': self.motors.m2.angle
        }

    def initiate_automation(self):
        print("Starting real Stitch automation...")
        self.motors.Automated_Motors()
        return True

    def manual_move(self, diff):
        print(f"Manual move request: diff={diff}")
        self.motors.Manual_Motors(1, diff)
        return True


# --------------------------------------------------------------------------------------
# GLOBAL GPIO SIMULATOR INSTANCE
# --------------------------------------------------------------------------------------

gpio = GPIOSimulator()


# --------------------------------------------------------------------------------------
# HTTP SERVER HANDLER
# --------------------------------------------------------------------------------------

class GPIORequestHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        return super().do_GET()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')

        response = {}

        # ----------------------------- ROUTES ------------------------------------

        if self.path == '/toggle':
            new_state = gpio.toggle_pin()
            response = {'status': 'ON' if new_state else 'OFF'}

        elif self.path == '/set_origin':
            data = json.loads(post_data)
            success = gpio.set_origin(data['radius'], data['theta'], data['z'])
            response = {'success': success}

        elif self.path == '/automation':
            success = gpio.initiate_automation()
            response = {'success': success}

        # ⭐ NEW: Calibrate using Stitch file
        elif self.path == '/calibrate':
            gpio.motors.Calibration(1)
            response = {'success': True}

        # ⭐ NEW: Manual angle adjustment
        elif self.path == '/manual':
            data = json.loads(post_data)
            diff = float(data.get("diff", 0))
            gpio.manual_move(diff)
            response = {'success': True}

        elif self.path == '/status':
            response = gpio.get_status()

        # -------------------------------------------------------------------------
        # SEND RESPONSE
        # -------------------------------------------------------------------------

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())


# --------------------------------------------------------------------------------------
# HTML FILE GENERATION
# --------------------------------------------------------------------------------------

def generate_html():
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Turret Control Panel</title>
</head>
<body>
    <h1>Team 18 Turret Control</h1>

    <h2>GPIO Toggle</h2>
    <button id="toggleBtn">Toggle ON/OFF</button>
    <div id="statusDisplay">Status: OFF</div>

    <h2>Set Origin / Calibration</h2>
    <button id="calibrateBtn">Calibrate Motors</button>

    <h2>Manual Control</h2>
    <button id="leftBtn">Rotate Left</button>
    <button id="rightBtn">Rotate Right</button>

    <h3>Current Values</h3>
    <div>Motor 1: <span id="motor1Angle">0</span>°</div>
    <div>Motor 2: <span id="motor2Angle">0</span>°</div>

    <h2>Automation</h2>
    <button id="automationBtn">Start Automation</button>

<script>
const statusDisplay = document.getElementById('statusDisplay');
const motor1Angle = document.getElementById('motor1Angle');
const motor2Angle = document.getElementById('motor2Angle');

// ------------------ BUTTON LOGIC ------------------------

document.getElementById("toggleBtn").onclick = async () => {
    const r = await fetch('/toggle', { method: 'POST' });
    const data = await r.json();
    statusDisplay.textContent = `Status: ${data.status}`;
};

document.getElementById("calibrateBtn").onclick = async () => {
    await fetch('/calibrate', { method: 'POST' });
    alert("Calibration Complete");
};

document.getElementById("leftBtn").onclick = async () => {
    await fetch('/manual', {
        method: 'POST',
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ diff: -10 })
    });
};

document.getElementById("rightBtn").onclick = async () => {
    await fetch('/manual', {
        method: 'POST',
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ diff: 10 })
    });
};

document.getElementById("automationBtn").onclick = async () => {
    await fetch('/automation', { method: 'POST' });
    alert("Automation Started");
};

// ------------------ AUTO REFRESH STATUS ------------------------

async function refreshStatus() {
    try {
        const res = await fetch('/status');
        const data = await res.json();

        motor1Angle.textContent = data.motor1_angle.toFixed(2);
        motor2Angle.textContent = data.motor2_angle.toFixed(2);
        statusDisplay.textContent = `Status: ${data.pin_state}`;
    } catch (err) {
        console.log("Status update error:", err);
    }
}

setInterval(refreshStatus, 1000);
refreshStatus();

</script>
</body>
</html>
"""
    return html


# --------------------------------------------------------------------------------------
# SERVER STARTUP
# --------------------------------------------------------------------------------------

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

def start_server(port=8080):
    # create html file:
    with open('index.html', 'w') as f:
        f.write(generate_html())

    with ReusableTCPServer(("", port), GPIORequestHandler) as httpd:
        print(f"Server running at http://localhost:{port}")
        httpd.serve_forever()


if __name__ == "__main__":
    start_server()
