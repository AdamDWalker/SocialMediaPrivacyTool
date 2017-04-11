'''
    File Name: Charts.py
    Author: Adam Walker
    Date Created: 11/04/2017
    Date Last Modified: 11/04/2017
    Python Version: 3.6.0
'''

import matplotlib.pyplot as plot
import numpy as np


def generatePieChart(n, data, labels, explode, title, filename):
    fig = plot.figure(n)
    ax = plot.axes([0.1, 0.1, 0.8, 0.8])

    ax.pie(data, explode, labels, autopct='%1.1f%%',
            shadow=False, startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.set_title(title)
    fig.savefig("Output_Images/" + filename, bbox_inches='tight')
    print("\nChart generated and saved as: " + filename)

def generateBarChart(n, data1, data2, data3, labels, legend, y_label, x_label, title, filename):
    index = np.arange(len(labels))
    bar_width = 0.3

    fig = plot.figure(n, figsize=(6, 6))
    ax = fig.add_subplot(111)

    rects1 = ax.bar(index, data1, bar_width, alpha=0.8)
    rects2 = ax.bar(index + bar_width, data2, bar_width, alpha=0.8)
    rects3 = ax.bar(index + bar_width * 2, data3, bar_width, alpha=0.8)

    ax.set_xticks(index + bar_width)
    ax.set_xticklabels(labels)

    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)

    ax.set_title(title)
    ax.legend((rects1, rects2, rects3), legend )
    fig.savefig("Output_Images/" + filename, bbox_inches='tight')
    print("\nChart generated and saved as: " + filename)
