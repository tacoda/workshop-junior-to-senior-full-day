"""checkout — a small ports-and-adapters cash-register service.

Layout (the hexagon):
    money.py, model.py   the domain values/entities (pure, no I/O)
    ports.py             the interfaces the domain depends on
    service.py           the checkout use case — depends ONLY on ports
    adapters/            the concrete implementations of the ports

Rule of the hexagon: the domain never imports an adapter. Concretes are wired
together only in the composition root (../main.py).
"""
