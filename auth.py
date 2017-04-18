import aiohttp
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
        self.__baseurl = "https://authserver.mojang.com"
        self.__session = None

    async def __force_session(self):
        if self.__session is None:
            self.__session = aiohttp.ClientSession()

    async def make_api_request(self, endpoint, payload):
        await self.__force_session()
        async with self.__session.post(self.__baseurl + endpoint,
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

        request = await self.make_api_request("/authenticate", request)
        profile_data = await request.json()
        
        return Profile(self, username=username, **profile_data)

    async def signout(username, password):
        request = {
            "username": username,
            "password": password
        }

        await self.make_api_request("/signout", request)

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

        response = await self.__api.make_api_request("/refresh", refresh_payload)
        response_data = await response.json()

        for kw in response_data:
            setattr(self, kw, response_data[kw])

    async def validate(self):
        validate_payload = self.__create_token_payload()

        await self.__api.make_api_request("/validate", validate_payload)

class OfflineProfile(object):
    def __init__(self, username):
        self.username = username
