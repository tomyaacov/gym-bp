from collections import deque
from importlib import import_module
from inspect import getmembers, isfunction, isclass
from z3 import *
import gym_bp.envs.global_variables as gv


class Bprogram:

    def __init__(self):
        self.scenarios = None
        self.tickets = []
        self.variables = None
        #self.event_selection_strategy = event_selection_strategy
        #self.listener = listener
        #self.external_events = deque()

    def setup(self, source_name):
        self.scenarios = [o[1]() for o in getmembers(import_module(source_name)) if isfunction(o[1]) and o[1].__module__ == source_name]
        self.variables = dict([o for o in getmembers(import_module(source_name)) if isinstance(o[1], ExprRef) or isinstance(o[1], list)])
        self.tickets = []
        for sc in self.scenarios:
            ticket = next(sc)  # Run the scenario to its first yield and collect the ticket
            ticket['sc'] = sc  # Maintain a pointer to the scenario in the ticket
            self.tickets.append(ticket)  # Add the ticket to the list of tickets
        self.trigger_next_state()

    def trigger_next_state(self):
        # Compute a disjunction of may constraints and a conjunction of must constraints
        (may, must) = (True, True)  # TODO: change may back to false
        for ticket in self.tickets:
            if 'may' in ticket:
                may = Or(may, ticket['may'])
            if 'must' in ticket:
                must = And(must, ticket['must'])
        # adding action assignment
        if gv.action:
            must = And(must, self.variables['action'] == gv.action)
        # Compute a satisfying assignment and break if it does not exist
        sl = Solver()
        sl.add(And(may, must))
        if sl.check() == sat:
            gv.m = sl.model()
            #print(gv.m)
            return False
        else:
            return True

    def trigger_action(self, action):
        gv.action = action
        # Reset the list of tickets before rebuilding it
        old_tickets = self.tickets
        self.tickets = []
        # Run the scenarios to their next yield and collect new tickets
        for oldTicket in old_tickets:
            # Check whether the scenario waited for the computed assignment
            if 'wait-for' in oldTicket and is_true(gv.m.eval(oldTicket['wait-for'])):
                # Run the scenario to the next yield and collect its new ticket
                new_ticket = next(oldTicket['sc'], 'ended')
                # Add the new ticket to the list of tickets (if the scenario didn't end)
                if not new_ticket == 'ended':
                    new_ticket['sc'] = oldTicket['sc']  # Copy the pointer to the scenario
                    self.tickets.append(new_ticket)
            else:
                # Copy the old tickets to the new list
                self.tickets.append(oldTicket)





