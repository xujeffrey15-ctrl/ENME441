class GPIOSimulator:
    def __init__(self):
        self.motors = Stepper_Motors()
        self.radius = 0
        self.theta = 0
        self.z = 0
        self.automation_thread = None

    # ---- Laser (momentary fire) ----
    def fire_laser(self):
        self.motors.Engage_Laser()
        return True

    # ---- Calibration ----
    def set_origin(self, radius, theta, z):
        self.radius = float(radius)
        self.theta = float(theta)
        self.z = float(z)
        self.motors.Calibration(1)
        return True

    # ---- Status ----
    def get_status(self):
        return {
            'radius': self.radius,
            'theta': self.theta,
            'z': self.z,
            'motor1_angle': self.motors.x_angle_tracking,
            'motor2_angle': self.motors.z_angle_tracking
        }

    # ---- Automation ----
    def initiate_automation(self):
        if self.automation_thread is None or not self.automation_thread.is_alive():
            self.automation_thread = threading.Thread(
                target=self.motors.Automated_Motors,
                daemon=True
            )
            self.automation_thread.start()
        return True

    # ---- Manual Control ----
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
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        response = {}

        if self.path == '/fire':
            gpio.fire_laser()
            response = {'success': True}

        elif self.path == '/calibrate':
            gpio.motors.Calibration(1)
            response = {'success': True}

        elif self.path == '/automation':
            gpio.initiate_automation()
            response = {'success': True}

        elif self.path == '/manual':
            data = json.loads(post_data)
            gpio.manual_move(
                float(data.get("x_angle", 0)),
                float(data.get("z_angle", 0))
            )
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
<title>Turret Control Panel</title>
<style>
body { font-family: Arial; margin: 20px; }
button { margin: 5px; padding: 6px 12px; }
canvas { border: 1px solid black; margin-top: 10px; }
</style>
</head>
<body>

<h1>Team 18 Turret Control</h1>

<h2>Laser</h2>
<button id="fireBtn">🔥 Fire Laser</button>

<h2>Calibration</h2>
<button id="calibrateBtn">Calibrate Motors</button>

<h2>Manual Control</h2>
<input id="xAngle" type="number" placeholder="X Angle">
<input id="zAngle" type="number" placeholder="Z Angle">
<button id="manualBtn">Move</button>

<h3>Motor Angles</h3>
<div>X: <span id="motor1Angle">0</span>°</div>
<div>Z: <span id="motor2Angle">0</span>°</div>

<canvas id="angleCanvas" width="400" height="200"></canvas>

<h2>Automation</h2>
<button id="automationBtn">Start Automation</button>

<script>
document.getElementById("fireBtn").onclick = () =>
    fetch('/fire', { method: 'POST' });

document.getElementById("calibrateBtn").onclick = () =>
    fetch('/calibrate', { method: 'POST' });

document.getElementById("manualBtn").onclick = () => {
    fetch('/manual', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            x_angle: document.getElementById('xAngle').value,
            z_angle: document.getElementById('zAngle').value
        })
    });
};

document.getElementById("automationBtn").onclick = () =>
    fetch('/automation', { method: 'POST' });

async function refreshStatus() {
    const r = await fetch('/status');
    const d = await r.json();
    document.getElementById("motor1Angle").textContent = d.motor1_angle.toFixed(2);
    document.getElementById("motor2Angle").textContent = d.motor2_angle.toFixed(2);
}
setInterval(refreshStatus, 500);
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

if __name__ == "__main__":
    start_server()
