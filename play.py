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

class PlayStatisticsPacket():
    def __init__(self, statistics={}):
        self.statistics = statistics

class PlayerStatisticsPacketSerializer():
    def __init__(self):
        self.id = 7
        self.type = PlayStatisticsPacket

    def serialize(self, packet):
        b = bytearray()
        primative.w_vi(b, self.id)
        primative.w_vi(b, len(packet.statistics))
        for k, v in packet.statistics:
            primative.w_u8(b, k)
            primative.w_vi(b, v)
        return b

    def deserialize(self, b):
        stats = dict()
        cnt = primative.r_vi(b)
        for i in range(cnt):
            k = primative.r_u8(b)
            v = primative.r_vi(b)
            stats[k] = v

        return self.type(stats)

class PlayBlockBreakAnimationPacket():
    def __init__(self, e_id, position, stage):
        self.e_id = e_id
        self.position = position
        self.stage = stage

class PlayBlockBreakAnimationPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 8
        self.fields = [
            ["e_id", primative.vi],
            ["position", primative.position],
            ["stage", primative.s_byte]]
        self.type = PlayBlockBreakAnimationPacket

class PlayUpdateBlockEntityPacket():
    def __init__(self, location, action, data):
        self.location = location
        self.action = action
        self.data = data

class PlayUpdateBlockEntityPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 9
        self.fields = [
            ["location", primative.position],
            ["action", primative.u_byte],
            ["data", primative.m_nbt]]
        self.type = PlayUpdateBlockEntityPacket

class PlayBlockActionPacket():
    def __init__(self, location, action_id, action_param, block_type):
        self.location = location
        self.action_id = action_id
        self.action_param = action_param
        self.block_type = block_type

class PlayBlockActionPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0xa
        self.fields = [
            ["location", primative.position],
            ["action_id", primative.u_byte],
            ["action_param", primative.u_byte],
            ["block_type", primative.vi]]
        self.type = PlayBlockActionPacket

class PlayBlockChangePacket():
    def __init__(self, location, block_id):
        self.location = location
        self.block_id = block_id

class PlayBlockChangePacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0xb
        self.fields = [
            ["location", primative.position],
            ["block_id", primative.vi]]
        self.type = PlayBlockChangePacket

class PlayBossBarPacket():
    def __init__(self, uuid, action, **kwargs):
        self.uuid = uuid
        self.action = action
        for k, v in kwargs:
            setattr(self, k, v)

class PlayBossBarAddSerializer():
    def serialize(self, buf, packet):
        primative.w_json(buf, packet.title)
        primative.w_float(buf, packet.health)
        primative.w_vi(buf, packet.color)
        primative.w_vi(buf, packet.division)
        primative.w_u_byte(buf, packet.flags)

    def deserialize(self, buf):
        d = dict()
        d["title"] = primative.r_json(buf)
        d["health"] = primative.r_float(buf)
        d["color"] = primative.r_vi(buf)
        d["division"] = primative.r_vi(buf)
        d["flags"] = primative.r_u_byte(buf)
        return d

class PlayBossBarRmSerializer():
    def serialize(self, buf, packet):
        pass

    def deserialize(self, buf):
        return dict()

class PlayBossBarHealthSerializer():
    def serialize(self, buf, packet):
        primative.w_float(buf, packet.health)

    def deserialize(self, buf):
        d = dict()
        d["health"] = primative.r_float(buf)
        return d

class PlayBossBarTitleSerializer():
    def serialize(self, buf, packet):
        primative.w_json(buf, packet.title)

    def deserialize(self, buf):
        d = dict()
        d["title"] = primative.r_json(buf)
        return d

class PlayBossBarStyleSerializer():
    def serialize(self, buf, packet):
        primative.w_vi(buf, packet.color)
        primative.w_vi(buf, packet.division)

    def deserialize(self, buf):
        d = dict()
        d["color"] = primative.r_vi(buf)
        d["divisoin"] = primative.r_vi(buf)
        return d

class PlayBossBarFlagsSerializer():
    def serialize(self, buf, packet):
        primative.w_u_byte(buf, packet.flags)

    def deserialize(self, buf):
        d = dict()
        d["flags"] = primative.r_u_byte(buf)
        return d

