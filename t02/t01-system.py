import argparse
import m5
from m5.objects import *

# Add "common" gem5 scripts to the path
# m5.util.addToPath("/u/csc368h/winter/pub/scripts/gem5/")

# import the common/SimpleOpts module
# from common import SimpleOpts

# addition for T2
#parser = argparse.ArgumentParser()
#parser.add_argument('binary', type=str, default=DEFAULT_BINARY)
#parser.add_argument('-a', '--binary_args')

## Add the "binary" option to the script
DEFAULT_BINARY = '/u/csc368h/winter/pub/workloads/hello'
# SimpleOpts.add_option("binary", nargs="?", default=DEFAULT_BINARY)

# addition for T2
parser = argparse.ArgumentParser()
parser.add_argument('binary', type=str, default=DEFAULT_BINARY)
parser.add_argument('-a', '--binary_args')


# addition for T2
args = parser.parse_args()

## Parse command-line arguments
# args = SimpleOpts.parse_args()

# System creation
system = System()

## gem5 needs to know the clock and voltage
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '200MHz'
system.clk_domain.voltage_domain = VoltageDomain() # defaults to 1V

## Create a crossbar so that we can connect main memory and the CPU (below)
system.membus = SystemXBar()
system.system_port = system.membus.cpu_side_ports

## Use atomic mode for memory modelling
system.mem_mode = 'atomic'

# CPU Setup
system.cpu = X86AtomicSimpleCPU()
system.cpu.icache_port = system.membus.cpu_side_ports
system.cpu.dcache_port = system.membus.cpu_side_ports

## This is needed when we use x86 CPUs
system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

# Memory setup
system.mem_ctrl = MemCtrl()
system.mem_ctrl.port = system.membus.mem_side_ports

## A memory controller interfaces with main memory; create it here
system.mem_ctrl.dram = DDR3_1600_8x8()

## A DDR3_1600_8x8 has 8GB of memory, so setup an 8 GB address range
address_ranges = [AddrRange('8GB')]
system.mem_ranges = address_ranges
system.mem_ctrl.dram.range = address_ranges[0]

# Process setup
process = Process()

## Use a full path to the binary
binary = args.binary
# process.cmd = [binary]
process.cmd = [binary, args.binary_args] # T2 addition

## The necessary gem5 calls to initialize the workload and its threads
system.workload = SEWorkload.init_compatible(binary)
system.cpu.workload = process
system.cpu.createThreads()

# Start the simulation
root = Root(full_system=False, system=system) # must assign a root

m5.instantiate() # must be called before m5.simulate
m5.simulate()

print('End of t01-system.py')

