# Final Year Project (MSci): Reinforcement Learning

The repository for holding all of the code and related documentation for my Msci final year project

supervisor : Anand Subramoney anand.subramoney@rhul.ac.uk


links:

 - [submissions](https://moodle.royalholloway.ac.uk/course/view.php?id=2125#section-0)
 - [project booklet](https://moodle.royalholloway.ac.uk/course/view.php?id=2125&section=2)

## [project description](https://projects.cs.rhul.ac.uk/List2023.php?PROJECT-TYPE=MSci)

**Aims**: 
To understand reinforcement learning (RL) and implement RL for some simple scenarios

**Background**: 
Reinforcement Learning (RL) is the branch of machine learning in which an agent learns to perform sequences of actions in response to rewards and punishments. There is growing evidence that some animal learning uses essentially these algorithms: within the brain, rewards seem to be represented by dopamine surges.
In this project, you will understand the basic formalisation of RL as finding an optimal policy in a Markov Decision Process. This theory is nice, and not quite as complicated as it sounds (although there is a lot to learn). You will need to understand policy optimisation by dynamic programming, and the Bellman equation. This is widely applicable computational maths (not just in RL), and is good to know.

You will implement a demonstration of RL with a GUI as a MVC (model view controller) design pattern, and you will perform some experiments to determine the efficiency of the learning.

Early Deliverables:
 - Proof of concept program: Implementation of exact policy optimisation by value iteration for a general MDP.
 - Proof of concept program: Implementation of Q-learning for grid world.
 - Proof of concept program: GUI built with buttons etc.,
 - Proof of concept program: MVC program with with controls.
 - Report on Markov decision processes (MDPs)
 - Report on notions of policy and value function; optimal policy/value function via the Bellman equation. Finding optimal policies by value iteration and policy iteration
 - Report on Concept of learning as incrementally optimising policy in a MDP
 - Report on Q-learning

Final Deliverables:
 - The program must have a full object-oriented design, with a full implementation life cycle using modern software engineering principles
 - The program will at least demonstrate Q-learning with various exploration strategies in a simple world.
 - The program must have a text based control file from which it can be configured.
 - The program will have a Graphical User Interface that can be used to animate simulations.
 - The report will describe the software engineering process involved in generating your software.
 - The report will include a description of the theory of MDPs, optimal policies and value functions via the Bellman equation, dynamic programming methods of finding optimal policies, and Q-learning.
 - The report will include some experiments that compare the effects of different parameter choices on the progress of Q-learning: over-optimistic values causing excessive exploration, and pessimistic initial values causing the development of superstitions.

Suggested Extensions:
 - Implementing RL for more a more challenging problem than a grid world, such as an acrobat.
 - Experimental analysis of the performance of different learning algorithms is interesting but challenging

Reading:
 - Chapter on Reinforcement Learning in 'Machine Learning' by Tom Mitchell

Prerequisites:
 This project is already challenging. The maths is not complicated - but you will find it new, and you really will have to understand it properly. You would find it helpful to take the third year courses in Computational Optimisation and also in Machine Learning, but this is not essential.
