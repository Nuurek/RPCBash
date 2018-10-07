import asyncio
import sys

from rpcudp.protocol import RPCProtocol


class RPCClient(RPCProtocol):

    async def listen(self):
        while True:
            command = input()
            await self.command(('127.0.0.1', 1234), command)

    async def rpc_stdout(self, sender, message):
        sys.stdout.write(message.decode())
        return True

    async def rpc_stderr(self, sender, message):
        sys.stderr.write(message.decode())
        return True


loop = asyncio.get_event_loop()
listen = loop.create_datagram_endpoint(RPCClient, local_addr=('127.0.0.1', 4567))
_, client = loop.run_until_complete(listen)

try:
    loop.run_until_complete(client.listen())
except KeyboardInterrupt:
    loop.close()
