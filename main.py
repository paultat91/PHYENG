#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 08:26:28 2022

@author: paul
"""

from PHY_WORLD import *
from pygame.locals import (QUIT, KEYDOWN, K_ESCAPE)
import Box2D.b2 as b2
import pygame as py


phy = WORLD(g=0, walls_hidden=False)

def my_draw_polygon(polygon, body, fixture):
    vertices = [(body.transform * v) * phy.PPM for v in polygon.vertices]
    vertices = [(v[0], phy.SCREEN_HEIGHT - v[1]) for v in vertices]
    py.draw.polygon(phy.screen, phy.colors[body.type], vertices)    
b2.polygonShape.draw = my_draw_polygon

def my_draw_circle(circle, body, fixture):
    position = body.transform * circle.pos * phy.PPM
    position = (position[0], phy.SCREEN_HEIGHT - position[1])
    py.draw.circle(phy.screen, phy.colors[body.type], [int(
        x) for x in position], int(circle.radius * phy.PPM))
b2.circleShape.draw = my_draw_circle


running = True
while running:
    # Check the event queue
    keystate_0 = py.key.get_pressed()
    for event in py.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            running = False
        if event.type == py.MOUSEBUTTONDOWN:
            pos = pygame_to_box(py.mouse.get_pos(), phy.SCREEN_HEIGHT)
            
            make_body(phy, (10,20), friction=0, shape=b2.polygonShape, restitution=1, type=b2.dynamicBody)
            make_body(phy, (15,10), friction=0, shape=b2.polygonShape, restitution=1, type=b2.dynamicBody)

            #make_distance_joint(phy, phy.world.bodies[-1], phy.world.bodies[-2], phy.world.bodies[-1].position, phy.world.bodies[-2].position)
            make_revolute_joint(phy, phy.world.bodies[-1], phy.world.bodies[-2])
            #make_pulley_joint(phy, phy.world.bodies[-1], phy.world.bodies[-2], b2.vec2(15,5), b2.vec2(25,5))

    if keystate_0[py.K_LEFT]:
        phy.world.bodies[-1].ApplyLinearImpulse((-5,0),phy.world.bodies[-1].position,  True)
                   
    # Draw the world
    phy.screen.fill((0, 0, 0, 0))
    for body in phy.world.bodies:
        for fixture in body.fixtures:
            fixture.shape.draw(body, fixture)

    # Make Box2D simulate the physics of our world for one step.
    phy.world.Step(phy.TIME_STEP, 10, 10)

    # Flip the screen and try to keep at the target FPS
    py.display.flip()
    phy.clock.tick(phy.FPS)  
del(running)          
py.quit()
print('Done!')