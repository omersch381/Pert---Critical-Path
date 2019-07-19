# Pert---Critical-Path
The Pert program (at least this one) is supposed to show how much time can we save
(when we cut some activities' duration), with given different activities and different durations.
Before reviewing the program, I would like to mention a few variables I used:
Activities: were represented (also by) a "node_from" and a "node_to".
The node_from is the direct parent of the node_to in that specific activity.
Parents_dictionary: each key represents a node name and each value represents a list of its parents.
Children_dictionary: each key represents a node name and each value represents a list of its children.
Priority: an activity which it's node_from has to be made before it's Node_to's

The photo that I was working with (and also explains a bit) is this one:

![alt text](https://drive.google.com/open?id=1r4t3BPQ9RSK8PuNOgKk6G7c6bgO5uVex)
