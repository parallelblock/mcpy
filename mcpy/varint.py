import struct

# http://wiki.vg/Protocol#VarInt_and_VarLong
def prefixed_with_varlong(buf, mlen=10):
    """
    Returns whether the data is prefixed with what is probably a valid varint
    """
    for i in range(mlen):
        if len(buf) <= i:
            return False

        if buf[i] & 0x80 == 0x00:
            return True
    return False

def prefixed_with_varint(data):
    return prefixed_with_varlong(data, mlen=5)

def write_long(value, buf, bits=64, cap=10):
    if value < 0:
        value += (1 << bits)

    while True:
        tmp = value & 0x7f
        value >>= 7
        if not value or len(buf) is cap:
            buf.extend(struct.pack('B', tmp))
            return
       
        buf.extend(struct.pack('B', tmp | 0x80))

def write_int(value, buf):
    return write_long(value, buf, bits=32, cap=5)

def read_long(buf, bits=64, cap=10):
    read_cnt = 0
    value = 0
    while True:
        byte = buf[read_cnt] & 0xff
        value |= ((byte & 0x7f) << (7 * read_cnt))
        
        read_cnt += 1
        if read_cnt > cap:
            raise "varnum too long"
        if not byte & 0x80:
            if value & (1 << (bits - 1)):
                value -= (1 << bits)
            return value, read_cnt

def read_int(buf):
    return read_long(buf, cap=5, bits=32)
