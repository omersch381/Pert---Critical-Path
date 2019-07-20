from Node import Node


class Activity:  # which means edge in our case
    def __init__(self, name, duration, node_from_name, node_to_name):
        self.name = name
        self.duration = duration
        self.node_from = Node(node_from_name)
        self.node_to = Node(node_to_name)

    def __repr__(self):
        return "Activity Name : " + self.name + ", Duration: " + str(
            self.duration) + ", From " + self.node_from.node_name + " To " + \
               self.node_to.node_name
