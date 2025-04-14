#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 27 17:18:35 2025

@author: computer
"""

import numpy as np
import sympy
from sympy.abc import X

class Node:
    '''Класс узла стержневой системы, силы и моменты содержатся по осям в массивах'''
    def __init__(self, x: int, y: int, z: int, name):
        self.coord = np.array([x, y, z])
        self.forces = np.array([0, 0, 0])
        self.moments = np.array([0, 0, 0])
        self.parents = []
        self.name = name
    
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
    def __init__(self, node_start: Node, node_end: Node):
        self.forces = np.array([0, 0, 0])
        self.forces_types = [None, None, None]
        self.length = np.linalg.norm(node_start.coord - node_end.coord)
        
        self.node_start = node_start
        self.node_end = node_end
        self.node_start.parents.append(self)
        self.node_end.parents.append(self)
        
        self.basis = np.array([
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
            ])
        self._init_basis()
        print("new basis", self.basis)
        
        self.moment_diagram_eqs = None # уравнения для построения эпюр
        
    
    def _init_basis(self):
        parent = None
        for i in self.node_start.parents:
            if i==self:
                continue
            else:
                parent = i
                break
        if parent == None:
            return None
        
        # вектора балок родителя и актиной балки
        vec1 = parent.node_end.coord - parent.node_start.coord
        vec2 = self.node_end.coord - self.node_start.coord
        
        phi = np.arccos(vec1.dot(vec2)) # угол поворота вокруг оси
        cos = np.cos(phi)
        sin = np.sin(phi)
        x, y, z = np.cross(vec1, vec2) # ось поворота
        rotate_matrix = np.around(np.array([
            [x*x*(1-cos)+cos, x*y*(1-cos)-z*sin, x*z*(1-cos)+y*sin],
            [x*y*(1-cos)+z*sin, y*y*(1-cos)+cos, y*z*(1-cos)-x*sin],
            [x*z*(1-cos)-y*sin, y*z*(1-cos)+x*sin, z*z*(1-cos)+cos]
            ]), decimals=10) # точность базиса
        
        self.basis = np.dot(self.basis, rotate_matrix)
    
    def add_force(self, fx: float, fy: float, fz: float, force_type=['rect', 'rect', 'rect']):
        self.forces += np.array([fx, fy, fz])
        self.forces_types = force_type
    
    def section_method_moments(self, parent_node):
        #функция для метода сечений
        #все действия выполняются на основе проекций векторов сил и моментов в глобальных координатах
        if parent_node == self.node_start:
            active_node = self.node_end
        if parent_node == self.node_end:
            active_node = self.node_start
        
        forces_beam = (self.forces*self.length, (self.node_end.coord-self.node_start.coord)*0.5 + self.node_start.coord)
        forces_node = (active_node.forces, active_node.coord)
        moments = (active_node.moments, active_node.coord)
        
        forces_global, moments_global = [], []
        
        
        #print("Выполняется перебор соседов для стержня {}-{}".format(active_node.name, parent_node.name))
        #input("Нажмите enter")
        
        self.moment_diagram_eqs = [0, 0, 0]
        
        if active_node.parents == [self]:
            forces_global, moments_global = [forces_beam, forces_node], [moments]
        else:
            for i in active_node.parents:
                #print("Анализируется балка {}-{}".format(i.node_start.name, i.node_end.name))
                if i == self or i.moment_diagram_eqs != None:
                    #print("Это и есть активная или уже обсчитывалась")
                    continue 
                else:
                    #print("Балка ранее не встречалась, вход в рекурсию")
                    f_g, m_g = i.section_method_moments(active_node)
                    #print("Рекурсия для балки {}-{} закончена".format(i.node_start.name, i.node_end.name))
                    forces_global.extend(f_g)
                    moments_global.extend(m_g)
        
        print("Балка {}-{} проанализирована, получены силы".format(active_node.name, parent_node.name))
        # здесь типа код для метода сечений этого стержня, 
        #...
        # на выходе - изменения в self.moments_diagram_eqs
        #print("Произошел пересчет балки {}-{}".format(active_node.name, parent_node.name))
        
        return forces_global, moments_global

class BeamSystem:
    '''Класс стержневой системы, какая-то дичь, по хорошему надо бы нормально придумать хранение элементов'''
    def __init__(self):
        self.elements = []
        
    def add_element(self, element: Beam):
        self.elements.add(element)

if __name__ == "__main__":
    print("ку")
    a0 = Node(-1, 0, 0, "0")
    a1 = Node(0, 0, 0, "1")
    a2 = Node(0, -1, 0, "2")
    a3 = Node(1, 0, 0, "3")
    a4 = Node(0, 0, -1, "4")
    
    b1 = Beam(a0, a1)
    b2 = Beam(a1, a2)
    b3 = Beam(a1, a3)
    b4 = Beam(a1, a4)
    
    b1.section_method_moments(a1)