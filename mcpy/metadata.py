from mcpy import primative

def r_rotation(buf):
    x = primative.r_float(buf)
    y = primative.r_float(buf)
    z = primative.r_float(buf)
    return x, y, z

def w_rotation(buf, val):
    primative.w_float(buf, val[0])
    primative.w_float(buf, val[1])
    primative.w_float(buf, val[2])

class Slot():
    def __init__(self, b_id, count, damage, meta):
        self.b_id = b_id
        self.count = count
        self.damage = damage
        self.meta = meta

def r_slot(buf):
    b_id = primative.r_s_short(buf)
    if b_id == -1:
        return None
    count = primative.r_u_byte(buf)
    damage = primative.r_u_short(buf)
    if b_id != 0:
        nbt = primative.r_nbt(buf)
    else:
        nbt = None

    return Slot(b_id, count, damage, nbt)


def w_slot(buf, val):
    if val is None:
        primative.w_s_short(buf, -1)
        return
    primative.w_s_short(buf, val.b_id)
    primative.w_u_byte(buf, val.count)
    primative.w_u_short(buf, val.damage)
    if val.b_id != 0:
        primative.w_nbt(buf, val.nbt)

m_slot = [r_slot, w_slot]

metadata_types = {
    0: primative.u_byte,
    1: primative.vi,
    2: primative.m_float,
    3: primative.u8,
    4: primative.json, # chat
    5: [r_slot, w_slot], # slot
    6: primative.m_bool,
    7: [r_rotation, w_rotation], # rotation
    8: primative.position,
    9: primative.opt(primative.position),
    10: primative.vi, # direction
    11: primative.opt(primative.uuid),
    12: primative.vi # optblockid
}

class MetaEntry():
    def __init__(self, idx, tid, d):
        self.idx = idx
        self.tid = tid
        self.d = d

    def get(meta):
        return meta.get(self.idx, self.d)
    
    def set(meta, val):
        meta.set(self.idx, self.tid, val)

    def rm(meta):
        meta.rm(self.idx)

class MetaBitEntry():
    def __init__(self, idx, mask, off, d):
        self.idx = idx
        self.mask = mask
        self.off = off
        self.d = d

    def get(meta):
        parent = meta.get(self.idx, None)
        if parent is None:
            return self.d
        return parent & mask >> off

    def set(meta, val):
        val = val & self.mask
        parent = meta.get(self.idx, None)
        if parent is None:
            parent = 0
        parent |= val << self.off
        meta.set(self.idx, 0, parent)

    def rm(meta):
        self.set(meta, self.d)
        

