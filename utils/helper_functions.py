import json
from asyncio import StreamReader, StreamWriter
import socket
import utils.Debug as Debug
from typing import Any
from utils.Types import ResultType


def make_response_strjson(code_type: int, data: Any) -> str:
    """
    Takes in a dict and returns a bytes type request json data
    """
    return json.dumps({"Type": code_type, "Payload": data})


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
    str_data = ""
    byte_data = b""
    read_content_length = await reader.readuntil(b'\n')
    data_len = int(read_content_length)  # Get's the content len in int

    while len(str_data) < data_len:
        byte_data = await reader.read(1)
        if not byte_data:
            break
        str_data += byte_data.decode("utf-8")

    return str_data


async def async_write_data(data: str, writer: StreamWriter):
    """
    Writes the data to socket
    """
    write_len = len(data)
    byte_data = data.encode("gbk")

    # Write the length of data to send
    writer.write((str(write_len)).encode("gbk"))
    writer.write(b'\n')
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

    bytes_data = data.encode('gbk')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

        # Connect
        try:
            sock.connect((host, port))
        except ConnectionRefusedError as cre:
            Debug.error(0, "Failed to connect to host ({}, {})".format(host, port))
            return ""

        # Send data
        sock.sendall(str(len(bytes_data)).encode('gbk')) # Send length
        sock.sendall(b'\n')  # A new line
        sock.sendall(bytes_data)  # the real data

        # Receive data
        while True:
            temp = sock.recv(1)
            if not temp: break
            resp += temp

    result = resp.decode('utf-8')

    return result[result.find('\n'):]  # removes the first line which contains the number
