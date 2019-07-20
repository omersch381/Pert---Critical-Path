from Graph import Graph
from Activity import Activity
from Node import Node

if __name__ == '__main__':
    g = Graph()
    g.add_activity("Task1", 4, 'Start', 'A')
    g.add_activity("Task9", 5, 'Start', 'C1')
    g.add_activity("Task5", 6, 'Start', 'B')
    g.add_activity("Priority1", 0, 'A', 'B')
    g.add_activity("Task2", 2, 'B', 'D')  # false
    g.add_activity("Priority3", 0, 'D', 'C2')
    g.add_activity("Priority2", 0, 'D', 'C1')
    g.add_activity("Task3", 2, 'D', 'F')
    g.add_activity("Task8", 5, 'D', 'E')  # false
    g.add_activity("Task10", 8, 'D', 'End')
    g.add_activity("Task6", 4, 'C1', 'C2')
    g.add_activity("Priority5", 0, 'E', 'C2')
    g.add_activity("Priority4", 0, 'F', 'End')
    g.add_activity("Task4", 5, 'E', 'End')
    g.add_activity("Task7", 6, 'C2', 'End')
    g.calculate_all()  # we need that method because in some of the stages there is not critical path / valid pert

    print('isolated node is: ', g.get_isolated_node())
    print('starting node is: ', g.get_starting_node())
    print('nodes list: ', g.nodes_dictionary)
    print('critical path is: ', g.get_critical_path())
    print('pert is: ', g.get_pert())
