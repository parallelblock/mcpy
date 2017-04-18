import login
from primative import r_vi
import status

class ProtoState():
    def __init__(self, server=False):
        self.server = server
        self.inbound = dict()
        self.outbound = dict()
    
    def decode(self, buf):
        p_id = r_vi(buf)
        p = self.inbound.get(p_id)

        if p is None:
            raise "state: no packet with id {}".format(p_id)

        return p.deserialize(buf)
       
    def encode(self, packet):
        t = type(packet)
        p = self.outbound.get(t)

        if p is None:
            raise "state: no encoder for type {}".format(t)

        return p.serialize(packet)

    def register(self, serializer, server_bound):
        if self.server is not server_bound:
            self.outbound[serializer.type] = serializer
        else:
            self.inbound[serializer.id] = serializer


class HandshakeState(ProtoState):
    def __init__(self, server=False):
        super().__init__(server)
        self.register(status.HandshakePacketSerializer(), True)

class StatusState(ProtoState):
    def __init__(self, server=False):
        super().__init__(server)
        self.register(status.StatusRequestPacketSerializer(), True)
        self.register(status.StatusPingPacketSerializer(), True)
        self.register(status.StatusResponsePacketSerializer(), False)
        self.register(status.StatusPongPacketSerializer(), False)

class LoginState(ProtoState):
    def __init__(self, server=False):
        super().__init__(server)

        self.register(login.LoginStartPacketSerializer(), True)
        self.register(login.LoginEncryptionResponsePacketSerializer(), True)

        self.register(login.LoginDisconnectPacketSerializer(), False)
        self.register(login.LoginEncryptionRequestPacketSerializer(), False)
        self.register(login.LoginSuccessPacketSerializer(), False)
        self.register(login.LoginSetCompressionPacketSerializer(), False)

class PlayState(ProtoState):
    def __init__(self, server=False):
        super().__init__(server)

class StateAdapter():
    def __init__(self, raw_source, raw_sink, initial_state):
        self.raw_source = raw_source
        self.raw_sink = raw_sink
        self.state = initial_state
    
    async def read_packet(self):
        d = await self.raw_source()
        return self.state.decode(d)

    async def write_packet(self, packet):
        d = self.state.encode(packet)
        await self.raw_sink(d)

