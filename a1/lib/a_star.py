class Search(object):
    def __init__(self,  transition_function=None, h_function=None, data_structure=None, goal_state=None, start_state=None):
        """
        Initialize a Search class, injecting the needed methods.

        :transition_function: A function to return possible next states.
        :h_function: the heuristic function to be called on each possible state.
        :data_structure: The data structure which possible states are added and retrieved from
        """
        if not all([transition_function, h_function, data_structure, goal_state, start_state]):
            raise TypeError("Search is missing required arguments")
