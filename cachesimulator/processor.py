import * from MSI

class Processor():

    def __init__(self, cache):
        self._cache = cache
        # self._state = INVALID
        return 

    def read(address):
        """Read the value at the given address

        Args:
            address (int): memory address
        """

        cache_hit = self.cache.is_hit(address)
        
        return

    def write(address):
        """Store a value at a given address

        Args:
            address (int): memory address
        """
        return