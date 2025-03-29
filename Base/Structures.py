#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 27 17:18:35 2025

@author: computer
"""

'''
Реализовано

Базовые классы для узлов и самих стержней
Намечен класс стержневой системы

Node содержит:
    координату
    силы по осям
    моменты по осям
    заделки по осям
    Метод добавления силы (перезаписи?)
    Метод добавления момента (перезаписи?)
    Метод добавления заделки

Beam содержит:
    стартовый и конечный узел
    силы по осям
    длину стержня
    тип нагрузки по осям
'''

'''
Планы

В Node нужно добавить:

В Beam нужно добавить:
    метод добавления нагрузки + тип
'''

import numpy as np

class Node:
    '''Класс узла стержневой системы, силы и моменты содержатся по осям в массивах'''
    def __init__(self, x: int, y: int, z: int):
        self.coord = np.array([x, y, z])
        self.forces = np.array([0, 0, 0])
        self.moments = np.array([0, 0, 0])
        self.supports = [False, False, False]
    
    def add_force(self, fx: float, fy: float, fz: float): 
        self.forces += np.array([fx, fy, fz])

    def add_moment(self, mx: float, my: float, mz: float): 
        self.moments += np.array([mx, my, mz])

    def set_support(self, x_fixed: bool, y_fixed: bool, z_fixed: bool):
        self.supports = [x_fixed, y_fixed, z_fixed]


class Beam:
    '''Класс стержня стержневой системы'''
    def __init__(self, node_start, node_end):
        self.forces = np.array([0, 0, 0])
        self.forces_types = [None, None, None]
        self.length = np.linalg.norm(node_start.coord - node_end.coord)
        self.node_start = node_start
        self.node_end = node_end
    
    def add_force(self, fx: float, fy: float, fz: float, force_type=['rect', 'rect', 'rect']):
        self.forces += np.array([fx, fy, fz])
        self.forces_types = force_type
        

class BeamSystem:
    '''Класс стержневой системы, какая-то дичь, по хорошему надо бы нормально придумать хранение элементов'''
    def __init__(self):
        self.elements = {}
        self.name_last = 0 # номер последнего элемента
        
    def add_element(self, name_parent, element):
        self.name_last += 1
        element.node_start = self.elements[name_parent].node_end
        self.elements[str(self.name_last)] = element