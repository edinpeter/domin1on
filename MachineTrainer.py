import copy
import datetime as dt
import logging
import os
import random
import warnings
from collections import Counter
from multiprocessing import Pool

import keras
import numpy as np
from keras.layers import Dense
from keras.models import Sequential, clone_model

from Game import Game
from utils.Player import HumanPlayer, MachinePlayer, Player

warnings.simplefilter(action="ignore", category=FutureWarning)


def clone_network(network):
    mutated_nn = clone_model(network.model)
    print("cloned model...")
    mutated_nn.set_weights(network.get_weights())
    return mutated_nn


def new_network_inf():
    model = Sequential()
    model.add(Dense(24, input_dim=55, activation="relu"))
    # model.add(Dense(8, activation="relu"))
    # model.add(Dense(24, activation="relu"))
    model.add(Dense(24, activation="relu"))
    model.add(Dense(1, activation="sigmoid"))

    model.compile(loss="binary_crossentropy", optimizer="adam")
    model._make_predict_function()

    return (model.get_config(), model.get_weights())


GLOBAL_NETWORKS = new_network_inf()


def new_network_info():
    return copy.deepcopy(GLOBAL_NETWORKS)


def mutate_network_weights(network_weights):
    new_weights = []
    for layer in network_weights:
        if len(layer.shape) == 1:
            new_weights.append(layer)
        else:
            layer_weights = layer
            r = np.random.random(layer_weights.shape)
            r = np.subtract(r, np.ones(r.shape) * 0.5)
            r = r * 0.25
            new_weight_layer = np.add(layer_weights, r)
            new_weights.append(new_weight_layer)
    return new_weights


def mutate_network_info(network_info):
    network_config, network_weights = network_info[0], network_info[1]
    network_weights = mutate_network_weights(network_weights)
    return copy.deepcopy((network_config, network_weights))


def mutate_netset(netset):
    networks = {}
    for name in netset.keys():
        networks[name] = mutate_network_info(netset[name])
    return networks


def save_model_set(networks_config, model_name):
    print("Saving model: %s" % model_name)
    # Iterate over dictionary with kv = {"net_name" : (model_config, model_weights)}
    # Return netset for each network {"net_name" : predict-able_network }
    for network_name in networks_config:
        network_config = networks_config[network_name]
        model = import_model(network_config)
        model.save("%s_%s.h5" % (model_name, network_name))
    return 0


def import_model(model_info):
    config, weights = model_info[0], model_info[1]
    model = Sequential.from_config(config)
    model.set_weights(weights)
    model._make_predict_function()
    return model


class NetSet:
    def __init__(self):
        self.init_networks()

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
            self.networks[network_name] = new_network_info()

    def get_configs(self):
        return self.networks


class MachineTrainer:
    def __init__(self, num_bots=15):
        self.num_bots = num_bots
        self.bots = self.get_initial_bots()
        self.matchups = self.get_matchups()
        pass

    def update_bots(self, winners, new_gen, children_per=9):
        new_bots = {}
        uniq_id = 0
        print(winners)
        for winner in winners:
            winner_name = winner[0]
            new_bots[winner_name] = self.bots[winner_name]
            for i in range(children_per):
                bot_name = "gen-%i-id-%i" % (new_gen, uniq_id)
                # print(self.bots[winner_name])
                new_bots[bot_name] = mutate_netset(self.bots[winner_name])
                uniq_id += 1
        print("New number of bots: %d" % len(new_bots))
        self.bots = new_bots

    def play_game(self, game_info):
        game_num, config1, config2 = game_info[0], game_info[1], game_info[2]
        p1networks, p1name = config1[0], config1[1]
        p2networks, p2name = config2[0], config2[1]
        # print("Starting game")

        g = Game()
        g.add_player(MachinePlayer(p1name, g.supply, p1networks))
        g.add_player(MachinePlayer(p2name, g.supply, p2networks))
        scores = g.play()
        # print("Finished Game #%d, winner: %s" % (game_num, scores))

        return scores

    def get_initial_bots(self):
        bots = {}
        for i in range(self.num_bots):
            bot_name = "gen-%i-id-%i" % (0, i)
            bots[bot_name] = NetSet().get_configs()

        return bots

    def get_matchups(self):
        print("Getting game networks..")
        players = self.bots
        matchups = []
        i = 0
        for p1 in players.keys():
            for p2 in players.keys():
                if p1 is not p2:
                    matchups.append((i, (players[p1], p1), (players[p2], p2)))
                    i += 1
        return matchups

    def parallel_games(self, num_generations=1000):
        game_name = str(dt.datetime.now())
        max_pop, max_tt = 0, 0
        for i in range(1, num_generations):
            print("Getting game networks..")
            print("Got game networks...")
            with Pool(64) as p:
                scores = p.map(self.play_game, self.matchups)
                scores = [scoreset for scoreset in scores if scoreset]
            player_scores = Counter()
            for scoreset in scores:
                player_scores.update(scoreset)
            print(player_scores)
            self.update_bots(player_scores.most_common(4), i, children_per=4)
            self.matchups = self.get_matchups()
            top_tier = player_scores.most_common(5)
            print(top_tier)
            avg_score_pop = sum(player_scores.values()) / len(player_scores)
            avg_score_highest = sum(map(lambda x: x[1], top_tier)) / 5
            max_pop = max(max_pop, avg_score_pop)
            if avg_score_highest > max_tt and i > 10:
                save_model_set(
                    self.bots[top_tier[0][0]], "models/%s_Gen_%i_" % (game_name, i)
                )
            max_tt = max(max_tt, avg_score_highest)
            print("Generation: %i, Pop Max: %i, TT Max: %i" % (i, max_pop, max_tt))
            print("\033[31mPopulation Average score: %d\033[0m" % avg_score_pop)
            print("\033[31mTopTier Average score: %d\033[0m" % avg_score_highest)


if __name__ == "__main__":
    MachineTrainer(10).parallel_games()
