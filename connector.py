from asyncio import open_connection, start_server

import mcsocket

async def client_connect(host=None, port=None, **kwargs):
    reader, writer = await open_connection(host, port, **kwargs)
    return mcsocket.MinecraftSocketAdapter(host, port, reader, writer)

async def server_bind(cb, host=None, port=None, **kwargs):
    def cb_wrap(reader, writer):
        cb(mcsocket.MinecraftSocketAdapter(reader, writer))

    return await start_server(cb_wrap, host, port, **kwargs)
