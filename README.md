# Pert---Critical-Path
The Pert program (at least this one) is supposed to show how much time can we save
(when we cut some activities' duration), with given different activities and different durations.<br>
Before reviewing the program, I would like to mention a few variables I used:<br>
Left_value: the node's earliest completion time<br>
Right_value: the node's latest completion time<br>
Activities: were represented (also by) a "node_from" and a "node_to".<br>
The node_from is the direct parent of the node_to in that specific activity.<br>
Parents_dictionary: each key represents a node name and each value represents a list of its parents.<br>
Children_dictionary: each key represents a node name and each value represents a list of its children.<br>
Priority: an activity which it's node_from has to be made before it's Node_to's<br><br>

The photo that I was working with (and also explains a bit) is this one:
![][logo]

[logo]: https://github.com/omersch381/Pert---Critical-Path/blob/master/PERT.JPG
