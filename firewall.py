'''
Coursera:
- Software Defined Networking (SDN) course
-- Module 4 Programming Assignment

Professor: Nick Feamster
Teaching Assistant: Muhammad Shahbaz
'''

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os
''' Add your imports here ... '''
import csv


log = core.getLogger()
policyFile = "%s/CSC485A/pox/pox/misc/firewall-policies.csv" % os.environ[ 'HOME' ]  

''' Add your global variables here ... '''
with open(policyFile) as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    mac_0 = []
    mac_1 = []
    count = 0
    for row in spamreader:
	if(count>0):
            mac_0.append(row[1])
            mac_1.append(row[2])
	count = count +1
    
"""
    addr = '00:00:00:00:00:01'
    index = 0
    for mac in mac_0:
	if addr == mac:
	    print "yes"
	    break
	index = index+1
"""    

class Firewall (EventMixin):

    def __init__ (self):
        self.listenTo(core.openflow)
        log.debug("Enabling Firewall Module")

    def _handle_ConnectionUp (self, event):    
        ''' Add your logic here ... '''
	"""
	#print mac_0
	#print mac_1
	for src, dst in zip(mac_0, mac_1):
	    #print src, dst
	    match = of.ofp_match()
	    match.dl_src = src
	    match.dl_dst = dst
	    print match
        """
	for i in range(len(mac_0)):
		fm = of.ofp_flow_mod()
		fm.match.dl_src = EthAddr(mac_0[i])
		fm.match.dl_dst = EthAddr(mac_1[i])
		# I tried all actions in ofp_action_output, found out that OFPP_TABLE works
		# reference from https://openflow.stanford.edu/display/ONL/POX+Wiki
		fm.actions.append(of.ofp_action_output(port = of.OFPP_TABLE))
		event.connection.send(fm)
    
        log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))

def launch ():
    '''
    Starting the Firewall module
    '''
    core.registerNew(Firewall)
