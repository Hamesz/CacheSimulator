# contains the trace file paths
import pathlib
import os

data_path = os.path.dirname(os.path.realpath(__file__))

# Trace files used
trace1 = os.path.join(data_path,"trace1.txt")
trace2 = os.path.join(data_path,"trace2.txt")
test_trace = os.path.join(data_path,"test_trace.txt")
trace_addre_1 = os.path.join(data_path,"trace_addr_1.txt")
optimize_trace = os.path.join(data_path,"optimize_trace.txt")
trace_test_RW_no_sharers = os.path.join(data_path,"trace_test_RW_no_sharers.txt")
B0 = os.path.join(data_path,"b0.txt")
