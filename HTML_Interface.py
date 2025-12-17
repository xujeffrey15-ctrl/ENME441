import http.server
import socketserver
import json
import threading
import multiprocessing
import time

# Import your updated Stepper_Motors class
from Stich_Code import Stepper_Motors

# -------------------- GPIO / Motor Wrapper --------------------

class GPIOSimulator:
    def __init__(self):
        self.pin_state = False
        self.motors = Stepper_Motors()
        self.radius = 0
        self.theta = 0
        self.z = 0
        self.automation_thread = None

    def toggle_pin(self):
        self.pin_state = not self.pin_state
        return self.pin_state

    def set_origin(self, radius, theta, z):
        self.radius = float(radius)
        self.theta = float(theta)
        self.z = float(z)
        self.motors.Calibration(1)
        return True

    def get_status(self):
        return {
            'pin_state': 'ON' if self.pin_state else 'OFF',
            'radius': self.radius,
            'theta': self.theta,
            'z': self.z,
            'motor1_angle': self.motors.x_angle_tracking,
            'motor2_angle': self.motors.z_angle_tracking
        }

    def initiate_automation(self):
        if self.automation_thread is None or not self.automation_thread.is_alive():
            self.automation_thread = threading.Thread(target=self.motors.Automated_Motors, daemon=True)
            self.automation_thread.start()
        return True

    def manual_move(self, x_angle, z_angle):
        print(f"Manual move request: x={x_angle}, z={z_angle}")
        self.motors.Manual_Motors(1, x_angle, z_angle)
        return True

gpio = GPIOSimulator()

# -------------------- HTTP Request Handler --------------------

class GPIORequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(generate_html().encode())
        else:
            self.send_error(404)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        response = {}

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

        elif self.path == '/calibrate':
            gpio.motors.Calibration(1)
            response = {'success': True}

        elif self.path == '/manual':
            data = json.loads(post_data)
            x_angle = float(data.get("x_angle", 0))
            z_angle = float(data.get("z_angle", 0))
            gpio.manual_move(x_angle, z_angle)
            response = {'success': True}

        elif self.path == '/status':
            response = gpio.get_status()

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

# -------------------- HTML Generator --------------------

def generate_html():
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Turret Control Panel</title>
<style>
body { font-family: Arial, sans-serif; margin: 20px; }
h1, h2, h3 { margin-bottom: 10px; }
canvas { display: block; margin: 20px 0; border: 1px solid #000; }
input { width: 60px; margin-right: 10px; }
button { margin: 5px; padding: 5px 10px; }
.status { font-weight: bold; }
</style>
</head>
<body>

<h1>Team 18 Turret Control</h1>

<h2>GPIO Toggle</h2>
<button id="toggleBtn">Toggle ON/OFF</button>
<div class="status" id="statusDisplay">Status: OFF</div>

<h2>Calibration / Set Origin</h2>
<button id="calibrateBtn">Calibrate Motors</button>

<h2>Manual Control</h2>
<input type="number" id="xAngle" placeholder="X Angle" value="0">
<input type="number" id="zAngle" placeholder="Z Angle" value="0">
<button id="manualBtn">Move Motors</button>

<h3>Current Motor Angles</h3>
<div>Motor 1 (X): <span id="motor1Angle">0</span>°</div>
<div>Motor 2 (Z): <span id="motor2Angle">0</span>°</div>

<h3>Motor Angle Visualization</h3>
<canvas id="angleCanvas" width="400" height="200"></canvas>

<h2>Automation</h2>
<button id="automationBtn">Start Automation</button>

<script>
const statusDisplay = document.getElementById('statusDisplay');
const motor1Angle = document.getElementById('motor1Angle');
const motor2Angle = document.getElementById('motor2Angle');
const canvas = document.getElementById('angleCanvas');
const ctx = canvas.getContext('2d');

function drawMotorAngles(x_angle, z_angle) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const radius = 80;
    const centerX1 = 100;
    const centerX2 = 300;
    const centerY = 150;

    ctx.lineWidth = 2;
    ctx.strokeStyle = '#aaa';

    ctx.beginPath();
    ctx.arc(centerX1, centerY, radius, Math.PI, 0, false);
    ctx.stroke();
    ctx.fillStyle = 'black';
    ctx.fillText("Motor 1", centerX1 - 25, centerY + 20);

    ctx.beginPath();
    ctx.arc(centerX2, centerY, radius, Math.PI, 0, false);
    ctx.stroke();
    ctx.fillText("Motor 2", centerX2 - 25, centerY + 20);

    function drawPointer(cx, cy, angle, color) {
        const rad = Math.PI - (angle * Math.PI / 180);
        const length = radius - 10;
        ctx.beginPath();
        ctx.moveTo(cx, cy);
        ctx.lineTo(cx + length * Math.cos(rad), cy - length * Math.sin(rad));
        ctx.strokeStyle = color;
        ctx.lineWidth = 4;
        ctx.stroke();
    }

    drawPointer(centerX1, centerY, x_angle, 'red');
    drawPointer(centerX2, centerY, z_angle, 'blue');
}

document.getElementById("toggleBtn").onclick = async () => {
    const r = await fetch('/toggle', { method: 'POST' });
    const data = await r.json();
    statusDisplay.textContent = `Status: ${data.status}`;
};

document.getElementById("calibrateBtn").onclick = async () => {
    await fetch('/calibrate', { method: 'POST' });
    alert("Calibration Complete");
};

document.getElementById("manualBtn").onclick = async () => {
    const x_angle = parseFloat(document.getElementById('xAngle').value) || 0;
    const z_angle = parseFloat(document.getElementById('zAngle').value) || 0;

    await fetch('/manual', {
        method: 'POST',
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ x_angle: x_angle, z_angle: z_angle })
    });
};

document.getElementById("automationBtn").onclick = async () => {
    alert("Automation Started");
    await fetch('/automation', { method: 'POST' });
};

async function refreshStatus() {
    try {
        const res = await fetch('/status');
        const data = await res.json();

        motor1Angle.textContent = parseFloat(data.motor1_angle).toFixed(2);
        motor2Angle.textContent = parseFloat(data.motor2_angle).toFixed(2);
        statusDisplay.textContent = `Status: ${data.pin_state}`;

        drawMotorAngles(data.motor1_angle, data.motor2_angle);
    } catch (err) {
        console.log("Status update error:", err);
    }
}

setInterval(refreshStatus, 500);
refreshStatus();
</script>
</body>
</html>"""

# -------------------- SERVER STARTUP --------------------

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

def start_server(port=8080):
    with ReusableTCPServer(("", port), GPIORequestHandler) as httpd:
        print(f"Server running at http://localhost:{port}")
        httpd.serve_forever()

if __name__ == "__main__":
    start_server()
