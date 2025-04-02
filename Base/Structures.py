#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 27 17:18:35 2025

@author: computer
"""

import numpy as np
import sympy

x = sympy.abc.x

class Node:
    '''Класс узла стержневой системы, силы и моменты содержатся по осям в массивах'''
    def __init__(self, x: int, y: int, z: int):
        self.coord = np.array([x, y, z])
        self.forces = np.array([0, 0, 0])
        self.moments = np.array([0, 0, 0])
    
    def add_force(self, fx: float, fy: float, fz: float): 
        self.forces += np.array([fx, fy, fz])

    def add_moment(self, mx: float, my: float, mz: float): 
        self.moments += np.array([mx, my, mz])
        
class support(Node): # он же шарнир, если не все support активны
    '''Класс заделки и шариров, указываются направления в которых теряется подвижность'''
    def __init__(self, x: int, y: int, z: int, sup_x: bool, sup_y: bool, sup_z: bool):
        super().__init__(x, y, z)
        self.supports = [sup_x, sup_y, sup_z]

class MovablePivot(Node): # подвижность указывается в локальных координатах!
    '''Класс подвижного шарнира, указываются направления получающие подвижность'''
    def __init__(self, x: int, y: int, z: int, pivot_y: bool, pivot_z: bool):
        super().__init__(x, y, z)
        self.piv_y = pivot_y
        self.piv_z = pivot_z


class Beam:
    '''Класс стержня стержневой системы'''
    def __init__(self, node_start: Node, node_end: Node, parents):
        self.forces = np.array([0, 0, 0])
        self.forces_types = [None, None, None]
        self.length = np.linalg.norm(node_start.coord - node_end.coord)
        self.node_start = node_start
        self.node_end = node_end
        self.parents = parents
        self.basis_x = np.array([1, 0, 0])
        self.basis_y = np.array([0, 1, 0])
        self.basis_z = np.array([0, 0, 1])
        self.moment_diagram_eqs = [0, 0, 0] # уравнения для построения эпюр
    
    def add_force(self, fx: float, fy: float, fz: float, force_type=['rect', 'rect', 'rect']):
        self.forces += np.array([fx, fy, fz])
        self.forces_types = force_type
    
    def section_method_moments(self):
        #функция для метода сечений
        #все действия выполняются на основе проекций векторов сил и моментов в глобальных координатах
        
        forces_beam = (self.forces*self.length, (self.node_end-self.node_start)*0.5 + self.node_start)
        forces_node = (self.node_start.forces, self.node_start.coord)
        moments = (self.node_start.moments, self.node_start.coord)
        
        forces_global, moments_global = [], []
        
        if self.parents == None:
            forces_global, moments_global = [forces_beam, forces_node], [moments]
        else:
            for i in self.parents:
                 f_g, m_g = i.section_method_moments()
                 forces_global.extend(f_g)
                 moments_global.extend(m_g)
        
        # здесь типа код для метода сечений этого стержня, 
        #...
        # на выходе - изменения в self.moments_diagram_eqs
        
        return forces_global, moments_global
        

class BeamSystem:
    '''Класс стержневой системы, какая-то дичь, по хорошему надо бы нормально придумать хранение элементов'''
    def __init__(self):
        self.elements = []
        
    def add_element(self, element: Beam):
        self.elements.add(element)