import random

from pacai.agents.base import BaseAgent
from pacai.agents.search.multiagent import MultiAgentSearchAgent
from pacai.core.search.heuristic import distance
from pacai.core.directions import Directions
from pacai.core.gamestate import AbstractGameState
from pacai.agents.search.multiagent import MultiAgentSearchAgent

class ReflexAgent(BaseAgent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.
    You are welcome to change it in any way you see fit,
    so long as you don't touch the method headers.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        `ReflexAgent.getAction` chooses among the best options according to the evaluation function.

        Just like in the previous project, this method takes a
        `pacai.core.gamestate.AbstractGameState` and returns some value from
        `pacai.core.directions.Directions`.
        """

        # Collect legal moves.
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions.
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best.

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current `pacai.bin.pacman.PacmanGameState`
        and an action, and returns a number, where higher numbers are better.
        Make sure to understand the range of different values before you combine them
        in your evaluation function.
        """

        successorGameState = currentGameState.generatePacmanSuccessor(action)

        # Useful information you can extract.
        newPosition = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        # oldFood = currentGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        # newScaredTimes = [ghostState.getScaredTimer() for ghostState in newGhostStates]

        # *** Your Code Here ***
        #okay pacboi primary goal eat all the food
        foodDist = [distance.manhattan(newPosition, food) for food in newFood.asList()]
        if foodDist:
            minFoodDist = min(foodDist)
            recip = 1/minFoodDist
        else:
            #avoid /0
            recip = 0

        #okay is pacboi close to ghost, if so gtfo
        badPacman = 0
        for ghostState in newGhostStates:
            if distance.manhattan(newPosition, ghostState.getPosition()) < 2:
                #pacboi too close to ghost gtfo, increase badPacman penalty
                badPacman = -float('inf')
                break
        
        #combine all scores
        return successorGameState.getScore() + recip + badPacman

class MinimaxAgent(MultiAgentSearchAgent):
    """
    A minimax agent.

    Here are some method calls that might be useful when implementing minimax.

    `pacai.core.gamestate.AbstractGameState.getNumAgents()`:
    Get the total number of agents in the game

    `pacai.core.gamestate.AbstractGameState.getLegalActions`:
    Returns a list of legal actions for an agent.
    Pacman is always at index 0, and ghosts are >= 1.

    `pacai.core.gamestate.AbstractGameState.generateSuccessor`:
    Get the successor game state after an agent takes an action.

    `pacai.core.directions.Directions.STOP`:
    The stop direction, which is always legal, but you may not want to include in your search.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the minimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    #okay first method of implmentation getting action
    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.treeDepth
        and self.evaluationFunction.
        """
        # idk rando values for our variables
        bestAction = Directions.STOP
        bestScore = float('-inf')

        # get legal actions for pacboi
        for action in gameState.getLegalActions(0):
            if action != Directions.STOP:
                # okay get successor states for the action
                successor = gameState.generateSuccessor(0, action)
                # minValue starting with the first ghost, index 1
                score = self.minValue(successor, 1, 0)

                # if the score of this action is better
                if score > bestScore:
                    bestScore = score
                    bestAction = action

        return bestAction

    def minValue(self, gameState, agentIndex, depth):
        # did we hit max depth
        if gameState.isWin() or gameState.isLose() or depth == self.getTreeDepth():
            return self.getEvaluationFunction()(gameState)

        # min so start with highest val
        minScore = float('inf')

        # for every action ghost can take
        for action in gameState.getLegalActions(agentIndex):
            if action != Directions.STOP:
                # get ghost successor states for each ghost
                successor = gameState.generateSuccessor(agentIndex, action)
                # does depth need to be increases
                nextAgent = agentIndex + 1
                if nextAgent >= gameState.getNumAgents():
                    #go to pacboi agnet
                    nextAgent = 0
                    nextDepth = depth + 1
                else:
                    nextDepth = depth

                # recursive score calc
                if nextAgent == 0:
                    score = self.maxValue(successor, nextDepth)
                else:
                    score = self.minValue(successor, nextAgent, nextDepth)

                # Update the minimum score found
                minScore = min(minScore, score)

        return minScore

    def maxValue(self, gameState, depth):
        # Check for terminal state or maximum depth reached
        if gameState.isWin() or gameState.isLose() or depth == self.getTreeDepth():
            return self.getEvaluationFunction()(gameState)

        # Initialize the maximum value very low
        maxScore = float('-inf')

        # Loop through all legal actions for Pacman
        for action in gameState.getLegalActions(0):
            if action != Directions.STOP:
                # Generate successor state for the action
                successor = gameState.generateSuccessor(0, action)
                # Calculate the score recursively
                score = self.minValue(successor, 1, depth)  # First ghost's turn (Min)
                # Update the maximum score found
                maxScore = max(maxScore, score)

        return maxScore
        

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    A minimax agent with alpha-beta pruning.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the minimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    #code didnt work dont push


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    An expectimax agent.

    All ghosts should be modeled as choosing uniformly at random from their legal moves.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the expectimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)
    
def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable evaluation function.

    DESCRIPTION: <write something here so we know what you did>
    """

    return currentGameState.getScore()

class ContestAgent(MultiAgentSearchAgent):
    """
    Your agent for the mini-contest.

    You can use any method you want and search to any depth you want.
    Just remember that the mini-contest is timed, so you have to trade off speed and computation.

    Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
    just make a beeline straight towards Pacman (or away if they're scared!)

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)
