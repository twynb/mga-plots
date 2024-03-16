import matplotlib as mpl
import matplotlib.pyplot as plt
import argparse


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
    ax.set_title(title + " (first " + str(smaller_plot_size) + " samples)")


def setup_ax(len: int, ax):
    ax.set_ylabel("Energy (% of maximum)")
    ax.set_ylim([0, 105])
    ax.set_xlim([0, len])
    ax.set_xlabel("Sample")


parser = argparse.ArgumentParser()
parser.add_argument("-s", "--show", action="store_true")
args = parser.parse_args()
show = args.show

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


plot_csv("data/cube_snapshot.csv", "Cube Snapshot", 5000, "cube_snapshot.pgf", show)
plot_csv("data/cube_interp.csv", "Cube Interpolated", 5000, "cube_interp.pgf", show)
plot_csv("data/l_snapshot.csv", "L Snapshot", 2000, "l_snapshot.pgf", show)
plot_csv("data/l_interp.csv", "L Interpolated", 2000, "l_interp.pgf", show)

plot_compare(
    "data/cube_snapshot.csv",
    "data/cube_interp.csv",
    "Cube Scene",
    5000,
    "cube_compare.pgf",
    doShow=show,
)
plot_compare(
    "data/l_snapshot.csv",
    "data/l_interp.csv",
    "L-Shaped Scene",
    5000,
    "l_compare.pgf",
    doShow=show,
)