class PlayBossBarPacketSerializer():
    def __init__(self):
        self.id = 0xc
        self.type = PlayBossBarPacket
        self.actions = {
            0: PlayBossBarAddSerializer(),
            1: PlayBossBarRmSerializer(),
            2: PlayBossBarHealthSerializer(),
            3: PlayBossBarTitleSerializer(),
            4: PlayBossBarStyleSerializer(),
            5: PlayBossBarFlagsSerializer()}

    def serialize(self, packet):
        b = bytearray()
        primative.w_vi(b, self.id)
        primative.w_uuid(b, packet.uuid)
        primative.w_vi(b, packet.action)
        handler = self.actions[packet.action]
        handler.serialize(b, packet)
        return b

    def deserialize(self, b):
        u = primative.r_uuid(b)
        action = primative.r_vi(b)
        handler = self.actions[action]
        d = handler.deserialize(b)
        return PlayBossBarPacket(u, action, d)

        return self.type(stats)

class PlayDifficultyPacket():
    def __init__(self, difficulty):
        self.difficulty = difficulty

class PlayDifficultyPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0xd
        self.fields = [
            ["difficulty", primative.u_byte]]
        self.type = PlayDifficultyPacket

class PlayTabCompleteResponsePacket():
    def __init__(self, matches):
        self.matches = matches

class PlayTabCompleteResponsePacketSerializer():
    def __init__(self):
        self.id = 0xe
        self.type = PlayTabCompleteResponsePacket

    def serialize(self, packet):
        b = bytearray()
        primative.w_vi(b, self.id)
        primative.w_vi(b, len(packet.matches))
        for i in packet.matches:
            primative.w_u8(b, i)
        return b

    def deserialize(self, b):
        cnt = primative.r_vi(b)
        m = []
        for i in range(cnt):
            m.append(primative.r_u8(b))
        return PlayTabCompleteResponsePacket(m)

class PlayChatPacket():
    def __init__(self, chat, position=0):
        self.chat = chat

class PlayChatPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0xf
        self.fields = [
            ["chat", primative.json],
            ["position", primative.s_byte]]
        self.type = PlayChatPacket

class PlayMultiBlockChangePacket():
    def __init__(self, c_x, c_y, records):
        self.c_x = c_x
        self.c_y = c_y
        self.records = records

class PlayTabCompleteResponsePacketSerializer():
    def __init__(self):
        self.id = 0x10
        self.type = PlayMultiBlockChangePacket

    def serialize(self, packet):
        b = bytearray()
        primative.w_vi(b, self.id)
        primative.w_s_int(b, self.c_x)
        primative.w_s_int(b, self.c_z)
        primative.w_vi(b, len(packet.records))
        for r in packet.records:
            xz = (r.x & 0xf) | ((r.z & 0xf) << 4)
            primative.w_u_byte(b, xz)
            primative.w_u_byte(b, r.y)
            primative.w_vi(b, r.b_id)
        return b

    def deserialize(self, b):
        c_x = primative.r_s_int(b)
        c_y = primative.r_s_int(b)
        cnt = primative.r_vi(b)
        r = []
        for i in range(cnt):
            rec = dict()
            xz = primative.r_u_byte(b)
            rec["x"] = xz & 0xf
            rec["z"] = (xz >> 4) & 0xf
            rec["y"] = primative.r_u_byte(b)
            rec["b_id"] = primative.r_vi(b)
            r.append(rec)
        return PlayMultiBlockChangePacket(c_x, c_y, r)

class PlayConfirmInvTransactionPacket():
    def __init__(self, w_id, action_number, accepted):
        self.w_id = w_id
        self.action_number = action_number
        self.accepted = accepted

class PlayConfirmInvTransactionPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0x11
        self.fields = [
            ["w_id", primative.s_byte],
            ["action_number", primative.s_short],
            ["accepted", primative.m_bool]]
        self.type = PlayConfirmInvTransactionPacket

class PlayCloseWindowPacket():
    def __init__(self, w_id):
        self.w_id = w_id

class PlayCloseWindowPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0x12
        self.fields = [["w_id", primative.u_byte]]
        self.type = PlayCloseWindowPacket

class PlayOpenWindowPacket():
    def __init__(self, w_id, w_type, title, slots, e_id=None):
        self.w_id = w_id
        self.w_type = w_type
        self.title = title
        self.slots = slots
        self.e_id = e_id

class PlayOpenWindowPacketSerializer():
    def __init__(self):
        self.id = 0x13
        self.type = PlayOpenWindowPacket

    def serialize(self, packet):
        b = bytearray()
        primative.w_vi(b, self.id)
        primative.w_u_byte(b, packet.w_id)
        primative.w_u8(b, packet.w_type)
        primative.w_json(b, packet.title)
        primative.w_u_byte(b, packet.slots)
        if packet.e_id is not None:
            primative.w_s_int(b, packet.e_id)
        return b

    def deserialize(self, b):
        w_id = primative.r_u_byte(b)
        w_type = primative.r_u8(b)
        title = primative.r_json(b)
        slots = primative.r_u_byte(b)
        e_id = None
        if w_type != "EntityHorse":
            e_id = primative.r_s_int(b)

        return PlayOpenWindowPacket(w_id, w_type, title, slots, e_id)

class PlayWindowItemsPacket():
    def __init__(self, w_id, items):
        self.w_id = w_id
        self.items = items

class PlayWindowItemsPacketSerializer():
    def __init__(self):
        self.id = 0x14
        self.type = PlayWindowItemsPacket

    def serialize(self, packet):
        b = bytearray()
        primative.w_vi(b, self.id)
        primative.w_u_byte(b, packet.w_id)
        primative.w_s_short(b, len(packet.items))
        for i in packet.items:
            metadata.w_slot(b, i)
        return b

    def deserialize(self, b):
        w_id = primative.r_u_byte(b)
        cnt = primative.r_s_short(b)
        itms = []
        for i in range(cnt):
            itms.append(metadata.r_slot(b))
        return PlayWindowItemsPacket(w_id, itms)

class PlayWindowPropertyPacket():
    def __init__(self, w_id, prop, value):
        self.w_id = w_id
        self.prop = prop
        self.value = value

class PlayWindowPropertyPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0x15
        self.fields = [
            ["w_id", primative.u_byte],
            ["prop", primative.s_short],
            ["value", primative.s_short]]
        self.type = PlayWindowPropertyPacket

class PlaySetSlotPacket():
    def __init__(self, w_id, slot_num, data):
        self.w_id = w_id
        self.slot_num = slot_num
        self.data = data

class PlaySetSlotPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0x16
        self.fields = [
            ["w_id", primative.u_byte],
            ["slot_num", primative.s_short],
            ["data", [metadata.r_slot, metadata.w_slot]]]
        self.type = PlaySetSlotPacket

class PlaySetCooldownPacket():
    def __init__(self, item_id, cooldown):
        self.item_id = item_id
        self.cooldown = cooldown

class PlaySetCooldownPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0x17
        self.fields = [
            ["item_id", primative.vi],
            ["cooldown", primative.vi]]
        self.type = PlaySetCooldownPacket

class PlayPluginMessageClientboundPacket():
    def __init__(self, channel, data):
        self.channel = channel
        self.data = data

class PlayPluginMessageClientboundPacketSerializer():
    def __init__(self):
        self.id = 0x18
        self.type = PlayPluginMessageClientboundPacket

    def serialize(self, packet):
        b = bytearray()
        primative.w_vi(b, self.id)
        primative.w_u8(b, packet.channel)
        b.extend(packet.data)
        return b
    
    def deserialize(self, buf):
        channel = primative.r_u8(buf)
        return PlayPluginMessageClientboundPacket(channel, buf)

class PlayNamedSoundEffectPacket():
    def __init__(self, name, catagory, x, y, z, volume, pitch):
        self.name = name
        self.catagory = catagory
        self.x = x
        self.y = y
        self.z = z
        self.volume = volume
        self.pitch = pitch

class PlayNamedSoundEffectPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0x19
        self.fields = [
            ["name", primative.u8],
            ["catagory", primative.vi],
            ["x", primative.s_int],
            ["y", primative.s_int],
            ["z", primative.s_int],
            ["volume", primative.m_float],
            ["pitch", primative.m_float]]
        self.type = PlayNamedSoundEffectPacket

class PlayKickPacket():
    def __init__(self, reason):
        self.reason = reason

class PlayKickPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0x1a
        self.fields = [["reason", primative.json]]
        self.type = PlayKickPacket

class PlayEntityStatusPacket():
    def __init__(self, e_id, status):
        self.e_id = e_id
        self.status = status

class PlayEntityStatusPacketSerializer(PacketSerialier):
    def __init__(self):
        self.id = 0x1b
        self.fields = [
            ["e_id", primative.s_int],
            ["status", primative.s_byte]]
        self.type = PlayEntityStatusPacket

class PlayExplosionPacket():
    def __init__(self, x, y, z, radius, records, p_x, p_y, p_z):
        self.x = x
        self.y = y
        self.z = z
        self.radius = radius
        self.records = records
        self.p_x = p_x
        self.p_y = p_y
        self.p_z = p_z

class PlayExplosionPacketSerializer():
    def __init__(self):
        self.id = 0x1c
        self.type = PlayExplosionPacket

    def serialize(self, packet):
        b = bytearray()
        primative.w_float(b, packet.x)
        primative.w_float(b, packet.y)
        primative.w_float(b, packet.z)
        primative.w_float(b, packet.radius)
        primative.w_s_int(b, len(packet.records))
        for r in packet.records:
            for i in range(3):
                primative.w_s_byte(b, r[i])
        primative.w_float(b, packet.p_x)
        primative.w_float(b, packet.p_y)
        primative.w_float(b, packet.p_z)
        return b

    def deserialize(self, b):
        x = primative.r_float(b)
        y = primative.r_float(b)
        z = primative.r_float(b)
        radius = primative.r_float(b)
        cnt = primative.r_s_int(b)
        rcds = []
        for i in range(cnt):
            rcds.append((primative.r_s_byte(b), 
                primative.r_s_byte(b), primative.r_s_byte(b)))
        p_x = primative.r_float(b)
        p_y = primative.r_float(b)
        p_z = primative.r_float(b)
        return PlayExplosionPacket(x, y, z, radius, rcds, p_x, p_y, p_z)

class PlayUnloadChunkPacket():
    def __init__(self, c_x, c_z):
        self.c_x = c_x
        self.c_z = c_z

class PlayUnloadChunkPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0x1d
        self.fields = [
            ["c_x", primative.s_int],
            ["c_z", primative.s_int]]
        self.type = PlayUnloadChunkPacket

class PlayChangeGameStatePacket():
    def __init__(self, reason, value):
        self.reason = reason
        self.value = value

class PlayChangeGameStatePacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0x1e
        self.fields = [
            ["reason", primative.u_byte],
            ["value", primative.m_float]]
        self.type = PlayChangeGameStatePacket

class PlayKeepAliveClientboundPacket():
    def __init__(self, ka_id):
        self.ka_id = ka_id

class PlayKeepAliveClientboundPacketSerializer(PacketSerialier):
    def __init__(self):
        self.id = 0x1f
        self.fields =[["ka_id", primative.vi]]
        self.type = PlayKeepAliveClientboundPacket

# TODO: Implement this in a sane way
class PlayChunkDataPacket():
    def __init__(self):
        pass

class PlayChunkDataPacketSerialier(PacketSerializer):
    def __init__(self):
        self.id = 0x20
        self.fields = []
        self.type = PlayChunkDataPacket

class PlayEffectPacket():
    def __init__(self, e_id, location, data, disable_relative_volume):
        self.e_id = e_id
        self.location = location
        self.data = data
        self.disable_relative_volume = disable_relative_volume

class PlayEffectPacketSerialier(PacketSerializer):
    def __init__(self):
        self.id = 0x21
        self.fields = [
            ["e_id", primative.s_int],
            ["location", primative.position],
            ["data", primative.s_int],
            ["disable_relative_volume", primative.m_bool]]
        self.type = PlayEffectPacket

