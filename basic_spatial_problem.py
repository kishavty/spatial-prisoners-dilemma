import numpy as np
import matplotlib.pyplot as plt

"""
klasa agent
-init: lokalizacja, status C albo D, payoff, nastepny status
-ustaw status w nastepny_status
-zmien status (status=nastepny_status)
-reset payoff

klasa siatka
- init: rozmiar N, prawd agentow C na start, jakie payoffy rtps, 
        -tworzy siatke
        - losuje strategie wg prawd C
- zbierz 4 sasiadow (tu robimy periodic na krawedziach) do listy up down..
- graj z jednym sasiadem (bez zmiany strategii jeszzce)
- oblicz sume payoffy po grze z sasiadami
    reset payoffow, metoda graj z jednym sasiadem dla kazdego, zsumuj payoffy
- najlepsza strategia: kazdy agent wybiera najlepsza strategie wsrod sasiadow do next_strategy
- aktualizacja strategii status=nastepny status
- iteracja: -liczymy sume payoffow, wybieramy strategie, aaktualizacja
- symulacja: iterujemy ile chcemy, mozna historie zapisac
"""

class Agent:
    def __init__(self, localization, status, next_status, payoff):
        self.localization = localization #(i,j)
        self.status = status
        self.next_status = next_status
        self.payoff = payoff
    
    def prepare_next_strategy(self, strategy):
        self.next_status = strategy
        return self.next_status

    def change_status(self):
        self.status = self.next_status
        return self.status
    
    def reset_payoff(self):
        self.payoff = 0.0
        return self.payoff


class Net:
    def __init__(self, N, C_prob_start, R, T, P, S):
        self.N = N
        self.C_prob_start = C_prob_start
        self.R = R
        self.T = T
        self.P = P
        self.S = S
        self.grid = np.empty((N,N), dtype = object)
        # self.grid = np.random.choice([1, 0], size=(N,N), p=[C_prob_start, 1-C_prob_start], replace=True) 
        for i in range(N):
            for j in range(N):
                status = np.random.choice([1, 0], p=[C_prob_start, 1 - C_prob_start], replace=True) #1 for C, 0 for D
                self.grid[i, j] = Agent(localization=(i, j), status=status, next_status=status, payoff=0.0)

    def init_coop_cluster(self): # TODO
        return self.grid

    def get_four_neighbours(self, i, j): #i row, j column
        """ periodic """
        u = self.grid[i-1, j]
        r = self.grid[i, (j+1)% self.N]
        d = self.grid[(i+1)%self.N, j]
        l = self.grid[i, j-1]
        return [u, r, d, l]

    def play_one_time(self, chosen_agent, opponent):  # zwraca payoff dla glownego agenta
        status_chosen = getattr(chosen_agent, "status")
        status_opponent = getattr(opponent, "status")

        # using the matrix input from the article
        if status_chosen == 1 and status_opponent == 1:
            return self.R
        elif status_chosen == 1 and status_opponent == 0:
            return self.S
        elif status_chosen == 0 and status_opponent == 1:
            return self.T
        elif status_chosen == 0 and status_opponent == 0:
            return self.P

    def sum_payoffs(self): #for all 
        """reset payoffow dla main agenta, metoda graj z jednym sasiadem dla kazdego, zsumuj payoffy """
        for i in range(self.N):
            for j in range(self.N):
                chosen_agent = self.grid[i, j]
                chosen_agent.reset_payoff()

                neighbours = self.get_four_neighbours(i, j)
                sum_payoff = 0.0

                for opponent in neighbours:
                    payoff = self.play_one_time(chosen_agent, opponent)
                    sum_payoff += payoff

                chosen_agent.payoff = sum_payoff


    def choose_best_strategy(self):
        """najlepsza strategia: kazdy agent wybiera najlepsza strategie wsrod sasiadow do next_strategy"""
        for i in range(self.N):
            for j in range(self.N):
                neighbours = self.get_four_neighbours(i, j)
                chosen_agent = self.grid[i, j]
                highest_payoff = chosen_agent.payoff
                best_agent = chosen_agent

                for neighbour in neighbours:
                    payoff = getattr(neighbour, "payoff")

                    if payoff > highest_payoff:
                        highest_payoff = payoff
                        best_agent = neighbour

                chosen_agent.prepare_next_strategy(best_agent.status)

    def update_strategies(self):
        """ aktualizacja strategii status=nastepny status"""
        for i in range(self.N):
            for j in range(self.N):
                chosen_agent = self.grid[i, j]
                chosen_agent.change_status()

    def iterate(self):
        """iteracja: -liczymy sume payoffow, wybieramy strategie, aaktualizacja """
        self.sum_payoffs()
        self.choose_best_strategy()
        self.update_strategies()

    def return_statuses(self):
        return np.array([[self.grid[i, j].status for j in range(self.N)] for i in range(self.N)])


    def cooperators_ratio(self):
        """ratio=cooperators (symbol 1) /(n*n)"""
        statuses = self.return_statuses()
        return float(np.mean())

    def simulate(self, time):
        history = []
        retios = []
        for t in range(time):
            history.append(self.return_statuses())
            ratios.append(self.cooperators_ratio())
            self.iterate()
        return history


# net = Net(
#     N=40,
#     C_prob_start=0.0,
#     R=3.0,
#     T=3.5,
#     P=0.5,
#     S=0.0)

# net.init_single_cluster_3x3()
# history = net.simulate(time=50)