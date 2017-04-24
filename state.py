import login
import play
from primative import r_vi
import status

class StateException(Exception):
    pass

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
        try:
            return p.deserialize(buf)
        except:
            raise StateException(
                    "failed to deserialize! id: {} data: {} deserializer: {}"
                    .format(p_id, buf, p))
       
    def encode(self, packet):
        t = type(packet)
        p = self.outbound.get(t)

        if p is None:
            raise StateException("state: no encoder for type {}".format(t))

        try:
            return p.serialize(packet)
        except:
            raise StateException("failed to serialize! packet: {} serializer: {}".format(packet, p))

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
        cb = [
            play.PlaySpawnObjectPacketSerializer,
            play.PlaySpawnExpOrbPacketSerializer,
            play.PlaySpawnGlobalEntityPacketSerializer,
            play.PlaySpawnMobPacketSerializer,
            play.PlaySpawnPaintingPacketSerializer,
            play.PlaySpawnPlayerPacketSerializer,
            play.PlayerAnimationPacketSerializer,
            play.PlayStatisticsPacketSerializer,
            play.PlayBlockBreakAnimationPacketSerializer,
            play.PlayUpdateBlockEntityPacketSerializer,
            play.PlayBlockActionPacketSerializer,
            play.PlayBlockChangePacketSerializer,
            play.PlayBossBarPacketSerializer,
            play.PlayDifficultyPacketSerializer,
            play.PlayTabCompleteResponsePacketSerializer,
            play.PlayChatPacketSerializer,
            play.PlayMultiBlockChangePacketSerializer,
            play.PlayConfirmInvTransactionPacketSerializer,
            play.PlayCloseWindowPacketSerializer,
            play.PlayOpenWindowPacketSerializer,
            play.PlayWindowItemsPacketSerializer,
            play.PlayWindowPropertyPacketSerializer,
            play.PlaySetSlotPacketSerializer,
            play.PlaySetCooldownPacketSerializer,
            play.PlayPluginMessageClientBoundPacketSerializer,
            play.PlayNamedSoundEffectPacketSerializer,
            play.PlayKickPacketSerializer,
            play.PlayEntityStatusPacketSerializer,
            play.PlayExplosionPacketSerializer,
            play.PlayUnloadChunkPacketSerializer,
            play.PlayChangeGameStatePacketSerializer,
            play.PlayKeepAliveClientBoundPacketSerializer,
            play.PlayChunkDataPacketSerializer,
            play.PlayEffectPacketSerializer,
            play.PlayParticlePacketSerializer,
            play.PlayMapPacketSerializer,
            play.PlayEntityRelativeMovePacketSerializer,
            play.PlayEntityLookAndRelativeMovePacketSerializer,
            play.PlayEntityLookPacketSerializer,
            play.PlayEntityPacketSerializer,
            play.PlayVehicleMoveClientBoundPacketSerializer,
            play.PlayOpenSignEditorPacketSerializer,
            play.PlayPlayerAbilitiesClientBoundPacketSerializer,
            play.PlayCombatEventPacketSerializer,
            play.PlayPlayerListItemPacketSerializer,
            play.PlayPlayerPositionAndLookPacketSerializer,
            play.PlayUseBedPacketSerializer,
            play.PlayDestroyEntitiesPacketSerializer,
            play.PlayRemoveEntityEffectPacketSerializer,
            play.PlayResourcePackPacketSerializer,
            play.PlayrespawnPacketSerializer,
            play.PlayEntityHeadLookPacketSerializer,
            play.PlayWorldBorderPacketSerializer,
            play.PlayCameraPacketSerializer,
            play.PlayHeldItemChangeClientBoundPacketSerializer,
            play.PlayDisplayScoreboardPacketSerializer,
            play.PlayEntityMetadataPacketSerializer,
            play.PlayAttachEntityPacketSerializer,
            play.PlayEntityVelocityPacketSerializer,
            play.PlayEntityEquipmentPacketSerializer,
            play.PlaySetExperiencePacketSerializer,
            play.PlayUpdateHealthPacketSerializer,
            play.PlayScoreboardObjectivePacketSerializer,
            play.PlaySetPassengersPacketSerializer,
            play.PlayTeamsPacketSerializer,
            play.PlayUpdateScorePacketSerializer,
            play.PlaySpawnPositionPacketSerializer,
            play.PlayTimeUpdatePacketSerializer,
            play.PlayTitlePacketserializer,
            play.PlaySoundEffectPacketSerializer,
            play.PlayPlayerListHeaderFooterPacketSerializer,
            play.PlayCollectItemPacketSerializer,
            play.PlayEntityTeleportPacketSerializer,
            play.PlayEntityPropertiesPacketSerializer,
            play.PlayEntityEffectPacketSerializer
        ]

        sb = [
            play.PlayTeleportConfirmPacketSerializer,
            play.PlayTabCompleteRequestPacketSerializer,
            play.PlayChatMessageServerBoundPacketSerializer,
            play.PlayClientStatusPacketSerializer,
            play.PlayClientSettingsPacketSerializer,
            play.PlayConfirmInvTransactionServerBoundPacketSerializer,
            play.PlayEnchantItemPacketSerializer,
            play.PlayClickWindowPacketSerializer,
            play.PlayCloseWindowServerBoundPacketSerializer,
            play.PlayPluginMessageServerBoundPacketSerializer,
            play.PlayUseEntityPacketSerializer,
            play.PlayKeepAliveServerBoundPacketSerializer,
            play.PlayPlayerPositionPacketSerializer,
            play.PlayPlayerLookPacketSerializer,
            play.PlayPlayerPacketSerializer
            play.PlayVehicleMoveServerBoundPacketSerializer,
            play.PlaySteerBoatPacketSerializer,
            play.PlayPlayerAbilitiesServerBoundPacketSerializer,
            play.PlayDiggingPacketSerializer,
            play.PlayEntityActionPacketSerializer,
            play.PlaySteerVehiclePacketSerializer,
            play.PlayResourcePackStatusPacketSerializer,
            play.PlayHeldItemChangeServerBoundPacketSerializer,
            play.PlayCreativeInvActionPacketSerializer,
            play.PlayUpdateSignPacketSerializer,
            play.PlayAnimationServerBoundPacketSerializer,
            play.PlaySpectatePacketSerializer,
            play.PlayblockPlacementPacketSerializer,
            play.PlayUseItemPacketSerializer
        ]

        for c in cb:
            self.register(c(), False)

        for s in sb:
            self.register(s(), True)

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