metadata_definitions = {
        # entity
        "on_fire": MetaBitEntry(0, 0x1, 0, 0),
        "crouched": MetaBitEntry(0, 0x2, 1, 0),
        "sprinting": MetaBitEntry(0, 0x8, 3, 0),
        "invisible": MetaBitEntry(0, 0x20, 5, 0),
        "glowing": MetaBitEntry(0, 0x40, 6, 0),
        "elytra": MetaBitEntry(0, 0x80, 7, 0),
        "air": MetaEntry(1, 1, 300),
        "custom_name": MetaEntry(2, 3, ""),
        "custom_name_visible": MetaEntry(3, 6, False),
        "silent": MetaEntry(4, 6, False),
        "no_gravity": MetaEntry(5, 6, False),
        
        # potion
        "potion_slot": MetaEntry(6, 5, None),
        
        # falling block
        "spawn_position": MetaEntry(6, 8, (0, 0, 0)),

        # area effect cloud
        "radius": MetaEntry(6, 2, 0.5),
        "effect_color": MetaEntry(7, 1, 0),
        "ignore_radius": MetaEntry(8, 6, False),
        "particle_id": MetaEntry(9, 1, 15),
        "particle_param_1": MetaEntry(10, 1, 0),
        "particle_param_2": MetaEntry(11, 1, 0),

        # fishing hook
        "hooked_entity": MetaEntry(6, 1, 0),
         
        # arrow
        "critical": MetaBitEntry(6, 0x1, 0, 0),

        # tipped_arrow
        "arrow_color": MetaEntry(7, 1, -1),
        
        # boat
        "time_since_last_hit": MetaEntry(6, 1, 0),
        "forward_direction": MetaEntry(7, 1, 1),
        "damage_taken": MetaEntry(8, 2, 0.0),
        "boat_type": MetaEntry(9, 1, 0),
        "right_paddle": MetaEntry(10, 6, False),
        "left_paddle": MetaEntry(11, 6, False),

        # ender crystal
        "beam_target": MetaEntry(6, 9, None),
        "show_bottom": MetaEntry(7, 6, True),

        # wither skull
        "invulnerable": MetaEntry(6, 6, False),

        # fireworks
        "firework_info": MetaEntry(6, 5, None),
        "firework_entity_source": MetaEntry(7, 1, 0),
        # item frame and item
        "item": MetaEntry(6, 5, None),
        "itemframe_rotation": MetaEntry(7, 1, 0),
        
        # living
        "is_hand_active": MetaBitEntry(6, 0x1, 0, 0),
        "active_hand": MetaBitEntry(6, 0x2, 1, 0),
        "health": MetaEntry(7, 2, 1.0),
        "potion_effect_color": MetaEntry(8, 1, 0),
        "potion_ambient": MetaEntry(9, 6, False),
        "arrows_in_entity": MetaEntry(10, 1, 0),

        # player
        "addtl_hearts": MetaEntry(11, 1, 0),
        "score": MetaEntry(12, 1, 0),
        "cape_enabled": MetaBitEntry(13, 0x1, 0, False),
        "jacket_enabled": MetaBitEntry(13, 0x2, 1, False),
        "leftsleeve_enabled": MetaBitEntry(13, 0x4, 2, False),
        "rightsleeve_enabled": MetaBitEntry(13, 0x8, 3, False),
        "leftpants_enabled": MetaBitEntry(13, 0x10, 4, False),
        "rightpants_enabled": MetaBitEntry(13, 0x20, 5, False),
        "hat_enabled": MetaBitEntry(13, 0x40, 6, False),
        "main_hand": MetaEntry(14, 0, 1),

        # armor stand
        "is_small": MetaBitEntry(11, 0x1, 0, False),
        "has_arms": MetaBitEntry(11, 0x4, 2, False),
        "no_base_plate": MetaBitEntry(11, 0x8, 3, False),
        "set_marker": MetaBitEntry(11, 0x10, 4, False),
        "head_rotation": MetaEntry(12, 7, (0.0, 0.0, 0.0)),
        "body_rotation": MetaEntry(13, 7, (0.0, 0.0, 0.0)),
        "left_arm_rotation": MetaEntry(14, 7, (-10.0, 0.0, -10.0)),
        "right_arm_roation": MetaEntry(15, 7, (-15.0, 0.0, 10.0)),
        "left_leg_rotation": MetaEntry(16, 7, (-1.0, 0.0, -1.0)),
        "right_leg_rotation": MetaEntry(17, 7, (1.0, 0.0, 1.0)),

        # insentient
        "no_ai": MetaBitEntry(11, 0x1, 0, False),
        "left_handed": MetaBitEntry(11, 0x2, 1, False),

        # bat
        "is_hanging": MetaBitEntry(12, 0x1, 0, False),
        
        # ageable
        "is_baby": MetaEntry(12, 6, False),

        # abstract horse
        "is_tame": MetaBitEntry(13, 0x2, 1, False),
        "is_saddled": MetaBitEntry(13, 0x4, 2, False),
        "has_chest": MetaBitEntry(13, 0x8, 3, False),
        "is_bred": MetaBitEntry(13, 0x10, 4, False),
        "is_eating": MetaBitEntry(13, 0x20, 5, False),
        "is_rearing": MetaBitEntry(13, 0x40, 6, False),
        "is_mouth_open": MetaBitEntry(13, 0x80, 7, False),
        "horse_owner": MetaEntry(14, 11, None),

        # horse
        "horse_variant": MetaEntry(15, 1, 0),
        "horse_armor": MetaEntry(16, 1, 0),

        # chested horse
        "chested_has_chest": MetaEntry(15, 6, False),

        # llama
        "llama_strength": MetaEntry(16, 1, 0),
        "llama_carpet_color": MetaEntry(17, 1, -1),
        "llama_variant": MetaEntry(18, 1, 0),

        # pig
        "has_saddle": MetaEntry(13, 6, False),
        "pig_boost": MetaEntry(14, 1, 0),

        # rabbit
        "rabbit_type": MetaEntry(13, 1, 0),

        # polar bear
        "standing_up": MetaEntry(13, 6, False),

        # sheep
        "sheep_color": MetaBitEntry(13, 0xf, 0, 0),
        "is_sheared": MetaBitEntry(13, 0x10, 4, False),

        # tameable animal
        "is_sitting": MetaBitEntry(13, 0x1, 0, False),
        "is_angry": MetaBitEntry(13, 0x2, 1, False),
        "is_tamed": MetaBitEntry(13, 0x4, 2, False),
        "tameable_owner": MetaEntry(14, 11, None),

        # ocelot
        "ocelot_variant": MetaEntry(15, 1, 0),

        # wolf
        "wolf_damage_taken": MetaEntry(15, 2, 1.0),
        "is_begging": MetaEntry(16, 6, False),
        "collar_color": MetaEntry(17, 1, 14),

        # villager
        "profession": MetaEntry(13, 1, 0),

        # iron golem
        "is_player_created": MetaBitEntry(12, 0x1, 0, False),

        # snowman
        "no_pumpkin_hat": MetaBitEntry(12, 0x10, 4, True),
        
        # shulker
        "shulker_direction": MetaEntry(12, 10, 0),
        "shulker_attachment_pos": MetaEntry(13, 9, None),
        "shulker_shield_height": MetaEntry(14, 0, 0),
        "shulker_color": MetaEntry(15, 0, 10),

        # blaze
        "on_fire": MetaBitEntry(12, 0x1, 0, False),

        # creeper
        "creeper_state": MetaEntry(12, 1, -1),
        "is_charged": MetaEntry(13, 6, False),
        "is_ignited": MetaEntry(14, 6, False),

        # guardian
        "is_retracting_spikes": MetaEntry(12, 6, False),
        "guardian_target": MetaEntry(13, 1, 0),

        # evocation illager
        "illager_spell": MetaEntry(12, 0, 0),

        # vex
        "is_in_attack_mode": MetaBitEntry(12, 0x1, 0, False),

        # skeleton
        "is_swinging_arms": MetaEntry(12, 6, False),

        # spider
        "is_climbing": MetaBitEntry(12, 0x1, 0, False),
        
        # witch
        "is_aggressive": MetaEntry(12, 6, False),
        
        # wither
        "center_head_target": MetaEntry(12, 1, 0),
        "left_head_target": MetaEntry(13, 1, 0),
        "right_head_target": MetaEntry(14, 1, 0),
        "invulnerability_time": MetaEntry(15, 1, 0),

        # zombie
        # "is_baby" -- ageable
        "zombie_type": MetaEntry(13, 1, 0),
        "zombie_hands_up": MetaEntry(14, 6, False),

        # zombie villager
        "zombie_is_converting": MetaEntry(15, 6, False),
        "zombie_profession": MetaEntry(16, 1, 0),

        # enderman
        "carried_block": MetaEntry(12, 12, -1),
        "is_screaming": MetaEntry(13, 6, False),

        # ender dragon
        "dragon_phase": MetaEntry(12, 1, 10),

        # ghast
        "is_attacking": MetaEntry(12, 6, False),
        
        # slime
        "slime_size": MetaEntry(12, 1, 1),

        # minecart
        "minecart_shaking_power": MetaEntry(6, 1, 0),
        "minecart_shaking_direction": MetaEntry(7, 1, 1),
        "minecart_shaking_multiplier": MetaEntry(8, 2, 0.0),
        "minecart_custom_id_dam": MetaEntry(9, 1, 0),
        "minecart_custom_y": MetaEntry(10, 1, 6),
        "minecart_show_custom": MetaEntry(11, 6, False),

        # minecart furnace
        "minecart_is_powered": MetaEntry(12, 6, False),

        # minecart command block
        "minecart_command": MetaEntry(12, 3, ""),
        "minecart_last_output": MetaEntry(13, 4, {"text": ""}),

        # tnt primed
        "tnt_fuse_time": MetaEntry(6, 1, 80)
}

