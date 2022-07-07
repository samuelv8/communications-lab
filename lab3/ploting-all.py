import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import splev, splrep, make_interp_spline
import math

def find_roots(x,y):
    s = np.abs(np.diff(np.sign(y))).astype(bool)
    return x[:-1][s] + np.diff(x)[s]/(np.abs(y[1:][s]/y[:-1][s])+1)

def plot_graph(save_fig=True, show_fig=False, fig_format='eps'):
    df4 = pd.read_csv("lab3/results4.csv")
    df1 = pd.read_csv("lab1/results.csv")
    df2 = pd.read_csv("results2.csv")
    df1["rsr"] = df1["none"].apply(lambda x: - math.log1p(2 * x - 1))

    _, ax = plt.subplots()
    ax.set_xscale("log")
    ax.set_yscale("log")
    x = df4["rsr"].tolist()[::-1]
    y = df4["none"].tolist()[::-1]
    model = make_interp_spline(x,y)
    xnew = np.linspace(x[0], x[-1], 300)
    ynew = model(xnew)
    ax.plot(xnew, ynew)
    z = find_roots(xnew, ynew - 1e-4)[0]
    print("None: ", z)
    ax.plot(df1["rsr"], df1["hamming"])
    x = df1["rsr"].tolist()[::-1]
    y = df1["hamming"].tolist()[::-1]
    model = make_interp_spline(x,y)
    xnew = np.linspace(x[0], x[-1], 300)
    ynew = model(xnew)
    # ax.plot(xnew, ynew)
    z = find_roots(xnew, ynew - 1e-4)[0]
    print("Hamming: ", z)
    ax.plot(df1["rsr"], df1["custom"])
    x = df1["rsr"].tolist()[::-1]
    y = df1["custom"].tolist()[::-1]
    model = make_interp_spline(x,y)
    xnew = np.linspace(x[0], x[-1], 300)
    ynew = model(xnew)
    # ax.plot(xnew, ynew)
    z = find_roots(xnew, ynew - 1e-4)[0]
    print("Custom: ", z)
    ax.plot(df1["rsr"], df2["n: 12 k: 7"])
    x = df1["rsr"].tolist()[::-1]
    y = df2["n: 12 k: 7"].tolist()[::-1]
    model = make_interp_spline(x,y)
    xnew = np.linspace(x[0], x[-1], 300)
    ynew = model(xnew)
    # ax.plot(xnew, ynew)
    z = find_roots(xnew, ynew - 1e-4)[0]
    print("Ciclic: ", z)
    ax.plot(df4["rsr"], df4["4"])
    x = df4["rsr"].tolist()[::-1]
    y = df4["4"].tolist()[::-1]
    model = make_interp_spline(x,y)
    xnew = np.linspace(x[0], x[-1], 300)
    ynew = model(xnew)
    # ax.plot(xnew, ynew)
    z = find_roots(xnew, ynew - 1e-4)[0]
    print("Conv: ", z)
    plt.axhline(y=1e-4, color='grey', linestyle='--')
    ax.set_xlabel("Relação sinal ruído")
    ax.set_ylabel("Probabilidade de erro do sistema")
    ax.set_title("Grafico de probabilidade de erro")
    ax.legend(['Nenhum', 'Hamming', 'Personalizado', 'Cíclico', 'Convolucional'])
    
    if show_fig:
        plt.show()
    if save_fig:
        plt.savefig(f'lab3/error-probability-graph-all.{fig_format}', format=fig_format)

if __name__ == '__main__':
    plot_graph()