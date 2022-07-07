import matplotlib.pyplot as plt
import pandas as pd


def plot_graph(save_fig=True, show_fig=False, fig_format="eps"):
    df = pd.read_csv("../lab3/results.csv")

    _, ax = plt.subplots()
    ax.set_xscale("log")
    ax.set_yscale("log")
    # ax.plot(df["none"], df["3"])
    ax.plot(df["none"], df["4"])
    ax.plot(df["none"], df["m_euclid"])
    # ax.plot(df["none"], df["6"])
    ax.plot([0, 0.5], [0, 0.5])
    plt.gca().invert_xaxis()
    ax.set_xlabel("Probabilidade de inversao do canal")
    ax.set_ylabel("Probabilidade de erro do sistema")
    ax.set_title("Grafico de probabilidade de erro")
    ax.legend(["m = 4", "m = 4 euclid", "None"])

    if show_fig:
        plt.show()
    if save_fig:
        plt.savefig(f"../lab3/error-probability-graph.{fig_format}", format=fig_format)


if __name__ == "__main__":
    plot_graph()
