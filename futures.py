import asyncio
from datetime import datetime

from twisted.internet.task import react, LoopingCall
from twisted.internet.defer import ensureDeferred, Deferred
from twisted.internet import asyncioreactor

asyncioreactor.install(asyncio.get_event_loop())


def sleep(secs):
    coroutine = asyncio.sleep(secs)
    future = asyncio.ensure_future(coroutine)
    return Deferred.fromFuture(future)


async def start_request():
    urls = [
        'https://example.com/page/1',
        'https://example.com/page/2',
        'https://example.com/page/3'
    ]

    for url in urls:
        print(f"Downloading page '{url}'", end="...\n")
        await sleep(1)
        print(f"Page '{url}' download finished")


async def after_request():
    await sleep(2)
    print("Downloaded all pages!")


def main(reactor):
    counter = LoopingCall(lambda: print(datetime.now()))
    counter.start(0.5)

    deferred = ensureDeferred(start_request())
    deferred.addCallback(lambda r: ensureDeferred(after_request()))
    deferred.addErrback(print)
    return deferred


if __name__ == "__main__":
    react(main)
