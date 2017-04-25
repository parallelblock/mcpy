from mcpy import primative, serializer
PacketSerializer = serializer.PacketSerializer

class StatusRequestPacket():
    def __init__(self):
        pass

class StatusRequestPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0
        self.fields = []
        self.type = StatusRequestPacket

class StatusPingPacket():
    def __init__(self, payload):
        self.payload = payload

class StatusPingPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 1
        self.fields = [["payload", primative.s_long]]
        self.type = StatusPingPacket

class StatusResponsePacket():
    def __init__(self, response):
        self.response = response

class StatusResponsePacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0
        self.fields = [["response", primative.json]]
        self.type=StatusResponsePacket

class StatusPongPacket():
    def __init__(self, payload):
        self.payload = payload

class StatusPongPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 1
        self.fields = [["payload", primative.s_long]]
        self.type = StatusPongPacket

class HandshakePacket():
    def __init__(self, proto_version, server_address, server_port, next_state):
        self.proto_version = proto_version
        self.server_address = server_address
        self.server_port = server_port
        self.next_state = next_state

class HandshakePacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0
        self.fields = [
                ["proto_version", primative.vi],
                ["server_address", primative.u8],
                ["server_port", primative.u_short],
                ["next_state", primative.vi]]
        self.type = HandshakePacket

