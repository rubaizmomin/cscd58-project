from mininet.net import Mininet
from mininet.node import OVSSwitch, Host, OVSController, Node
from mininet.link import TCLink, Intf # this library makes it more realistic with metrics like bamdwidth, delay, packet loss

# failed links will return infinity
def parse_ping(s: str) -> float:

    stats = s.split('\n')[-2].split('/')
    if len(stats) > 5:
        return float(stats[-2])
    
    return float('inf')

def extract_link(h1: Node, h2:  Node) -> float:
    assert h1 is not h2
    assert len(h1.connectionsTo(h2)) > 0
    cmdStr = "ping -c 1 " + h2.IP()
    pingStr = h1.cmd(cmdStr)
    return  parse_ping(pingStr)# parse_ping(pingStr)


# gets takes all the links in net and passes a ping through 
def extract_mininet(net: Mininet) -> dict:
    weights = {}
    for s1 in net.switches:
        for h2 in net.hosts:
            if len(s1.connectionsTo(h2)) > 0:
                weights[s1, h2] = extract_link(s1, h2)
            
        
        for s2 in net.switches:
            if s1 is not s2 and len(s1.connectionsTo(s2)) > 0:
                weights[s1, s2] = extract_link(s1, s2)


    return weights