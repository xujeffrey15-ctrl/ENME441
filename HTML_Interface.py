from flask import Flask, request, render_template_string
from Stich_Code import Stepper_Motors  # <-- Replace with your actual file
import time

app = Flask(__name__)
motors = Stepper_Motors()

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Motor Control Panel</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            max-width: 600px; 
            margin: 40px auto; 
            padding: 20px; 
            background: #f4f4f4; 
            border-radius: 10px;
        }
        h2 { color: #333; }
        form {
            background: #fff;
            padding: 20px;
            margin-bottom: 25px;
            border-radius: 8px;
            box-shadow: 0 0 5px rgba(0,0,0,0.1);
        }
        button {
            padding: 10px 18px;
            font-size: 16px;
            cursor: pointer;
            border: none;
            color: white;
            background: #0077cc;
            border-radius: 5px;
        }
        button:hover {
            background: #005fa3;
        }
        input[type="number"] {
            padding: 8px;
            width: 150px;
            margin-bottom: 10px;
        }
    </style>
</head>

<body>

    <h1>Motor Control Panel</h1>

    <!-- Calibration Control -->
    <form action="/calibrate" method="post">
        <h2>Calibration</h2>
        <p>Click below to run calibration routine.</p>
        <input type="hidden" name="toggle" value="1">
        <button type="submit">Run Calibration</button>
    </form>

    <!-- Manual Motor Movement -->
    <form action="/manual" method="post">
        <h2>Manual Motor Movement</h2>

        <label for="diff">Rotation Amount (diff):</label><br>
        <input type="number" id="diff" name="diff" step="0.1" required><br><br>

        <label>
            <input type="checkbox" name="toggle" value="1">
            Enable Manual Movement
        </label><br><br>

        <button type="submit">Move Motors</button>
    </form>

    <!-- Automation Control -->
    <form action="/automation" method="post">
        <h2>Automation Sequence</h2>
        <p>Click below to start full automated turret + ball sequence.</p>
        <input type="hidden" name="toggle" value="1">
        <button type="submit">Run Automation</button>
    </form>

</body>
</html>
"""

# ---------------------------------------------------------
# Routes
# ---------------------------------------------------------

@app.route("/")
def index():
    return render_template_string(HTML_PAGE)

@app.route("/calibrate", methods=["POST"])
def calibrate():
    toggle = int(request.form.get("toggle", 0))
    motors.Calibration(toggle)
    return render_template_string(HTML_PAGE + "<p><b>Calibration complete.</b></p>")

@app.route("/manual", methods=["POST"])
def manual():
    toggle = int(request.form.get("toggle", 0))
    diff = float(request.form.get("diff", 0))
    motors.Manual_Motors(toggle, diff)
    return render_template_string(HTML_PAGE + f"<p><b>Manual movement complete (diff={diff}).</b></p>")

@app.route("/automation", methods=["POST"])
def automation():
    toggle = int(request.form.get("toggle", 0))
    if toggle == 1:
        motors.Automated_Motors()
    return render_template_string(HTML_PAGE + "<p><b>Automation sequence completed.</b></p>")

# ---------------------------------------------------------
# Run Flask
# ---------------------------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
