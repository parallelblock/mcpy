from json import dumps, loads
import math
import struct
from uuid import UUID
import varint

def rip(buf, t, size):
    v = struct.unpack(t, buf[:size])[0]
    del buf[:size]
    return v

def pack(buf, t, val):
    buf.extend(struct.pack(t, val))

def r_s_byte(buf):
    return rip(buf, 'b', 1)

def w_s_byte(buf, val):
    pack(buf, 'b', val)

def r_u_byte(buf):
    return rip(buf, 'B', 1)

def w_u_byte(buf, val):
    pack(buf, 'B', val)

def r_bool(buf):
    return r_u_byte(buf) is 0x01

def w_bool(buf, val):
    w_u_byte(buf, val is True)

def r_s_short(buf):
    return rip(buf, 'h', 2)

def w_s_short(buf, val):
    pack(buf, 'h', val)

def r_u_short(buf):
    return rip(buf, 'H', 2)

def w_u_short(buf, val):
    pack(buf, 'H', val)

def r_s_int(buf):
    return rip(buf, 'i', 4)

def w_s_int(buf, val):
    pack(buf, 'i', val)

def r_s_long(buf):
    return rip(buf, 'q', 8)

def w_s_long(buf, val):
    pack(buf, 'q', val)

def r_float(buf):
    return rip(buf, 'f', 4)

def w_float(buf, val):
    pack(buf, 'f', val)

def r_double(buf):
    return rip(buf, 'd', 8)

def w_double(buf, val):
    pack(buf, 'd', val)

def r_vi(buf):
    b, n = varint.read_int(buf)
    del buf[:n]
    return b

def w_vi(buf, val):
    varint.write_int(val, buf)

def r_u8(buf):
    l = r_vi(buf)
    b = buf[:l]
    del buf[:l]
    return b.decode('utf-8')

def w_u8(buf, val):
    w_vi(buf, len(val))
    buf.extend(val.encode('utf-8'))

def r_json(buf):
    s = r_u8(buf)
    return loads(s)

def w_json(buf, val):
    w_u8(buf, dumps(s))

def r_vl(buf):
    b, n = varint.read_long(buf)
    del buf[:n]
    return b

def w_vi(buf, val):
    varint.write_long(val, buf)

# in radians!!!
def r_angle(buf):
    return 2 * math.pi * r_u_byte(buf) / 256

def w_angle(buf, val):
    w_u_byte(buf, val * 256 / 2 / math.pi)

def r_s_uuid(buf):
    u_s = r_u8(buf)
    return UUID(u_s)

def w_s_uuid(buf, val):
    w_u8(buf, str(val))

def r_uuid(buf):
    ur = buf[:16]
    del buf[:16]
    return UUID(bytes=ur)

def w_uuid(buf, val):
    buf.extend(val.bytes)

def r_v_bytes(buf):
    v = r_vi(buf)
    b = buf[:v]
    del buf[:v]
    return b

def w_v_bytes(buf, b):
    w_vi(buf, len(b))
    buf.extend(b)

s_byte = [r_s_byte, w_s_byte]
u_byte = [r_u_byte, w_u_byte]
m_bool = [r_bool, w_bool]
s_short = [r_s_short, w_s_short]
u_short = [r_u_short, w_u_short]
s_int = [r_s_int, w_s_int]
s_long = [r_s_long, w_s_long]
m_float = [r_float, w_float]
m_double = [r_double, w_double]
vi = [r_vi, w_vi]
angle = [r_angle, w_angle]
uuid = [r_uuid, w_uuid]
s_uuid = [r_s_uuid, w_s_uuid]
u8 = [r_u8, w_u8]
json = [r_json, w_json]
v_bytes = [r_v_bytes, w_v_bytes]
