import primative
from serializer import PacketSerializer

class LoginDisconnectPacket():
    def __init__(self, reason):
        self.reason = reason

class LoginDisconnectPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0
        self.fields = [["reason", primative.json]]
        self.type = LoginDisconnectPacket

class LoginEncryptionRequestPacket():
    def __init__(self, server_id, public_key, verify_token):
        self.server_id = server_id
        self.public_key = public_key
        self.verify_token = verify_token

class LoginEncryptionRequestPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 1
        self.fields = [
                ["server_id", primative.u8],
                ["public_key", primative.v_bytes],
                ["verify_token", primative.v_bytes]]
        self.type = LoginEncryptionRequestPacket

class LoginSuccessPacket():
    def __init__(self, uuid, username):
        self.uuid = uuid
        self.username = username

class LoginSuccessPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 2
        self.fields = [
                ["uuid", primative.uuid],
                ["username", primative.u8]]
        self.type = LoginSuccessPacket

class LoginSetCompressionPacket():
    def __init__(self, threshold):
        self.threshold = threshold

class LoginSetCompressionPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 3
        self.fields = [["threshold", primative.vi]]
        self.type = LoginSetCompressionPacket

class LoginStartPacket():
    def __init__(self, username):
        self.username = username

class LoginStartPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0
        self.fields = [["username", primative.u8]]
        self.type = LoginStartPacket

class LoginEncryptionResponsePacket():
    def __init__(self, shared_secret, verify_token):
        self.shared_secret = shared_secret
        self.verify_token = verify_token

class LoginEncryptionResponsePacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 1
        self.fields = [
                ["shared_secret", primative.v_bytes],
                ["verify_token", primative.v_bytes]]
        self.type = LoginEncryptionResponsePacket
