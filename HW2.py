class Node:
    def __init__(self, name=""):
        self.node_name = name
        self.left_value = 0
        self.right_value = 0

    def __repr__(self):
        return 'Node name: %s, left value: %s, right value: %s' % (self.node_name, self.left_value, self.right_value)

    def __eq__(self, other):
        return self.node_name == other


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


class Graph:
    def __init__(self):
        self.activity_list = list()
        self.nodes_list = list()
        self.parents_dictionary = dict()  # "Parents" of each node
        self.sons_dictionary = dict()  # "Sons" of each node

    def add_activity(self, name, duration, node_from_name, node_to_name):
        self.add_nodes_to_nodes_list(node_from_name, node_to_name)
        activity_to_add = Activity(name, duration, node_from_name, node_to_name)
        self.update_activity_nodes(activity_to_add)
        self.activity_list.append(activity_to_add)
        self.calculate_left_value_after_addition(activity_to_add)

    def add_nodes_to_nodes_list(self, *args):
        for node_name in args:
            current_node = Node(node_name)
            if current_node not in self.nodes_list:
                self.nodes_list.append(current_node)

    def update_activity_nodes(self, activity_to_add):
        if activity_to_add.node_to in self.nodes_list:
            for node in self.nodes_list:
                if activity_to_add.node_to.node_name == node.node_name:
                    activity_to_add.node_to.left_value = node.left_value
        if activity_to_add.node_from in self.nodes_list:
            for node in self.nodes_list:
                if activity_to_add.node_from.node_name == node.node_name:
                    activity_to_add.node_from.left_value = node.left_value

    def print_all_activities(self):
        for activity in self.activity_list:
            print(activity)

    def get_isolated_node(self):
        isolated_node_name = ""
        for node_name in self.sons_dictionary.keys():
            if len(self.sons_dictionary[node_name]) == 0:  # which means the list is empty
                isolated_node_name = node_name
        for node in self.nodes_list:
            if isolated_node_name == node.node_name:
                return node

    def get_starting_node(self):
        starting_node_name = ""
        for node_name in self.parents_dictionary.keys():
            if len(self.parents_dictionary[node_name]) == 0:  # which means the list is empty
                starting_node_name = node_name
        for node in self.nodes_list:
            if starting_node_name == node.node_name:
                return node

    def get_activity(self, node_from_name, node_to_name):
        for activity in self.activity_list:
            if activity.node_from.node_name == node_from_name and activity.node_to.node_name == node_to_name:
                return activity
        return None

    def get_node(self, node_name):
        for node in self.nodes_list:
            if node.node_name == node_name:
                return node
        return None

    def calculate_left_value_after_addition(self, activity):
        son_maximal_left_value = max(activity.node_to.left_value,
                                     activity.duration + activity.node_from.left_value)
        for node in self.nodes_list:
            if node.node_name == activity.node_to.node_name:
                node.left_value = son_maximal_left_value

    def calculate_all(self):
        self.update_activities_and_dictionaries()
        self.initiate_infinity_to_right_values(999999)
        self.assign_right_value_to_isolated_node()
        self.update_activities_and_dictionaries()
        self.calculate_right_values()

    def assign_right_value_to_isolated_node(self):
        isolated_node = self.get_isolated_node()
        isolated_node_left_value = isolated_node.left_value
        for node in self.nodes_list:
            if node.node_name == isolated_node.node_name:
                node.right_value = isolated_node_left_value

    def initiate_infinity_to_right_values(self, num):
        for node in self.nodes_list:
            node.right_value = num

    def calculate_right_values(self):
        for i in range(len(self.nodes_list)):  # the maximum iteration times will be the num of nodes
            for parent_name in self.sons_dictionary.keys():
                for son in self.sons_dictionary[parent_name]:
                    minimal_value = son.right_value - self.get_activity(parent_name, son.node_name).duration
                    current_parent_right_value = self.get_node(parent_name).right_value
                    if minimal_value > current_parent_right_value:
                        minimal_value = current_parent_right_value
                    self.assign_right_value_to(parent_name, minimal_value)
            self.update_activities_and_dictionaries()

    def assign_right_value_to(self, parent_name, value):
        for node in self.nodes_list:
            if node.node_name == parent_name:
                node.right_value = value

    def update_activities_and_dictionaries(self):
        self.update_activity_list()
        self.update_parents_dictionary()
        self.update_sons_dictionary()

    def update_activity_list(self):
        for activity in self.activity_list:
            for node in self.nodes_list:
                if activity.node_from == node:
                    activity.node_from.left_value = node.left_value
                    activity.node_from.right_value = node.right_value
                if activity.node_to == node:
                    activity.node_to.left_value = node.left_value
                    activity.node_to.right_value = node.right_value

    def update_sons_dictionary(self):
        sons_dictionary = {}
        for node in self.nodes_list:
            sons_dictionary[node.node_name] = list()
            for activity in self.activity_list:
                self.update_activity_nodes(activity)
                if node.node_name == activity.node_from.node_name:
                    sons_dictionary[node.node_name].append(activity.node_to)
        self.sons_dictionary = sons_dictionary

    def update_parents_dictionary(self):
        parents_dictionary = {}
        for node in self.nodes_list:
            parents_dictionary[node.node_name] = list()
            for activity in self.activity_list:
                if node.node_name == activity.node_to.node_name:
                    parents_dictionary[node.node_name].append(activity.node_from)
        self.parents_dictionary = parents_dictionary

    def get_critical_path(self):
        reversed_critical_path_list = list()
        reversed_critical_path_list.append(self.get_isolated_node())
        for current_node in reversed_critical_path_list:
            for activity in self.activity_list:
                if activity.node_to.node_name == current_node.node_name and activity.node_to.right_value - \
                        activity.duration == activity.node_from.left_value:
                    reversed_critical_path_list.append(activity.node_from)
                    break
        return list(reversed(reversed_critical_path_list))


g = Graph()
g.add_activity("Task1", 4, 'Start', 'A')
g.add_activity("Task9", 5, 'Start', 'C1')
g.add_activity("Task5", 6, 'Start', 'B')
g.add_activity("Priority1", 0, 'A', 'B')
g.add_activity("Task2", 2, 'B', 'D')
g.add_activity("Priority3", 0, 'D', 'C2')
g.add_activity("Priority2", 0, 'D', 'C1')
g.add_activity("Task3", 2, 'D', 'F')
g.add_activity("Task8", 5, 'D', 'E')
g.add_activity("Task10", 8, 'D', 'End')
g.add_activity("Task6", 4, 'C1', 'C2')
g.add_activity("Priority5", 0, 'E', 'C2')
g.add_activity("Priority4", 0, 'F', 'End')
g.add_activity("Task4", 5, 'E', 'End')
g.add_activity("Task7", 6, 'C2', 'End')
g.calculate_all()
print('isolated node is: ', g.get_isolated_node())
print('starting node is: ', g.get_starting_node())
print(g.nodes_list)
print(g.get_critical_path())
