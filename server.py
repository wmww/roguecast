#!/usr/bin/python3
import sys
from typing import Any
import cast_channel_pb2

def read_byte() -> int:
    buf = bytes()
    while len(buf) == 0:
        buf = sys.stdin.buffer.read(1)
    assert len(buf) == 1
    return buf[0]

def write_bytes(data: bytes):
    sys.stdout.buffer.write(data)
    sys.stdout.flush()

def read_message() -> Any:
    size = 0
    for i in range(4):
        size *= 256
        size += read_byte()
    print('reading message with', size, 'bytes', file=sys.stderr)
    b = bytearray()
    while (size):
        b.append(read_byte())
        size -= 1
    return cast_channel_pb2.CastMessage().FromString(b)

def write_message(msg: Any) -> None:
    b = msg.SerializeToString()
    size = len(b)
    size_array = []
    for i in range(4):
        size_array.insert(0, size % 256)
        size /= 256
    write_bytes(bytes(size_array))
    write_bytes(b)

def main():
    msg = read_message()
    print('received:\n', repr(msg), file=sys.stderr)
    msg = cast_channel_pb2.CastMessage()
    msg.protocol_version = cast_channel_pb2.CastMessage.CASTV2_1_0
    msg.destination_id = '*'
    msg.source_id = 'sender-0'
    msg.namespace = 'urn:x-cast:com.google.cast.tp.deviceauth'
    msg.payload_type = cast_channel_pb2.CastMessage.BINARY
    auth_response = cast_channel_pb2.DeviceAuthMessage()
    resp = cast_channel_pb2.AuthResponse()
    resp.signature = bytes()
    resp.client_auth_certificate = bytes()
    auth_response.response.CopyFrom(resp)
    msg.payload_binary = auth_response.SerializeToString()
    print('sending:\n', repr(msg), file=sys.stderr)
    write_bytes(msg.SerializeToString())
    msg = read_message()
    print('received:\n', repr(msg), file=sys.stderr)

if __name__ == '__main__':
    main()
