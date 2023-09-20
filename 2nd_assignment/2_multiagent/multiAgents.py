# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random
import util

from game import Agent


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (exercise 1)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getPossibleActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateNextState(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWinningState():
        Returns whether or not the game state is a winning state

        gameState.isLosingState():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def miniMax(gameState, depth):
        
            def maxValue(gameState, depth):
                if gameState.isWinningState() or gameState.isLosingState() or depth == self.depth:             ###The trvial situations(state)
                    return(self.evaluationFunction(gameState), None)
                
                v = float("-inf")                                                                                ###We are trying to implement the 2 sides of the minimax algorithm the max and the min
                act = None
            
                actions = gameState.getPossibleActions(0)

                for action in actions:                                                                          ###In that way that the 2 functions are calling each other is like building the tree(diagrams from tha class)
                    succVal = minValue(gameState.generateNextState(0, action), 1, depth)                          #We have the available moves and we are seeking for the "best" one
                    succVal = succVal[0]                                                                      #It is working exactly as the theory of minimax algorithm commands

                    if v < succVal:                                                                            #Here we have as start -infinite
                        v = succVal
                        act = action

                return (v, act)
            

            def minValue(gameState, agentIndex, depth):
                if not gameState.getPossibleActions(agentIndex):
                    return(self.evaluationFunction(gameState), None)
                
                v = float("inf")                                                                                  ###As we see in contrast with max we begin from +infinte
                act = None

                actions = gameState.getPossibleActions(agentIndex)

                for action in actions:

                    if agentIndex == (gameState.getNumAgents() - 1):
                        succVal = maxValue(gameState.generateNextState(agentIndex, action), depth + 1)
                    else:
                        succVal = minValue(gameState.generateNextState(agentIndex, action), agentIndex + 1, depth)        ###We are doing exactly the opposite from the max "function"

                    succVal = succVal[0]

                    if v > succVal:
                        v = succVal
                        act = action

                return (v, act)
            
            miniMax = maxValue(gameState, depth)[1]
            return miniMax

        return miniMax(gameState, 0)

        util.raiseNotDefined()


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (exercise 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def alphaBeta(gameState, depth, a, b):

            def max_value(gameState, depth, a, b):
                if gameState.isWinningState() or gameState.isLosingState() or depth == self.depth:
                    return (self.evaluationFunction(gameState), None)

                v = (float("-inf"))                                                                             ###We can see that the alpha beta agent is almost the same as the minimax with the difference
                act = None                                                                                       ###We can see that the alpha beta agent is almost the same as the minimax with the difference
                                                                                                                ###that now we have the pruning if w>a or w<b in the 2 "edges"
                actions = gameState.getPossibleActions(0) # Get actions of pacman
                
                for action in actions:
                    succVal = min_value(gameState.generateNextState(0, action), 1, depth, a, b)
                    succVal = succVal[0]

                    if v < succVal:
                        v = succVal
                        act = action

                    if v > b:
                        return (v, act)
                    
                    a = max(a, v)

                return (v, act)

            def min_value(gameState, agentIndex, depth, a, b):
                if not gameState.getPossibleActions(agentIndex):
                        return(self.evaluationFunction(gameState), None)    
                                                                                                                
                v = float("inf")
                act = None

                actions = gameState.getPossibleActions(agentIndex) # Get the actions of the ghost

                for action in actions:

                    if agentIndex == (gameState.getNumAgents() - 1):
                        succVal = max_value(gameState.generateNextState(agentIndex, action), depth + 1, a, b)
                    else:
                        succVal = min_value(gameState.generateNextState(agentIndex, action), agentIndex + 1, depth, a, b)
                    
                    succVal = succVal[0]

                    if v > succVal:
                        v = succVal
                        act = action

                    if v < a:
                        return (v, act)

                    b = min(b, v)

                return(v, act)                                                                                      ###I think there is nothing else to be said about this agent

            
            alphaBeta = max_value(gameState, 0, a, b)[1]
            return alphaBeta
        
        a = float("-inf")
        b = float("inf")
        return alphaBeta(gameState, 0, a, b)    
    
        util.raiseNotDefined()


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (exercise 3)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def expectiMax(gameState, depth):

            def maxValue(gameState, depth):
                    if gameState.isWinningState() or gameState.isLosingState() or depth == self.depth:             ###The trvial situations(state)
                        return(self.evaluationFunction(gameState), None)
                    
                    v = float("-inf")                                                                                ###We are trying to implement the 2 sides of the minimax algorithm the max and the min
                    act = None
                
                    actions = gameState.getPossibleActions(0)

                    for action in actions:                                                                          ###In that way that the 2 functions are calling each other is like building the tree(diagrams from tha class)
                        succVal = expValue(gameState.generateNextState(0, action), 1, depth)                          #We have the available moves and we are seeking for the "best" one
                        succVal = succVal[0]                                                                      #It is working exactly as the theory of minimax algorithm commands

                        if v < succVal:                                                                            #Here we have as start -infinite
                            v = succVal
                            act = action

                    return (v, act)
            
            def expValue(gameState, agentIndex, depth):
                    if not gameState.getPossibleActions(agentIndex):
                        return(self.evaluationFunction(gameState), None)
                    
                    v = 0                                                                                  ###As we see in contrast with max we begin from +infinte
                    act = None

                    actions = gameState.getPossibleActions(agentIndex)

                    for action in actions:

                        if agentIndex == (gameState.getNumAgents() - 1):
                            succVal = maxValue(gameState.generateNextState(agentIndex, action), depth + 1)
                        else:
                            succVal = expValue(gameState.generateNextState(agentIndex, action), agentIndex + 1, depth)        ###We are doing exactly the opposite from the max "function"

                        succVal = succVal[0]
                        prob = succVal / len(actions)
                        v += prob

                    return (v, act)

            expectiMax = maxValue(gameState, 0)[1]
            return expectiMax    
        
        return expectiMax(gameState, 0)
    
        util.raiseNotDefined()


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (exercise 4).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pacmanPos = currentGameState.getPacmanPosition()
    foodList = currentGameState.getFood().asList()
    ghostStates = currentGameState.getGhostStates()

    # Calculate distance to the nearest food pellet
    if len(foodList) > 0:
        foodDistances = [manhattanDistance(pacmanPos, food) for food in foodList]
        nearestFood = min(foodDistances)
    else:
        nearestFood = 0

    # Calculate distance to the nearest ghost
    ghostDistances = [manhattanDistance(pacmanPos, ghost.getPosition()) for ghost in ghostStates]
    nearestGhost = min(ghostDistances)

    # Calculate evaluation function based on the above factors
    evaluation = 2 * currentGameState.getScore() - 10 * nearestFood - 100 * nearestGhost - 100 * len(foodList)

    return evaluation

    util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction