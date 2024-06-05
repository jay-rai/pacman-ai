import time
import random
from pacai.agents.capture.capture import CaptureAgent
from pacai.core.directions import Directions
from pacai.util import util
from collections import Counter

FRONTLINE = 'pacai.student.myTeam.Frontline'
REAR_DEFENSE = 'pacai.student.myTeam.RearDefense'

def createTeam(firstIndex, secondIndex, isRed,
        first = FRONTLINE,
        second = REAR_DEFENSE):
    """
    This function should return a list of two agents that will form the capture team,
    initialized using firstIndex and secondIndex as their agent indexed.
    isRed is True if the red team is being created,
    and will be False if the blue team is being created.
    """
    firstAgent = Frontline
    secondAgent = RearDefense
    return [
        firstAgent(firstIndex),
        secondAgent(secondIndex),
    ]

"""
    Okay so we basically have a frontline and rear of pacman defense and offense
    given that you are frontline we need to eat food and given yo are backline you
    need to defend food

    Like some other ideas and things ive seen i like the idea of creating the base
    actions both sides will need, then getting more specific to each one

    Shared Actions include:
    getting successor states
    evaluating states
    get feature data
    get weights

    Frontline:
        Goal: Collect Food, Avoid Ghost, Collect Power Capusle, Return Safely
        Features: successor, food distance, capsule distance, ghost distance
        nearest enemy maybe, distance back to saftey?
    
    Rear Defense:
        Goal: Portect Food, Beat Up Pacbois, Defend Capsule and other areas
        Features: successor, pacboi distance, dont stop, dont go back!

"""


class Actions:
    
    # Ty githubio for the general actions class idea

    def getSuccessor(self, gameState, action):
        successor = gameState.generateSuccessor(self.index, action)
        pos = successor.getAgentState(self.index).getPosition()
        if pos != util.nearestPoint(pos):
            # Only half a grid position was covered
            return successor.generateSuccessor(self.index, action)
        else:
            return successor

    def evaluate(self, gameState, action):
        features = self.getFeatures(gameState, action)
        weights = self.getWeights(gameState, action)
        return sum(features[feature] * weights[feature] for feature in features)

    def getFeatures(self, gameState, action):
        features = Counter()
        successor = self.getSuccessor(gameState, action)
        features['successorScore'] = self.agent.getScore(successor)
        return features

    def getWeights(self, gameState, action):
        return {'successorScore': 1.0}


