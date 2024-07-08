import asyncio
import logging
import websockets

class Socket:
    """
    A WebSocket server that handles client connections, sends log updates, and manages connected clients.

    This class implements the observer pattern to receive updates from a log monitor
    and broadcasts these updates to all connected clients.
    """

    def __init__(self, host: str, port: int, log_monitor):
        """
        Initialize the Socket instance.

        Args:
            host (str): The host address to bind the server to.
            port (int): The port number to listen on.
            log_monitor: An instance of a log monitor that this socket will observe.
        """
        self.host = host
        self.port = port
        self.log_monitor = log_monitor
        self.clients = set()
        self.loop = asyncio.get_event_loop()
        self.log_monitor.register_observer(self)

    async def register(self, websocket: websockets.WebSocketServerProtocol):
        """
        Register a new client websocket connection.

        Args:
            websocket (websockets.WebSocketServerProtocol): The websocket connection to register.
        """
        self.clients.add(websocket)
        logging.info(f"Client {websocket.remote_address} connected")

    async def unregister(self, websocket: websockets.WebSocketServerProtocol):
        """
        Unregister a client websocket connection.

        Args:
            websocket (websockets.WebSocketServerProtocol): The websocket connection to unregister.
        """
        if websocket in self.clients:
            self.clients.remove(websocket)
            logging.info(f"Client {websocket.remote_address} disconnected")
        self.log_monitor.unregister_observer(websocket)

    async def send_message(self, message: str):
        """
        Send a message to all connected clients.

        Args:
            message (str): The message to send.
        """
        logging.info(f"Sending message to {len(self.clients)} clients: {message}")
        if self.clients:
            await asyncio.gather(*[client.send(message) for client in self.clients])

    def update(self, line: str):
        """
        Receive an update from the log monitor and schedule it to be sent to all clients.

        Args:
            line (str): The new log line to send.
        """
        logging.info(f"Update received: {line}")
        asyncio.run_coroutine_threadsafe(self.send_message(line), self.loop)

    async def tail_log(self, websocket: websockets.WebSocketServerProtocol, path: str):
        """
        Handle a new client connection by sending the last log lines and keeping the connection open.

        Args:
            websocket (websockets.WebSocketServerProtocol): The websocket connection.
            path (str): The connection path (unused in this implementation).
        """
        await self.register(websocket)
        try:
            last_lines = self.log_monitor.get_last_lines()
            await websocket.send(last_lines)
            while True:
                await asyncio.sleep(0.1)
        finally:
            await self.unregister(websocket)

    async def start_server(self):
        """Start the WebSocket server and keep it running indefinitely."""
        async with websockets.serve(self.tail_log, self.host, self.port):
            await asyncio.Future()

    async def ping_clients(self):
        """Periodically ping clients to check their connection status."""
        while True:
            logging.info("Pinging clients")
            disconnected_clients = []
            for client in self.clients:
                try:
                    await client.ping()
                except Exception:
                    logging.info(f"Client {client.remote_address} is disconnected")
                    disconnected_clients.append(client)
            for client in disconnected_clients:
                await self.unregister(client)
            await asyncio.sleep(10)

    def run(self):
        """Run the WebSocket server and client pinger in the event loop."""
        asyncio.set_event_loop(self.loop)
        self.loop.create_task(self.start_server())
        self.loop.create_task(self.ping_clients())
        self.loop.run_forever()