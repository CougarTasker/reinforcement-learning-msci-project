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
    - [Policy iteration](#policy-iteration)
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


 | strategy                   | description                                                                    |
 | ---------------------------- | ------------------------------------------------------------------------------ |
 | $\epsilon$-greedy            | randomly select actions a small fraction of the time                           |
 | Upper Confidence Bound (UCB) | slightly favour chose an action that has got the least samples at a given time |



## Chapter 3

 - MDPs are a formalisation of sequential decision making

 - terms:
   - the learner and decision maker: **agent**
   - what the agent interacts with: **the environment**
     - the agent environment barrier does not necessarily define the barrier of knowledge but is the barrier of where the agent can arbitrary change.
   - **finite MDP**: the set of states actions and rewards have a finite set of values
   - **markov property**: The state includes information about all aspects of the past agent–environment interaction that make a difference for the future
   - **dynamics**: this is defined by the p function. this is the probability distribution of a given new state and reward given the current state and action 
   - **episodic**: tasks that have an ending as opposed to **continuous** tasks
     - an episodic task can be made continuous with resetting the state at the end and providing a penalty
     - to unify episodic and non episodic terminology
       - we omit the episode number when it is not relevant
       - we consider the end state of the episodic task as an absorbing state of an continuous environment
     - there are three other characterisations
       - *finite-horizon tasks*: in which interaction terminates after a particular fixed number of time steps
       - *indefinite-horizon tasks*: in which interaction can last arbitrarily long but must eventually terminate
       - *infinite-horizon tasks*: in which interaction does not terminate
   - **Value function**: this describes how desirable it is for an agent to be in a given state
   - **Policy**: this is a mapping from states to the possibility of picking different actions
   - **Bellman optimality equation**: expresses the fact that the value of a state under an optimal policy must equal the expected return for the best action from that state


idea: the reward signal should be for demonstrating what should be archived not how it is supposed to be done.

if you reward sub-goals or anything that is not the primary objective the agent may learn to exploit these "sub-goals" rather than actually learning


the value function defines an ordering over the possible policies, this means there are one or more policies that are as good if not better than the rest. we denote this best policy (even if there are multiple) $\pi_*$. all of these optimal policies share the same optimal action value function $v_*$. this function gives the expected return for taking action a in states s if we follow an optimal policy

> **self-consistency condition given by the Bellman equation**
>
> the bellman equation shows the value of a state is equal to the immediate reward you get in that state, plus the expected value of all future rewards you will receive as you follow the optimal policy from that state. this means that the value of each state must be consistent with all of the states that it can lead onto 


if the dynamics function $p$ is known you can solve a system of simultaneous equations to compute the optimal-value function $v_*$ and with some non-linear methods you can solve $q_*$ 

a greedy one step approach over $v_*$ or even $q_*$ is actually optimal because of how $v_*$ and $q_*$ encode the future value, however calculating this is not practical in many cases. for example the computational or memory constraints. However for many cases an approximation will suffice perhaps some of the state space is very unlikely to be visited so the optimal behaviour there will have a very little impact on cumulative reward
  
## Chapter 4

policy evaluation: finding the state-value function $v$ for a given policy

> **iterative policy evaluation**: 
>   the value of state s is picked arbitrarily to begin with, after each observation $k$ the the value is updated with the reward and the discounted value of the next state. 
> This is shown to converge to the $v_\pi$ as $k \rightarrow \infty$


### Policy iteration

A reason to compute the state-value function is to compute better policies, but how do we do this

with the state value function $v()$ we know the value of a given state under a given action
what happens if we consider a different action in some state but then go back to the original, we may observe a higher reward, 
 - if this is the case then then under the markov principle it would always be better to pick this action, 
   - therefore a new policy that picks this action instead would be better 
   - this idea in general is called **policy improvement theorem**

$$q_\pi(s,\pi'(s)) \ge v_\pi(s) \implies \pi' \ge \pi$$


if you apply this theorem greedily by comparing all actions for a state under this above relation then you have **policy improvement**

if this greedy improved policy is as good but not better than the original then the polices are all optimal


policy iteration is this policy improvement process applied to all states, after each round of policy improvement we compute a new value function under this new policy, that itself can be used for the next policy iteration

> note: when computing each new value function we start with the one from the previous policy, as it shouldn't have changed much this speeds up computation substantially

because a finite MDP only has a finite number of policies this process must converge on an optimal policy in a finite time

we know a policy has converged when it doesn't change after a policy improvement step

page 104 section 4.4

## Chapter 6

