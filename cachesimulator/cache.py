from cachesimulator.cacheline import Line
from cachesimulator.config import CACHE_SIZE, LINE_SIZE
from cachesimulator import MSI
from cachesimulator.statistics import Statistic
import numpy as np
from cachesimulator.optimizer import Optimizer

import cachesimulator.Logger
import logging

logger = logging.getLogger('cachesimulator.Logger')

class Cache():

    def __init__(self, id, directory=None):
        self.id = id
        self._CACHE_SIZE = CACHE_SIZE
        self._OFFSET_BITS = int(np.log2(LINE_SIZE))
        self._INDEX_BITS = int(np.log2(CACHE_SIZE))
        self._TAG_BITS = 32 - self._INDEX_BITS - self._OFFSET_BITS
        self._initialise_lines()
        self.directory = directory
    
    def __repr__(self):
        return f'{self.id}'

    def _initialise_lines(self):
        self._cachelines = np.zeros(self._CACHE_SIZE, dtype=object)
        for idx, line in enumerate(self._cachelines):
            new_line = Line()
            self._cachelines[idx] = new_line
        
    # -- Writes -- #
    def write(self, address):
        """Perfroms a write operation to the cache

        Args:
            address (int): Address of the word

        Returns:
            hit (bool): True if there is a write hit, else false
        """
        logger.info('cache {} writing to address: {}'.format(self, address))
        tag, index, offset = get_address_parameters(address, self._INDEX_BITS, self._OFFSET_BITS)        
        line = self.cachelines[index]

        Statistic.cache_probe() # checking tag and state
        if (tag == line.tag and line.valid==True):
            # need to check the state
            if (line.state == MSI.SHARED):
                logger.debug('Line is in SHARED state')
                # we need to tell directory to send invalidates for this address
                self._write_miss(line, tag, address, False)
                return False
            elif(line.state == MSI.INVALID):
                logger.debug('Line is in INVALID state')
                Statistic.coherence_miss()
                self._write_miss(line, tag, address, True)
                return False
            elif(line.state == MSI.MODIFIED):
                logger.debug('Line is in MODIFIED state')
                self._write_hit(line, tag, address)
                return True
            elif(Optimizer.OPTIMIZE and line.state==MSI.EXCLUSIVE):
                logger.debug('Line is in Exlusive state, so skipping directory and writing to modified')
                self._write_hit(line, tag, address)
                return True
        else:
            # block not in cache so get block from directory,
            if (line.valid == False):
                Statistic.compulsory_miss()

            # Now we can skip this section and cheat a bit but we will do it anyway
            logger.debug('Line tag: {} vs addres tag: {}'.format(line.tag, tag))
            logger.debug('Line validity: {}'.format(line.valid))
            if (line.state == MSI.MODIFIED):
                logger.info(f"Line w/ address {address} is in state Modified but tags don't match so creating replacement writeback")
                Statistic.replacement_writeback()
            
            if (line.valid):
                stored_address = get_stored_address(line.tag, index, self._INDEX_BITS, self._OFFSET_BITS)
            else:
                stored_address = None
            self._write_miss(line, tag, address, True, stored_address=stored_address)
            return False

    def _write_miss(self, line, tag, address, need_data, stored_address=None):
        """This is when a write happens but the state of the line is Invalid

        Args:
            line (Line): The cacheline
            tag  (int): The value of the tag
            address (int): Address of the new word 
            need_data (bool): Flag that determines whether the cache needs the data
            stored_address (int): The address that is stored in the cache currently but is about to be overwritten
                it is none if the tags match.
        """
        logger.info('Write miss for cache: {} and need data: {} and stored address: {}'.format(self, need_data, stored_address))
        self.pending_address = address
        # note that the num_invalidates to expect will appear after we have recieved all
        # the acknowledged invalidations
        Statistic.directory_request()
        num_invalidates = self.directory.write_miss(self, address, need_data, stored_address)
        logger.debug(f"Cache {self} expecting {num_invalidates} invalidations")
        Statistic.cache_probe()
        line.write(tag)
        logger.debug(f"Cache {self} probed and accessed to address: {address}")

    def _write_hit(self, line, tag, address):
        """This is when a write happens and the state of the line is Modified

        Args:
            line (Line): The cacheline
            tag  (int): The value of the tag
            address (int): Address of the word 
        """
        logger.info('Read hit for cache: {}'.format(self))
        line.write(tag)
        Statistic.private_access()

    # -- Reads -- #
    def read(self, address):
        """Perfroms a read operation to the cache, if there is no hit then 
            it asks the directory for the information

        Args:
            address (int): Address of the word

        Returns:
            hit (bool): True if there is a cache hit, else false
        """
        logger.info('cache {} reading address: {}'.format(self, address))
        tag, index, offset = get_address_parameters(address, self._INDEX_BITS, self._OFFSET_BITS)
        line = self.cachelines[index]

        Statistic.cache_probe()
        if (tag == line.tag and line.valid==True):
            if (line.state == MSI.INVALID):
                Statistic.coherence_miss()
                self._read_miss(line, tag, address)
                return False
            else:
                self._read_hit(line, tag, address)
                return True
        else:
            logger.debug(f"Tag mismatch, tag in cache: {line.tag} vs tag for given addres:{tag}")
            # it is either compulsory or conflict
            if (line.valid == False):
                Statistic.compulsory_miss()
            else:
                Statistic.conflic_miss()
                
            # block not in cache so get block from directory
            if (line.state == MSI.MODIFIED):
                logger.info(f"Line w/ address {address} is in state Modified but tags don't match so creating replacement writeback")
                # check if it was modified state
                Statistic.replacement_writeback()
            
            # for optimization
            if line.valid:
                stored_address = get_stored_address(line.tag, index, self._INDEX_BITS, self._OFFSET_BITS)
            else:
                stored_address = None
            self._read_miss(line, tag, address, stored_address=stored_address)
            return False

    def _read_miss(self, line, tag, address, stored_address=None):
        """This is when a read happens when there is a read miss eithee because the
            state is invalid or tag miss

        Args:
            line (Line): The cacheline
            tag  (int): The value of the tag
            address (int): Address of the word 
        """
        logger.info('Read miss for cache: {}, with stored address: {}'.format(self,stored_address))
        Statistic.directory_request()
        num_sharers = self.directory.read_miss(self, address, stored_address)
        # set cache state
        if (Optimizer.OPTIMIZE and num_sharers==0):
            logger.info(f"Cache {self} setting address {address} to state exclusive")
            line.read(tag) # auto sets it to shared
            line.set_state(MSI.EXCLUSIVE)
        else:
            logger.info(f"Cache {self} setting address {address} to state shared")
            line.set_state(MSI.SHARED) # provides a cache probe
            line.read(tag)  
        

    def _read_hit(self, line, tag, address):
        """This is when a read happens and the state of either Shared or Modified

        Args:
            line (Line): The cacheline
            tag  (int): The value of the tag
            address (int): Address of the word 
        """
        logger.info('Read hit for cache: {}'.format(self))
        # We never change state when we read, even when optimization is enabled
        Statistic.cache_access()
        Statistic.private_access()
        return


    # -- Remote Operations -- #
    def remote_read_miss(self, address):
        """Another cache has issued a read miss. Thus we need to set the state to shared if 
            we are in modified state. Perfroms cache probe and coherence writeback if line is
            in state M.

        Args:
            address (int): Address of the word
        """
        logger.info('Remote read miss issued for cache {} with address: {}'.format(self, address))
        tag, index, offset = get_address_parameters(address, self._INDEX_BITS, self._OFFSET_BITS)
        line = self.cachelines[index]

        # check if the line is actuall valid
        if (tag == line.tag and line.valid == True):
            if (line.state == MSI.MODIFIED):
                logger.info('Changing line {} to state SHARED, since it was in modified'.format(line))
                line.state = MSI.SHARED
                Statistic.coherence_writeback()
            elif(line.state == MSI.EXCLUSIVE and Optimizer.OPTIMIZE):
                logger.info('Changing line {} to state SHARED, since it was in exlusive'.format(line))
                line.state = MSI.SHARED

    def send_line(self, cache, address):
        """Sends the data of the line to the desired cache. We don't actaully
            send data so this method is a placeholder.

        Args:
            cache (Cache): Cache to send data to
            address (int): Address of the word
        """
        logger.info('Cache {} sending line with address {} to cache {}'.format(self, address, cache))
        tag, index, offset = get_address_parameters(address, self._INDEX_BITS, self._OFFSET_BITS)
        line = self.cachelines[index]
        return

    def alert_last_sharer(self, address, cache):
        """This method is called when this cache is the last sharer for an address

        Args:
            int: Address of the word
            Cache: cache that has just been removed as a sharer
        """
        # check if optimization is on
        if (Optimizer.OPTIMIZE):
            logger.info(f'Directory informing cache {self} that it is last sharer for address: {address} because other sharer cache: {cache} invalidated'.format(self, address, cache))
            tag, index, offset = get_address_parameters(address, self._INDEX_BITS, self._OFFSET_BITS)
            line = self.cachelines[index]
            if (line.tag == tag and line.valid==True):
                logger.debug(f'cache {self} changing address {address} to state exclusive')
                # change state to exlusive since it is last sharer but dont probe as this will overlap
                line.state = MSI.EXCLUSIVE
                # send acknowledgment to directory but this overlaps

    # -- Invalidations -- #
    def invalidate_line(self, address, cache):
        """Invalidates the cache line. Probes the cache

        Args:
            address (int): Address of the word
            cache (Cache): The cache that asked for invalidation
        """
        logger.info('Cache {} is invalidating line with address: {} asked from cache: {}'.format(self, address, cache))
        tag, index, offset = get_address_parameters(address, self._INDEX_BITS, self._OFFSET_BITS)
        line = self.cachelines[index]
        # check if the line is actuall valid
        if (tag == line.tag and line.valid == True):
        #     if (line.state == MSI.MODIFIED):
                # logger.debug('line w/ address {} is in modified so creating coherence writeback'.format(address))
                # line.state = MSI.SHARED
                # Statistic.coherence_writeback()
            line.invalidate()
            cache.confirm_invalidation(address)

    def confirm_invalidation(self, address):
        """This is sent from another cache confirming an invalidation for a given address.
            It then decrements the num of validations expected

            Args:
                address (int): Address of the word
        """
        logger.debug('Confirming invalidation for cache: {}'.format(self))
        # if (self.num_invalidates == 0):
        #     raise Exception('Too many confirm invalidations sent, expected {}'.format(self.num_invalidates))
        # else:
        #     logger.debug('Invalidation acknowledged')
        #     self.num_invalidates -= 1

        # if (self.num_invalidates == 0):
        #     logger.debug('All invalidations recieved')
        #     if (address == self.pending_address):
        #         tag, index, offset = get_address_parameters(self.pending_address, self._INDEX_BITS, self._OFFSET_BITS)
        #         line = self.cachelines[index]
        #         # here we would change the state but we are cheating since we do it earlier
        #         # line.state(MSI.MODIFIED)
        #         # now set pending address = -1
        #         self.pending_address = -1
        #     else:
        #         raise Exception('Address invalidated {} does not mach pending address {}'.format(address, self.pending_address))
                        
    def contains_address(self, address):
        """Checks if the given address is valid within the cache

        Args:
            address (int): Address of the word

        Returns:
            bool: True if the address is valid in the cache
        """
        logger.debug('Cache {} checking if it contains the address: {}'.format(self, address))
        tag, index, offset = get_address_parameters(address, self._INDEX_BITS, self._OFFSET_BITS)
        line = self.cachelines[index]
        
        if (line.tag == tag and line.valid == True and line.state != MSI.INVALID):
            return True
        else:
            return False


    @property
    def cachelines(self):
        return self._cachelines

    @property
    def LINE_SIZE(self):
        return self._CACHE_SIZE


