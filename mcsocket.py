import asyncio
import traceback
import zlib

from Crypto.Cipher import AES

import varint

class ProtoException(Exception):
    pass

class MinecraftSocketAdapter:
    def __init__(self, host, port, reader=None, writer=None):
        self.host = host
        self.port = port
        self.reader = reader
        self.writer = writer

        self.comp_threshold = -1
        
        self.read_lock = asyncio.Lock()
        self.write_lock = asyncio.Lock()

        self.decrypt = None
        self.encrypt = None

    def start_encryption(self, key):
        if self.decrypt is not None or self.encrypt is not None:
            raise ProtoException("illegal state: already started encryption!")

        self.decrypt = AES.new(key=key, mode=AES.MODE_CFB, IV=key)
        self.encrypt = AES.new(key=key, mode=AES.MODE_CFB, IV=key)

    def start_compression(self, compression):
        self.comp_threshold = compression
    
    async def send_packet(self, data):
        await self.write_lock.acquire()
        try:    
            unc_len = len(data)
            if self.comp_threshold >= 0:
                buf = bytearray()
                if self.comp_threshold <= unc_len:
                    varint.write_int(unc_len, buf)
                    buf.extend(zlib.compress(data))
                else:
                    varint.write_int(0, buf)
                    buf.extend(data)
                data = buf

            buf = bytearray()
            l = len(data)
            varint.write_int(l, buf)
            buf.extend(data)

            if self.encrypt is not None:
                buf = self.encrypt.encrypt(buf)

            self.writer.write(buf)
        finally:
            self.write_lock.release()

    async def _read_bytes(self, n=-1, exact=False):
        if exact:
            b = await self.reader.readexactly(n)
        else:
            b = await self.reader.read(n)
        
        if self.decrypt:
            b = self.decrypt.decrypt(b)
        
        return b

    async def read_packet(self):
        await self.read_lock.acquire()
        try:
            prefix_length_left = 10
            packet_len = -1
            buf = bytearray()
            while prefix_length_left > 0:
                byt = await self._read_bytes(n=1, exact=True)
                buf.extend(byt)
                if varint.prefixed_with_varint(buf):
                    packet_len, n = varint.read_int(buf)
                    del buf[:n]
                    break
                prefix_length_left -= 1

            if packet_len is -1:
                raise ProtoException("proto error: packet length varint overran")
                
            dat = await self._read_bytes(n=packet_len-len(buf), exact=True)
            buf.extend(dat)

            if self.comp_threshold >= 0:
                uncomp_len, n = varint.read_int(buf)
                if uncomp_len is not 0 and uncomp_len < self.comp_threshold:
                    raise ProtoException("proto error: sent compressed packet below threshold")
                del buf[:n]
                if uncomp_len is not 0:
                    buf = zlib.decompress(buf, bufsize=uncomp_len)
                    if len(buf) is not uncomp_len:
                        raise ProtoException("proto error: uncompressed size doesn't match expected")

            return buf
        finally:
            self.read_lock.release()

    def close(self):
        self.writer.close()

