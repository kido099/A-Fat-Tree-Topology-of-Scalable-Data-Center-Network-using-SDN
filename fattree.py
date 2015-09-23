#!/usr/bin/env python

import sys
import time

from mininet.net import Mininet
from mininet.node import Host, OVSSwitch, Controller, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import Link, Intf, TCLink
from mininet.topo import Topo
from mininet.util import dumpNodeConnections
import os


CoreSwitchList = []
AggSwitchList = []
EdgeSwitchList = []
HostList = []

pod = 4
iCoreLayerSwitch = 4
iAggLayerSwitch = 8
iEdgeLayerSwitch = 8
iHost = 16
end = 2

net = Mininet()
#c1 = net.addController('c0', controller=RemoteController, ip='10.190.82.223', port = 6633)
#c2 = net.addController('c1', controller=RemoteController, ip='172.16.51.1', port = 6633)
c3 = net.addController('c0', controller=RemoteController, ip='172.16.192.1', port = 6633)
#c4 = net.addController('c3', controller=RemoteController, ip='127.0.0.1', port = 6633)



MAC_LAST = 0

#CoreSwitch
core = 1
for x in range(1, iCoreLayerSwitch + 1):
    PREFIX = "s100"
    if x % end == 0:
        IP = "00100004" + "000" + str((x/(end + 1)) + 1) + "000" + str(end)
    else:
        IP = "00100004" + "000" + str((x/(end + 1)) + 1) + "000" + str(x % end)
    MAC_LAST_16 = str(hex(MAC_LAST))
    MAC_new = MAC_LAST_16.split('x')[1]
    MACADDR = "00:00:00:00:00:0" + MAC_new
    CoreSwitchList.append(net.addSwitch(PREFIX + str(x), dpid = IP))
    #, ip = IP, mac = MACADDR))
    #CoreSwitchList[core-1].setIP(ip = IP)
    CoreSwitchList[core-1].setMAC(mac = MACADDR)
    core = core + 1
    MAC_LAST = MAC_LAST + 1

#AggSwitch
agg = 1
for i in range(pod):
    for j in range(pod/2,pod):
        PREFIX = "s200"
        IPString = "0010" + "000" + str(i) + "000" + str(j) + "0001";
        Name = PREFIX + str(agg)
        MAC_LAST_16 = str(hex(MAC_LAST))
        MAC_new = MAC_LAST_16.split('x')[1]
        MACADDR = "00:00:00:00:00:" + MAC_new
        AggSwitchList.append(net.addSwitch(Name, dpid = IPString))
        #AggSwitchList[agg-1].setIP(ip = IPString)
        AggSwitchList[agg-1].setMAC(mac = MACADDR)
        agg = agg + 1
        MAC_LAST = MAC_LAST + 1

#EdgeSwitch
edg = 1
for i in range(pod):
    for j in range(pod/2):
        PREFIX = "s300"
        Name = PREFIX + str(edg)
        IPString = "0010" + "000" + str(i) + "000" + str(j) + "0001"
        MAC_LAST_16 = str(hex(MAC_LAST))
        MAC_new = MAC_LAST_16.split('x')[1]
        MACADDR = "00:00:00:00:00:" + MAC_new
        EdgeSwitchList.append(net.addSwitch(Name, dpid = IPString))
        #EdgeSwitchList[edg-1].setIP(ip = IPString)
        EdgeSwitchList[edg-1].setMAC(mac = MACADDR)
        edg = edg + 1
        MAC_LAST = MAC_LAST + 1

#Hosts
h = 1
for i in range(pod):
    for j in range(pod/2):
        for m in range(2,pod/2+2):
            PREFIX = "h00"
            if h >= int(10):
                PREFIX = "h0"
            Name = PREFIX + str(h)
            IPString = "10." + str(i) + "." + str(j) + "." + str(m)
            MAC_LAST_16 = str(hex(MAC_LAST))
            MAC_new = MAC_LAST_16.split('x')[1]
            MACADDR = "00:00:00:00:00:" + MAC_new
            HostList.append(net.addHost(Name, ip=IPString))
            #HostList[h-1].setIP(IPString, intf=intf)
            h = h + 1
            MAC_LAST = MAC_LAST + 1
                        
#Add E2H link
for x in range(0,iEdgeLayerSwitch):
    for i in range(0, end):
        net.addLink(EdgeSwitchList[x],HostList[end * x + i])
                                
                                
#Add A2E link
for x in range(0,iEdgeLayerSwitch,end):
    for i in range(0,end):
        for j in range(0,end):
            net.addLink(AggSwitchList[x+i],EdgeSwitchList[x+j])
                                            
#Add C2A link
for x in range(0,iAggLayerSwitch,end):
    for i in range(0,end):
        for j in range(0,end):
            net.addLink(CoreSwitchList[i*end+j],AggSwitchList[x+i])
                                                        
                                                        
net.start()
                                                        
#test
#print "h001: IP:", HostList[0].IP(), "MAC:", HostList[0].MAC()
#print "h016: IP:", HostList[15].IP(), "MAC:", HostList[15].MAC()
#print "s1001: dpid:", CoreSwitchList[0].dpid, "MAC:", CoreSwitchList[0].MAC()
#print "s2001: dpid:", AggSwitchList[0].IP(), "MAC:", AggSwitchList[0].MAC()
#print "s3001: dpid:", EdgeSwitchList[0].IP(), "MAC:", EdgeSwitchList[0].MAC()
                                                        
                                                        
CLI(net)
net.stop()
                                                        
