from cachesimulator.directory import Directory
from cachesimulator.cache import Cache

def create_directory():
        directory = Directory()
        return directory

def create_caches(directory, num):
    caches = []
    for i in range(num):
        cache = Cache(i, directory=directory)
        caches.append(cache)
    return caches