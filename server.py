import asyncio
import socket
import time

HEADERSIZE = 10

class WebSocketServer:
    def __init__(self, host='localhost', port=1234):
        self.host = host
        self.port = port
        self.clients = set()

    async def handle_client(self, reader, writer):
        # Add client to the set
        self.clients.add(writer)
        addr = writer.get_extra_info('peername')
        print(f"Connection from {addr} has been established!")

        try:
            # Send welcome message
            welcome_msg = "Welcome to the server!"
            await self.send_message(writer, welcome_msg)

            # Keep connection alive and send time updates
            while True:
                msg = f'The time is {time.time()}'
                await self.send_message(writer, msg)
                await asyncio.sleep(3)  # Non-blocking sleep

        except ConnectionResetError:
            print(f"Client {addr} disconnected")
        except Exception as e:
            print(f"Error handling client {addr}: {e}")
        finally:
            self.clients.remove(writer)
            writer.close()
            await writer.wait_closed()

    async def send_message(self, writer, message):
        # Prepare message with header
        full_msg = f'{len(message):<{HEADERSIZE}}' + message
        writer.write(full_msg.encode('utf-8'))
        await writer.drain()

    async def start_server(self):
        # Create a socket explicitly
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))
        sock.listen(5)
        sock.setblocking(False)  # Make the socket non-blocking for async operations
        
        # Create server using the explicit socket
        server = await asyncio.start_server(
            self.handle_client,
            sock=sock  # Use our explicitly created socket
        )

        addr = server.sockets[0].getsockname()
        print(f'Serving on {addr} using explicit socket')

        async with server:
            await server.serve_forever()

async def main():
    server = WebSocketServer()
    await server.start_server()

if __name__ == "__main__":
    asyncio.run(main())


