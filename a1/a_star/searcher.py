class Searcher(object):
    """
    Searcher ties together components of a search and actually performs it.
    """
    def __init__(self,  transition_function=None, cost_function=None, data_structure=None, start_state=None, goal_state=None, track_states=False):
        """
        Inject the necessary functions for searching
        Note that whichever object is used for tracking State, that it must be
        comparable to other states using '=='

        :transition_function: A function that returns an iterable of possible next states
        :cost_function: A function to return the cost of going from one state to another
        :data_structure: The data structure which possible states are added and retrieved from in the desired order.
        :start_state: The state we start in
        :goal_state: The state we wish to achieve
        """
        if not all([transition_function, cost_function, data_structure, goal_state, start_state]):
            raise TypeError("Searcher is missing required arguments")

        self.transition_function = transition_function
        self.cost_function = cost_function
        self.data_structure = data_structure
        self.data_structure.add(start_state)
        self.goal_state = goal_state
        self.total_cost = 0
        self.track_states = track_states
        if self.track_states:
            self.states = [start_state]

    def __call__(self):
        """
        Run the actual Search
        """
        self.current_state = self.data_structure.next()
        while self.current_state != self.goal_state:
            # Get all possible next states
            next_states = self.transition_function(self.current_state)
            # Add all possible next states to our data_structure
            self.data_structure.extend(next_states)
            past_state = self.current_state
            # Transition states
            self.current_state = self.data_structure.next()
            # Track total cost so far
            self.total_cost += self.cost_function(past_state, self.current_state)
            # Keep our path to victory
            if self.track_states:
                self.states.append(self.current_state)

        if self.track_states:
            return self.total_cost, self.states
        else:
            return self.total_cost
