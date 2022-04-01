import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def imshow_plot(data, y_tick_labels, x_tick_labels, x_label, y_label, title):
    fig, ax = plt.subplots()
    im = ax.imshow(data)

    ax.set_yticks(np.arange(len(y_tick_labels)), labels=y_tick_labels)
    ax.set_xticks(np.arange(len(x_tick_labels)), labels=x_tick_labels)

    for y in np.arange(len(y_tick_labels)):
        for x in np.arange(len(x_tick_labels)):
            ax.text(x, y, data[y, x], ha="center", va="center", color="w")

    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    ax.set_title(title)
    plt.show()


def imshow_2plots(data1,
                  y1_tick_labels,
                  x1_tick_labels,
                  y1_label,
                  x1_label,
                  title1,
                  data2,
                  y2_tick_labels,
                  x2_tick_labels,
                  y2_label,
                  x2_label,
                  title2):

    fig, (ax1, ax2) = plt.subplots(1, 2)
    im1 = ax1.imshow(data1)

    ax1.set_yticks(np.arange(len(y1_tick_labels)), labels=y1_tick_labels)
    ax1.set_xticks(np.arange(len(x1_tick_labels)), labels=x1_tick_labels)

    for y in np.arange(len(y1_tick_labels)):
        for x in np.arange(len(x1_tick_labels)):
            ax1.text(x, y, data1[y, x], ha="center", va="center", color="w")

    ax1.set_ylabel(y1_label)
    ax1.set_xlabel(x1_label)
    ax1.set_title(title1)

    im2 = ax2.imshow(data2)

    ax2.set_yticks(np.arange(len(y2_tick_labels)), labels=y2_tick_labels)
    ax2.set_xticks(np.arange(len(x2_tick_labels)), labels=x2_tick_labels)

    for y in np.arange(len(y2_tick_labels)):
        for x in np.arange(len(x2_tick_labels)):
            ax2.text(x, y, data2[y, x], ha="center", va="center", color="w")

    ax2.set_ylabel(y2_label)
    ax2.set_xlabel(x2_label)
    ax2.set_title(title2)
    fig.tight_layout()
    plt.show()