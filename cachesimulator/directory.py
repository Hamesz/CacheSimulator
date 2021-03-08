import logging
from cachesimulator.config import NUMBER_OF_CACHES
from cachesimulator.statistics import Statistic
from cachesimulator.optimizer import Optimizer
logger = logging.getLogger('cachesimulator.Logger')

class Directory():

    def __init__(self):
        self._sharers = []
        return

    def append_sharer(self, sharer):
        self.sharers.append(sharer)

    def read_miss(self, cache, address, stored_address):
        """A read miss has occured from a cache, meaning it wants some data
            but either its line is invalid or tags dont match. Hence we need to 
            give it the data or tell another cache to give it

        Args:
            cache (Cache): The cache issuing the read miss
            address (int): Address of the word

        Returns:
            int: number of sharers
        """
        logger.debug('Directory read miss')

        # lets do optimization where we check for sharers of the old addrress
        self._optimize_check(stored_address, cache)

        # Need to check if any other caches contain the data by asking them,
        # we should really keep a track of all the cachelines but takes up more storage
        cache_containers = self._get_sharers(cache, address)
        # send remote read misses to them
        self._send_remote_read_miss(cache_containers, address)

        # now we need to choose the closest cache to issuing cache, if there exists a cache that
        # has a copt of the data
        if (len(cache_containers) != 0):
            cache_closest = self._get_closest_cache(cache_containers, cache)
            logger.info('closest cache to {} is {}'.format(cache, cache_closest))
            # ask the closest cache to send the data to issuing cache 
            cache_closest.send_line(cache, address)
            Statistic.directory_request()   # ask to send line
            Statistic.cache_probe()
            Statistic.cache_access() # for cache accessing data to send

            furthest_distance = self._get_furthest_distance(cache_containers, cache)
            Statistic.processor_hop(furthest_distance)
            Statistic.remote_access()
        else:
            # there is no cache that holds the data, we need to query memory and send it personally
            logger.info('No cache has line {}, so fetching it from memory'.format(address))
            Statistic.memory_access()

            logger.debug("Sending line to cache: {}".format(cache))
            
            Statistic.directory_request()

            Statistic.off_chip_access()

        return len(cache_containers)

    def write_miss(self, cache, address, need_data, stored_address):
        """A write missed has occured from a cache which means it wants to write
            but it first needs to make sure everyone else is invalidated and it also needs
            the data to write.

        Args:
            cache (Cache): The cache issuing the read miss
            address (int): Address of the word
            need_data (bool): Does the 
            stored_address (int): The address that is stored in the cache currently but is about to be overwritten
                it is none if the tags match.
        
        Returns:
            int : Number of invalidations to expect 
        """
        logger.debug(f'Directory write miss, is data needed: {need_data}')

        if (need_data):
            Statistic.write_miss_data_needed()

        # lets do optimization where we check for sharers of the old addrress
        self._optimize_check(stored_address, cache)

        # get caches which contain the address
        cache_containers = self._get_sharers(cache, address)
        if (len(cache_containers) > 0):
            logger.info('Sending invalidations to sharers: {}'.format(cache_containers))
            # send ivalidations to them all (remote write miss)
            Statistic.directory_request()
            self._send_invalidations(cache, cache_containers, address)
            

            if (need_data):
                closest_cache = self._get_closest_cache(cache_containers, cache)
                closest_cache.send_line(cache, address)
                # if the cache_containers > 1, then the data access overlaps
                # with the acknowledged invalidation from processor hops 
                if (len(cache_containers) > 1):
                    pass
                else:
                    Statistic.cache_access()

            # this is for invalidations
            Statistic.cache_probe()

            furthest_distance = self._get_furthest_distance(cache_containers, cache)
            Statistic.processor_hop(furthest_distance)

            Statistic.invalidation_sent(len(cache_containers))
            Statistic.remote_access()

            return len(cache_containers)
        # No sharers
        else:
            logger.info('No sharers')
            # need to get from main memory and send to cache
            if (need_data):
                Statistic.memory_access()
                Statistic.off_chip_access()
                
            else:
                # the cache does not need data just telling us to send invalidations
                logger.info("Getting data from memory")
                Statistic.write_miss_no_sharers()
                Statistic.remote_access()
                pass
            # directory sends data to cache
            Statistic.directory_request()
            
            return 0

    def _send_remote_read_miss(self, caches, address):
        """Sends remote read miss to the caches so they can change their state to Invalid

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
        logger.info('Sending invalidations to caches: {} for address {}'.format(caches, address))
        for c in caches:
            c.invalidate_line(address, cache)

    def _get_sharers(self, cache, address, no_latency=False):
        """Gets the caches which contain a valid copy of the address. Performs a directory access

        Args:
            cache (Cache): The cache issuing the read miss
            address (int): Address of the word

        Returns:
            list(Cache): list of caches which contain the address
        """
        logger.debug('Getting sharers for address {}'.format(address))
        cache_containers = []
        for c in self.sharers:
            if (cache != c):
                contains = c.contains_address(address)
                # if this cache contains the address then add it to containers
                if (contains):
                    cache_containers.append(c)
        if (no_latency == False):
            Statistic.directory_access()
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
        logger.info('Finding closest cache with caches: {}, to closest cache: {}'.format(caches, cache))
        distances = []
        for c in caches:
            if (Optimizer.OPTIMIZE):
                logger.debug(f"using optimised: {Optimizer.OPTIMIZE}")
                distance = ((c.id - cache.id)) % (NUMBER_OF_CACHES)
                logger.debug('Distance between cache {} & {}: {}'.format(cache, c, distance))
                distances.append(distance)
            else:
                distance = ((cache.id - c.id)) % (NUMBER_OF_CACHES)
                logger.debug('Distance between cache {} & {}: {}'.format(cache, c, distance))
                distances.append(distance)
        
        min_distance = min(distances)
        min_index = distances.index(min_distance)
        closest_cache = caches[min_index]

        return closest_cache

    def _get_furthest_distance(self, caches, cache):
        """Gets the distance to the furthest cache using a ring network

        Args:
            caches (list(Cache)): List of caches 
            cache (Cache): cache to compare distance to

        Returns:
            int: furthest distance to cache
        """
        distances = []
        # getting furthest cache to send invalidation too
        for c in caches:
            if (Optimizer.OPTIMIZE):
                logger.debug(f"using optimised: {Optimizer.OPTIMIZE}")
                distance = ((c.id - cache.id)) % (NUMBER_OF_CACHES)
                logger.debug('Distance between cache {} & {}: {}'.format(cache, c, distance))
                distances.append(distance)
            else:
                distance = ((cache.id - c.id)) % (NUMBER_OF_CACHES)
                logger.debug('Distance between cache {} & {}: {}'.format(cache, c, distance))
                distances.append(distance)
        
        max_distance = max(distances)
        max_index = distances.index(max_distance)
        furthest_cache = caches[max_index]
        return max_distance

    def _optimize_check(self, stored_address, cache):
        """Checks if we have to process the optimization

        Args:
            stored_address (int): Address that is being kicked out of the cache
            cache (Cache): cache who had a tag miss
        """
        if ( (stored_address != None) and Optimizer.OPTIMIZE):    # check it does not equal None
            logger.info(f"Cache {cache} has invalidated address: {stored_address}, checking for sharers")
            cache_containers_for_stored_address = self._get_sharers(cache, stored_address, no_latency=True)
            if (len(cache_containers_for_stored_address) == 1):
                last_sharer = cache_containers_for_stored_address[0] 
                logger.info(f"Alerting cache {last_sharer} that it is last sharer for address {stored_address}")
                last_sharer.alert_last_sharer(stored_address, cache)
        else:
            logger.debug(f"Stored address not set")

    @property
    def sharers(self):
        return self._sharers