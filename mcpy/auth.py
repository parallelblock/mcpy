import aiohttp
import asyncio
from Crypto.Hash import SHA
import json

class AuthError(Exception):
    pass


class AuthAPIError(AuthError):
    def __init__(self, error, message, cause):
        self.error = error
        self.message = message
        if cause is not None:
            self.cause = cause


class AuthMigratedError(AuthError):
    def __init__(self, error, message, cause):
        self.error = error
        self.message = message
        self.cause = cause


class AuthInvalidCredsError(AuthError):
    def __init__(self, error, message):
        self.error = error
        self.message = message


class AuthTooManyAttemptsError(AuthError):
    def __init__(self, error, message):
        self.error = error
        self.message = message


class AuthInvalidTokenError(AuthError):
    def __init__(self, error, message):
        self.error = error
        self.message = message


class AuthAPI(object):

    def __init__(self, proxy_generator=None):
        self.__default_agent = {"name": "Minecraft", "version": 1}
        self.__authurl = "https://authserver.mojang.com"
        self.__sessionurl = "https://sessionserver.mojang.com"
        self.__session = None

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if self.__session is not None:
            asyncio.ensure_future(self.__session.close())

    async def __force_session(self):
        if self.__session is None:
            self.__session = aiohttp.ClientSession()

    async def make_auth_request(self, endpoint, payload):
        return await self.make_api_request(self.__authurl, endpoint, payload)

    async def make_session_request(self, endpoint, payload):
        return await self.make_api_request(self.__sessionurl, endpoint, payload)

    async def make_api_request(self, base, endpoint, payload):
        await self.__force_session()
        async with self.__session.post(base + endpoint,
                headers={"Content-Type": "application/json"},
                data=json.dumps(payload)) as response:
            if response.status >= 400:
                response_json = await response.json()
                if "cause" in response_json:
                    ex = (response_json["error"], response_json["errorMessage"], response_json["cause"])
                else:
                    ex = (response_json["error"], response_json["errorMessage"])

                if response_json["error"] == "ForbiddenOperationException":
                    if "cause" in response_json:
                        if response_json["cause"] == "UserMigratedException":
                            raise AuthMigratedError(*ex)
                    elif response_json["errorMessage"] == "Invalid credentials.":
                        raise AuthTooManyAttemptsError(*ex)
                    elif response_json["errorMessage"] == "Invalide token.":
                        raise AuthInvalidTokenError(*ex)
                    else:
                        raise AuthInvalidCredsError(*ex)
                raise AuthAPIError(*ex)
            
            return response


    async def authenticate(self, username, password, 
            client_token=None, agent=None, user=True):

        if agent is None:
            agent = self.__default_agent

        request = {
            "agent": agent,
            "username": username,
            "password": password
        }

        if client_token is not None:
            request["clientToken"] = client_token

        if user is True:
            request["requestUser"] = True

        request = await self.make_auth_request("/authenticate", request)
        profile_data = await request.json()
        
        return Profile(self, username=username, **profile_data)

    async def signout(username, password):
        request = {
            "username": username,
            "password": password
        }

        await self.make_auth_request("/signout", request)

    async def has_joined(self, username, server_hash):
        await self.__force_session()
        async with self.__session.get(self.__sessionurl + 
                "/session/minecraft/hasJoined?username={}&serverId={}"
                .format(username, server_hash)) as response:
            if response.status >= 400:
                return None
            
            return await response.json()

    def gen_server_id(self, server_id, secret, public_key):
        h = SHA.new()
        h.update(server_id.encode("ASCII"))
        h.update(secret)
        h.update(public_key)
        d = int(h.hexdigest(), 16)
        if d >> 39 * 4 & 0x8:
            d = "-{:x}".format((-d) & (2 ** (40 * 4) - 1))
        else:
            d = "{:x}".format(d)
        return d

class Profile(object):
    def __init__(self, api, **kwargs):
        self.online = True
        self.__api = api
        for kw in kwargs:
            setattr(self, kw, kwargs[kw])

    def __create_token_payload(self):
        return {
            "accessToken": self.accessToken,
            "clientToken": self.clientToken
        }


    async def refresh(self, user=False):
        refresh_payload = self.__create_token_payload()
        if user is True:
            refresh_payload["requestUser"] = True

        response = await self.__api.make_auth_request("/refresh", refresh_payload)
        response_data = await response.json()

        for kw in response_data:
            setattr(self, kw, response_data[kw])

    async def validate(self):
        validate_payload = self.__create_token_payload()

        await self.__api.make_auth_request("/validate", validate_payload)

    async def join(self, server_hash):
        join_payload = {
            "accessToken": self.accessToken,
            "selectedProfile": self.selectedProfile['id'],
            "serverId": server_hash
        }
        await self.__api.make_session_request("/session/minecraft/join", join_payload)

class OfflineProfile(object):
    def __init__(self, username):
        self.username = username
