import asyncio
from subprocess import Popen, PIPE
from threading import Thread

from rpcudp.protocol import RPCProtocol


class RPCServer(RPCProtocol):

    def __init__(self):
        super().__init__()
        self.pipe = None

    async def rpc_command(self, sender, command):
        pipe = Popen(command, stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)
        stdout_thread = Thread(target=self.send_stdout, args=(sender, pipe))
        stdout_thread.run()
        stderr_thread = Thread(target=self.send_stderr, args=(sender, pipe))
        stderr_thread.run()
        return True

    def send_stdout(self, sender, pipe):
        for line in iter(pipe.stdout.readline, 'b'):
            if line:
                self.stdout(sender, line)
            else:
                break

    def send_stderr(self, sender, pipe):
        for line in iter(pipe.stderr.readline, 'b'):
            if line:
                self.stderr(sender, line)
            else:
                break


loop = asyncio.get_event_loop()
listen = loop.create_datagram_endpoint(RPCServer, local_addr=('127.0.0.1', 1234))
transport, protocol = loop.run_until_complete(listen)

try:
    loop.run_forever()
except KeyboardInterrupt:
    loop.close()
