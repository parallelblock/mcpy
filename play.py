import metadata
import primative
from serializer import PacketSerializer

class PlaySpawnObjectPacket():
    def __init__(self, eid, uuid, o_type, x, y, z, pitch, yaw, data, vx, vy, vz):
        self.eid = eid
        self.uuid = uuid
        self.o_type = o_type
        self.x = x
        self.y = y
        self.z = z
        self.pitch = pitch
        self.yaw = yaw
        self.data = data
        self.vx = vx
        self.vy = vy
        self.vz = vz

class PlaySpawnObjectPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0
        self.fields = [
                ["eid", primative.vi],
                ["uuid", primative.uuid],
                ["type", primative.u_byte],
                ["x", primative.m_double],
                ["y", primative.m_double],
                ["z", primative.m_double],
                ["pitch", primative.angle],
                ["yaw", primative.angle],
                ["data", primative.s_int],
                ["vx", primative.s_short],
                ["vy", primative.s_short],
                ["vz", primative.s_short]]
        self.type = PlaySpawnObjectPacket

class PlaySpawnExpOrbPacket():
    def __init__(self, eid, x, y, z, count):
        self.eid = eid
        self.x = x
        self.y = y
        self.z = z
        self.count = count

class PlaySpawnExpOrbPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 1
        self.fields = [
            ["eid", primative.vi],
            ["x", primative.m_double],
            ["y", primative.m_double],
            ["z", primative.m_double],
            ["count", primative.u_short]]
        self.type = PlaySpawnExpOrbPacket

class PlaySpawnGlobalEntityPacket():
    def __init__(self, eid, e_type, x, y, z):
        self.eid = eid
        self.e_type = e_type
        self.x = x
        self.y = y
        self.z = z

class PlaySpawnGlobalEntityPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 2
        self.fields = [
            ["eid", primative.vi],
            ["e_type", primative.u_byte],
            ["x", primative.m_double],
            ["y", primative.m_double],
            ["z", primative.m_double]]
        self.type = PlaySpawnGlobalEntityPacket

class PlaySpawnMobPacket():
    def __init__(self, eid, e_uuid, e_type, x, y, z, yaw, pitch, head_pitch, 
            vx, vy, vz, metadata):
        self.eid = eid
        self.e_uuid = e_uuid
        self.e_type = e_type
        self.x = x
        self.y = y
        self.z = z
        self.yaw = yaw
        self.pitch = pitch
        self.head_pitch = head_pitch
        self.vx = vx
        self.vy = vy
        self.vz = vz
        self.metadata = metadata

class PlayerSpawnMobPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 3
        self.fields = [
            ["eid", primative.vi],
            ["e_uuid", primative.uuid],
            ["e_type", primative.vi],
            ["x", primative.m_double],
            ["y", primative.m_double],
            ["z", primative.m_double],
            ["yaw", primative.angle],
            ["pitch", primative.angle],
            ["head_pitch", primative.angle],
            ["vx", primative.s_short],
            ["vy", primative.s_short],
            ["vz", primative.s_short],
            ["metadata", metadata.meta_type]]
        self.type = PlayerSpawnMobPacket

class PlaySpawnPaintingPacket():
    def __init__(self, e_id, e_uuid, title, location, direction):
        self.e_id = e_id
        self.e_uuid = e_uuid
        self.title = title
        self.location = location
        self.direction = direction

class PlayerSpawnPaintingPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 4
        self.fields = [
            ["e_id", primative.vi],
            ["e_uuid", primative.uuid],
            ["title", primative.u8],
            ["location", primative.position],
            ["direction", primative.u_byte]]
        self.type = PlaySpawnPaintingPacket

class PlaySpawnPlayerPacket():
    def __init__(self, e_id, p_uuid, x, y, z, yaw, pitch, metadata):
        self.e_id = e_id
        self.p_uuid = p_uuid
        self.x = x
        self.y = y
        self.z = z
        self.yaw = yaw
        self.pitch = pitch
        self.metadata = metadata

class PlayerSpawnPlayerPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 5
        self.fields = [
            ["e_id", primative.vi],
            ["p_uuid", primative.uuid],
            ["x", primative.m_double],
            ["y", primative.m_double],
            ["z", primative.m_double],
            ["yaw", primative.angle],
            ["pitch", primative.angle],
            ["metadata", metadata.meta_type]]
        self.type = PlayerSpawnPlayerPacket

class PlayAnimationPacket():
    def __init__(self, e_id, animation):
        self.e_id = e_id
        self.animation = animation

class PlayerAnimationPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 6
        self.fields = [
            ["e_id", primative.vi],
            ["animation", primative.u_byte]]
        self.type = PlayerAnimationPacket
