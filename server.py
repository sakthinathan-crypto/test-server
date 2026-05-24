from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

# =====================================
# DEVICES
# =====================================

devices = {}

# =====================================
# LOGS
# =====================================

logs = []

# =====================================
# COMMAND STORAGE
# =====================================

commands = {}

# =====================================
# HOME PAGE
# =====================================

@app.route("/")
def home():

    html = """

    <html>

    <head>

    <meta http-equiv="refresh"
          content="2">

    </head>

    <body style='background:black;
                 color:white;
                 font-family:Arial;
                 padding:20px;'>

    <h1 style='text-align:center;'>

    Cloud IoT Dashboard 😄🔥

    </h1>

    <hr>

    """

    # SHOW DEVICES
    for device_id in devices:

        html += f"""

        <div style='background:#222;
                    padding:20px;
                    margin-bottom:20px;
                    border-radius:10px;'>

        <h2>{device_id}</h2>

        <a href='/sendBlink/{device_id}'>

        <button style='padding:15px;
                       font-size:20px;'>

        BLINK LED

        </button>

        </a>

        </div>

        """

    html += """

    <hr>

    <h2>EVENT LOGS</h2>

    """

    # SHOW LOGS
    for log in reversed(logs):

        html += f"""

        <div style='background:#111;
                    padding:15px;
                    margin-bottom:10px;
                    border-radius:10px;'>

        <h3>{log}</h3>

        </div>

        """

    html += """

    </body>

    </html>

    """

    return html

# =====================================
# REGISTER DEVICE
# =====================================

@app.route("/register")
def register():

    device_id = request.args.get(
        "device_id"
    )

    devices[device_id] = True

    current_time = datetime.now().strftime(
        "%I:%M:%S %p"
    )

    logs.append(
        f"{device_id} CONNECTED 😄"
        f" — {current_time}"
    )

    return "REGISTERED"

# =====================================
# BUTTON EVENT
# =====================================

@app.route("/button")
def button():

    device_id = request.args.get(
        "device_id"
    )

    current_time = datetime.now().strftime(
        "%I:%M:%S %p"
    )

    logs.append(
        f"{device_id} BUTTON PRESSED 😎"
        f" — {current_time}"
    )

    return "OK"

# =====================================
# SEND BLINK COMMAND
# =====================================

@app.route("/sendBlink/<device_id>")
def sendBlink(device_id):

    commands[device_id] = "BLINK"

    current_time = datetime.now().strftime(
        "%I:%M:%S %p"
    )

    logs.append(
        f"{device_id} BLINK COMMAND SENT 🔥"
        f" — {current_time}"
    )

    return """

    <script>

    window.location.href='/'

    </script>

    """

# =====================================
# GET COMMAND
# =====================================

@app.route("/getCommand")
def getCommand():

    device_id = request.args.get(
        "device_id"
    )

    command = commands.get(
        device_id,
        "NONE"
    )

    return command

# =====================================
# CLEAR COMMAND
# =====================================

@app.route("/clearCommand")
def clearCommand():

    device_id = request.args.get(
        "device_id"
    )

    commands[device_id] = "NONE"

    return "CLEARED"

# =====================================
# RUN
# =====================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )