Rajarshi Chattopadhyay - rxc170010@utdallas.edu
AI CS6364- Homework 2

Problems Solved:
- Programming assignment for Problem 1: A and B

Files:
1) gen_tree.py: generates the game tree
2) output.txt: writes output of gen_tree.py
3) gen_tree_minimax.py: generates the game tree with minimax values
4) output_minimax.txt: writes output of gen_tree_minimax.py

Programming language: Python3
Development Environment: Unix

Code operation:
1) `python3 gen_tree.py`
2) `python3 gen_tree_minimax.py`

Description:
We track which players have won
Initial state/node of the game is set
We store all generated nodes/states of the game
We count the number of turn levels covered
There is option for the nodes states to be printed or the game state to be visualised
Output can be written to a file
There are functions to/for
- get current position of a player
- moves
- Determines if the made move is a legal move
- Get list of all possible actions
- Taking the action
- Check if a player won
- Find the winner
- Check if the game has ended
- Check if a state repeats
- Print/Draw the game state
- Check utility value of node
- Compute min/max values
- Compute minimax to determine next action
At each turn
- Check if game end
- Check moves available for 1
- Check for stagnation (no moves available for 1)
- for all moves available for 1
    - move 1
    - check if repeated state
    - save the state
    - Check if game end
- Repeat for players 2, 3, 4
After turn of Player 4, the state is appended to the queue of ply states.
Level is incremented after covering 4 plies in each turn.
The generation of nodes is repeated starting from each states from the ply states queue.
We print the following:
- Number of levels covered
- Number of nodes generated
- Number of winning states for each player

Special considerations:
For the minimax calculation, a depth of 6 has been used to compute bounded minimax values.
The best value along with the best action is printed for all the non repeating nodes.