class PlayParticlePacket():
    def __init__(self, p_id, long_distance, x, y, z, o_x, o_y, o_z, data,
            count, b_data1=None, b_data2=None):
        self.p_id = p_id
        self.long_distance = long_distance
        self.x = x
        self.y = y
        self.z = z
        self.o_x = o_x
        self.o_y = o_y
        self.o_z = o_z
        self.data = data
        self.count = count
        self.b_data1 = b_data1
        self.b_data2 = b_data2

class PlayParticlePacketSerialier(PacketSerializer):
    def __init__(self):
        self.id = 0x22
        self.fields = [
            ["p_id", primative.s_int],
            ["long_distance", primative.m_bool],
            ["x", primative.m_float],
            ["y", primative.m_float],
            ["z", primative.m_float],
            ["o_x", primative.m_float],
            ["o_y", primative.m_float],
            ["o_z", primative.m_float],
            ["data", primative.m_float],
            ["count", primative.s_int],
            ["b_data1", primative.maybe(primative.vi)],
            ["b_data2", primative.maybe(primative.vi)]]
        self.type = PlayParticlePacket

# TODO: Implement this in a sane way
class PlayMapPacket():
    def __init__(self):
        pass

class PlayMapPacketSerialier(PacketSerializer):
    def __init__(self):
        self.id = 0x24
        self.fields = []
        self.type = PlayMapPacket

class PlayEntityRelativeMovePacket():
    def __init__(self, e_id, x, y, z, on_ground):
        self.e_id = e_id
        self.x = x
        self.y = y
        self.z = z
        self.on_ground = on_ground

class PlayEntityRelativeMovePacketSerialier(PacketSerializer):
    def __init__(self):
        self.id = 0x25
        self.fields = [
            ["e_id", primative.vi],
            ["x", primative.s_short],
            ["y", primative.s_short],
            ["z", primative.s_short],
            ["on_ground", primative.m_bool]]
        self.type = PlayEntityRelativeMovePacket

class PlayEntityLookAndRelativeMovePacket():
    def __init__(self, e_id, x, y, z, yaw, pitch, on_ground):
        self.e_id = e_id
        self.x = x
        self.y = y
        self.z = z
        self.yaw = yaw
        self.pitch = pitch
        self.on_ground = on_ground

class PlayEntityLookAndRelativeMovePacketSerialier(PacketSerializer):
    def __init__(self):
        self.id = 0x26
        self.fields = [
            ["e_id", primative.vi],
            ["x", primative.s_short],
            ["y", primative.s_short],
            ["z", primative.s_short],
            ["yaw", primative.angle],
            ["pitch", primative.angle],
            ["on_ground", primative.m_bool]]
        self.type = PlayEntityLookAndRelativeMovePacket

class PlayEntityLookPacket():
    def __init__(self, e_id, yaw, pitch, on_ground):
        self.e_id = e_id
        self.yaw = yaw
        self.pitch = pitch
        self.on_ground = on_ground

class PlayEntityLookPacketSerialier(PacketSerializer):
    def __init__(self):
        self.id = 0x27
        self.fields = [
            ["e_id", primative.vi],
            ["yaw", primative.angle],
            ["pitch", primative.angle],
            ["on_ground", primative.m_bool]]
        self.type = PlayEntityLookPacket

class PlayEntityPacket():
    def __init__(self, e_id):
        self.e_id = e_id

class PlayEntityPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0x28
        self.fields = [["e_id", primative.vi]]
        self.type = PlayEntityPacket

class PlayVehicleMoveClientBoundPacket():
    def __init__(self, x, y, z, yaw, pitch):
        self.x = x
        self.y = y
        self.z = z
        self.yaw = yaw
        self.pitch = pitch

class PlayVehicleMoveClientBoundPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0x29
        self.fields = [
            ["x", primative.m_double],
            ["y", primative.m_double],
            ["z", primative.m_double],
            ["yaw", primative.m_float],
            ["pitch", primative.m_float]]
        self.type = PlayVehicleMoveClientBoundPacket

class PlayOpenSignEditorPacket():
    def __init__(self, position):
        self.position = position

class PlayOpenSignEditorPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0x2a
        self.fields = [["position", primative.position]]
        self.type = PlayOpenSignEditorPacket

