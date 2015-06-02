#!/usr/bin/env python
import sys


def read_input(filename):
    with open(filename, 'r') as f:
        cases = []

        # Read company info N, C, D
        company_info = f.readline().strip().split(' ')
        while company_info != ['0', '0', '0']:
            # initialize a case
            company_machines = CompanyMachines(*company_info)
            # add list of machine info
            for i in range(company_machines.N):
                machine_info = f.readline().strip().split(' ')
                company_machines.machines.append(Machine(*machine_info))
            # after all machines read, add this to the case
            cases.append(company_machines)
            # initialize new case
            company_info = f.readline().strip().split(' ')

    return cases


class Node(object):
    """Make each buy and sell option into a node"""
    # Example Tree of Nodes
    #                           Initial
    #                        buy /   \ stay
    # day 1              outcome1     outcome2
    #                buy / \ stay    buy / \ stay
    # day 3       outcome3 outcome4 outcome5 outcome6
    #
    # CompanyMachines.max_profit() will find best of last day outcomes after day D

    def __init__(self):
        self.buy = None
        self.stay = None

        self.curr_machine = None
        self.curr_dollars = 0

        self.node_day = None


class Machine(object):
    """Each machine has 4 attributes"""

    def __init__(self, di, pi, ri, gi):
        self.di = int(di)  # day for sale
        self.pi = int(pi)  # price
        self.ri = int(ri)  # resale value
        self.gi = int(gi)  # generated daily profit


class CompanyMachines(object):

    def __init__(self, N, C, D):
        self.N = int(N)  # number of machines
        self.C = int(C)  # company dollars
        self.D = int(D)  # days of restructure
        self.machines = []

    def max_profit(self):
        """Determine the max profit of buying/selling machines"""
        # sort machine list by day available with insertion sort
        for m_index in range(self.N):
            curr = m_index
            while curr > 0 and \
                    self.machines[curr - 1].di > \
                    self.machines[curr].di:
                # swap order of machines
                self.machines[curr - 1], self.machines[curr] = \
                    self.machines[curr], self.machines[curr - 1]
                curr -= 1

        # initialize a tree with buy and stay options
        outcome_tree = Node()
        outcome_tree.curr_machine = None  # just to be  explicit
        outcome_tree.curr_dollars = self.C
        outcome_tree.node_day = 0

        # for each day, add value to profits whether buy or sell as a tree
        curr_row = [outcome_tree, ]

        # only need to check paths on day machines are avail.
        for machine in self.machines:
            next_row = []

            for outcome_tree in curr_row:

                outcome_tree.buy = Node()
                outcome_tree.stay = Node()
                outcome_tree.buy.node_day = machine.di
                outcome_tree.stay.node_day = machine.di

                # buy branch #
                # do you already own a machine to sell?
                sell_for = 0
                profit = 0
                if outcome_tree.curr_machine:
                    sell_for = outcome_tree.curr_machine.ri
                    # calc profit since last day calculated:
                    profit = outcome_tree.curr_machine.gi * \
                                    (machine.di - outcome_tree.node_day - 1)

                # buy if you have enough
                if machine.pi <= (outcome_tree.curr_dollars + profit + sell_for):
                    # profit from owning last machine
                    outcome_tree.buy.curr_dollars = \
                                outcome_tree.curr_dollars + \
                                profit + \
                                sell_for + \
                                - machine.pi

                    outcome_tree.buy.curr_machine = machine

                    next_row.append(outcome_tree.buy)

                # stay branch #
                outcome_tree.stay.curr_machine = outcome_tree.curr_machine

                try:
                    outcome_tree.stay.curr_dollars = \
                            outcome_tree.curr_dollars + \
                            outcome_tree.curr_machine.gi * \
                            (machine.di - outcome_tree.node_day)
                except AttributeError:
                    outcome_tree.stay.curr_dollars = outcome_tree.curr_dollars
                next_row.append(outcome_tree.stay)

            curr_row = next_row

        # find most profitable outcome
        max_outcome = 0
        for outcome in curr_row:
            # sell current machine & calc profit
            try:
                final = outcome.curr_dollars + \
                        outcome.curr_machine.gi * \
                        (self.D - outcome.node_day) + \
                        outcome.curr_machine.ri
            # will get an AttributeError if no machine owned.
            except AttributeError:
                final = outcome.curr_dollars
            if final > max_outcome:
                max_outcome = final

        return max_outcome


if __name__ == '__main__':
    cases = read_input(sys.argv[1])
    count = 1
    for case in cases:
        print 'Case %i: %i' % (count, case.max_profit())
        count += 1
