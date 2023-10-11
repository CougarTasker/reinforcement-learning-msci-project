# Research notes

Reinforcement Learning is the overarching concept of an agent learning to make decisions through interaction with an environment.
Markov Decision Process (MDP) provides a formal framework for modeling such decision-making scenarios.
The Bellman Equation is a crucial equation in RL that expresses how an agent evaluates the quality of its decisions by considering immediate and future rewards.
Q-learning is a specific algorithm within RL that uses the Bellman equation to learn the best actions to take in each state of an MDP.

## concepts

### Reinforcement Learning (RL):

Definition: Reinforcement Learning is a type of machine learning where an agent learns to make decisions by interacting with an environment.
Key Idea: The agent takes actions to maximize a reward signal it receives from the environment.

Important notes:

- **Unlike other MDP's in RL the agent does not have perfect knowledge of the state and reward functions**
  - this means no background knowledge of the task
  - delayed reward: the reward is not known until the action is made
- the agent influences the distribution of training examples by the action sequence it chooses. which experimentation strategy produces most effective learning? The tradeoff in choosing whether to favor exploration of unknown states and actions (to gather new information), or exploitation of states and actions that it has already learned will yield high reward (to maximize its cumulative reward)
- Partially observations, the agent may not observe the entire state with its sensors, may need to include previous sensor data to get a fuller picture

### Markov Decision Process (MDP):

Definition: MDP is a mathematical framework used to model decision-making problems in RL.
Key Idea: MDP describes how an agent interacts with an environment through states, actions, rewards, and transition probabilities. It assumes the Markov property, meaning the future depends only on the current state and action.

Notes: 

- if you can know the reward or state function,the optimal action can be considered the action that would maximise the value of the reward and the discounted future reward from the resultant state
  - this is the same as the perfect domain knowledge scenario so would not be reinforcement learning but exploration based learning
  - for many practical problems this is not possible

### Bellman Equation:

Definition: The Bellman Equation is a fundamental equation in RL that relates the value of being in a certain state to the expected cumulative rewards the agent can obtain from that state onward.
Key Idea: It breaks down the total expected reward into the immediate reward plus the expected future rewards from the next state. There are two versions: the state-value Bellman equation (V) and the action-value Bellman equation (Q).

Notes: 

  - V function:
    - this returns the cumulative reward that will be received from one starting state under a certain policy. return value from this function is called the discounted cumulative reward
  - Q function: 
    - this returns the cumulative reward that will be received from one starting state and action under a certain policy
    - if you can learn this function you can produce optimal actions

### Q-learning:

Definition: Q-learning is a specific RL algorithm used to learn the action-value function (Q-function) in an MDP.
Key Idea: Q-learning iteratively updates Q-values based on the Bellman equation. It helps the agent learn the best action to take in each state to maximize its cumulative rewards.

Notes:

- The agent makes a Hypothesis of the Q function this is a table that covers all combinations of state action pairs
  - this can be impossible in some many cases and instead Q-learning needs to be paired with another learning technique such as Neural-networks with back propagation
- the policy is a function that maps the current state (as perceived by the agents sensors) to an action
- the optimal policy for a initial state is one that creates the greatest cumulative reward for the robot over time -> denoted $\pi$
  - this is weighted in favour of recent rewards by a factor $\gamma$ because in many cases it is preferable to receive rewards sooner rather than later called the discounted reward
  - this discourages waiting or doing stuff that doesn't get rewarded before doing the right action
 - how to learn the Q function?
    - one key insight is that the Q function can be defined recursively in terms of itself and the reward and state functions -> no need to know the V function
    - to represent a learners estimate of the Q function a table is constructed for each pair of action and state combinations
      - to start these values can be random
    - the agent can then pick actions, with the realised reward and state value updating the table to get better more accurate values
    - this algorithm in the limit approximates the q function
  - different exploration strategies
    - you could chose actions that always have the highest recorded Q value but you might miss unexplored actions with an even higher Q values
      - this fails on the convergent theorem
  - Updating strategies: the reward for an action propagates backwards from the actions that lead up to it, if we update the q-values forwards this slows down the convergence as it takes more iterations forwards for the information to travel backwards
    - if we instead store the actions and replay them backwards once a reward is reached then we can converge quicker
  - non-determinism:
    - the reward and state functions return a probability distribution. this means the V function needs to be adapted as the cumulative expected reward
    - the Q function is updated in mostly the same way however previous values need to be discounted by a value $\alpha_{n}$
  - The Q learning algorithm works by reducing the discrepancies between estimates made at different times
    - so far this has been done with one step lookahead (13.5) it can be done with more steps of lookahead
    - Sutton describes a general process of blending different levels of lookahead into one Q estimate

## ideas

[extension: car](https://gymnasium.farama.org/environments/box2d/car_racing/)

## sources

 - Chapter on reinforcement Learning in 'Machine Learning' by Tom Mitchell
 - Reinforcement Learning An Introduction by Richard S. Sutton and Andrew G. Barto
   - page: 24
   - only read up to chaper 8: max 