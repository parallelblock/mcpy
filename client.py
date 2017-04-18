import auth
import connector
import dns
import login
import state
import status
import time
import traceback

from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

_authapi = auth.AuthAPI()
_resolver = dns.MCDNSResolver()

_handshake_client_state = state.HandshakeState()
_status_client_state = state.StatusState()
_login_client_state = state.LoginState()

def _current_milli_time():
    return int(round(time.time() * 1000))

async def online_login(username, password):
    return await _authapi.authenticate(username, password)

def offline_login(username):
    return auth.OfflineProfile(username)

class ClientException(Exception):
    pass

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
        raise ClientException("failed to connect")

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
            raise ValueError("state is none")

        self.state_man.state = state

    async def send_packet(self, packet):
        await self.state_man.write_packet(packet)

    async def read_packet(self):
        return await self.state_man.read_packet()

    def close_connection(self):
        self.socket.close()

class StatusClient(Client):
    def __init__(self, socket, state_man):
        super().__init__(socket, state_man)

    async def request(self):
        await self.send_packet(status.StatusRequestPacket())
        ret = await self.read_packet()
        if type(ret) is not status.StatusResponsePacket:
            raise ClientException("server responded with incorrect packet type")
        return ret

    async def ping(self, payload=_current_milli_time()):
        await self.send_packet(status.StatusPingPacket(payload))
        ret = await self.read_packet()
        if type(ret) is not status.StatusPongPacket:
            raise ClientException("server responded with incorrect packet type")

        if ret.payload != payload:
            raise ClientException("server responded with different payload")

        return ret

class LoginClient(Client):
    def __init__(self, socket, state_man):
        super().__init__(socket, state_man)

    async def login(self, profile):
        name = profile.selectedProfile["name"] if hasattr(profile, "selectedProfile") else profile.username
        await self.send_packet(
                login.LoginStartPacket(name))
        
        while True:
            response = await self.read_packet()
            if type(response) is login.LoginEncryptionRequestPacket:
                if getattr(profile, "join", None) is None:
                    raise ClientException("server in online mode but offline profile passed!")
                rng = Random.new()
                shared_secret = rng.read(16)
                hsh = _authapi.gen_server_id(response.server_id,
                    shared_secret, response.public_key)
                await profile.join(hsh)
                rsa = RSA.importKey(response.public_key)
                cipher = PKCS1_v1_5.new(rsa)
                shared_secret_enc = cipher.encrypt(shared_secret)
                verify_token = cipher.encrypt(response.verify_token)
                await self.send_packet(
                        login.LoginEncryptionResponsePacket(shared_secret_enc, verify_token))
                self.start_encryption(shared_secret)
                print("started encryption")
            elif type(response) is login.LoginSetCompressionPacket:
                self.start_compression(response.threshold)
            elif type(response) is login.LoginSuccessPacket:
                return True # todo: new client
            elif type(response) is login.LoginDisconnectPacket:
                raise ClientException("login disconnected: reason: {}".format(response.reason))
            else:
                raise ClientException("login: server responoded with unexpected packet: {}".format(response))

async def ping_server(address, proto_version=316, ip_port=None):
    socket = await setup_server_connection(address, ip_port)
    
    state_adapter = state.StateAdapter(socket.read_packet, socket.send_packet,
            _handshake_client_state)

    c = StatusClient(socket, state_adapter)
    domain, _ = _resolver.split_domain_port(address)
    await c.send_packet(status.HandshakePacket(proto_version, 
        domain, c.socket.port, 1))

    c.set_state(_status_client_state)
    return c

async def join_server(address, proto_version=316, ip_port=None):
    socket = await setup_server_connection(address, ip_port)

    state_adapter = state.StateAdapter(socket.read_packet, socket.send_packet,
            _handshake_client_state)
    c = LoginClient(socket, state_adapter)
    domain, _ = _resolver.split_domain_port(address)
    await c.send_packet(status.HandshakePacket(proto_version,
        domain, c.socket.port, 2))
    
    c.set_state(_login_client_state)
    return c

