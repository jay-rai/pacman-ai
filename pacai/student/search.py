"""
In this file, you will implement generic search algorithms which are called by Pacman agents.
"""

from pacai.util.stack import Stack
from pacai.util.queue import Queue
from pacai.util.priorityQueue import PriorityQueue

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
    #if we break out of this loop we dumb or unsovleable i guess idk
    return []


def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """

    # *** Your Code Here ***
    
    #Okay now we know that our frontier is going to act as a Priority Queue in which we keep track of cost
    frontier = PriorityQueue()
    #here we just are tracking the lowest cost to a state visited
    visited_states = {}

    #initialize the frontier
    frontier.push((problem.startingState(), []), 0)

    while not frontier.isEmpty():
        #get the latest state and path
        current_state, path = frontier.pop()

        #are we at the finish line yeet
        if problem.isGoal(current_state):
            print(f'The best path found was: {path}')
            return path
        
        #get our current cost of getting here
        current_cost = problem.actionsCost(path)
        #if a state visited with cost less or equal to current cost no need to explroe again cause we foudn better path haha 
        if current_state in visited_states and visited_states[current_state] <= current_cost:
            continue
        
        visited_states[current_state] = current_cost

        #for all the successor states, or neighboring states, around our current state
        for successor, action, step_cost in problem.successorStates(current_state):
            new_path = path + [action]
            new_cost = problem.actionsCost(new_path)
            #if state not in visited states or better cost then we need to add it to our frontier
            if successor not in visited_states or new_cost < visited_states[successor]:
                frontier.push((successor, new_path), new_cost)
    #if none of this works or we somehow break or loop i guess idk 
    return []


def aStarSearch(problem, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """

    # *** Your Code Here ***

    #okay given that this is an A* search we need to list (closed, open) in order to keep tracks of evaluated nodes and nodes to explore
    #given that we can make our fronteir our open list that keeps tracks of nodes to explore and evaluated states as the closed list
    frontier = PriorityQueue()
    eval_states = set()

    #okay so within the frontier we need init with the ((starting state, path to state, cost) hueristic estimate)
    frontier.push((problem.startingState(), [], 0), heuristic(problem.startingState(), problem))

    while not frontier.isEmpty():
        #lets keep trakc of the state, path to state, and cost
        current_state, path, cost = frontier.pop()

        #as per normal if goal yeet
        if problem.isGoal(current_state):
            print(f'The final path to win was: {path}')
            return path
        
        if current_state in eval_states:
            continue
        
        eval_states.add(current_state)

        for successor, action, step_cost in problem.successorStates(current_state):
            #where cost is cost and let h be hueristic, given that the f(n) = h(n) + cost(n)
            #get the cost of current state and the step cost to the neighbor, as well as the huersitic value of the measurement and add them
            successor_cost = cost + step_cost
            successor_h = heuristic(successor, problem)
            successor_eval = successor_cost + successor_h

            #if a successor, or neighboring state has a cheaper cost, or has not been discovered yet push that into our PQ
            if not any(successor == eval_states for eval_state in eval_states):
                frontier.push((successor, path + [action], successor_cost), successor_eval)
    return []

            

    raise NotImplementedError()
