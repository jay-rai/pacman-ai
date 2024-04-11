"""
In this file, you will implement generic search algorithms which are called by Pacman agents.
"""

from pacai.util.stack import Stack
from pacai.util.queue import Queue

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first [p 85].

    Your search algorithm needs to return a list of actions that reaches the goal.
    Make sure to implement a graph search algorithm [Fig. 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    ```
    print("Start: %s" % (str(problem.startingState())))
    print("Is the start a goal?: %s" % (problem.isGoal(problem.startingState())))
    print("Start's successors: %s" % (problem.successorStates(problem.startingState())))
    ```
    """

    # *** Your Code Here ***
    
    #frontier is stack cause DFS, we need to keep track of our visited states
    frontier = Stack()
    visited_states = set()
    #we need to intialize our stack with where we start and then for now an empty array we can use to track the path we took to get there
    frontier.push((problem.startingState(), []))

    #DFS Loop
    while not frontier.isEmpty():
        #check the most recent in current state, last one pushed in LIFO
        current_state, path = frontier.pop()

        #If the state has not been visited, if its not in our set of visited states add it dummy
        if current_state not in visited_states:
            visited_states.add(current_state)
        
            #if the current state is the goal state yeet
            if problem.isGoal(current_state):
                print(f'The final path to the food was: {path}')
                return path

            #okay so successorStates returns some list of possible next states
            #pacboi makes an action so we get back the succesor state itself, the action taken i.e 'North' 'South' and cost of action which i dont think we care for so _
            for successor, action, _ in problem.successorStates(current_state):
                if successor not in visited_states:
                    #add successor to stack and path to get there
                    frontier.push((successor, path + [action]))
        else:
            #no path was found so idk
            return []

    raise NotImplementedError()

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first. [p 81]
    """
    # *** Your Code Here ***

    #This time our frontier will be a Queue since BFS
    frontier = Queue()
    visited_states = set()

    #Now we load the frontier with our starting state
    frontier.push((problem.startingState(), []))

    #BFS Loop
    while not frontier.isEmpty():
        current_state, path = frontier.pop()

        #check if we got the goal yeet
        if problem.isGoal(current_state):
            print(f'The final pathway to the food is: {path}')
            return path
        
        #if visited skip otherwise gtfo
        if current_state in visited_states:
            continue
        
        #add to our set of visited states
        visited_states.add(current_state)

        #exploration time, look at successor states and if its not in our visited states push it into our frontier 
        for successor, action, _ in problem.successorStates(current_state):
            if successor not in visited_states:
                frontier.push((successor, path + [action]))
    #if we break out of this loop we dumb or not sovleable i guess idk
    return []






    raise NotImplementedError()

def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """

    # *** Your Code Here ***
    raise NotImplementedError()

def aStarSearch(problem, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """

    # *** Your Code Here ***
    raise NotImplementedError()
