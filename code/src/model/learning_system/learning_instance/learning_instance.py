from src.model.learning_system.base_entity_decorator import BaseEntityDecorator
from src.model.transition_information import TransitionInformation


class LearningInstance(BaseEntityDecorator):
    """An instance of an agent interacting with the environment."""

    def get_current_state(self) -> int:
        """Get the current state ID.

        Returns:
            int: the current state ID
        """
        current_state = self.statistics.get_statistics().current_state
        if current_state is not None:
            return current_state
        return self.dynamics.initial_state_id()

    def reset_state(self) -> int:
        """Reset the current state to the initial state.

        Returns:
            int: the initial state id
        """
        initial_state_id = self.dynamics.initial_state_id()
        self.statistics.set_current_state(initial_state_id)
        return initial_state_id

    def perform_action(
        self,
    ) -> TransitionInformation:
        """Perform one action chosen by the agent.

        Returns:
            TransitionInformation: the transition information, the last
            state, the action chosen, the next state, the reward received for
            this action.
        """
        last_state = self.get_current_state()
        agent = self.agent
        action = agent.evaluate_policy(last_state)
        next_state, reward = self.dynamics.next_state_id(last_state, action)

        transition = TransitionInformation(
            last_state, action, next_state, reward
        )
        agent.record_transition(transition)
        self.statistics.record_transition(transition)
        return transition
