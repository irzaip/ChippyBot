import queue

# create a priority queue
q = queue.PriorityQueue()

# add items to the priority queue with different priorities
q.put((3345, "item 1"))
q.put((1133, "item 2"))
q.put((2133, "item 3"))

# process items in the priority queue based on their priority
while not q.empty():
    item = q.get()[1]
    print(item)