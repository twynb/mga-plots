import matplotlib as mpl
import matplotlib.pyplot as plt
import argparse
import math


def plot_csv(
    fname: str, title: str, smaller_plot_size: int, outfile: str, doShow: bool = False
):
    values = parse_values_from_file(fname)
    _fig, ax = plt.subplots()
    plot_all_values(values, title, ax)
    if doShow:
        plt.show()
    else:
        plt.savefig("result/" + outfile)

    _fig, ax = plt.subplots()
    plot_first_n_values(values, title, smaller_plot_size, ax)
    if doShow:
        plt.show()
    else:
        plt.savefig("result/partial_" + outfile)


def plot_compare(
    fname_1: str,
    fname_2: str,
    suptitle: str,
    smaller_plot_size: int,
    outfile: str,
    title1: str = "Snapshot",
    title2: str = "Interpolated",
    doShow: bool = False,
):
    values_1 = parse_values_from_file(fname_1)
    values_2 = parse_values_from_file(fname_2)
    fig, axs = plt.subplots(
        ncols=2, nrows=1, layout="compressed", dpi=100, figsize=(6.4, 3)
    )
    plot_all_values(values_1, title1, axs[0])
    plot_all_values(values_2, title2, axs[1])
    fig.suptitle(suptitle)
    if doShow:
        plt.show()
    else:
        plt.savefig("result/" + outfile)

    fig, axs = plt.subplots(
        ncols=2, nrows=1, layout="compressed", dpi=100, figsize=(6.4, 3)
    )
    plot_first_n_values(values_1, title1, smaller_plot_size, axs[0])
    plot_first_n_values(values_2, title2, smaller_plot_size, axs[1])
    fig.suptitle(suptitle)
    if doShow:
        plt.show()
    else:
        plt.savefig("result/partial_" + outfile)


def parse_values_from_file(fname: str):
    with open(fname) as f:
        line = f.readline()
    # trim out last ';' so we don't have to worry about it messing with split below
    line = line[:-1]
    values = [float(x) for x in line.split(";")]
    scaling_factor = 100 / max(values)
    return [x * scaling_factor for x in values]


def plot_all_values(values: list, title: str, ax):
    setup_ax(len(values), ax)
    ax.plot(values)
    ax.set_title(title)


def plot_first_n_values(values: list, title: str, smaller_plot_size: int, ax):
    setup_ax(smaller_plot_size, ax)
    ax.plot(values[:smaller_plot_size])
    ax.set_title(f"{title} (first {str(smaller_plot_size)} samples)")


def setup_ax(len: int, ax):
    ax.set_ylabel("Energy (% of maximum)")
    ax.set_ylim([0, 105])
    ax.set_xlim([0, len])
    ax.set_xlabel("Sample")


C50_LIMIT = int(44100 * 50 / 1000)
"""
44100 samples * 50 milliseconds
"""


def print_c50(fname: str, name: str):
    values = parse_values_from_file(fname)
    c50 = c50_from_values(values)
    print(f"{name}: {str(c50)}")


def c50_from_values(values: list):
    index = 0
    while values[index] == 0:
        index += 1
    values = values[index:]
    before_limit = sum(values[:C50_LIMIT])
    after_limit = sum(values[(C50_LIMIT + 1) :])
    return 10 * math.log10(before_limit / after_limit)


parser = argparse.ArgumentParser()
parser.add_argument("-s", "--show", action="store_true")
parser.add_argument("-np", "--noplots", action="store_true")
args = parser.parse_args()
show = args.show
no_plots = args.noplots

if not show:
    mpl.use("pgf")
    mpl.rcParams.update(
        {
            "pgf.texsystem": "pdflatex",
            "font.family": "serif",
            "text.usetex": True,
            "pgf.rcfonts": False,
        }
    )

if not no_plots:
    plot_csv(
        "data/cube_snapshot_1.csv", "Cube Snapshot", 5000, "cube_snapshot.pgf", show
    )
    plot_csv(
        "data/cube_interp_1.csv", "Cube Interpolated", 5000, "cube_interp.pgf", show
    )
    plot_csv("data/l_snapshot_1.csv", "L Snapshot", 2000, "l_snapshot.pgf", show)
    plot_csv("data/l_interp_1.csv", "L Interpolated", 2000, "l_interp.pgf", show)

    plot_compare(
        "data/cube_snapshot_1.csv",
        "data/cube_interp_1.csv",
        "Cube Scene",
        5000,
        "cube_compare.pgf",
        doShow=show,
    )
    plot_compare(
        "data/l_snapshot_1.csv",
        "data/l_interp_1.csv",
        "L-Shaped Scene",
        2000,
        "l_compare.pgf",
        doShow=show,
    )

for idx in range(1, 4):
    print(f"Running tests for {str(idx)}")
    print_c50(f"data/cube_snapshot_{str(idx)}.csv", "Cube Snapshot")
    print_c50(f"data/cube_interp_{str(idx)}.csv", "Cube Interp")
    print_c50(f"data/l_snapshot_{str(idx)}.csv", "L Snapshot")
    print_c50(f"data/l_interp_{str(idx)}.csv", "L Interp")
