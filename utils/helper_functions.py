import json
from asyncio import StreamReader, StreamWriter
from pathlib import Path
import socket
import utils.Debug as Debug
from typing import Any
from utils.Types import RequestType, ResultType
import utils.Config as Config
import aiofiles
import os


def make_response_strjson(code_type: int, data: Any, info: str = "") -> str:
    """
    Takes in a dict and returns a bytes type request json data
    """
    if code_type == RequestType.PING:
        return json.dumps({"Type": code_type, "Payload": {"info": info}})

    elif code_type in [
        RequestType.SEARCH,
        RequestType.GET_INFO,
        RequestType.SEND_PKG,
        RequestType.FETCH_PKG,
    ]:
        return json.dumps(
            {"Type": code_type, "Payload": {"Package Name": data, "info": info}}
        )

    elif code_type == RequestType.PKG_INDEX:
        return json.dumps({"Type": code_type, "Payload": {"info": info, "index": data}})

    elif code_type == RequestType.PEER_INFO:
        return json.dumps({"Type": code_type, "Payload": {"info": info}})

    elif code_type == RequestType.ADD_PEER:
        host, port = data
        return json.dumps(
            {"Type": code_type, "Payload": {"host": host, "port": port, "info": info}}
        )


def make_result_strjson(result_type: int, data: Any, error: str = "") -> str:
    """
    Takes in a dict and returns a byptes type json data
    """
    return json.dumps(
        {"Result": result_type, "Payload": {"Data": data, "Error": error}}
    )


# TODO: type annotation
def dict_from_str(data: str) -> Any:
    """
    process the string data into dict or list[dict]
    returns the 0th index of the list[dict]
    """
    # json_data: Union[list, None] = None  # TODO: type annotation
    json_data: Any = None
    try:
        json_data = json.loads(data)
    except json.JSONDecodeError:
        # Debug.error(0, "[Connection] failed to decode JSON")
        return None
    except Exception as ex:
        Debug.error(0, "Exception while parsing data: " + str(ex))
        return None

    if isinstance(json, list) and len(json_data) == 0:
        return None

    return json_data[0] if (isinstance(json_data, list)) else json_data


async def async_read_data(reader: StreamReader) -> str:
    """
    Reads the data from readers and returns the read string
    """
    str_data = ""
    byte_data = b""
    try:
        read_content_length = await reader.readuntil(b'\n')
        #read_content_length = await reader.readline()
        data_len = int(read_content_length[:-1])  # Get's the content len in int

        # Now read th data
        while len(str_data) < data_len:
            byte_data = await reader.read(1)
            if not byte_data:
                break
            str_data += byte_data.decode("utf-8")

        return str_data
    except Exception as e:
        Debug.debug("[Connection] Failed to read data: " + str(e))
        return ""


async def async_write_data(data: str, writer: StreamWriter):
    """
    Writes the data to socket
    """
    write_len = len(data)
    byte_data = data.encode("gbk")

    # Write the length of data to send
    writer.write((str(write_len)).encode("gbk"))
    writer.write(b"\n")
    await writer.drain()

    # write the data
    writer.write(byte_data)
    await writer.drain()


async def async_error_writer(msg: str, writer: StreamWriter) -> None:
    peername = writer.get_extra_info("peername")
    Debug.error(0, f"[Connection {peername} ]: " + msg)
    error_message = make_result_strjson(ResultType.ERROR, {}, msg)
    # error_message = make_strjson(-1, msg)
    await async_write_data(error_message, writer)


def send_data(data: str, host: str, port: int) -> str:
    """
    Sends data to (host, port) and returns response
    using Block socket connection
    """
    resp = b""

    bytes_data = data.encode("gbk")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

        # Connect
        try:
            sock.connect((host, port))
        except ConnectionRefusedError as cre:
            Debug.error(0, "Failed to connect to host ({}, {})".format(host, port))
            return ""

        # Send data
        sock.sendall(str(len(bytes_data)).encode("gbk"))  # Send length
        sock.sendall(b"\n")  # A new line
        sock.sendall(bytes_data)  # the real data

        # Receive data
        while True:
            temp = sock.recv(1)
            if not temp:
                break
            resp += temp

    result = resp.decode("utf-8")

    return result[
        result.find("\n") :
    ]  # removes the first line which contains the number


async def send_file(file_location: str, writer: StreamWriter) -> None:
    """
    sends file to writer
    """
    Debug.debug(
        f"[Package] sending {file_location} to {writer.get_extra_info('peername')}"
    )

    Debug.info(f"[USELESS] file_loc: {file_location}")
    file_size = os.path.getsize(file_location)

    data = str(file_size)
    writer.write(str(data + "\n").encode("gbk"))
    await writer.drain()

    async with aiofiles.open(file_location, mode="rb") as f:
        while data != b"":
            data = await f.read(1024)  # TODO: Chunk it better
            writer.write(data)

    await writer.drain()


async def recv_file(filename: str, reader: StreamReader) -> str:
    """
    recevices the files and returns the stored locations
    TODO: What if the file is very large
    """
    file_size = int(await reader.readline())

    Debug.info(f"[USELESS] file size: {file_size}")

    cache_path = Config.get_cachedir()
    Debug.info(f"[USELESS] cache dir: {cache_path}")

    file_loc = Path(cache_path) / filename

    Debug.info(f"[USELESS] file_loc: {file_loc}")

    try:
        async with aiofiles.open(file_loc, mode="wb") as f:
            while True:
                data: bytes = await reader.read(1024)
                if len(data) == 0:
                    break
                await f.write(data)

        Debug.debug(f"[File] file received: {file_loc}")

        return str(file_loc)
    except Exception as e:
        Debug.error(0, f"[File] Failed to Receive file: {filename} ({str(e)})")
        return ""
