from failures.lock import mininet_cmd_lock

def convert_mininet_to_nx(net, weightKey=None):
    nx_graph = {}

    for node in net.switches + net.hosts:
        nx_graph[node.name] = {}

    for link in net.links:
        if1 = link.intf1
        if2 = link.intf2

        # prevent race conditions with random failures by locking the thread
        with mininet_cmd_lock:
            up1 = if1.isUp()
            up2 = if2.isUp()

        # dont create a link if link is down
        if not up1 or not up2:
            continue

        n1 = if1.node.name
        n2 = if2.node.name

        if weightKey is None:
            weight = 1
            
        nx_graph[n1][n2] = weight
        nx_graph[n2][n1] = weight

    return nx_graph