class PlayPlayerAbilitiesClientBoundPacket():
    def __init__(self, flags, fly_speed, field_of_view):
        self.flags = flags
        self.fly_speed = fly_speed
        self.field_of_view = field_of_view

class PlayPlayerAbilitiesClientBoundPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0x2b
        self.fields = [
            ["flags", primative.s_byte],
            ["fly_speed", primative.m_float],
            ["field_of_view", primative.m_float]]
        self.type = PlayPlayerAbilitiesClientBoundPacket

# TODO: Implement specific events
class PlayCombatEventPacket():
    def __init__(self, event):
        self.event = event

class PlayCombatEventPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0x2c
        self.fields = [["event", primative.vi]]
        self.type = PlayCombatEventPacket

# TODO: Implement
class PlayPlayerListItemPacket():
    def __init__(self):
        pass

class PlayPlayerListItemPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0x2d
        self.fields = []
        self.type = PlayPlayerListItemPacket

class PlayPlayerPositionAndLookPacket():
    def __init__(self, x, y, z, yaw, pitch, flags, tp_id):
        self.x = x
        self.y = y
        self.z = z
        self.yaw = yaw
        self.pitch = pitch
        self.flags = flags
        self.tp_id = tp_id

class PlayPlayerPositionAndLookPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0x2e
        self.fields = [
            ["x", primative.m_double],
            ["y", primative.m_double],
            ["z", primative.m_double],
            ["yaw", primative.m_float],
            ["pitch", primative.m_float],
            ["flags", primative.u_byte],
            ["tp_id", primative.vi]]
        self.type = PlayPlayerPositionAndLookPacket

class PlayUseBedPacket():
    def __init__(self, e_id, position):
        self.e_id = e_id
        self.position = position

class PlayUseBedPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0x2f
        self.fields = [
            ["e_id", primative.vi],
            ["position", primative.position]]
        self.type = PlayUseBedPacket

class PlayDestroyEntitiesPacket():
    def __init__(self, entities):
        self.entities = entities

class PlayDestroyEntitiesPacketSerializer():
    def __init__(self):
        self.id = 0x30
        self.type = PlayDestroyEntitiesPacket

    def serialize(self, packet):
        b = bytearray()
        primative.w_vi(b, self.id)
        primative.w_vi(b, len(packet.entities))
        for e in packet.entities:
            primative.w_vi(b, e)
        return b

    def deserialize(self, b):
        c = primative.r_vi(b)
        e = []
        for i in range(c):
            e.append(primative.r_vi(b))
        return PlayDestroyEntitiesPacket(e)

class PlayRemoveEntityEffectPacket():
    def __init__(self, e_id, effect_id):
        self.e_id = e_id
        self.effect_id = effect_id
    
class PlayRemoveEntityEffectPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0x31
        self.fields = [
            ["e_id", primative.vi],
            ["effect_id", primative.u_byte]]
        self.type = PlayRemoveEntityEffectPacket

class PlayResourcePackPacket():
    def __init__(self, url, hsh):
        self.url = url
        self.hsh = hsh

class PlayResourcePackPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0x32
        self.fields = [
            ["url", primative.u8],
            ["hsh", primative.u8]]
        self.type = PlayResourcePackPacket

class PlayRespawnPacket():
    def __init__(self, dimension, difficulty, gamemode, level_type):
        self.dimension = dimension
        self.difficulty = difficulty
        self.gamemode = gamemode
        self.level_type = level_type

class PlayRespawnPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0x33
        self.fields = [
            ["dimension", primative.s_int],
            ["difficulty", primative.u_byte], 
            ["gamemode", primative.u_byte],
            ["level_type", primative.u8]]
        self.type = PlayRespawnPacket

class PlayEntityHeadLookPacket():
    def __init__(self, e_id, head_yaw):
        self.e_id = e_id
        self.head_yaw = head_yaw

class PlayEntityHeadLookPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0x34
        self.fields = [
            ["e_id", primative.vi],
            ["head_yaw", primative.angle]]
        self.type = PlayEntityHeadLookPacket

