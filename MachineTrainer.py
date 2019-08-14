import logging
import keras
from keras.models import Sequential, clone_model
from keras.layers import Dense
import numpy as np
from Game import Game
from utils.Player import Player, HumanPlayer, MachinePlayer
from multiprocessing import Pool
import multiprocessing
multiprocessing.set_start_method('spawn', force=True)
def clone_network(network):
    mutated_nn = clone_model(network.model)
    print("cloned model...")
    mutated_nn.set_weights(network.get_weights())
    return mutated_nn


def mutate_network(network):
    # https://github.com/keras-team/keras/issues/1765
    print("Cloning model")
    print(network)
    mutated_nn = clone_model(network.model)
    print("cloned model...")
    mutated_nn.set_weights(network.get_weights())

    for layer in mutated_nn.layers:
        print("Updating layer...")
        layer_inf = layer.get_weights()
        layer_weights = layer_inf[0]
        r = np.random.random(layer_weights.shape)
        r = np.subtract(r, np.ones(r.shape) * 0.5)
        r = r * 0.5
        new_weights = np.add(layer_weights, r)
        layer_inf[0] = new_weights
        layer.set_weights(layer_inf)
    mutated_nn._make_predict_function()
    return mutated_nn


def new_network():
    model = Sequential()
    model.add(Dense(8, input_dim=55, activation="relu"))
    model.add(Dense(8, activation="relu"))
    model.add(Dense(8, activation="relu"))
    model.add(Dense(8, activation="relu"))
    model.add(Dense(1, activation="sigmoid"))

    model.compile(loss="binary_crossentropy", optimizer="adam")
    model._make_predict_function()

    return model


class NetSet:
    def __init__(self, existing_netset=None):
        self.networks = {}
        if not existing_netset:
            self.init_networks()
        else:
            self.mutate_from_existing(existing_netset)

    def init_networks(self):
        network_names = [
            "gain",
            "draw_discard",
            "trash",
            "action",
            "buy",
            "discard",
            "discard_number",
        ]
        self.networks = {}
        for network_name in network_names:
            self.networks[network_name] = new_network()

    def mutate_from_existing(self, netset):
        #for network_name in netset.networks:
        #    network = netset.networks[network_name]
        #    print("Cloning network...")
        #    self.networks[network_name] = mutate_network(network)
        print("Got network pointers")
        for network_name in sorted(netset.networks):
            network = netset.networks[network_name]
            self.networks[network_name] = mutate_network(network)

        p = Pool(7)
        networks = list(map(lambda x: netset.networks[x], sorted(netset.networks.keys())))
        print(networks, self.networks.values())
        print(networks)
        p.map(mutate_network, networks)

        p.join()


class MachineTrainer:
    def __init__(self, parallel_networks=50):
        self.parallel_networks = parallel_networks
        self.bots = {}

    def create_bots(self):
        for i in range(self.parallel_networks):
            pass

    def play_parallel(self):
        with Pool(32) as p:
            i = range(100)
            p.map(self.play, i)

    def play(self, game_num):
        ns1, ns2 = NetSet(), NetSet()
        game_num = 0
        for i in range(100):
            #keras.backend.clear_session()
            g = Game()
            g.add_player(MachinePlayer("MACHINE", g.supply, ns1))
            g.add_player(MachinePlayer("MACHINE2", g.supply, ns2))
            winner = g.play()
            print("Finished Game #%d" % game_num)
            if winner == "MACHINE":
                ns2 = NetSet(existing_netset=ns1)
                #print(ns1.networks["gain"].layers[1].get_weights())
                #print(ns2.networks["gain"].layers[1].get_weights())
            elif winner == "MACHINE2":
                ns1 = NetSet(existing_netset=ns2)
            else:
                print("No winner, rematching!")
            game_num += 1

    def play_10(self, game_num):
        for i in range(10):
            g = Game()
            g.add_player(MachinePlayer("MACHINE", g.supply, NetSet()))
            g.add_player(MachinePlayer("MACHINE2", g.supply, NetSet()))
            g.play()


if __name__ == "__main__":
    MachineTrainer().play(1)
