import argparse
import asyncio
import sys

from rpcudp.protocol import RPCProtocol


class RPCClient(RPCProtocol):

    def __init__(self, server_ip, server_port):
        super().__init__()
        self.server_ip = server_ip
        self.server_port = server_port

    async def listen(self):
        while True:
            command = input()
            await self.command((self.server_ip, self.server_port), command)

    async def rpc_stdout(self, sender, message):
        sys.stdout.write(message.decode())
        return True

    async def rpc_stderr(self, sender, message):
        sys.stderr.write(message.decode())
        return True


def run_client(client_ip, client_port, server_ip, server_port):
    loop = asyncio.get_event_loop()

    def spawn_client():
        return RPCClient(server_ip, server_port)

    listen = loop.create_datagram_endpoint(spawn_client, local_addr=(client_ip, client_port))
    _, client = loop.run_until_complete(listen)

    try:
        loop.run_until_complete(client.listen())
    except KeyboardInterrupt:
        loop.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--address', type=str, required=True, help="Address to bind")
    parser.add_argument('--server_address', type=str, required=True, help="Server address")

    args = parser.parse_args(sys.argv[1:])

    _client_ip, _client_port = args.address.split(':')
    _server_ip, _server_port = args.server_address.split(':')

    run_client(_client_ip, int(_client_port), _server_ip, int(_server_port))
