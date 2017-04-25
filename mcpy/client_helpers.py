from mcpy import async_helpers, play
import rx

class KeepAliveObserver(async_helpers.AsyncObserver):
    def __init__(self, client):
        self.client = client

    def on_next(self, keep_alive):
        self.client.keep_alive.on_next(keep_alive.ka_id)
        send = self.client.send_packet(play.PlayKeepAliveServerBoundPacket(ka_id))
        self.async_fire(send)

    def on_completed(self):
        self.client.keep_alive.on_completed()

    def on_error(self, error):
        self.client.keep_alive.on_error(error)

def attach_keep_alive(play_client):
    ka_ob = play_client.packet_event(play.PlayKeepAliveClientBoundPacket)
    play_client.keep_alive = rx.subjects.Subject()
    ka_ob.subscribe(KeepAliveObserver(play_client))
