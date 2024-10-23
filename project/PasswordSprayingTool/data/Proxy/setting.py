ROTATING_PROXY_LIST_PATH = '/my/path/proxies.txt' # Path that this library uses to store list of proxies
NUMBER_OF_PROXIES_TO_FETCH = 5 # Controls how many proxies to use


DOWNLOADER_MIDDLEWARES = {
    'rotating_free_proxies.middlewares.RotatingProxyMiddleware': 610,
    'rotating_free_proxies.middlewares.BanDetectionMiddleware': 620,
}