#!/usr/bin/env python
'''
    Author: Jana Becker, Jan Disselhoff
'''

import numpy as np
import pygame

class BoundingBox():
    center = [] #achsen normiert, koordinaten des objekts
    axes = []
    lengths = []

    dragging = False

    def __init__(self, center, axes, lengths):
        self.center = np.array(center)
        self.axes = np.array(axes)
        self.lengths = np.array(lengths)

    def check_collision(self, point_coordinates):
        point_centered = (np.array(point_coordinates) - self.center)
        #test collision in direction of first axis of bounding box
        if(np.abs(np.dot(point_centered, self.axes[0])) > self.lengths[0]):
            return False
        #test in second direction
        if(np.abs(np.dot(point_centered, self.axes[1])) > self.lengths[1]):
            return False

        return True

    def check_collision_return_location(self,point_coordinates):
        point_centered = (np.array(point_coordinates) - self.center)
        #test collision in direction of first axis of bounding box
        ax1_pos = np.dot(point_centered, self.axes[0])
        ax2_pos = np.dot(point_centered, self.axes[1])
        col_pos = point_centered+ [ax1_pos,ax2_pos]

        ax1_percentage = ax1_pos/self.lengths[0]
        ax2_percentage = ax2_pos/self.lengths[1]


        #test both axes
        if(np.abs(ax1_pos) > self.lengths[0] or np.abs(ax2_pos)>self.lengths[1]):
            return False,ax1_percentage,ax2_percentage,col_pos


        return True,ax1_percentage,ax2_percentage,col_pos



    def update(self, center, axes, lengths):
        self.center = np.array(center)
        self.axes = np.array(axes)
        self.lengths = np.array(lengths)


    def draw(self,surface):
        rect = pygame.Rect((self.center-self.axes[0]*self.lengths[0]-self.axes[1]*self.lengths[1]),
                            (self.lengths))
        pygame.draw.rect(surface,(0,0,255),rect)
