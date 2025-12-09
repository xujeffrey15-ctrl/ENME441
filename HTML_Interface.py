import http.server
import socketserver
import urllib.parse
from Stich_Code import Stepper_Motors

motors = Stepper_Motors()
PORT = 8080  # you can change this if needed

# HTML template with a placeholder for messages
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Motor Control Panel</title>
    <style>
        body {{ font-family: Arial; max-width: 600px; margin: 40px auto; padding: 20px; background: #f4f4f4; border-radius: 10px; }}
        form {{ background: #fff; padding: 20px; margin-bottom: 25px; border-radius: 8px; box-shadow: 0 0 5px rgba(0,0,0,0.1); }}
        button {{ padding: 10px 18px; font-size: 16px; background: #0077cc; border: none; color: white; border-radius: 5px; }}
        button:hover {{ background: #005fa3; }}
    </style>
</head>
<body>
    <h1>Motor Control Panel</h1>

    <form action="/calibrate" method="post">
        <h2>Calibration</h2>
        <p>Click below to run calibration routine.</p>
        <input type="hidden" name="toggle" value="1">
        <button type="submit">Run Calibration</button>
    </form>

    <form action="/manual" method="post">
        <h2>Manual Motor Movement</h2>
        <label for="diff">Rotation Amount (diff):</label><br>
        <input type="number" id="diff" name="diff" step="0.1" required><br><br>
        <label>
            <input type="checkbox" name="toggle" value="1"> Enable Manual Movement
        </label><br><br>
        <button type="submit">Move Motors</button>
    </form>

    <form action="/automation" method="post">
        <h2>Automation Sequence</h2>
        <p>Click below to start full automated turret + ball sequence.</p>
        <input type="hidden" name="toggle" value="1">
        <button type="submit">Run Automation</button>
    </form>

    {message}
</body>
</html>
"""

# -------------------- Request Handler --------------------

class MotorRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Always return the main page for GET requests
        html = HTML_TEMPLATE.format(message="")
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(html)))
        self.end_headers()
        self.wfile.write(html.encode())

    def do_POST(self):
        # Read POST data
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode()
        form = {k: v[0] for k, v in urllib.parse.parse_qs(post_data).items()}

        message = ""

        try:
            if self.path == "/calibrate":
                toggle = int(form.get("toggle", 0))
                motors.Calibration(toggle)
                message = "<p><b>Calibration complete.</b></p>"

            elif self.path == "/manual":
                toggle = int(form.get("toggle", 0))
                diff = float(form.get("diff", 0))
                motors.Manual_Motors(toggle, diff)
                message = f"<p><b>Manual movement complete (diff={diff}).</b></p>"

            elif self.path == "/automation":
                toggle = int(form.get("toggle", 0))
                if toggle == 1:
                    motors.Automated_Motors()
                message = "<p><b>Automation sequence completed.</b></p>"

            else:
                message = "<p><b>Unknown action.</b></p>"

        except Exception as e:
            message = f"<p><b>Error: {e}</b></p>"

        # Return updated page
        html = HTML_TEMPLATE.format(message=message)
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(html)))
        self.end_headers()
        self.wfile.write(html.encode())

# -------------------- Reusable TCP Server --------------------

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

def start_server(port=PORT):
    with ReusableTCPServer(("", port), MotorRequestHandler) as httpd:
        print(f"Server running at http://localhost:{port}")
        print("Access from other devices using http://<YOUR_LAN_IP>:{port}")
        httpd.serve_forever()

# -------------------- Main --------------------

if __name__ == "__main__":
    start_server()

