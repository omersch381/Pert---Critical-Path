class Node:
    def __init__(self, name=""):
        self.node_name = name
        self.left_value = 0
        self.right_value = 0

    def __repr__(self):
        return 'Node name: %s, left value: %s, right value: %s' % (self.node_name, self.left_value, self.right_value)

    def __eq__(self, other):
        return self.node_name == other
