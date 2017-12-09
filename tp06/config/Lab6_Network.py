#!/usr/bin/python

"""
This script creates the network environment for Lab6:
- Starts all routers, switches and hosts;
- Turns on/off specific quagga daemons;
- Adds IPv6 addressing to hosts;
- Launches XTerm window for all devices.
"""
# Needed to check for display status 
import os

# Needed to patch Mininet's isShellBuiltin module
import sys

# Run commands when you exit the python script
import atexit

# patch isShellBuiltin (suggested by MiniNExT's authors)
import mininet.util
import mininext.util
mininet.util.isShellBuiltin = mininext.util.isShellBuiltin
sys.modules['mininet.util'] = mininet.util

# Loads the default controller for the switches
# We load the OVSSwitch to use openflow v1.3 for IPv6 packet support
from mininet.node import Controller, OVSSwitch

# Needed to set logging level and show useful information during script execution.
from mininet.log import setLogLevel, info

# To launch xterm for each node
from mininet.term import cleanUpScreens, makeTerms # for supporting copy/paste 

# Provides the mininext> prompt
from mininext.cli import CLI

# Primary constructor for the virtual environment.
from mininext.net import MiniNExT

# We import the topology class for Lab4
from Lab6_Topology import Lab6Topo

# Variable initialization
net = None
hosts = None


def run():
    # Creates the virtual environment, by starting the network and configuring debug information
    info('** Creating an instance of Lab6 network topology\n')
    topo = Lab6Topo()

    info('** Starting the network\n')

    global net
    global hosts
    # We specify the OVSSwitch for better IPv6 performance
    # We use mininext constructor with the instance of the network, the default controller and the customized openvswitch
    net = MiniNExT(topo, controller=Controller, switch=OVSSwitch)
    net.start()
    info('** Executing custom commands\n')
    # Space to add any customize command before prompting command line
    # We assign IPv6 addresses to hosts h1, h2, and h5 as they are not configured through Quagga
    
    # We gather only the hosts created in the topology (no switches nor controller)
    hosts = [ net.getNodeByName( h ) for h in topo.hosts() ]

    for host in hosts:
    	# Only to hosts: We assign IPv6 address
        if host.name == 'h1':
            host.cmd('ip -6 addr add 2001:1:0:1010::10/64 dev h1-eth1')
            host.cmd('ip -6 route add default via 2001:1:0:1010::1')
        elif host.name == 'h2':            
            host.cmd('ip -6 addr add 2001:1:0:2020::20/64 dev h2-eth1')
            host.cmd('ip -6 route add default via 2001:1:0:2020::2')
        elif host.name == 'h5':            
            host.cmd('ip -6 addr add 2001:1:0:5050::50/64 dev h5-eth1')
            host.cmd('ip -6 route add default via 2001:1:0:5050::5')
	
	# Enable Xterm window for every host
    info('** Enabling xterm for hosts only\n')
    # We check if the display is available
    if 'DISPLAY' not in os.environ:
        error( "Error starting terms: Cannot connect to display\n" )
        return
    # Remove previous (and possible non-used) socat X11 tunnels
    cleanUpScreens()
    # Mininet's function to create Xterms in hosts
    makeTerms( hosts, 'host' )

	# Enable the mininext> prompt 
    info('** Running CLI\n')
    CLI(net)


# Cleanup function to be called when you quit the script
def stopNetwork():
    "stops the network, cleans logs"

    if net is not None:
        info('** Tearing down Quagga network\n')
        
        # This command stops the simulation
        net.stop()

if __name__ == '__main__':
    # Execute the cleanup function
    atexit.register(stopNetwork)

    # Set the log level on terminal
    setLogLevel('info')
    
    # Execute the script
    run()