import random
import time
from mininet.log import info
from .lock import mininet_cmd_lock

def random_failures(net, fail_prob=0.1, recover_prob=0.05, sleep_interval=5):
    link_state = {}

    # get link pairs by sorting to prevent considering a,b and b,a as different links
    def key(a, b):
        return tuple(sorted([a, b]))

    # initialize all links as up in the beginning
    for link in net.links:
        a = link.intf1.node.name
        b = link.intf2.node.name
        link_state[key(a, b)] = "up"

    while True:
        time.sleep(sleep_interval)
        
        for (a, b), state in list(link_state.items()):
            # if the random value is less than the fail_prob, bring down the link
            if state == "up":
                if random.random() < fail_prob:
                    print(f"---- FAIL: {a}-{b} ----\n")
                    # prevent race condition with get_mininet_adj when running simulation 
                    with mininet_cmd_lock:
                        net.configLinkStatus(a, b, "down")
                    link_state[(a, b)] = "down"
            # if the random value is less than the recover_prob, bring up the link
            else:
                if random.random() < recover_prob:
                    print(f"---- RECOVER: {a}-{b} ----\n")
                    # prevent race condition with get_mininet_adj when running simulation 
                    with mininet_cmd_lock:
                        net.configLinkStatus(a, b, "up")
                    link_state[(a, b)] = "up"
