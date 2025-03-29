#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 29 20:06:01 2025

@author: computer
"""

import matplotlib.pyplot as plt

def plot_truss(nodes, elements):
    """Функция для визуализации стержневой системы"""
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    for element in elements:
        x = [element.node1.coordinates[0], element.node2.coordinates[0]]
        y = [element.node1.coordinates[1], element.node2.coordinates[1]]
        z = [element.node1.coordinates[2], element.node2.coordinates[2]]
        ax.plot(x, y, z, "bo-")

    plt.show()