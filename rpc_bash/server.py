import argparse
import asyncio
import sys
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


def run_server(server_ip, server_port):
    loop = asyncio.get_event_loop()
    listen = loop.create_datagram_endpoint(RPCServer, local_addr=(server_ip, server_port))
    loop.run_until_complete(listen)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--address', type=str, required=True, help="Address to bind")

    args = parser.parse_args(sys.argv[1:])

    ip, port = args.address.split(':')

    run_server(ip, int(port))
