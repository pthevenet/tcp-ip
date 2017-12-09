# ThreeAS_Topology

# Modules needed to get the absolute path to this file for quagga configuration
import inspect
import os

# You can show useful information during script execution
from mininet.log import info

# Class in mininext which includes PID namespaces, log and run isolation. 
from mininext.topo import Topo

# Class in mininext to setup the quagga service on virtual routers
from mininext.services.quagga import QuaggaService

# A container in python
from collections import namedtuple

# Variable initialization
NetworkHosts = namedtuple("NetworkHosts", "name IP DG")
net = None


class Lab6Topo(Topo):
    def __init__(self):
        #Initialize a topology of 3 hosts, 5 routers, 4 switches
        Topo.__init__(self)

        info( '*** Creating Quagga Routers\n' )
        # Absolute path to this python script
        selfPath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

        # Initialize the Quagga Service
        # autoStart=True (default) --> starts automatically quagga on the host
        # autoStop=True (default) --> stops automatically quagga (we don't want this)
        quaggaSvc = QuaggaService(autoStop=False) 

        # Configuration file path for quagga routers
        quaggaBaseConfigPath = selfPath + '/configs/'

        # Initializing local variables
        netHosts = []
        NodeList = []
        
        # List of all hosts in the network.
        # Note that each node requires at least one IP address.
        netHosts.append(NetworkHosts(name='h1', IP='192.10.10.10/24', DG='via 192.10.10.1'))
        netHosts.append(NetworkHosts(name='h2', IP='192.20.20.20/24', DG='via 192.20.20.2'))
        netHosts.append(NetworkHosts(name='h5', IP='192.50.50.50/24', DG='via 192.50.50.5'))
        netHosts.append(NetworkHosts(name='r1', IP='192.10.10.1/24', DG=''))
        netHosts.append(NetworkHosts(name='r2', IP='192.20.20.2/24', DG=''))
        netHosts.append(NetworkHosts(name='r3', IP='192.13.13.3/24', DG=''))
        netHosts.append(NetworkHosts(name='r4', IP='192.24.24.4/24', DG=''))
        netHosts.append(NetworkHosts(name='r5', IP='192.50.50.5/24', DG=''))
	
        for host in netHosts:
	        # We create a list of node names
            NodeList.append(host.name)
            if host.name in ['h1','h2','h5']: 
	            # We configure PCs with default gateway and without quagga service
                AddPCHost = self.addHost(name=host.name, ip=host.IP, defaultRoute=host.DG, hostname=host.name, privateLogDir=True, privateRunDir=True, inMountNamespace=True, inPIDNamespace=True, inUTSNamespace=True)
            else:
			    # We configure routers with quagga service without default gateway
                AddQuaggaHost = self.addHost(name=host.name, ip=host.IP, hostname=host.name, privateLogDir=True, privateRunDir=True, inMountNamespace=True, inPIDNamespace=True, inUTSNamespace=True)
                # We setup Quagga service and path to config files
                quaggaSvcConfig = {'quaggaConfigPath': quaggaBaseConfigPath + host.name}
                self.addNodeService(node=host.name, service=quaggaSvc, nodeConfig=quaggaSvcConfig)     	
        # Adding switches to the network, we specify OpenFlow v1.3 for IPv6 suppport
        SW1 = self.addSwitch('SW1', protocols='OpenFlow13')
        SW2 = self.addSwitch('SW2', protocols='OpenFlow13')
        SW5 = self.addSwitch('SW5', protocols='OpenFlow13')
        SW12 = self.addSwitch('SW12', protocols='OpenFlow13')
        SW13 = self.addSwitch('SW13', protocols='OpenFlow13')
        SW24 = self.addSwitch('SW24', protocols='OpenFlow13')
        SW345 = self.addSwitch('SW345', protocols='OpenFlow13')
        # We add links between switches and routers according to Fig.1 of Lab 4
        info( '*** Creating links\n' )
        self.addLink( SW1, NodeList[0], intfName2='h1-eth1'  )
        self.addLink( SW1, NodeList[3], intfName2='r1-eth3'  )

        self.addLink( SW2, NodeList[1], intfName2='h2-eth1'  )
        self.addLink( SW2, NodeList[4], intfName2='r2-eth3'  )

        self.addLink( SW5, NodeList[2], intfName2='h5-eth1'  )
        self.addLink( SW5, NodeList[7], intfName2='r5-eth1'  )

        self.addLink( SW12, NodeList[3], intfName2='r1-eth2'  )
        self.addLink( SW12, NodeList[4], intfName2='r2-eth2'  )

        self.addLink( SW13, NodeList[3], intfName2='r1-eth1'  )
        self.addLink( SW13, NodeList[5], intfName2='r3-eth1'  )

        self.addLink( SW24, NodeList[4], intfName2='r2-eth1'  )
        self.addLink( SW24, NodeList[6], intfName2='r4-eth1'  )

        self.addLink( SW345, NodeList[5], intfName2='r3-eth2'  )
        self.addLink( SW345, NodeList[6], intfName2='r4-eth2'  )
        self.addLink( SW345, NodeList[7], intfName2='r5-eth2'  )