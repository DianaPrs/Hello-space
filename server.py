import socket
import asyncio
import random

def run_server(host, port):

    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(handle_conn, host, port, loop=loop)
    server = loop.run_until_complete(coro)
    print('Serving on {}'.format(server.sockets[0].getsockname()))
    try:
      loop.run_forever()
    except KeyboardInterrupt:
      pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

async def handle_conn(reader, writer):
    while True:
        try:
            data = await reader.read(1024)
        except socket.timeout:
            print("close connection by timeout")
            break
        if not data:
            break
        res = str(random.randint(50, 250))
        writer.write(res.encode())


class Storage:

  def __init__(self, lst):
      self.lst = lst

stor = Storage([])
                    

if __name__ == '__main__':
  run_server('127.0.0.1', 8888)

