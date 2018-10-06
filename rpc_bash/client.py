import asyncio

from rpcudp.protocol import RPCProtocol


@asyncio.coroutine
def sayhi(rpc_protocol, address):
    result = yield from rpc_protocol.sayhi(address, "Snake Plissken")
    print(result[1] if result[0] else "No response received.")


loop = asyncio.get_event_loop()
listen = loop.create_datagram_endpoint(RPCProtocol, local_addr=('127.0.0.1', 4567))
transport, protocol = loop.run_until_complete(listen)

func = sayhi(protocol, ('127.0.0.1', 1234))
try:
    loop.run_until_complete(func)
    loop.run_forever()
except KeyboardInterrupt:
    pass
