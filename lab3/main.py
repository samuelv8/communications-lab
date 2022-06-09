from channel import Channel
from ploting import plot_graph
import timeit as tm
import pandas as pd
import math

p_list = [
    0.000002, 0.000005, 0.00001, 0.00002, 0.00005, 0.0001, 0.0002, 0.0005,
    0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5
]


def generate_binary_strings(bit_count):
    binary_strings = []

    def genbin(n, bs=''):
        if len(bs) == n:
            binary_strings.append(bs)
        else:
            genbin(n, bs + '0')
            genbin(n, bs + '1')

    genbin(bit_count)
    return binary_strings


def get_prev_states(state):
    return state[1:] + '0', state[1:] + '1'


def get_result(g, s, state):
    b = 0
    for i, bit in enumerate(g):
        if bit == '1':
            if i == 0:
                b = int(s)
            else:
                b = (b + int(state[i - 1])) % 2
    return b


def get_edge_cost(received_seq, prev_state, curr_state):
    s = curr_state[0]
    response = ''
    for g in [g1, g2, g3]:
        response += str(get_result(g, s, prev_state))
    hamming_dist = 0
    for i in range(len(received_seq)):
        if received_seq[i] != response[i]:
            hamming_dist += 1
    return hamming_dist


def set_next_min_paths(received_seq, distances, predecessors, itr):
    for state in states:
        prev_a, prev_b = get_prev_states(state)
        edge_a = get_edge_cost(received_seq, prev_a, state)
        edge_b = get_edge_cost(received_seq, prev_b, state)
        cost_a = distances[itr][prev_a] + edge_a
        cost_b = distances[itr][prev_b] + edge_b
        if (cost_a < cost_b):
            distances[itr + 1][state] = cost_a
            predecessors[itr + 1][state] = prev_a
        elif (cost_b < math.inf):
            distances[itr + 1][state] = cost_b
            predecessors[itr + 1][state] = prev_b
        else:
            distances[itr + 1][state] = math.inf
            predecessors[itr + 1][state] = -1


def get_expected_msg_from_min_path(distances, predecessors):
    seq = ''
    curr_state = min(distances[15], key=distances[15].get)
    for i in range(15):
        seq += curr_state[0]
        curr_state = predecessors[i][curr_state]
    return seq[::-1]


def get_hamming_weight(msg):
    w = 0
    for bit in msg:
        if bit == '1':
            w += 1
    return w


def main(p):
    print("p :", p)
    start = tm.default_timer()

    bsc = Channel(p)
    err = 0
    for i in range(445):
        dmins = [{}] * 16
        preds = [{}] * 16
        for state in states:
            dmins[0][state] = math.inf
        dmins[0]['000'] = 0

        for j in range(15):
            received = ''.join(str(x)
                               for x in bsc.transmit([0, 0, 0]))  # '000'
            set_next_min_paths(received, dmins, preds, j)

        msg = get_expected_msg_from_min_path(dmins, preds)
        err += get_hamming_weight(msg)

    prob = err / (445 * 15)
    stop = tm.default_timer()
    print('Execution time: ', stop - start)
    return prob

m = 3
states = generate_binary_strings(m)
g1 = '1011'
g2 = '1101'
g3 = '1111'

m3err = []
for p in p_list:
    m3err.append(main(p))

df = pd.DataFrame.from_dict({ 
    'none': p_list, 
    'm3': m3err,
    # 'm = 4': m4err,
    # 'm = 6': m6err,
})
df.to_csv("lab3/results.csv")
plot_graph(show_fig=False)
