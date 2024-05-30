import random
from collections import Counter
from pacai.agents.capture.capture import CaptureAgent
from pacai.core.distanceCalculator import Distancer
from pacai.util import util
from pacai.core.directions import Directions

class DummyAgent(CaptureAgent):
    """
    A Dummy agent to serve as an example of the necessary agent structure.
    You should look at `pacai.core.baselineTeam` for more details about how to create an agent.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def registerInitialState(self, gameState):
        """
        This method handles the initial setup of the agent and populates useful fields,
        such as the team the agent is on and the `pacai.core.distanceCalculator.Distancer`.

        IMPORTANT: If this method runs for more than 15 seconds, your agent will time out.
        """

        super().registerInitialState(gameState)

        # Your initialization code goes here, if you need any.
        self.start = gameState.getAgentState(self.index).getPosition()
        self.distancer = Distancer(gameState.getInitialLayout())
        self.distancer.getMazeDistances()

    def chooseAction(self, gameState):
        """
        Randomly pick an action.
        """

        actions = gameState.getLegalActions(self.index)
        return random.choice(actions)