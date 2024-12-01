import os

def save_citations(scholar, citations):
    with open(f"{os.getcwd()}/data/{scholar}.csv", "w") as file:
        for cit in citations:
            file.write(f"{cit}\n")

def save_network(network):
    with open(f"{os.getcwd()}/data/network.dat", "w") as file:
        for pair in network:
            file.write(f"{pair[0]} {pair[1]}\n")

