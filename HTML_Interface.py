import socket
from Stich_Code import Stepper_Motors
import urllib.parse

motors = Stepper_Motors()

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Motor Control Panel</title>
    <style>
        body { font-family: Arial; max-width: 600px; margin: 40px auto; padding: 20px; background: #f4f4f4; border-radius: 10px; }
        form { background: #fff; padding: 20px; margin-bottom: 25px; border-radius: 8px; box-shadow: 0 0 5px rgba(0,0,0,0.1); }
        button { padding: 10px 18px; font-size: 16px; background: #0077cc; border: none; color: white; border-radius: 5px; }
        button:hover { background: #005fa3; }
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

    {MESSAGE}
</body>
</html>
"""

# ---------------------------------------------------------------------

def http_response(body, status="200 OK"):
    return (
        f"HTTP/1.1 {status}\r\n"
        "Content-Type: text/html\r\n"
        f"Content-Length: {len(body)}\r\n"
        "Connection: close\r\n\r\n"
        + body
    )

def parse_post_data(request):
    if "\r\n\r\n" not in request:
        return ""
    return request.split("\r\n\r\n", 1)[1]

def parse_form(form_body):
    parsed = urllib.parse.parse_qs(form_body)
    # flatten values
    data = {k: v[0] for k, v in parsed.items()}
    return data

# ---------------------------------------------------------------------

HOST = "0.0.0.0"
PORT = 5000

print(f"Server running at http://{HOST}:{PORT}")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

while True:
    client, addr = server.accept()
    request = client.recv(4096).decode()

    if not request:
        client.close()
        continue

    # Determine the route
    request_line = request.split("\n")[0]
    method, path, _ = request_line.split(" ")

    message = ""

    # ---------------- ROUTING HANDLERS ------------------

    if method == "GET" and path == "/":
        response = http_response(HTML_PAGE.format(MESSAGE=""))
        client.sendall(response.encode())

    elif method == "POST" and path == "/calibrate":
        form = parse_form(parse_post_data(request))
        toggle = int(form.get("toggle", 0))
        motors.Calibration(toggle)
        message = "<p><b>Calibration complete.</b></p>"
        response = http_response(HTML_PAGE.format(MESSAGE=message))
        client.sendall(response.encode())

    elif method == "POST" and path == "/manual":
        form = parse_form(parse_post_data(request))
        toggle = int(form.get("toggle", 0))
        diff = float(form.get("diff", 0))
        motors.Manual_Motors(toggle, diff)
        message = f"<p><b>Manual movement complete (diff={diff}).</b></p>"
        response = http_response(HTML_PAGE.format(MESSAGE=message))
        client.sendall(response.encode())

    elif method == "POST" and path == "/automation":
        form = parse_form(parse_post_data(request))
        toggle = int(form.get("toggle", 0))
        if toggle == 1:
            motors.Automated_Motors()
        message = "<p><b>Automation sequence completed.</b></p>"
        response = http_response(HTML_PAGE.format(MESSAGE=message))
        client.sendall(response.encode())

    else:
        # unknown route
        response = http_response("<h1>404 Not Found</h1>", status="404 Not Found")
        client.sendall(response.encode())

    client.close()