# TODO: Implement
class PlayWorldBorderPacket():
    def __init__(self):
        pass

class PlayWorldBorderPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0x35
        self.fields = []
        self.type = PlayWorldBorderPacket

class PlayCameraPacket():
    def __init__(self, e_id):
        self.e_id = e_id

class PlayCameraPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0x36
        self.fields = [["e_id", primative.vi]]
        self.type = PlayCameraPacket

class PlayHeldItemChangeClientBoundPacket():
    def __init__(self, slot):
        self.slot = slot

class PlayHeldItemChangeClientBoundPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0x37
        self.fields = [["slot", primative.s_byte]]
        self.type = PlayHeldItemChangeClientBoundPacket

class PlayDisplayScoreboardPacket():
    def __init__(self, position, name):
        self.position = position
        self.name = name

class PlayDisplayScoreboardPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0x38
        self.fields = [
            ["position", primative.s_byte],
            ["name", primative.u8]]
        self.type = PlayDisplayScoreboardPacket

class PlayEntityMetadataPacket():
    def __init__(self, e_id, meta):
        self.e_id = e_id
        self.meta = meta

class PlayEntityMetadataPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0x39
        self.fields = [
            ["e_id", primative.vi],
            ["meta", metadata.meta_type]]
        self.type = PlayEntityMetadataPacket

class PlayAttachEntityPacket():
    def __init__(self, attached_eid, holding_eid):
        self.attached_eid = attached_eid
        self.holding_eid = holding_eid

class PlayAttachEntityPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0x3a
        self.fields = [
            ["attached_eid", primative.vi],
            ["holding_eid", primative.vi]]
        self.type = PlayAttachEntityPacket

class PlayEntityVelocityPacket():
    def __init__(self, e_id, vx, vy, vz):
        self.e_id = e_id
        self.vx = vx
        self.vy = vy
        self.vz = vz

class PlayEntityVelocityPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0x3b
        self.fields = [
            ["e_id", primative.vi],
            ["vx", primative.s_short],
            ["vy", primative.s_short],
            ["vz", primative.s_short]]
        self.type =- PlayEntityVelocityPacket

class PlayEntityEquipmentPacket():
    def __init__(self, e_id, slot, item):
        self.e_id = e_id
        self.slot = slot
        self.item = item

class PlayEntityEquipmentPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0x3c
        self.fields = [
            ["e_id", primative.vi],
            ["slot", primative.vi],
            ["item", [primative.r_slot, primative.w_slot]]]
        self.type = PlayEntityEquipmentPacket

class PlaySetExperiencePacket():
    def __init__(self, exp_bar, level, t_exp):
        self.exp_bar = exp_bar
        self.level = level
        self.t_exp = t_exp

class PlaySetExperiencePacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0x3d
        self.fields = [
            ["exp_bar", primative.m_float],
            ["level", primative.vi],
            ["t_exp", primative.vi]]
        self.type = PlaySetExperiencePacket

class PlayUpdateHealthPacket():
    def __init__(self, health, food, food_sat):
        self.health = health
        self.food = food
        self.food_sat = food_sat

class PlayUpdateHealthPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0x3e
        self.fields = [
            ["health", primative.m_float],
            ["food", primative.vi],
            ["food_sat", primative.m_float]]
        self.type = PlayUpdateHealthPacket

class PlayScoreboardObjectivePacket():
    def __init__(self, obj_name, mode, obj_value=None, obj_type=None):
        self.obj_name = obj_name
        self.mode = mode
        self.obj_value = obj_value
        self.obj_type = obj_type

class PlayScoreboardObjectivePacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0x3f
        self.fields = [
            ["obj_name", primative.u8],
            ["mode", primative.s_byte],
            ["obj_value", primative.maybe(primative.u8)],
            ["obj_type", primative.maybe(primative.u8)]]
        self.type = PlayScoreboardObjectivePacket

# TODO: implement
class PlaySetPassengersPacket():
    def __init__(self):
        pass

class PlaySetPassengersPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0x40
        self.fields = []
        self.type = PlaySetPassengersPacket

class PlayTeamsPacket():
    def __init__(self):
        pass

class PlayTeamsPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0x41
        self.fields = []
        self.type = PlayTeamsPacket

