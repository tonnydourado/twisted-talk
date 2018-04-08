import asyncio
from datetime import datetime

from twisted.internet.task import react, LoopingCall
from twisted.internet.defer import ensureDeferred, Deferred
from twisted.internet import asyncioreactor

# É preciso passar o event loop global do asyncio para o reactor, ou ele cria
# um novo event loop, e as corotinas acabam nunca rodando. Isso vai ser arrumado
# em próximas versões do Twisted:
asyncioreactor.install(asyncio.get_event_loop())


def sleep(secs):
    """
    Wrapper para usar asyncio.sleep com Twisted

    :param int secs: por quantos segundos 'dormir'
    :return: um Deferred que vai disparar em 'secs' segundos
    """
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
    # Imprime o timestamp atual a cada meio segundo, para demonstrar que o
    # reactor executa as tarefas concorrentemente:
    counter = LoopingCall(lambda: print(datetime.now()))
    counter.start(0.5)

    # Cria um Deferred a partir de uma corotina:
    deferred = ensureDeferred(start_request())
    # Também dá pra usar corotinas como callbacks, com alguma adaptação:
    deferred.addCallback(lambda r: ensureDeferred(after_request()))
    deferred.addErrback(print)
    return deferred


if __name__ == "__main__":
    # react é uma função que lida com o reactor. Você passa uma função que
    # retorna um Deferred, e react vai rodar o reactor, esperar o seu Deferred
    # disparar, e parar o reactor no final. É similar ao run_until_complete do
    # asyncio:
    react(main)
