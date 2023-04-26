import asyncio
import websockets

class WebSocketClient:
    def __init__(self, uri):
        self.uri = uri
        self.websocket = None

    async def connect(self):
        async with websockets.connect(self.uri) as websocket:
            self.websocket = websocket
            await self.receive_messages()

    async def receive_messages(self):
        while True:
            message = await self.websocket.recv()
            await asyncio.gather(
                self.process_message_1(message),
                self.process_message_2_with_delay(message)
            )

    async def process_message_1(self, message):
        # Process the message in any way you want
        print(f"Processing message 1: {message}")

    async def process_message_2_with_delay(self, message):
        # Wait for a set amount of time before processing the message
        await asyncio.sleep(5)  # Change this to the desired wait time in seconds
        # Process the message in any way you want
        print(f"Processing message 2 (with delay): {message}")

async def main():
    uri = "wss://your.websocket.server"  # Change this to your WebSocket server address
    client = WebSocketClient(uri)
    await client.connect()

if __name__ == "__main__":
    asyncio.run(main())
