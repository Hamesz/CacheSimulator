import logging
import os
logger = logging.getLogger('cachesimulator.Logger')

class Latency:
    # measured in clock cycles
    CACHE_PROBE = 1
    CACHE_ACCESS = 1
    SRAM_ACCESS = 1
    DIRECTORY_ACCESS = 1
    PROCESSOR_HOP = 3
    DIRECTORY_HOP = 5
    MEMORY_ACCESS = 15


class Statistic:
    """This class deals with getting the statistics and saving them
    """
    # number of instructions issued
    INSTRUCTIONS = 0

    # Extra statistics
    # miss because data is from start of program
    COMPULSORY_MISSES = 0   
    # miss when the data required was in the cache previously, but got evicted.
    CONFLICT_MISSES = 0     
    # miss occurs due to the limited size of a cache and not the cache's mapping function
    CAPACITY_MISSES = 0
    # miss because another cache invalidated the line     
    COHERENCE_MISSES = 0 

    # Line is in S, and cache wants to write so alerts the directory but there are no sharers 
    WRITE_MISS_BUT_NO_DATA_NEEDED_AND_NO_SHARERS = 0
    # line in I, and cache wants to write so alerts directory
    WRITE_MISS_BUT_DATA_NEEDED = 0

    THREE_HOPS = 0
    TWO_HOPS = 0
    ONE_HOPS = 0

    # latency statstics
    CACHE_PROBES = 0 
    CACHE_PROBES_PREV = CACHE_PROBES
    CACHE_ACCESSES = 0
    CACHE_ACCESSES_PREV = CACHE_ACCESSES 
    SRAM_ACCESSES = 0 
    SRAM_ACCESSES_PREV = SRAM_ACCESSES
    DIRECTORY_ACCESSES = 0 
    DIRECTORY_ACCESSES_PREV = DIRECTORY_ACCESSES
    PROCESSOR_HOPS = 0 
    PROCESSOR_HOPS_PREV = PROCESSOR_HOPS
    MEMORY_ACCESSES = 0 
    MEMORY_ACCESSES_PREV = MEMORY_ACCESSES
    DIRECTORY_HOPS = 0 
    DIRECTORY_HOPS_PREV = DIRECTORY_HOPS

    # statstics
    PRIVATE_ACCESSES = 0  
    PRIVATE_ACCESSES_PREV = PRIVATE_ACCESSES
    REMOTE_ACCESSES = 0   
    REMOTE_ACCESSES_PREV = REMOTE_ACCESSES    
    OFF_CHIP_ACCESS = 0   
    OFF_CHIP_ACCESS_PREV = OFF_CHIP_ACCESS

    REPLACEMENT_WRITEBACKS = 0
    COHERENCE_WRITEBACKS = 0
    INVALIDATIONS_SENT = 0

    AVERAGE_LATENCY = 0
    PRIV_LATENCIES = []
    REM_LATENCIES = []
    OFF_CHIP_LATENCIES = []
    TOTAL_LATENCY = 0 
    TOTAL_LATENCY_PREV = TOTAL_LATENCY

    @classmethod
    def add_instructions(self):
        self.INSTRUCTIONS += 1

    @classmethod
    def end_instruction(self):
        """sets all the previous values to current ones
            and checks which type access (private remote etc)
            and then stores that latency
        """
        instruction_latency = self.compute_current_latency()

        if(self.PRIVATE_ACCESSES != self.PRIVATE_ACCESSES_PREV):
            self.PRIV_LATENCIES.append(instruction_latency)
        elif(self.REMOTE_ACCESSES_PREV != self.REMOTE_ACCESSES):
            self.REM_LATENCIES.append(instruction_latency)
        elif(self.OFF_CHIP_ACCESS_PREV != self.OFF_CHIP_ACCESS):
            self.OFF_CHIP_LATENCIES.append(instruction_latency)
        else:
            raise Exception(f"No type of access (remote, private or chip) was done for the end of this instruction")

        self.CACHE_PROBES_PREV =        self.CACHE_PROBES
        self.CACHE_ACCESSES_PREV =      self.CACHE_ACCESSES
        self.SRAM_ACCESSES_PREV =       self.SRAM_ACCESSES
        self.DIRECTORY_ACCESSES_PREV =  self.DIRECTORY_ACCESSES
        self.PROCESSOR_HOPS_PREV =      self.PROCESSOR_HOPS
        self.MEMORY_ACCESSES_PREV =     self.MEMORY_ACCESSES
        self.DIRECTORY_HOPS_PREV =      self.DIRECTORY_HOPS
        # statstics       
        self.PRIVATE_ACCESSES_PREV = self.PRIVATE_ACCESSES      
        self.REMOTE_ACCESSES_PREV = self.REMOTE_ACCESSES
        self.OFF_CHIP_ACCESS_PREV = self.OFF_CHIP_ACCESS


    # -- Misses -- #
    @classmethod
    def compulsory_miss(self):
        logger.debug("-Compulsory miss-")
        self.COMPULSORY_MISSES += 1

    @classmethod
    def conflic_miss(self):
        logger.debug("-Conflict miss-")
        self.CONFLICT_MISSES += 1

    @classmethod
    def capacity_miss(self):
        logger.debug("-Capacity miss-")
        self.CAPACITY_MISSES += 1

    @classmethod
    def coherence_miss(self):
        logger.debug("-Coherence miss-")
        self.COHERENCE_MISSES += 1
    
    @classmethod
    def three_hops(self):
        self.THREE_HOPS += 1

    @classmethod
    def two_hops(self):
        self.TWO_HOPS += 1

    @classmethod
    def one_hops(self):
        self.ONE_HOPS += 1

    # latency requests
    @classmethod
    def cache_probe(self):
        logger.info('-Cache probe-')
        self.CACHE_PROBES += 1

    @classmethod
    def write_miss_no_sharers(self):
        logger.debug('-Write miss no need data and no sharers-')
        self.WRITE_MISS_BUT_NO_DATA_NEEDED_AND_NO_SHARERS += 1

    @classmethod
    def write_miss_data_needed(self):
        self.WRITE_MISS_BUT_DATA_NEEDED += 1
    # ------------------------------

    # -- Latency Actions -- #
    @classmethod
    def cache_access(self):
        logger.info('-Cache access-')
        self.CACHE_ACCESSES += 1

    @classmethod
    def sram_access(self):
        logger.info("-SRAM access-")
        self.SRAM_ACCESSES += 1

    @classmethod
    def directory_access(self):
        logger.info('-Directory Access-')
        self.DIRECTORY_ACCESSES += 1

    @classmethod
    def processor_hop(self, hops):
        logger.info('-{} Proccessor hops-'.format(hops))
        self.PROCESSOR_HOPS += hops

        if (hops == 3):
            self.three_hops()
        elif (hops == 2):
            self.two_hops()
        else:
            self.one_hops()

    @classmethod
    def directory_request(self):
        logger.info('-Directory Request-')
        self.DIRECTORY_HOPS += 1

    @classmethod
    def memory_access(self):
        logger.info('-Memory Access-')
        self.MEMORY_ACCESSES += 1

    #-----------------------------------------

    # -- Key statistics -- #
    @classmethod
    def private_access(self):
        logger.info('-Private Access-')
        self.PRIVATE_ACCESSES += 1
    
    @classmethod
    def remote_access(self):
        logger.info('-Remote Access-')
        self.REMOTE_ACCESSES += 1

    @classmethod
    def off_chip_access(self):
        logger.info('-Off Chip Access-')
        self.OFF_CHIP_ACCESS += 1

    @classmethod
    def replacement_writeback(self):
        logger.info('-Replacement Writeback-')
        self.REPLACEMENT_WRITEBACKS += 1

    @classmethod
    def coherence_writeback(self):
        logger.info('-Coherence Writeback-')
        self.COHERENCE_WRITEBACKS += 1

    @classmethod
    def invalidation_sent(self, num):
        logger.info(f'-{num} Invalidations Sent-')
        self.INVALIDATIONS_SENT += num
    # --------------------------------------------

    
    @classmethod
    def reset(self):
        self.INSTRUCTIONS = 0

        self.COMPULSORY_MISSES = 0   
        self.CONFLICT_MISSES = 0     
        self.CAPACITY_MISSES = 0 
        self.COHERENCE_MISSES = 0 

        self.WRITE_MISS_BUT_NO_DATA_NEEDED_AND_NO_SHARERS = 0
        self.WRITE_MISS_BUT_DATA_NEEDED = 0

        self.THREE_HOPS = 0
        self.TWO_HOPS = 0
        self.ONE_HOPS = 0

        self.CACHE_PROBES = 0         
        self.CACHE_PROBES_PREV = self.CACHE_PROBES
        self.CACHE_ACCESSES = 0      
        self.CACHE_ACCESSES_PREV = self.CACHE_ACCESSES 
        self.SRAM_ACCESSES = 0       
        self.SRAM_ACCESSES_PREV = self.SRAM_ACCESSES
        self.DIRECTORY_ACCESSES = 0    
        self.DIRECTORY_ACCESSES_PREV = self.DIRECTORY_ACCESSES
        self.PROCESSOR_HOPS = 0       
        self.PROCESSOR_HOPS_PREV = self.PROCESSOR_HOPS
        self.MEMORY_ACCESSES = 0      
        self.MEMORY_ACCESSES_PREV = self.MEMORY_ACCESSES
        self.DIRECTORY_HOPS = 0      
        self.DIRECTORY_HOPS_PREV = self.DIRECTORY_HOPS            

        # statstics
        self.REMOTE_ACCESSES = 0         
        self.PRIVATE_ACCESSES = 0
        self.OFF_CHIP_ACCESS = 0 
        self.REPLACEMENT_WRITEBACKS = 0
        self.COHERENCE_WRITEBACKS = 0
        self.INVALIDATIONS_SENT = 0
        self.PRIVATE_ACCESSES_PREV = self.PRIVATE_ACCESSES        
        self.REMOTE_ACCESSES_PREV = self.REMOTE_ACCESSES
        self.OFF_CHIP_ACCESS_PREV = self.OFF_CHIP_ACCESS


        self.AVERAGE_LATENCY = 0

        self.PRIV_LATENCIES = []
        self.REM_LATENCIES = []
        self.OFF_CHIP_LATENCIES = []
        self.TOTAL_LATENCY = 0 
        self.TOTAL_LATENCY_PREV = self.TOTAL_LATENCY
    
    # -- Latency Methods -- #
    @classmethod
    def compute_current_latency(self):
        """Computes the current latency taken by looking
            at previous actiond and current
        """
        cache_probes        = (self.CACHE_PROBES - self.CACHE_PROBES_PREV)*Latency.CACHE_PROBE    
        cache_accesses      = (self.CACHE_ACCESSES - self.CACHE_ACCESSES_PREV)*Latency.CACHE_ACCESS
        sram_accesses       = (self.SRAM_ACCESSES - self.SRAM_ACCESSES_PREV)*Latency.SRAM_ACCESS
        directory_accesses  = (self.DIRECTORY_ACCESSES - self.DIRECTORY_ACCESSES_PREV)*Latency.DIRECTORY_ACCESS
        processor_hops      = (self.PROCESSOR_HOPS - self.PROCESSOR_HOPS_PREV)*Latency.PROCESSOR_HOP
        memory_accesses     = (self.MEMORY_ACCESSES - self.MEMORY_ACCESSES_PREV)*Latency.MEMORY_ACCESS
        directory_hops      = (self.DIRECTORY_HOPS - self.DIRECTORY_HOPS_PREV)*Latency.DIRECTORY_HOP

        total_latency = cache_probes + cache_accesses + sram_accesses + directory_accesses + processor_hops + memory_accesses + directory_hops
        return total_latency

    @classmethod
    def total_latency(self):
        return sum(self.REM_LATENCIES) + sum(self.PRIV_LATENCIES) + sum(self.OFF_CHIP_LATENCIES)

    @classmethod
    def average_latency(self):
        average = sum(self.REM_LATENCIES) + sum(self.PRIV_LATENCIES) + sum(self.OFF_CHIP_LATENCIES)
        try:
            average = average/self.INSTRUCTIONS
        except:
            return 0
        return average
    
    @classmethod
    def rem_average_latency(self):
        if (len(self.REM_LATENCIES) != 0):
            return sum(self.REM_LATENCIES)/len(self.REM_LATENCIES)
        return 0

    @classmethod
    def priv_average_latency(self):
        if (len(self.PRIV_LATENCIES) != 0):
            return sum(self.PRIV_LATENCIES)/len(self.PRIV_LATENCIES)
        else:
            return 0

    @classmethod
    def off_chip_latency(self):
        if (len(self.OFF_CHIP_LATENCIES) != 0):
            return sum(self.OFF_CHIP_LATENCIES)/len(self.OFF_CHIP_LATENCIES)
        else:
            return 0

    # ---------------------------------


    # -- Printing Info -- #
    @classmethod
    def debug_statistics(self):
        string = f"""Instruction: {self.INSTRUCTIONS}
Total Cache accesses: {self.CACHE_ACCESSES}
    Instruction cache accesses: {self.CACHE_ACCESSES - self.CACHE_ACCESSES_PREV}
Total Cache probes: {self.CACHE_PROBES}
    Instruction cache probes: {self.CACHE_PROBES - self.CACHE_PROBES_PREV}
Total SRAM Accesses: {self.SRAM_ACCESSES}
    Instruction SRAM accesses: {self.SRAM_ACCESSES - self.SRAM_ACCESSES_PREV}
Total Processor Hops: {self.PROCESSOR_HOPS}
    Instruction processor hops: {self.PROCESSOR_HOPS - self.PROCESSOR_HOPS_PREV}
Total Directory Accesses: {self.DIRECTORY_ACCESSES}
    Instruction directory Accesses: {self.DIRECTORY_ACCESSES - self.DIRECTORY_ACCESSES_PREV}
Total Directory Requests/Hops: {self.DIRECTORY_HOPS}
    Instruction directory requests/hops: {self.DIRECTORY_HOPS - self.DIRECTORY_HOPS_PREV}
Total Memory Accesses: {self.MEMORY_ACCESSES}
    Instruction memory accesses: {self.MEMORY_ACCESSES - self.MEMORY_ACCESSES_PREV}
Instruction Latency: {self.compute_current_latency()}

Compulsory misses:  {self.COMPULSORY_MISSES}
Conflict misses:    {self.CONFLICT_MISSES}
Capacity misses:    {self.CAPACITY_MISSES}
Coherence misses:   {self.COHERENCE_MISSES}
Write miss, don't need data, with no sharers: {self.WRITE_MISS_BUT_NO_DATA_NEEDED_AND_NO_SHARERS}
write miss and data is needed: {self.WRITE_MISS_BUT_DATA_NEEDED}

Three hops: {self.THREE_HOPS}
Two hops: {self.TWO_HOPS}
One hops: {self.ONE_HOPS}
        """
        return string

    @classmethod
    def key_statistics(self):
        string = f"""Private-accesses: {self.PRIVATE_ACCESSES}
Remote-accesses: {self.REMOTE_ACCESSES}
Off-chip-accesses: {self.OFF_CHIP_ACCESS}
Total-accesses: {self.PRIVATE_ACCESSES + self.REMOTE_ACCESSES + self.OFF_CHIP_ACCESS}
Replacement-writebacks: {self.REPLACEMENT_WRITEBACKS}
Coherence-writebacks: {self.COHERENCE_WRITEBACKS}
Invalidations-sent: {self.INVALIDATIONS_SENT}
Average-latency: {self.average_latency()}
Priv-average-latency: {self.priv_average_latency()}
Rem-average-latency: {self.rem_average_latency()}
Off-chip-average-latency: {self.off_chip_latency()}
Total-latency: {self.total_latency()}"""
        return string

    @classmethod
    def hit_rate(self):
        """Calculates the hit rate by dividing the private accesses by 
            number of instructions issued

        Returns:
            float: The hit rate
        """
        if (self.INSTRUCTIONS != 0):
            return self.PRIVATE_ACCESSES/self.INSTRUCTIONS
        else:
            return 0

    # -------------------------------

def save_statistics(file_path):
    """Saves the key statstics in the given path with
        out_<trace_name>.txt.

    Args:
        file_path (string/path): Path to trace file
    """
    # get the filename and path
    path = os.path.dirname(file_path)
    name = os.path.basename(file_path)
    # create new path file
    file_name = f"out_{name}"
    file = os.path.join(path,file_name)

    # write to file, key statstics
    f = open(file, "w")
    f.write(Statistic.key_statistics())
    f.close()