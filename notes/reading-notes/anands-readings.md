## Sergey Levine

https://people.eecs.berkeley.edu/~svlevine/

researcher covering the latest interests in reinforcement learning


## Model-Free Active Exploration in Reinforcement Learning

https://openreview.net/forum?id=YEtstXIpP3
https://openreview.net/pdf?id=YEtstXIpP3

there are two different types of objectives 

- maximising reward during training 
  - Regret minimization
- minimising samples taken until an optimal policy can be found 
  - Best Policy Identification

this paper looked into model free best policy identification (MF-BPI)

lower bound problem = discovering the minimum amount of regret or sample complexity possible 


communicating -> there is a policy between any two given states 

the lower bound problem is hard but this paper introduced an approximation for this lower bound it uses bootstrapping

this approximation is called characteristic time U it is a upper bound of this lower bound and convex.

T is the lower bound these functions take an allocation and find the minimum time time for best policy identification.

an allocation is the distribution of effort across the state space.

they have taken an gods eye view of the problem to find an ideal allocation then looked at how they can find an approximation of tha ideal allocation based upon the information


## what I don't understand yet

what this M measure is? -> statistical moments of the value function
why and how they are using bootstrapping (ensemble methods) 

where the appendix is? 

how exactly are you supposed to learn this allocation 

## My notes


I like this option it pairs nicely with the focus on exploration strategies the project has at the moment and I think it would work well with the value iteration algorithm I could adapt this to measure regret 


my idea the cougar exploration strategy, equal allocation so the agent tries to allways pick the action that is the least explored.

this seams similar to Low-Discrepancy Action Selection (LDAS) but based upon information gain





## A Note on Stability in Asynchronous Stochastic Approximation without Communication Delays


https://arxiv.org/abs/2312.15091

This is about finding optimal solutions for stochastic problems in a asynchronous way. 

this paper extends a proof that this approach will be stable under many different kinds of randomness and still converge

 

## IMPALA

https://arxiv.org/abs/1802.01561

this framework seems so different from my current work it would require substantial changes