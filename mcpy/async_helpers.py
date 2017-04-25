import asyncio
import rx

class AsyncObserver(rx.Observer):
    def async_fire(self, coroutine):
        async def fire():
            try:
                await coroutine
            except Exception as e:
                self.on_error(e)
        asyncio.get_event_loop().ensure_future(fire())
