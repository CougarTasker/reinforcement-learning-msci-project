# Reinforcement Learning An Introduction by Richard S. Sutton and Andrew G. Barto

topics: 
 - Markov decision processes
 - policy and value function
   - Finding optimal policies by value iteration and policy iteration
 - Concept of learning as incrementally optimising policy in a MDP
 - Q-learning

## TOC

- [Reinforcement Learning An Introduction by Richard S. Sutton and Andrew G. Barto](#reinforcement-learning-an-introduction-by-richard-s-sutton-and-andrew-g-barto)
  - [TOC](#toc)
  - [Chapter 1](#chapter-1)
  - [Chapter 2](#chapter-2)
    - [exploration strategies](#exploration-strategies)
  - [Chapter 3](#chapter-3)
  - [Chapter 4](#chapter-4)
  - [Chapter 6](#chapter-6)

## Chapter 1

 - reinforcement learning is different from supervised and unsupervised learning because of its goal of maximising a reward signal
 - reinforcement learning has to trade off between trying known successful actions (exploitation) and trying new unknown action (exploration)
 - terms 
   - policy: the agents way of behaving at a given time
   - reward signal: provides the goal for the system (this is provided from outside the agent)
     - on each time step a single number representing the reward is given
     - the agent tries to maximise total reward
   - value function: this is a function that provides the cumulative reward for a given state.
     - this is the long term value compared with the reward signals immediate value
     - this is what we are most concerned with when making decisions
     - although the reward can be directly observed the values must be estimated and re-estimated as new observations are made
   - model: this is something that mimics the environment
     - allows us to make predictions on the outcomes of actions
 -  The use of value functions distinguishes reinforcement learning methods from evolutionary methods that search directly in policy space guided by evaluations of entire policies.

## Chapter 2

we often have formulas like 

$$NewEstimate \leftarrow OldEstimate + StepSize \cdot [Target - OldEstimate]$$

this is an efficient way to update the average (mean) with new observations from time to time.

the step size would be $\frac{1}{\text{number of steps}}$ to be accurate but sometimes when the environment is "non-stationary" this step size might be a constant or other function to give more weight to more recent observations

initial values

these provide a mechanism to provide some initial knowledge if wanted about rewards. with a constant step size this knowledge will stay around as constant but less significant bias

picking over optimistic initial values encourages more exploration at the beginning as the estimates values approach the actual values

### exploration strategies

$\epsilon$-greedy: randomly select actions a small fraction of the time 
Upper Confidence Bound (UCB) slightly favour chose an action that has got the least samples at a given time



## Chapter 3

 - MDPs are a formalisation of sequential decision making

 - terms:
   - the learner and decision maker: agent
   - what the agent interacts with: the environment
     - the agent environment barrier does not necessarily define the barrier of knowledge but is the barrier of where the agent can arbitrary change.
   - finite MDP: the set of states actions and rewards have a finite set of values
   - markov property: The state includes information about all aspects of the past agent–environment interaction that make a difference for the future
   - dynamics: this is defined by the p function. this is the probability distribution of a given new state and reward given the current state and action 
   - episodic: tasks that have an ending as opposed to continuous tasks
     - an episodic task can be made continuous with resetting the rate at the end and providing a penalty
> currently at 3.5 p 79

idea: the reward signal should be for demonstrating what should be archived not how it is supposed to be done.

if you reward sub-goals or anything that is not the primary objective the agent may learn to exploit these "sub-goals" rather than actually learning



## Chapter 4

## Chapter 6

