import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def imshow_plot(data, y_tick_labels, x_tick_labels, y_label, x_label, title):
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


def imshow_multiplot(dicts, rows, cols, text=True):
    data = []
    y_tick_labels = []
    x_tick_labels = []
    y_label = []
    x_label = []
    title = []

    for item in dicts:
        data.append(item["data"])
        y_tick_labels.append(item["y_tick_labels"])
        x_tick_labels.append(item["x_tick_labels"])
        y_label.append(item["y_label"])
        x_label.append(item["x_label"])
        title.append(item["title"])

    fig, axs = plt.subplots(rows, cols)
    for i, ax in enumerate(axs.flat):
        im = ax.imshow(data[i])

        ax.set_yticks(np.arange(len(y_tick_labels[i])), labels=y_tick_labels[i])
        ax.set_xticks(np.arange(len(x_tick_labels[i])), labels=x_tick_labels[i])

        if text:
            for y in np.arange(len(y_tick_labels[i])):
                for x in np.arange(len(x_tick_labels[i])):
                    ax.text(x, y, round(data[i][y, x]), ha="center", va="center", color="w")

        ax.set_ylabel(y_label[i])
        ax.set_xlabel(x_label[i])
        ax.set_title(title[i])
    fig.tight_layout()
    plt.show()

def imshow_dict(generic_dict, data, title):
    result = generic_dict.copy()
    result["title"] = title
    result["data"] = data
    return result