class OffensiveActions(Actions):
    def __init__(self, agent, index, gameState):
        self.agent = agent
        self.index = index
        self.agent.distancer.getMazeDistances()
        self.retreatMode = False

        if self.agent.red:
            boundaryLine = (gameState.getInitialLayout().getWidth() - 2) // 2
        else:
            boundaryLine = ((gameState.getInitialLayout().getWidth() - 2) // 2) + 1
        self.boundary = []
        for i in range(1, gameState.getInitialLayout().getHeight() - 1):
            if not gameState.hasWall(boundaryLine, i):
                self.boundary.append((boundaryLine, i))

    def getFeatures(self, gameState, action):
        features = Counter()
        successor = self.getSuccessor(gameState, action)

        # Compute score from successor state
        features['successorScore'] = self.agent.getScore(successor)
        # Get current position of the agent
        currentPos = successor.getAgentState(self.index).getPosition()

        # Compute the distance to the nearest boundary
        boundaryMinDist = min(self.agent.getMazeDistance(currentPos, b) for b in self.boundary)
        features['distanceToBoundary'] = boundaryMinDist

        # Compute distance to the nearest food
        foodList = self.agent.getFood(successor).asList()
        if len(foodList) > 0:
            minFoodDist = min(self.agent.getMazeDistance(currentPos, food) for food in foodList)
            features['distanceToFood'] = minFoodDist

        # Compute distance to the nearest capsule
        capsuleList = self.agent.getCapsules(successor)
        if len(capsuleList) > 0:
            minCapsuleDist = min(self.agent.getMazeDistance(currentPos, c) for c in capsuleList)
            features['distanceToCapsule'] = minCapsuleDist
        else:
            features['distanceToCapsule'] = 0

        # Compute distance to closest ghost
        enemyStates = [successor.getAgentState(i) for i in self.agent.getOpponents(successor)]
        visibleGhosts = [a for a in enemyStates if not a.isPacman() and a.getPosition() is not None]
        if visibleGhosts:
            closestGhost = min(
                visibleGhosts,
                key=lambda a: self.agent.getMazeDistance(currentPos, a.getPosition()))
            closestGhostDist = self.agent.getMazeDistance(currentPos, closestGhost.getPosition())
            if closestGhostDist <= 5:
                features['ghostDistance'] = closestGhostDist
        else:
            probGhostDist = [
                successor.getAgentDistances()[i] for i in self.agent.getOpponents(successor)]
            features['ghostDistance'] = min(probGhostDist)

        return features

    def getWeights(self, gameState, action):
        # If opponent is scared, the agent should not care about ghostDistance
        successor = self.getSuccessor(gameState, action)
        opponents = [successor.getAgentState(i) for i in self.agent.getOpponents(successor)]
        visibleGhosts = [a for a in opponents if not a.isPacman() and a.getPosition() is not None]
        if visibleGhosts:
            for ghost in visibleGhosts:
                if ghost._scaredTimer > 0:
                    if ghost._scaredTimer > 12:
                        return {
                            'successorScore': 110,
                            'distanceToFood': -10,
                            'distanceToEnemyPacman': 0,
                            'ghostDistance': -1,
                            'distanceToCapsule': 0,
                            'distanceToBoundary': 10
                        }

                    elif 6 < ghost._scaredTimer < 12:
                        return {
                            'successorScore': 110,
                            'distanceToFood': -5,
                            'distanceToEnemyPacman': 0,
                            'ghostDistance': -15,
                            'distanceToCapsule': -10,
                            'distanceToBoundary': -5
                        }

                # Visible and not scared
                else:
                    return {
                        'successorScore': 110,
                        'distanceToFood': -10,
                        'distanceToEnemyPacman': 0,
                        'ghostDistance': 20,
                        'distanceToCapsule': -15,
                        'distanceToBoundary': -15
                    }

        return {
            'successorScore': 1000,
            'distanceToFood': -7,
            'ghostDistance': 0,
            'distanceToEnemyPacman': 0,
            'distanceToCapsule': -5,
            'distanceToBoundary': 5
        }

    def chooseAction(self, gameState):
        start = time.time()
        actions = gameState.getLegalActions(self.agent.index)
        actions.remove(Directions.STOP)

        feasibleActions = []
        for a in actions:
            value = self.evaluate(gameState, a)
            feasibleActions.append((value, a))

        bestAction = max(feasibleActions)
        print(f'Eval time for offensive agent {self.agent.index}: {time.time() - start:.4f}')
        return bestAction[1]


class DefensiveActions(Actions):
    # Load the defensive information
    def __init__(self, agent, index, gameState):
        self.index = index
        self.agent = agent
        self.defensePositions = {}

        if self.agent.red:
            middleLine = (gameState.getInitialLayout().getWidth() - 2) // 2
        else:
            middleLine = ((gameState.getInitialLayout().getWidth() - 2) // 2) + 1
        self.boundary = []
        for i in range(1, gameState.getInitialLayout().getHeight() - 1):
            if not gameState.hasWall(middleLine, i):
                self.boundary.append((middleLine, i))

        self.targetPosition = None
        self.lastSeenFood = None
        # Update probabilities to each patrol point.
        self.updateDefenseProbabilities(gameState)

    def updateDefenseProbabilities(self, gameState):
        # This method calculates the minimum distance from our patrol
        # points to our dots.
        total = 0

        for position in self.boundary:
            foodList = self.agent.getFoodYouAreDefending(gameState).asList()
            closestFoodDistance = min(self.agent.getMazeDistance(position, f) for f in foodList)
            if closestFoodDistance == 0:
                closestFoodDistance = 1
            self.defensePositions[position] = 1.0 / float(closestFoodDistance)
            total += self.defensePositions[position]

        # Normalize.
        if total == 0:
            total = 1
        for x in self.defensePositions.keys():
            self.defensePositions[x] = float(self.defensePositions[x]) / float(total)

    def selectPatrolTarget(self):
        maxProb = max(self.defensePositions[x] for x in self.defensePositions.keys())
        bestTargets = [
            x for x in self.defensePositions.keys() if self.defensePositions[x] == maxProb]
        return random.choice(bestTargets)

    def chooseAction(self, gameState):
        defendingFoodList = self.agent.getFoodYouAreDefending(gameState).asList()
        if self.lastSeenFood and len(self.lastSeenFood) != len(defendingFoodList):
            self.updateDefenseProbabilities(gameState)
        currentPosition = gameState.getAgentPosition(self.index)
        if currentPosition == self.targetPosition:
            self.targetPosition = None

        # Visible enemy, keep chasing.
        enemyStates = [gameState.getAgentState(i) for i in self.agent.getOpponents(gameState)]
        visibleInvaders = [a for a in enemyStates if a.isPacman() and a.getPosition() is not None]
        if visibleInvaders:
            closestInvader = min(
                visibleInvaders,
                key=lambda a: self.agent.getMazeDistance(currentPosition, a.getPosition()))
            self.targetPosition = closestInvader.getPosition()
        elif self.lastSeenFood:
            eatenFood = set(
                self.lastSeenFood) - set(
                    self.agent.getFoodYouAreDefending(gameState).asList())
            if eatenFood:
                closestEatenFood = min(
                    eatenFood,
                    key=lambda f: self.agent.getMazeDistance(currentPosition, f))
                self.targetPosition = closestEatenFood

        self.lastSeenFood = self.agent.getFoodYouAreDefending(gameState).asList()

        # We have only a few dots.
        if self.targetPosition is None:
            foodList = self.agent.getFoodYouAreDefending(gameState).asList()
            if len(foodList) <= 4:
                foodAndCapsules = foodList + self.agent.getCapsulesYouAreDefending(gameState)
                self.targetPosition = random.choice(foodAndCapsules)

        # Random patrolling
        if self.targetPosition is None:
            self.targetPosition = self.selectPatrolTarget()

        actions = gameState.getLegalActions(self.index)
        feasibleActions = []
        for a in actions:
            new_state = gameState.generateSuccessor(self.index, a)
            newPosition = new_state.getAgentPosition(self.index)
            if (newPosition and self.targetPosition and not a == Directions.STOP
                    and not new_state.getAgentState(self.index).isPacman()):
                feasibleActions.append(
                    (self.agent.getMazeDistance(newPosition, self.targetPosition), a))

        bestAction = min(feasibleActions) if feasibleActions else (0, Directions.STOP)
        return bestAction[1]


class Frontline(CaptureAgent):
    def __init__(self, index):
        CaptureAgent.__init__(self, index)

    def registerInitialState(self, gameState):
        CaptureAgent.registerInitialState(self, gameState)
        self.defenseActions = DefensiveActions(self, self.index, gameState)
        self.offenseActions = OffensiveActions(self, self.index, gameState)

    def chooseAction(self, gameState):
        self.enemies = self.getOpponents(gameState)
        # invaders = [a for a in self.enemies if gameState.getAgentState(a).isPacman]
        if self.getScore(gameState) >= 13:
            return self.defenseActions.chooseAction(gameState)
        else:
            return self.offenseActions.chooseAction(gameState)


class RearDefense(CaptureAgent):
    def __init__(self, index):
        CaptureAgent.__init__(self, index)

    def registerInitialState(self, gameState):
        CaptureAgent.registerInitialState(self, gameState)
        self.defenseActions = DefensiveActions(self, self.index, gameState)
        self.offenseActions = OffensiveActions(self, self.index, gameState)

    def chooseAction(self, gameState):
        self.enemies = self.getOpponents(gameState)
        # invaders = [a for a in self.enemies if gameState.getAgentState(a).isPacman]
        # numInvaders = len(invaders)

        return self.defenseActions.chooseAction(gameState)
    