from Node import Node
from Activity import Activity


class Graph:
    def __init__(self):
        self.nodes_dictionary = dict()
        self.activity_list = list()
        self.parents_dictionary = dict()  # "Parents" of each node
        self.children_dictionary = dict()  # "Children" of each node

    def add_activity(self, name, duration, node_from_name, node_to_name):
        self.add_nodes_to_nodes_dictionary(node_from_name, node_to_name)
        activity_to_add = Activity(name, duration, node_from_name, node_to_name)
        assert activity_to_add, 'could not create an Activity instance'
        updated_activity = self.update_the_activity_nodes_from_nodes_dictionary(activity_to_add, "left")
        assert updated_activity, 'could not update the activity'
        self.activity_list.append(updated_activity)
        self.calculate_activity_left_value_after_addition(activity_to_add)

    def add_nodes_to_nodes_dictionary(self, *args):
        for node_name in args:
            current_node = Node(node_name)
            assert current_node, 'could not create a Node instance'
            if current_node not in self.nodes_dictionary.values():
                self.nodes_dictionary[node_name] = current_node

    def update_the_activity_nodes_from_nodes_dictionary(self, activity_to_add, side_value):  # left or right
        if activity_to_add.node_to in self.nodes_dictionary.values() and activity_to_add.node_from in self.nodes_dictionary.values():
            if side_value == 'left':
                activity_to_add.node_to.left_value = self.nodes_dictionary[activity_to_add.node_to.node_name].left_value
                activity_to_add.node_from.left_value = self.nodes_dictionary[
                    activity_to_add.node_from.node_name].left_value
            else:  # side_value is right:
                activity_to_add.node_to.right_value = self.nodes_dictionary[
                    activity_to_add.node_to.node_name].right_value
                activity_to_add.node_from.right_value = self.nodes_dictionary[
                    activity_to_add.node_from.node_name].right_value
        return activity_to_add

    def calculate_activity_left_value_after_addition(self, activity):
        child_maximal_left_value = max(activity.node_to.left_value,
                                       activity.duration + activity.node_from.left_value)
        self.nodes_dictionary[activity.node_to.node_name].left_value = child_maximal_left_value

    def get_activity(self, node_from_name, node_to_name):
        for activity in self.activity_list:
            if activity.node_from.node_name == node_from_name and activity.node_to.node_name == node_to_name:
                return activity
        return None

    def calculate_all(self):
        self.initiate_infinity_to_right_values(999999)  # which means infinity
        self.assign_right_value_to_isolated_node()
        self.calculate_right_values()

    def initiate_infinity_to_right_values(self, infinity):
        self.update_activities_and_dictionaries()
        for node in self.nodes_dictionary.values():
            self.assign_right_value_to(node.node_name, infinity)

    def update_activities_and_dictionaries(self):
        self.update_activity_list_to_have_same_values_as_nodes_dictionary()
        self.update_parents_dictionary()
        self.update_children_dictionary()

    def update_activity_list_to_have_same_values_as_nodes_dictionary(self):
        for activity in self.activity_list:
            self.update_the_activity_nodes_from_nodes_dictionary(activity, "left")
            self.update_the_activity_nodes_from_nodes_dictionary(activity, "right")

    def update_parents_dictionary(self):
        parents_dictionary = {}
        for node in self.nodes_dictionary.values():
            parents_dictionary[node.node_name] = list()
            for activity in self.activity_list:
                if node.node_name == activity.node_to.node_name:
                    parents_dictionary[node.node_name].append(activity.node_from)
        self.parents_dictionary = parents_dictionary

    def update_children_dictionary(self):
        children_dictionary = {}
        for node in self.nodes_dictionary.values():
            children_dictionary[node.node_name] = list()
            for activity in self.activity_list:
                if node.node_name == activity.node_from.node_name:
                    children_dictionary[node.node_name].append(activity.node_to)
        self.children_dictionary = children_dictionary

    def assign_right_value_to_isolated_node(self):
        isolated_node = self.get_isolated_node()
        assert isolated_node, 'could not find get isolated node'
        self.assign_right_value_to(isolated_node.node_name, isolated_node.left_value)

    def get_isolated_node(self):
        for parent_name in self.children_dictionary.keys():
            if len(self.children_dictionary[parent_name]) == 0:  # which means the list is empty \ has no children
                return self.nodes_dictionary[parent_name]

    def assign_right_value_to(self, parent_name, value):
        self.nodes_dictionary[parent_name].right_value = value

    def calculate_right_values(self):
        self.update_activities_and_dictionaries()
        for iteration in range(len(self.nodes_dictionary)):  # needs to iterate (num of nodes) times to make sure
            # the interesting part actually starts here:
            for parent_name in self.children_dictionary.keys():
                for child in self.children_dictionary[parent_name]:
                    current_activity = self.get_activity(parent_name, child.node_name)
                    assert current_activity, 'could not get current activity'
                    minimal_value = child.right_value - current_activity.duration
                    current_parent_right_value = self.nodes_dictionary[parent_name].right_value
                    minimal_value = min(minimal_value, current_parent_right_value)
                    self.assign_right_value_to(parent_name, minimal_value)
            self.update_activities_and_dictionaries()

    def get_starting_node(self):
        for child_name in self.parents_dictionary.keys():
            if len(self.parents_dictionary[child_name]) == 0:  # which means the list is empty \ has no parents
                return self.nodes_dictionary[child_name]

    def get_critical_path(self):
        critical_path_list = list()
        starting_node = self.get_starting_node()
        assert starting_node, 'could not get the starting node'
        critical_path_list.append(self.get_next_critical_path_activity(starting_node.node_name,
                                                                       self.children_dictionary[
                                                                           starting_node.node_name]))
        for activity in self.activity_list:
            for parent in self.children_dictionary.keys():
                if critical_path_list[-1] is not None and critical_path_list[-1].node_to.node_name \
                        != parent:  # setting the right parent
                    continue
                if parent == activity.node_from.node_name:  # setting the right activity
                    critical_path_list.append(
                        self.get_next_critical_path_activity(parent, self.children_dictionary[parent]))
                    if None not in critical_path_list:
                        break  # which means we added the right one
                    else:
                        critical_path_list.pop(-1)  # pop it and check for the next one
        return critical_path_list

    def get_next_critical_path_activity(self, parent_name, list_of_children):
        list_of_possible_children_tuples = list()
        parent_node = self.nodes_dictionary[parent_name]
        assert parent_node, 'could not get parent Node'
        for child in list_of_children:  # this for loop creates the list_of_possible_children_tuples
            current_activity = self.get_activity(parent_name, child.node_name)
            assert current_activity, 'could not get current activity'
            slack_time_of_current_child = child.right_value - current_activity.duration
            list_of_possible_children_tuples.append((child, slack_time_of_current_child))
        # for example: list_of_possible_children_tuples (for 'D') = [('F',17), ('End', 11), ('E',8), ('C2',13)]
        chosen_tuple = self.get_closest_tuple_to_current_parent_left_value(parent_node.left_value,
                                                                           list_of_possible_children_tuples)
        if chosen_tuple:
            return self.get_activity(parent_name, chosen_tuple[0].node_name)

    def get_closest_tuple_to_current_parent_left_value(self, value, list_of_possible_children_tuples):
        # current_tuple[0] = node, current_tuple[1] = current value
        list_to_check = list()
        min_diff_value = list_of_possible_children_tuples[0][1] - value  # the default will be the first one
        for current_tuple in list_of_possible_children_tuples:
            current_diff = current_tuple[1] - value
            min_diff_value = min(min_diff_value, current_diff)  # getting the min value out of all the tuples
        for current_tuple in list_of_possible_children_tuples:
            if min_diff_value == current_tuple[1] - value:
                list_to_check.append(current_tuple)
        if len(list_to_check) == 1:  # which means there is a single minimal tuple
            return list_to_check[0]

    def get_pert(self):
        # create a dictionary which the critical path names are the keys and 0's are the values
        # or in simpler words - what is the value that I can reduce for each activity duration in order to make the critical path to have the same activities
        pert = dict.fromkeys(list(activity.name for activity in self.get_critical_path() if activity is not None), 0)
        original_critical_path_list = self.get_critical_path()
        assert original_critical_path_list, 'could not get the original critical path'
        activity_was_changed = False
        for activity in self.activity_list:
            if activity.name not in pert.keys():
                continue
            current_critical_path = self.get_critical_path()
            assert current_critical_path, 'could not get the current critical path #1'
            while original_critical_path_list == current_critical_path and activity.duration > 1:
                activity.duration -= 1
                activity_was_changed = True
                pert[activity.name] += 1
                current_critical_path = self.get_critical_path()
                assert current_critical_path, 'could not get the current critical path #2'
            if activity_was_changed:
                activity.duration += pert[activity.name]  # so we don't maintain the change
                pert[activity.name] -= 1
                activity_was_changed = False
        return pert
