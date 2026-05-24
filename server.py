from flask import Flask, request
import requests
from datetime import datetime

app = Flask(__name__)

# =====================================
# DEVICE STORAGE
# =====================================

devices = {}

# =====================================
# DEVICE STATUS
# =====================================

device_status = {}

# =====================================
# EVENT LOGS
# =====================================

logs = []

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

    Central IoT Hub 😄🔥

    </h1>

    <hr>

    <h2>Connected Devices</h2>

    """

    # Poll Devices
    for device_id, ip in devices.items():

        try:

            response = requests.get(
                f"http://{ip}/status",
                timeout=1
            )

            device_status[device_id] = (
                response.text
            )

        except:

            device_status[device_id] = (
                "OFFLINE 😭"
            )

    # Show Devices
    for device_id, ip in devices.items():

        status = device_status.get(
            device_id,
            "UNKNOWN"
        )

        html += f"""

        <div style='background:#222;
                    padding:20px;
                    margin-bottom:15px;
                    border-radius:10px;'>

        <h2>{device_id}</h2>

        <p>IP : {ip}</p>

        <h3>Status : {status}</h3>

        <a href='/blink/{device_id}'>

        <button style='padding:15px;
                       font-size:20px;'>

        BLINK LED

        </button>

        </a>

        </div>

        """

    html += """

    <hr>

    <h2>Event Logs</h2>

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

    ip = request.args.get(
        "ip"
    )

    devices[device_id] = ip

    print(
        f"{device_id} REGISTERED 😄"
    )

    return "REGISTERED"

# =====================================
# BUTTON PRESS EVENT
# =====================================

@app.route("/button")
def button():

    device_id = request.args.get(
        "device_id"
    )

    current_time = datetime.now().strftime(
        "%I:%M:%S %p"
    )

    log = (
        f"{device_id} BUTTON PRESSED 😄"
        f" — {current_time}"
    )

    logs.append(log)

    print(log)

    return "OK"

# =====================================
# BLINK DEVICE
# =====================================

@app.route("/blink/<device_id>")
def blink(device_id):

    try:

        ip = devices[device_id]

        requests.get(
            f"http://{ip}/blink"
        )

        current_time = datetime.now().strftime(
            "%I:%M:%S %p"
        )

        logs.append(
            f"{device_id} BLINK COMMAND 😎"
            f" — {current_time}"
        )

    except:

        logs.append(
            f"{device_id} OFFLINE 😭"
        )

    return """

    <script>

    window.location.href='/'

    </script>

    """

# =====================================
# RUN SERVER
# =====================================

app.run(
    host="0.0.0.0",
    port=5000,
    debug=True
)