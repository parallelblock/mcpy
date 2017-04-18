import auth
import connector
import dns
import state
import status
import time
import traceback

_authapi = auth.AuthAPI()
_resolver = dns.MCDNSResolver()

_handshake_client_state = state.HandshakeState()
_status_client_state = state.StatusState()

def _current_milli_time():
    return int(round(time.time() * 1000))

async def login(username, password):
    return await _authapi.authenticate(username, password)

def offline_login(username):
    return auth.OfflineProfile(username)

async def setup_server_connection(address, ip_port=None):
    if ip_port is None:
        addrs = _resolver.resolve(address)
    else:
        async def yield_override():
            yield ip_port
        addrs = yield_override()

    client = None
    async for addr in addrs:
        try:
            client = await connector.client_connect(host=addr[0], port=addr[1])
            return client
        except:
            pass
    
    if client is None:
        raise "failed to connect"

    return client

class Client(object):
    def __init__(self, socket, state_man):
        self.socket = socket
        self.state_man = state_man

    async def send_raw_data(self, data):
        await self.socket.send_packet(data)

    async def read_raw_data(self):
        return await self.socket.read_packet()

    def start_encryption(self, key):
        self.socket.start_encryption(key)

    def start_compression(self, compression):
        self.socket.start_compression(compression)

    def set_state(self, state):
        if state is None:
            raise "state is none"

        self.state_man.state = state

    async def send_packet(self, packet):
        await self.state_man.write_packet(packet)

    async def read_packet(self):
        return await self.state_man.read_packet()

    def close_connection(self):
        self.socket.close()

class StatusClient(Client):
    def __init__(self, proto_version, socket, state_man):
        super().__init__(socket, state_man)

    async def request(self):
        await self.send_packet(status.StatusRequestPacket())
        ret = await self.read_packet()
        if type(ret) is not status.StatusResponsePacket:
            raise "server responded with incorrect packet type"
        return ret

    async def ping(self, payload=_current_milli_time()):
        await self.send_packet(status.StatusPingPacket(payload))
        ret = await self.read_packet()
        if type(ret) is not status.StatusPongPacket:
            raise "server responded with incorrect packet type"

        if ret.payload != payload:
            raise "server responded with different payload"

        return ret

async def ping_server(address, proto_version=316, ip_port=None):
    socket = await setup_server_connection(address, ip_port)
    
    state_adapter = state.StateAdapter(socket.read_packet, socket.send_packet,
            _handshake_client_state)

    c = StatusClient(proto_version, socket, state_adapter)
    domain, _ = _resolver.split_domain_port(address)
    print(c.socket.port)
    await c.send_packet(status.HandshakePacket(proto_version, 
        domain, c.socket.port, 1))

    c.set_state(_status_client_state)
    return c

async def join_server(address,  profile, ip_port=None):
    pass
    
