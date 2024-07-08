import asyncio
import websockets
import time
import random
import logging

logging.basicConfig(level=logging.INFO)

async def connect_to_websocket(uri, client_id):
    try:
        async with websockets.connect(uri) as websocket:
            logging.info(f"Client {client_id} connected")
            while True:
                message = f"Message from client {client_id}"
                await websocket.send(message)
                logging.info(f"Client {client_id} sent a message")

                await websocket.recv()
                logging.info(f"Client {client_id} received a message")

                # await asyncio.sleep(random.uniform(1000, 5000))
    except Exception as e:
        logging.error(f"Client {client_id} encountered an error: {e}")

async def load_test(uri, num_clients):
    tasks = []
    for client_id in range(num_clients):
        task = asyncio.ensure_future(connect_to_websocket(uri, client_id))
        tasks.append(task)
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    uri = "ws://192.168.105.2/ws" # minkube IP
    num_clients = 10

    start_time = time.time()
    asyncio.get_event_loop().run_until_complete(load_test(uri, num_clients))
    end_time = time.time()

    logging.info(f"Load test completed in {end_time - start_time} seconds")
