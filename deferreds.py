"""
Exemplo de como callbcks e errbacks são executadas.
"""

from twisted.internet import reactor, defer


def _triggerDeferred(d, x):
    """
    Chama métodos 'callback' e 'errback' diretamente, para simular o Deferred
    sendo disparado pelo reactor

    :param Deferred d: Deferred a ser 'disparado'
    :param int x: valor usado para calcular o resultado do Deferred
    """
    if x % 2 == 0:
        d.callback(x * 3)
    else:
        d.errback(ValueError("You used an odd number!"))


def getDeferred(x):
    """
    Retorna um Deferred que vai falhar ou retornar um resultado, dependendo do
    valor de 'x'

    :param int x: valor usado para calcular o resultado do Deferred
    :return: Deferred
    """
    d = defer.Deferred()
    # Fingir que demorou pra rodar:
    reactor.callLater(2, _triggerDeferred, d, x)
    d.addCallback(firstCallback)
    return d


def firstCallback(result):
    print("First callback!")
    return f"Result: {result}"


def cbPrintData(result):
    print("Yay!")
    print(result)


def ebPrintError(failure):
    print("Oh, no!")
    print(repr(failure))


def main():
    # Vai imprimir a mensagem de erro que passamos pra ValueError:
    d = getDeferred(3)
    d.addCallback(cbPrintData)
    d.addErrback(ebPrintError)

    # Vai imprimir "Result: 12":
    d = getDeferred(4)
    d.addCallback(cbPrintData)
    d.addErrback(ebPrintError)

    # Para o reactor após 4 segundos:
    reactor.callLater(4, reactor.stop)
    reactor.run()


if __name__ == "__main__":
    main()
