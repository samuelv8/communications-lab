from channel import Channel
import timeit as tm
import pandas as pd
import numpy as np
import math


def generate_binary_strings(bit_count):
    binary_strings = []

    def genbin(n, bs=""):
        if len(bs) == n:
            binary_strings.append(bs)
        else:
            genbin(n, bs + "0")
            genbin(n, bs + "1")

    genbin(bit_count)
    return binary_strings


def get_hamming_weight(msg):
    w = 0
    for bit in msg:
        if bit == "0":
            w += 1
    return w


def get_prox_states(state):
    return "0" + state[0:-1], "1" + state[0:-1]


def get_result_v2(g, s, state):
    b = int(s)
    for i in range(1, len(g)):
        b += int(g[i]) * int(state[i - 1])
    return b % 2


def get_edge_cost_eucli(received_seq, s, curr_state):
    response = []
    for g in [g1, g2, g3]:
        response.append(get_result_v2(g, s, curr_state))
    eucli_dist = 0
    for i in range(len(received_seq)):
        eucli_dist += (received_seq[i] - response[i]) ** 2
    return eucli_dist


def get_expected_msg_from_min_path_euclid(distances, predecessors):
    seq = ""
    curr_state = min(distances[15], key=distances[15].get)
    for i in range(14):
        seq = curr_state[0] + seq
        curr_state = predecessors[14 - i][curr_state]
    return seq


def set_next_min_paths_eucli(received_seq, distances, predecessors, itr):
    for state in states:
        if distances[itr][state] != math.inf:
            prox_0, prox_1 = get_prox_states(state)
            edge_0 = get_edge_cost_eucli(received_seq, 0, state)
            edge_1 = get_edge_cost_eucli(received_seq, 1, state)
            cost_0 = distances[itr][state] + edge_0
            cost_1 = distances[itr][state] + edge_1
            if cost_0 < distances[itr + 1][prox_0]:
                distances[itr + 1][prox_0] = cost_0
                predecessors[itr + 1][prox_0] = state
            if cost_1 < distances[itr + 1][prox_1]:
                distances[itr + 1][prox_1] = cost_1
                predecessors[itr + 1][prox_1] = state


def get_error_probability_euclid(rsr):
    start = tm.default_timer()

    bsc = Channel(None, rsr)
    err = 0
    for i in range(2):
        dmins = []
        preds = []
        for k in range(15):
            dmins.append({})
            preds.append({})
            for state in states:
                dmins[k][state] = math.inf
        dmins[0]["0" * m] = 0

        for j in range(15):
            received = bsc.transmit_eucli([1, 1, 1])  # '111'
            print(j)
            set_next_min_paths_eucli(received, dmins, preds, j)
            print(dmins[j])

        msg = get_expected_msg_from_min_path_euclid(dmins, preds)
        err += get_hamming_weight(msg)

    prob = err / (2 * 15)
    stop = tm.default_timer()

    return prob, stop - start


p_list = [
    0.01,
    0.2,
    0.49,
]


def main():

    for p in p_list:
        print(p)
        rnr = -3 * math.log(2 * p)
        pe_euclid, dt_euclid = get_error_probability_euclid(rnr)
        error_probs["m_euclid"].append(pe_euclid)
        print(error_probs["m_euclid"])
        exec_times["m_euclid"].append(dt_euclid)

    print(f"Mean execution time euclid (m = {m}): ", np.mean(exec_times["m_euclid"]))


error_probs = {"m_euclid": []}
exec_times = {"m_euclid": []}

m = 4
states = generate_binary_strings(m)
g1 = "10101"
g2 = "11011"
g3 = "11111"

main()
