import matplotlib.pyplot as plot
import numpy as np


class DataCollector:

    params = {
        'axes.labelsize': 8,
        # 'text.fontsize': 8,
        'legend.fontsize': 10,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'text.usetex': False,
        'figure.figsize': [4.5, 4.5]
    }

    def __init__(self):
        self.collection_items = {}

    def collect_data_item(self, name, value):
        if not self.collection_items.get(name, None):
            self.collection_items[name] = [value]
        else:
            self.collection_items[name].append(value)

    def add_to_plot(self, name, time):
        plot.plot(self.collection_items[time], self.collection_items[name], label=name, linewidth=2)

    def show_plot(self, title, legend_labels, ylabel, save_as="default.png"):
        legend = plot.legend(legend_labels, loc='lower left')
        frame = legend.get_frame()
        frame.set_facecolor('0.9')
        frame.set_edgecolor('0.9')
        plot.rcParams.update(self.params)
        plot.title(title)
        plot.xlabel('Simulation Time (Days)')
        plot.ylabel(ylabel)
        last_day = max(self.collection_items['oracle.timer'])
        plot.xticks(ticks=np.arange(0, last_day + 1, 24 * 3600), labels=[str(x) for x in np.arange(0, 8, 1)])
        plot.savefig(save_as)
        plot.show()
