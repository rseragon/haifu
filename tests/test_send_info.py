import asyncio
from daemon.request_handler import send_info
import utils.Config as Config

async def test_send_info():
    reader, writer = await asyncio.open_connection(*Config.get_hostport())
    await send_info(writer)

asyncio.run(test_send_info())
