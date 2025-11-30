'''
The code for creating an adjacency list from the mininet extraction logic 
can be written here? Just adding it here to make it more clear if we need to
use some graph helper functions to make our lives easier.
'''

'''
For now, we will assume that the graph looks something like this:
{
    "s0": {
        "s1": {"delay": 10, "bw": 5, "loss": 1},
        "s2": {"delay": 2,  "bw": 10, "loss": 0}
    },
    "s1": {
        "s0": {"delay": 10, "bw": 5, "loss": 1}
    }
}
'''