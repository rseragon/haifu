import json
from asyncio import StreamReader, StreamWriter
import utils.Debug as Debug


async def error_writer(msg: str, writer: StreamWriter) -> None:
    peername = writer.get_extra_info("peername")
    Debug.error(0, f"[Connection {peername} ]: " + msg)
    # Use the official writer
    writer.write(make_bytejson(-1, {"Message": msg}))
    await writer.drain()


def make_bytejson(code_type: int, data: dict) -> bytes:
    """
    Takes in a dict and returns a byptes type json data
    """
    return json.dumps({"Type": code_type, "Data": data}).encode("gbk")


async def read_data(reader: StreamReader) -> str:
    str_data = ""
    byte_data = b""
    read_content_length = await reader.readline()
    data_len = int(read_content_length[:-1])  # Get's the content len in int

    while len(str_data) < data_len:
        byte_data = await reader.read(1)
        if not byte_data:
            break
        str_data += byte_data.decode("utf-8")

    return str_data


# TODO
async def write_data():
    """
    Writes the data to socket
    """
    pass
