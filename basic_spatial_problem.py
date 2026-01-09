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

    def change_status(self, next_status):
        self.status = next_status
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
        #ta inicjalizacja grida jest slaba xD
        self.grid = np.random.choice([1, 0], size=(N,N), p=[C_prob_start, 1-C_prob_start], replace=True) #1 for C, 0 for D


    """lattice = np.array( [ [Site(i + j) for i in range(3)] for j in range(3) ],
                        dtype=object)
    """



    def get_four_neighbours(self, i, j): #i row, j column
        """ periodic """
        u = Agent([i-1, j]) #,status, next_status, payoff)
        r = Agent([i, (j+1)%self.N])
        d = Agent([(i+1)%self.N, j])
        l = Agent([i, j-1])
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

    def sum_payoffs(self, i, j): #for main agent
        neighbours = get_four_neighbours(i, j)

        


# agent = Agent([2,3], 0, 0, 0.0)
# name = getattr(agent, 'status')
# print(name)

# siatka =  np.random.choice([0, 1], size=(10,10), p=[0.5, 0.5], replace=True)
# print(siatka)