class PlayUpdateScorePacket():
    def __init__(self, score_name, action, objective, value):
        self.score_name = score_name
        self.action = action
        self.objective = objective
        self.value = value

class PlayUpdateScorePacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0x42
        self.fields = [
            ["score_name", primative.u8],
            ["action", primative.s_byte],
            ["objective", primative.u8],
            ["value", primative.maybe(primative.vi)]]
        self.type = PlayUpdateScorePacket

class PlaySpawnPositionPacket():
    def __init__(self, location):
        self.location = location

class PlaySpawnPositionPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0x43
        self.fields = [
            ["location", primative.position]]
        self.type = PlaySpawnPositionPacket

class PlayTimeUpdatePacket():
    def __init__(self, world_age, time_of_day):
        self.world_age = world_age
        self.time_of_day = time_of_day

class PlayTimeUpdatePacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0x44
        self.fields = [
            ["world_age", primative.s_long],
            ["time_of_day", primative.s_long]]
        self.type = PlayTimeUpdatePacket

# TODO: Implement
class PlayTitlePacket():
    def __init__(self, action):
        self.action = action

class PlayTitlePacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0x45
        self.fields = [
            ["action", primative.vi]]
        self.type = PlayTitlePacket

class PlaySoundEffectPacket():
    def __init__(self, s_id, s_cat, x, y, z, vol, pitch):
        self.s_id = s_id
        self.s_cat = s_cat
        self.x = x
        self.y = y
        self.z = z
        self.vol = vol
        self.pitch = pitch

class PlaySoundEffectPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0x46
        self.fields = [
            ["s_id", primative.vi],
            ["s_cat", primative.vi],
            ["x", primative.s_int],
            ["y", primative.s_int],
            ["z", primative.s_int],
            ["vol", primative.m_float],
            ["pitch", primative.m_float]]
        self.type = PlaySoundEffectPacket

class PlayerListHeaderFooterPacket():
    def __init__(self, header, footer):
        self.header = header
        self.footer = footer

class PlayerListHeaderFooterPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0x47
        self.fields = [
            ["header", primative.json],
            ["footer", primative.json]]
        self.type = PlayerListHeaderFooterPacket

class PlayCollectItemPacket():
    def __init__(self, collected_eid, collector_eid, count):
        self.collected_eid = collected_eid
        self.collector_eid = collector_eid
        self.count = count

class PlayCollectItemPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0x47
        self.fields = [
            ["collected_eid", primative.vi],
            ["collector_eid", primative.vi],
            ["count", primative.vi]]
        self.type = PlayCollectItemPacket

class PlayEntityTeleportPacket():
    def __init__(self, e_id, x, y, z, yaw, pitch, on_ground):
        self.e_id = e_id
        self.x = x
        self.y = y
        self.z = z
        self.yaw = yaw
        self.pitch = pitch
        self.on_ground = on_ground

class PlayEntityTeleportPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0x49
        self.fields = [
            ["e_id", primative.vi],
            ["x", primative.m_double],
            ["y", primative.m_double],
            ["z", primative.m_double],
            ["yaw", primative.angle],
            ["pitch", primative.angle],
            ["on_ground", primative.m_bool]]
        self.type = PlayEntityTeleportPacket

# TODO: Implement

class PlayEntityPropertiesPacket():
    def __init__(self, e_id):
        self.e_id = e_id

class PlayEntityPropertiesPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0x4a
        self.fields = [
            ["e_id", primative.vi]]
        self.type = PlayEntityPropertiesPacket

class PlayEntityEffectPacket():
    def __init__(self, e_id, effect_id, amp, duration, flags):
        self.e_id = e_id
        self.effect_id = effect_id
        self.amp = amp
        self.duration = duration
        self.flags = flags

class PlayEntityEffectPacketSerializer(PacketSerializer):
    def __init__(self):
        self.id = 0x4b
        self.fields = [
            ["e_id", primative.vi],
            ["effect_id", primative.s_byte],
            ["amp", primative.s_byte],
            ["duration", primative.vi],
            ["flags", primative.s_byte]]
        self.type = PlayEntityEffectPacket


