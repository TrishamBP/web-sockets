import asyncio

HEADERSIZE = 10

class WebSocketClient:
    def __init__(self, host='localhost', port=1234):
        self.host = host
        self.port = port

    async def receive_message(self, reader):
        try:
            while True:
                # Read header first
                header = await reader.read(HEADERSIZE)
                if not header:
                    break
                
                msglen = int(header.decode('utf-8').strip())
                
                # Read the actual message
                full_msg = ''
                remaining = msglen
                
                while remaining > 0:
                    chunk = await reader.read(min(remaining, 1024))
                    if not chunk:
                        break
                    full_msg += chunk.decode('utf-8')
                    remaining -= len(chunk)
                
                if full_msg:
                    print("Full message received:")
                    print(full_msg)
                
        except ConnectionResetError:
            print("Server disconnected")
        except Exception as e:
            print(f"Error receiving message: {e}")

    async def connect(self):
        try:
            reader, writer = await asyncio.open_connection(self.host, self.port)
            print(f"Connected to {self.host}:{self.port}")
            
            await self.receive_message(reader)
            
        except ConnectionRefusedError:
            print(f"Failed to connect to {self.host}:{self.port}")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            if 'writer' in locals():
                writer.close()
                await writer.wait_closed()

async def main():
    client = WebSocketClient()
    await client.connect()

if __name__ == "__main__":
    asyncio.run(main())
        