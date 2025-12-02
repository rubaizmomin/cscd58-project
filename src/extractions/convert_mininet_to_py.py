from mininet.net import Mininet
from mininet.node import OVSSwitch, Host, OVSController, Node, Switch
from mininet.link import TCLink, Intf # this library makes it more realistic with metrics like bandwidth, delay, packet loss
from failures.lock import mininet_cmd_lock

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
    with mininet_cmd_lock:
        pingStr = h1.cmd(cmdStr)
    return  parse_ping(pingStr)# parse_ping(pingStr)

# gets takes all the links in net and passes a ping through 
def extract_mininet(net: Mininet) -> dict:
    weights = {}
    for node in net.hosts + net.switches:
        weights[node.name] = {}

    for link in net.links:
        if1 = link.intf1
        if2 = link.intf2

        # prevent race conditions with random failures by locking the thread
        with mininet_cmd_lock:
            up1 = if1.isUp()
            up2 = if2.isUp()

        # if links are down then they dont share an edge, basically inf
        if not up1 or not up2:
            continue
        
        n1 = if1.node.name
        n2 = if2.node.name
        
        # check because switch to host is not possible to ping
        isHost1   = isinstance(if1.node, Host)
        isHost2   = isinstance(if2.node, Host)

        # assign the value from switch to host the same as host to switch
        if isHost1 and not isHost2:
            rtt = extract_link(if1.node, if2.node)
            weights[n1][n2] = rtt
            weights[n2][n1] = rtt
            continue

        if isHost2 and not isHost1:
            rtt = extract_link(if2.node, if1.node)
            weights[n1][n2] = rtt
            weights[n2][n1] = rtt
            continue
        
        weights[if1.node.name][if2.node.name] = extract_link(if1.node, if2.node)
        weights[if2.node.name][if1.node.name] = extract_link(if2.node, if1.node)
        
    return weights
