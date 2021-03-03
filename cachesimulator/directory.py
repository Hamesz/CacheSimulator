import logging
from cachesimulator.statistics import Statistic
logger = logging.getLogger('cachesimulator.Logger')

class Directory():

    def __init__(self):
        self._sharers = []
        return

    def append_sharer(self, sharer):
        self.sharers.append(sharer)

    def read_miss(self, cache, address):
        """A read miss has occured from a cache, meaning it wants some data
            but either its line is invalid or tags dont match. Hence we need to 
            give it the data or tell another cache to give it

        Args:
            cache (Cache): The cache issuing the read miss
            address (int): Address of the word
        """
        logger.debug('Directory read miss')
        # Need to check if any other caches contain the data by asking them,
        # we should really keep a track of all the cachelines but takes up more storage
        cache_containers = self._get_sharers(cache, address)
        # send remote read misses to them
        self._send_remote_read_miss(cache_containers, address)

        # now we need to choose the closest cache to issuing cache, if there exists a cache that
        # has a copt of the data
        if (len(cache_containers) != 0):
            cache_closest = self._get_closest_cache(cache_containers, cache)
            logger.debug('closest cache to {} is {}'.format(cache, cache_closest))
            # ask the closest cache to send the data to issuing cache 
            cache_closest.send_line(cache, address)
            
            Statistic.directory_request()
            Statistic.remote_access()
        else:
            # there is no cache that holds the data, we need to query memory and send it personally
            logger.debug('No cache has line {}, so fetching it from memory'.format(address))
            Statistic.memory_access()
            Statistic.off_chip_access()
            pass

    def write_miss(self, cache, address, need_data=False):
        """A write missed has occured from a cache which means it wants to write
            but it first needs to make sure everyone else is invalidated and it also needs
            the data to write.

        Args:
            cache (Cache): The cache issuing the read miss
            address (int): Address of the word
        
        Returns:
            int : Number of invalidations to expect 
        """
        logger.debug(f'Directory write miss, is data needed: {need_data}')

        # get caches which contain the address
        cache_containers = self._get_sharers(cache, address)
        if (len(cache_containers) > 0):
            logger.debug('Sending invalidations to sharers: {}'.format(cache_containers))
            # send ivalidations to them all (remote write miss)
            self._send_invalidations(cache, cache_containers, address)
            Statistic.directory_request()

            
            if (need_data):
                closest_cache = self._get_closest_cache(cache_containers, cache)
                closest_cache.send_line(cache, address)

            Statistic.invalidation_sent(len(cache_containers))
            Statistic.directory_request()
            Statistic.remote_access()

            return len(cache_containers)
        # No sharers
        else:
            logger.debug('No sharers so getting data from memory but should have already been done when doing read miss earlier')
            # need to get from main memory and send to cache
            if (need_data):
                Statistic.memory_access()
                Statistic.off_chip_access()
                
            else:
                # the cache does not need data just telling us to send invalidations
                Statistic.remote_access()
                pass
            # directory sends data to cache
            Statistic.directory_request()
            
            return 0

    def _send_remote_read_miss(self, caches, address):
        """Sends remote read miss to the caches so they can change their state to modified

        Args:
            caches (list(Cache)): List of caches containing the address
            address (int): Address of the word
        """
        logger.debug('Sending remote misses to caches: {}'.format(caches))
        for c in caches:
            c.remote_read_miss(address)

    def _send_invalidations(self, cache, caches, address):
        """Sends invalidations to the caches

        Args:
            cache (Cache): Cache which is needs acknowlegments
            caches (list(Cache)): Caches which need to be invalidated
            address (int): Address of the word
        """
        logger.debug('Sending invalidations to caches: {} for address {}'.format(caches, address))
        distances = []
        # getting furthest cache to send invalidation too
        for c in caches:
            distance = ((cache.id - c.id)) % (len(caches) + 1)
            logger.debug('Distance between cache {} & {}: {}'.format(cache, c, distance))
            distances.append(distance)
        
        max_distance = max(distances)
        max_index = distances.index(max_distance)
        furthest_cache = caches[max_index]
        Statistic.processor_hop(max_distance)

        for c in caches:
            c.invalidate_line(address, cache)

    def _get_sharers(self, cache, address):
        """Gets the caches which contain a valid copy of the address. Performs a directory access

        Args:
            cache (Cache): The cache issuing the read miss
            address (int): Address of the word

        Returns:
            list(Cache): list of caches which contain the address
        """
        logger.debug('Getting sharers for address {}'.format(address))
        Statistic.directory_access()
        cache_containers = []
        for c in self.sharers:
            if (cache != c):
                contains = c.contains_address(address)
                # if this cache contains the address then add it to containers
                if (contains):
                    cache_containers.append(c)
        return cache_containers

    def _get_closest_cache(self, caches, cache):
        """Determines the closest cache using a ring network

        Args:
            caches (list): list of Cache
            cache (Cache): cache to be close too
            max_caches (int): Highest number of caches

        Returns:
            Cache: The closest cache such that the network latency takes the least amount of time
        """
        logger.debug('Finding closest cache with caches: {}, to closest cache: {}'.format(caches, cache))
        distances = []
        for c in caches:
            distance = ((cache.id - c.id)) % (len(caches) + 1)
            logger.debug('Distance between cache {} & {}: {}'.format(cache, c, distance))
            distances.append(distance)
        min_distance = min(distances)
        max_distance = max(distances)

        min_index = distances.index(min_distance)
        max_index = distances.index(max_distance)

        closest_cache = caches[min_index]
        furthest_cache = caches[max_index]

        # Statistic.processor_hop(max_distance)
        return closest_cache

    @property
    def sharers(self):
        return self._sharers