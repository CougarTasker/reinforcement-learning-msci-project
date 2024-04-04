describe dynamics implementation trade off with value iteration and sampling

 - choosing to sample than return distribution directly
 - choosing to only model reachable states


epsilon greedy is not ideal with q-learning due to its off policy nature not accounting for random bad actions.

Upper confidence bound gets stuck in good but not optimal