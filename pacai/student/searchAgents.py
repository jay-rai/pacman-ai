"""
This file contains incomplete versions of some agents that can be selected to control Pacman.
You will complete their implementations.

Good luck and happy searching!
"""

import logging

from pacai.core.actions import Actions
from pacai.core.search import heuristic
from pacai.core.search.position import PositionSearchProblem
from pacai.core.search.problem import SearchProblem
from pacai.agents.base import BaseAgent
from pacai.agents.search.base import SearchAgent
from pacai.core.directions import Directions
from pacai.core.search.heuristic import numFood
from pacai.core.search.heuristic import distance

class CornersProblem(SearchProblem):
    """
    This search problem finds paths through all four corners of a layout.

    You must select a suitable state space and successor function.
    See the `pacai.core.search.position.PositionSearchProblem` class for an example of
    a working SearchProblem.

    Additional methods to implement:

    `pacai.core.search.problem.SearchProblem.startingState`:
    Returns the start state (in your search space,
    NOT a `pacai.core.gamestate.AbstractGameState`).

    `pacai.core.search.problem.SearchProblem.isGoal`:
    Returns whether this search state is a goal state of the problem.

    `pacai.core.search.problem.SearchProblem.successorStates`:
    Returns successor states, the actions they require, and a cost of 1.
    The following code snippet may prove useful:
    ```
        successors = []

        for action in Directions.CARDINAL:
            x, y = currentPosition
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            hitsWall = self.walls[nextx][nexty]

            if (not hitsWall):
                # Construct the successor.

        return successors
    ```
    """

    def __init__(self, startingGameState):
        super().__init__()

        self.walls = startingGameState.getWalls()
        self.startingPosition = startingGameState.getPacmanPosition()
        top = self.walls.getHeight() - 2
        right = self.walls.getWidth() - 2

        self.corners = ((1, 1), (1, top), (right, 1), (right, top))
        for corner in self.corners:
            if not startingGameState.hasFood(*corner):
                logging.warning('Warning: no food in corner ' + str(corner))

        # *** Your Code Here ***
        self.nodes_visited = 0
        # raise NotImplementedError()

    def actionsCost(self, actions):
        """
        Returns the cost of a particular sequence of actions.
        If those actions include an illegal move, return 999999.
        This is implemented for you.
        """

        if (actions is None):
            return 999999

        x, y = self.startingPosition
        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999

        return len(actions)
    
    ''' 
    Given to us by the comments we are told we need to 
    implment the startingState for the corners problem
    '''
    def startingState(self):
        # we can set a starting pos for our true pos and whether we have touched each corner
        starting_position = (self.startingPosition, (
            self.startingPosition == self.corners[0],
            self.startingPosition == self.corners[1],
            self.startingPosition == self.corners[2], 
            self.startingPosition == self.corners[3]
            ))
        return starting_position
    
    # We also need to define our successor states with some given code
    def successorStates(self, state):
        successors = []
        current_position, visited = state
        #given loop
        for action in Directions.CARDINAL:
            x, y = current_position
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            # if the nextx and next y is not a wall
            if not self.walls[nextx][nexty]:
                # append the new state with position and updated status of corners
                successors.append((
                        ((nextx, nexty), (
                        ((nextx, nexty) == self.corners[0]) or state[1][0],
                        ((nextx, nexty) == self.corners[1]) or state[1][1],
                        ((nextx, nexty) == self.corners[2]) or state[1][2],
                        ((nextx, nexty) == self.corners[3]) or state[1][3])),
                        action, 1))
        self.nodes_visited += 1
        return successors

    # We also need to define our completed goal state, if all corner true
    def isGoal(self, state):
        goal_state = state[1][0] and state[1][1] and state[1][2] and state[1][3]
        return goal_state
        

def cornersHeuristic(state, problem):
    """
    A heuristic for the CornersProblem that you defined.

    This function should always return a number that is a lower bound
    on the shortest path from the state to a goal of the problem;
    i.e. it should be admissible.
    (You need not worry about consistency for this heuristic to receive full credit.)
    """

    # Useful information.
    # corners = problem.corners  # These are the corner coordinates
    # walls = problem.walls  # These are the walls of the maze, as a Grid.

    # *** Your Code Here ***
    # lets try to do the manhattan distance but the stupid pacai core search one not working

    corners = problem.corners
    manh_dist = [0, 0, 0, 0]
    for corner in range(4):
        manh_dist[corner] = (abs(state[0][0] - corners[corner][0]) + 
                             abs(state[0][1] - corners[corner][1])) * (not state[1][corner])
    manh_dist.sort()
    return manh_dist[3]
    # return min(manhattan(position, corner) for corner in unvisited)
    # return heuristic.null(state, problem)  # Default to trivial solution

