from channel import Channel
from ploting import plot_graph
import timeit as tm
import pandas as pd
import numpy as np
import math

p_list = [
    0.000002,
    0.000005,
    0.00001,
    0.00002,
    0.00005,
    0.0001,
    0.0002,
    0.0005,
    0.001,
    0.002,
    0.005,
    0.01,
    0.02,
    0.05,
    0.07,
    0.09,
    0.1,
    0.2,
    0.3,
    0.4,
    0.49,
]


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


def get_prev_states(state):
    return state[1:] + "0", state[1:] + "1"


def get_prox_states(state):
    return "0" + state[0:-1], "1" + state[0:-1]


def get_result(g, s, state):
    b = 0
    for i, bit in enumerate(g):
        if bit == "1":
            if i == 0:
                b = int(s)
            else:
                b = (b + int(state[i - 1])) % 2
    return b


def get_result_v2(g, s, state):
    b = int(s)
    for i in range(1, len(g)):
        b += int(g[i]) * int(state[i - 1])
    return b % 2


def get_edge_cost(received_seq, prev_state, curr_state):
    s = curr_state[0]
    response = ""
    for g in [g1, g2, g3]:
        response += str(get_result_v2(g, s, prev_state))
    hamming_dist = 0
    for i in range(len(received_seq)):
        if received_seq[i] != response[i]:
            hamming_dist += 1
    return hamming_dist


def get_edge_cost_eucli(received_seq, s, curr_state):
    response = []
    for g in [g1, g2, g3]:
        response.append(get_result_v2(g, s, curr_state))
    eucli_dist = 0
    for i in range(len(received_seq)):
        eucli_dist += (received_seq[i] - response[i]) ** 2
    return eucli_dist


def set_next_min_paths(received_seq, distances, predecessors, itr):
    for state in states:
        prev_a, prev_b = get_prev_states(state)
        edge_a = get_edge_cost(received_seq, prev_a, state)
        edge_b = get_edge_cost(received_seq, prev_b, state)
        cost_a = distances[itr][prev_a] + edge_a
        cost_b = distances[itr][prev_b] + edge_b
        if cost_a < cost_b:
            distances[itr + 1][state] = cost_a
            predecessors[itr + 1][state] = prev_a
        elif cost_b < math.inf:
            distances[itr + 1][state] = cost_b
            predecessors[itr + 1][state] = prev_b
        else:
            distances[itr + 1][state] = math.inf
            predecessors[itr + 1][state] = -1


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


def get_expected_msg_from_min_path(distances, predecessors):
    seq = ""
    curr_state = min(distances[15], key=distances[15].get)
    for i in range(15):
        seq = curr_state[0] + seq
        curr_state = predecessors[15 - i][curr_state]
    return seq


def get_expected_msg_from_min_path_euclid(distances, predecessors):
    seq = ""
    curr_state = min(distances[15], key=distances[15].get)
    for i in range(15):
        seq = curr_state[0] + seq
        curr_state = predecessors[15 - i][curr_state]
    return seq


def get_hamming_weight(msg):
    w = 0
    for bit in msg:
        if bit == "1":
            w += 1
    return w


def get_error_probability(p):
    start = tm.default_timer()

    bsc = Channel(p)
    err = 0
    for i in range(445):
        dmins = []
        preds = []
        for k in range(16):
            dmins.append({})
            preds.append({})
        for state in states:
            dmins[0][state] = math.inf
        dmins[0]["0" * m] = 0

        for j in range(15):
            received = "".join(str(x) for x in bsc.transmit([0, 0, 0]))  # '000'
            set_next_min_paths(received, dmins, preds, j)

        msg = get_expected_msg_from_min_path(dmins, preds)
        err += get_hamming_weight(msg)

    prob = err / (445 * 15)
    stop = tm.default_timer()

    return prob, stop - start


def get_error_probability_euclid(p):
    start = tm.default_timer()

    bsc = Channel(p)
    err = 0
    for i in range(445):
        dmins = []
        preds = []
        for k in range(16):
            dmins.append({})
            preds.append({})
            for state in states:
                dmins[k][state] = math.inf
        dmins[0]["0" * m] = 0

        for j in range(15):
            received = bsc.transmit_eucli([0, 0, 0])  # '000'
            set_next_min_paths_eucli(received, dmins, preds, j)

        msg = get_expected_msg_from_min_path_euclid(dmins, preds)
        err += get_hamming_weight(msg)

    prob = err / (445 * 15)
    stop = tm.default_timer()

    return prob, stop - start


def main():
    for p in p_list:
        pe, dt = get_error_probability(p)
        error_probs[m].append(pe)
        exec_times[m].append(dt)
    print(f"Mean execution time (m = {m}): ", np.mean(exec_times[m]))

    for p in p_list:
        pe_euclid, dt_euclid = get_error_probability_euclid(p)
        error_probs["m_euclid"].append(pe_euclid)
        exec_times["m_euclid"].append(dt_euclid)
    print(f"Mean execution time euclid (m = {m}): ", np.mean(exec_times["m_euclid"]))


error_probs = {"none": p_list, 4: [], "m_euclid": []}
exec_times = {4: [], "m_euclid": []}

# error_probs = {"none": p_list, 3: [], 4: [], 6: []}
# exec_times = {3: [], 4: [], 6: []}


""" m = 3
states = generate_binary_strings(m)
g1 = "1011"
g2 = "1101"
g3 = "1111"

main() """

m = 4
states = generate_binary_strings(m)
g1 = "10101"
g2 = "11011"
g3 = "11111"

main()

""" m = 6
states = generate_binary_strings(m)
g1 = "1001111"
g2 = "1010111"
g3 = "1101101"

main() """

df = pd.DataFrame.from_dict(error_probs)
df.to_csv("../lab3/results.csv")
plot_graph(show_fig=False)
