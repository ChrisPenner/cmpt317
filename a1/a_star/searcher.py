class Search(object):
    def __init__(self,  transition_function=None, cost_function=None, data_structure=None, goal_state=None, start_state=None, track_states=False):
        """
        Initialize a Search class, injecting the needed methods.

        :transition_function: A function to return possible next states in the form (cost to transition, state)
        :data_structure: The data structure which possible states are added and retrieved from in the desired order.
        """
        if not all([transition_function, cost_function, data_structure, goal_state, start_state]):
            raise TypeError("Search is missing required arguments")
        self.transition_function = transition_function
        self.cost_function = cost_function
        self.data_structure = data_structure
        self.goal_state = goal_state
        self.current_state = start_state
        self.total_cost = 0
        self.track_states = track_states
        if self.track_states:
            self.states = []

    def __call__(self):
        while self.current_state != self.goal_state:
            if self.track_states:
                self.states.append(self.current_state)
            next_states = self.transition_function(self.current_state)
            self.data_structure.extend(next_states)
            past_state = self.current_state
            self.current_state = self.data_structure.next()
            self.total_cost += self.cost_function(past_state, self.current_state)
        if self.track_states:
            self.states.append(self.current_state)

        if self.track_states:
            return self.total_cost, self.states
        else:
            return self.total_cost
