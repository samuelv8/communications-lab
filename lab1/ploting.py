import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("results.csv")

fig, ax = plt.subplots()

ax.set_xscale("log")
ax.set_yscale("log")

ax.plot(df["p"], df["bit_error"])
ax.plot([0, 0.5], [0, 0.5])
plt.gca().invert_xaxis()
ax.set_xlabel("Probabilidade de inversao do canal")
ax.set_ylabel("Probabilidade de erro do sistema")
ax.set_title("Grafico de probabilidade de erro")


plt.savefig("Error probability graph")
