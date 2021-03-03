import logging
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


    # latency requests
    @classmethod
    def cache_probe(self):
        logger.debug('-Cache probe-')
        self.CACHE_PROBES += 1

    @classmethod
    def cache_access(self):
        logger.debug('-Cache access-')
        self.CACHE_ACCESSES += 1

    @classmethod
    def sram_access(self):
        self.SRAM_ACCESSES += 1

    @classmethod
    def directory_access(self):
        logger.debug('-Directory Access-')
        self.DIRECTORY_ACCESSES += 1

    @classmethod
    def processor_hop(self, hops):
        logger.debug('-{} Proccessor hops-'.format(hops))
        self.PROCESSOR_HOPS += hops

    @classmethod
    def directory_request(self):
        logger.debug('-Directory Request-')
        self.DIRECTORY_HOPS += 1

    @classmethod
    def memory_access(self):
        logger.debug('-Memory Access-')
        self.MEMORY_ACCESSES += 1

    # statistics
    @classmethod
    def private_access(self):
        logger.debug('-Private Access-')
        self.PRIVATE_ACCESSES += 1
    
    @classmethod
    def remote_access(self):
        logger.debug('-Remote Access-')
        self.REMOTE_ACCESSES += 1

    @classmethod
    def off_chip_access(self):
        logger.debug('-Off Chip Access-')
        self.OFF_CHIP_ACCESS += 1

    @classmethod
    def replacement_writeback(self):
        logger.debug('-Replacement Writeback-')
        self.REPLACEMENT_WRITEBACKS += 1

    @classmethod
    def coherence_writeback(self):
        logger.debug('-Coherence Writeback-')
        self.COHERENCE_WRITEBACKS += 1

    @classmethod
    def invalidation_sent(self, num):
        logger.debug(f'-{num} Invalidations Sent-')
        self.INVALIDATIONS_SENT += num

    @classmethod
    def reset(self):
        self.INSTRUCTIONS = 0

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
        self.PRIVATE_ACCESSES_PREV = self.PRIVATE_ACCESSES
        self.OFF_CHIP_ACCESS = 0         
        self.REMOTE_ACCESSES_PREV = self.REMOTE_ACCESSES
        self.REPLACEMENT_WRITEBACKS = 0
        self.OFF_CHIP_ACCESS_PREV = self.OFF_CHIP_ACCESS

        self.COHERENCE_WRITEBACKS = 0
        self.INVALIDATIONS_SENT = 0
        self.AVERAGE_LATENCY = 0

        self.PRIV_LATENCIES = []
        self.REM_LATENCIES = []
        self.OFF_CHIP_LATENCIES = []
        self.TOTAL_LATENCY = 0 
        self.TOTAL_LATENCY_PREV = self.TOTAL_LATENCY

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
        average = average/self.INSTRUCTIONS
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

    @classmethod
    def debug_statistics(self):
        string = f"""
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
        """
        return string

    @classmethod
    def key_statistics(self):
        string = f"""
        Instruction: {self.INSTRUCTIONS}
        Private-accesses: {self.PRIVATE_ACCESSES}
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