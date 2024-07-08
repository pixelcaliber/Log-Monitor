import threading
import os
from app import create_app
from app.log_monitor.log_monitor import LogMonitor
from app.socket.socket import Socket
from app.utils.logger import configure_logging

app = create_app()


def start_flask():
    app.run(host='0.0.0.0', port=5000)


if __name__ == "__main__":
    configure_logging()

    # Start the Flask server in a separate thread
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.start()

    # Create the LogMonitor and Start the LogMonitor in a separate thread
    log_monitor = LogMonitor(app.config["LOG_FILE_PATH"])
    log_monitor_thread = threading.Thread(
        target=log_monitor.tail_log, daemon=True
    ).start()

    # Start the WebSocket server in a separate thread
    websocket_server = Socket('0.0.0.0', 9010, log_monitor)
    websocket_thread = threading.Thread(
        target=websocket_server.run, daemon=True
    ).start()
    

    # Keep the main thread running to handle any additional logic if needed
    flask_thread.join()
    websocket_thread.join()
    log_monitor_thread.join()
