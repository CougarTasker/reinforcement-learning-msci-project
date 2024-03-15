from dataclasses import dataclass

from src.model.dynamics.actions import Action


@dataclass(frozen=True, slots=True)
class TransitionInformation(object):
    """Combine all the transition information in one object."""

    previous_state: int
    previous_action: Action
    new_state: int
    reward: float