class MetadataException(Exception):
    pass

def read_metadata(buf):
    dat = dict()
    while True:
        index = primative.r_u_byte(buf)
        if index == 0xff:
            break
        m_type = primative.r_u_byte(buf)
        serializer = metadata_types.get(m_type, None)
        if serializer is None:
            raise MetadataException("Invalid metadata type sent")
        dat[index] = (m_type, serializer[0](buf))

    return EntityMetadata(dat=dat)

def write_metadata(buf, val):
    for k, v in val.dat:
        primative.w_u_byte(buf, k)
        primative.w_u_byte(buf, v[0])
        serializer = metadata_types.get(v[0], None)
        if serializer is None:
            raise MetadataException("Invalid serializer type set")
        serializer[1](buf, v[1])

    primative.w_u_byte(buf, 0xff)

class EntityMetadata():
    def __init__(self, dat={}):
        self.dat = dat

    def set(self, index, v_type, value):
        self.dat[index] = (v_type, value)

    def get(self, index, d=None):
        return self.dat.get(index, d)

    def rm(self, index):
        del self.dat[index]

    def __getattr__(self, name):
        if name == "dat":
            return super().__getattr__(name)

        mdd = metadata_definitions[name]
        return mdd.get(self)

    def __setattr__(self, name, value):
        if name == "dat":
            super().__setattr__(name, value)
            return
        mdd = metadata_definitions[name]
        mdd.set(self, value)

    def __delattr__(self, name):
        if name == "dat":
            super().__delattr__(name)
            return
        mdd = metadata_definitions[name]
        mdd.rm(self)

meta_type = [read_metadata, write_metadata]