def foodHeuristic(state, problem):
    """
    Your heuristic for the FoodSearchProblem goes here.

    This heuristic must be consistent to ensure correctness.
    First, try to come up with an admissible heuristic;
    almost all admissible heuristics will be consistent as well.

    If using A* ever finds a solution that is worse than what uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!
    On the other hand, inadmissible or inconsistent heuristics may find optimal solutions,
    so be careful.

    The state is a tuple (pacmanPosition, foodGrid) where foodGrid is a
    `pacai.core.grid.Grid` of either True or False.
    You can call `foodGrid.asList()` to get a list of food coordinates instead.

    If you want access to info like walls, capsules, etc., you can query the problem.
    For example, `problem.walls` gives you a Grid of where the walls are.

    If you want to *store* information to be reused in other calls to the heuristic,
    there is a dictionary called problem.heuristicInfo that you can use.
    For example, if you only want to count the walls once and store that value, try:
    ```
    problem.heuristicInfo['wallCount'] = problem.walls.count()
    ```
    Subsequent calls to this heuristic can access problem.heuristicInfo['wallCount'].
    """

    # *** Your Code Here ***
    position, foodGrid = state
    foods = foodGrid.asList()

    # reach goal state, no more food to eat
    if len(foods) == 0:
        return 0

    food_left = []
    result = 0

    for food in foods:
        food_left.append(food)

    # Since current state has eaten all foods, heuristics is 0
    if not food_left:
        return 0

    # one food left so eat it
    if len(food_left) == 1:
        return distance.manhattan(position, food_left[0])

    closest_food_distance = float('inf')

    # manhattan from current pso to closest corner
    for food in food_left:
        current_distance = distance.manhattan(position, food)
        if current_distance < closest_food_distance:
            closest_food_distance = current_distance

    # min sum of distance between unvisited food
    # if found manhattan between next and current closest food
    closest_food = food_left[0]
    while food_left:
        next_closest_food = food_left[0]
        next_min_distance = float('inf')

        for foods in food_left:
            current_distance = distance.manhattan(closest_food, foods)
            if current_distance < next_min_distance:
                next_min_distance = current_distance
                next_closest_food = foods

        closest_food = next_closest_food
        result += next_min_distance
        food_left.remove(next_closest_food)

    return closest_food_distance + result
    

    


class ClosestDotSearchAgent(SearchAgent):
    """
    Search for all food using a sequence of searches.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)
        

    def registerInitialState(self, state):
        self._actions = []
        self._actionIndex = 0

        currentState = state

        while (currentState.getFood().count() > 0):
            nextPathSegment = self.findPathToClosestDot(currentState)  # The missing piece
            self._actions += nextPathSegment

            for action in nextPathSegment:
                legal = currentState.getLegalActions()
                if action not in legal:
                    raise Exception('findPathToClosestDot returned an illegal move: %s!\n%s' %
                            (str(action), str(currentState)))

                currentState = currentState.generateSuccessor(0, action)

        logging.info('Path found with cost %d.' % len(self._actions))

    def findPathToClosestDot(self, gameState):
        """
        Returns a path (a list of actions) to the closest dot, starting from gameState.
        """

        # Here are some useful elements of the startState
        # startPosition = gameState.getPacmanPosition()
        # food = gameState.getFood()
        # walls = gameState.getWalls()
        problem = AnyFoodSearchProblem(gameState)

        # *** Your Code Here ***
        from pacai.student.search import breadthFirstSearch
        path = breadthFirstSearch(problem)
        
        return path

class AnyFoodSearchProblem(PositionSearchProblem):
    """
    A search problem for finding a path to any food.

    This search problem is just like the PositionSearchProblem,
    but has a different goal test, which you need to fill in below.
    The state space and successor function do not need to be changed.

    The class definition above, `AnyFoodSearchProblem(PositionSearchProblem)`,
    inherits the methods of `pacai.core.search.position.PositionSearchProblem`.

    You can use this search problem to help you fill in
    the `ClosestDotSearchAgent.findPathToClosestDot` method.

    Additional methods to implement:

    `pacai.core.search.position.PositionSearchProblem.isGoal`:
    The state is Pacman's position.
    Fill this in with a goal test that will complete the problem definition.
    """

    def __init__(self, gameState, start = None):
        super().__init__(gameState, goal = None, start = start)

        # Store the food for later reference.
        self.food = gameState.getFood()

    def isGoal(self, state):
        return self.food[state[0]][state[1]]

class ApproximateSearchAgent(BaseAgent):
    """
    Implement your contest entry here.

    Additional methods to implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Get a `pacai.bin.pacman.PacmanGameState`
    and return a `pacai.core.directions.Directions`.

    `pacai.agents.base.BaseAgent.registerInitialState`:
    This method is called before any moves are made.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)
        self.actions = []
        self.actionIndex = 0
    
    def registerInitialState(self, state):
        
        from pacai.student.search import uniformCostSearch

        current_state = state

        # While there are still foods left on the board
        while current_state.getFood().count() > 0:
            # Create a problem instance to find the closest food
            problem = AnyFoodSearchProblem(current_state)

            # find closest food via bfs
            closest_food_path = uniformCostSearch(problem)

            # add path to total actions taken
            self.actions.extend(closest_food_path)

            # for each action update state based on cloest food search
            for action in closest_food_path:
                legal = current_state.getLegalActions()
                if action not in legal:
                    raise Exception("Illegal action generated by UCS.")
                current_state = current_state.generateSuccessor(0, action)

    def getAction(self, state):
        if self.actionIndex < len(self.actions):
            action = self.actions[self.actionIndex]
            self.actionIndex += 1
            return action
        else:
            return Directions.STOP
    
    
