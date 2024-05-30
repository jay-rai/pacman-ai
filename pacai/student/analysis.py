"""
Analysis question.
Change these default values to obtain the specified policies through value iteration.
If any question is not possible, return just the constant NOT_POSSIBLE:
```
return NOT_POSSIBLE
```
"""

NOT_POSSIBLE = None

def question2():
    """
    Reducing the noise level means the action that are chosen by the agent are more likely
    to result in the expected outcome, a higher noise there is a greater probability that
    planned out actions can still result in unintended states.
    """

    answerDiscount = 0.9
    answerNoise = 0.01

    return answerDiscount, answerNoise

def question3a():
    """
    [Enter a description of what you did here.]
    In order to get the closer gate as a target we want to lower the discount rate
    In order to not allow for more prob or random exploration for higher reward we
    lower the noise. We give a negative living reward to also insight the agent to
    take the fasted closest path near the cliff
    """
    answerDiscount = 0.5
    answerNoise = 0.01
    answerLivingReward = -1.0

    return answerDiscount, answerNoise, answerLivingReward

def question3b():
    """
    [Enter a description of what you did here.]
    Now in order to make sure we hit the closer gate and not the further gate we
    lower discount factor and noise Here we actual will give the agent points for
    living, avoiding the cliff
    """
    answerDiscount = 0.2
    answerNoise = 0.09
    answerLivingReward = 0.02

    return answerDiscount, answerNoise, answerLivingReward

def question3c():
    """
    [Enter a description of what you did here.]
    In order to insight taking a riskier path we will give a negative reward
    towards living, so the agent doesnt go up and around.
    In order to incentivise the later gate we increased the discount rate
    form prior questions
    """
    answerDiscount = 0.5
    answerNoise = 0.01
    answerLivingReward = -0.1

    return answerDiscount, answerNoise, answerLivingReward

def question3d():
    """
    Again in this case in order to avoid the cliff we give a
    positive reward for living, and to go up and around
    better discound and stochastic prob noise.
    """
    answerDiscount = 0.8
    answerNoise = 0.5
    answerLivingReward = 0.1

    return answerDiscount, answerNoise, answerLivingReward

def question3e():
    """
    [Enter a description of what you did here.]
    if you dont want to win and just ultimately not die by the cliff just
    value living the most and the discount factor very high
    leave noise down to allow for a more planned path
    """
    answerDiscount = 0.9
    answerNoise = 0.02
    answerLivingReward = 3.5

    return answerDiscount, answerNoise, answerLivingReward

def question6():
    """
    Not possible after hours of hacking at it
    """

    return NOT_POSSIBLE

if __name__ == '__main__':
    questions = [
        question2,
        question3a,
        question3b,
        question3c,
        question3d,
        question3e,
        question6,
    ]

    print('Answers to analysis questions:')
    for question in questions:
        response = question()
        print('    Question %-10s:\t%s' % (question.__name__, str(response)))
