describe dynamics implementation trade off with value iteration and sampling

 - choosing to sample than return distribution directly
 - choosing to only model reachable states


negative initial optimism leads to problems with reflective states

where d and n > 0
x * d - n = x 
x * (d -1) = - n 


x = -n/(1-d)

the pessimism encourage going back to known state and if the value is low enough it can lead to stuck agents 
epsilon greedy is not ideal with q-learning due to its off policy nature not accounting for random bad actions.

Upper confidence bound gets stuck in good but not optimal