def get_address_parameters(address, INDEX_BITS, OFFSET_BITS):
    """Get the Tag, Index and Offset for the given address

    Args:
        address (int): The address of the word
        INDEX_BITS (int): The number of index bits
        OFFSET_BITS (int): The number of offset bits

    Returns:
        tag (int): The tag
        index (int): The index
        offset (int): The offset
    """
    # logger.debug('Getting address parameters for address: {}'.format(address))
    tag = (address >> (OFFSET_BITS + INDEX_BITS))
    index = (address >>  OFFSET_BITS) & (np.power(2, INDEX_BITS) - 1)
    offset = address & (np.power(2, OFFSET_BITS) - 1)

    return tag, index, offset


def get_stored_address(tag, index, INDEX_BITS, OFFSET_BITS):
    """Creates the stored address with 0 offset and returns it

    Args:
        tag (int): The tag of the stored address
        index (int): The index of the stored address
        INDEX_BITS (int): The number of index bits
        OFFSET_BITS (int): The number of offset bits

    Returns:
        int : The address but with offset 0
    """
    logger.debug(f'Getting stored address with Tag: {tag}, index: {index}')
    tag = tag << (INDEX_BITS + OFFSET_BITS)
    index = index << OFFSET_BITS
    logger.debug(f'new tag: {tag}, new index: {index}')
    return tag | index | 0