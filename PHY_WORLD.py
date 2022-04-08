#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 08:02:13 2022

https://github.com/pybox2d/pybox2d/wiki/manual

@author: paul
"""

import Box2D.b2 as b2
import pygame as py

def pygame_to_box(pos, SCREEN_HEIGHT):
    return b2.vec2(pos[0]/20, SCREEN_HEIGHT/20 - pos[1]/20)

def box_to_pygame(pos, SCREEN_HEIGHT):
    return b2.vec2(20*pos[0], -20*pos[1]+SCREEN_HEIGHT)

class WORLD():
    def __init__(self, SCREEN_DIMS=(50,30), FPS=60, PPM=20, g=9.81,
                  GAME_NAME="NO_NAME", ground=True, ground_size=(50,1), 
                  hard_walls=True, walls_hidden=True):
        self.SCREEN_WIDTH = SCREEN_DIMS[0] * PPM
        self.SCREEN_HEIGHT = SCREEN_DIMS[1] * PPM
        self.FPS = FPS
        self.PPM = PPM
        self.TIME_STEP = 1.0 / FPS
        self.g = g

        # --- pygame setup ---
        self.screen = py.display.set_mode((self.SCREEN_WIDTH, 
                                            self.SCREEN_HEIGHT), 0, 32)
        py.display.set_caption(GAME_NAME)
        self.clock = py.time.Clock()

        self.clock = py.time.Clock()
        self.world = b2.world(gravity=(0, -self.g), doSleep=True)
        self.colors = {
            b2.staticBody: (255, 255, 255, 255),
            b2.dynamicBody: (127, 127, 127, 255),
            b2.kinematicBody: (0, 0, 255, 255),
            
        } 
        self.b2BodyDef = b2.bodyDef
        self.b2FixtureDef = b2.fixtureDef
        self.b2JointDef = b2.jointDef

        if ground:
            # And a static body to hold the ground shape
            ground_body = self.world.CreateStaticBody(
                position=(0,0),
                shapes=b2.polygonShape(box=ground_size),
            )

        if hard_walls:
            if walls_hidden:
                x0=1
                x1=1.055
            else:
                x0=x1=0
            # make hard walls
            left_wall_body = self.world.CreateStaticBody(
                position=(-x1,0),
                shapes=b2.polygonShape(box=(1,self.SCREEN_HEIGHT/self.PPM)),
            )            

            right_wall_body = self.world.CreateStaticBody(
                position=(self.SCREEN_WIDTH/self.PPM+x0,0),
                shapes=b2.polygonShape(box=(1,self.SCREEN_HEIGHT/self.PPM)),
            )  

            ceiling_body = self.world.CreateStaticBody(
                position=(0,self.SCREEN_HEIGHT/self.PPM+x1),
                shapes=b2.polygonShape(box=ground_size),
            ) 
# def WORLD(SCREEN_DIMS=(1000,600), FPS=60, PPM=20, g=9.81,
#          GAME_NAME="NO_NAME", ground=True, ground_size=(50,1), hard_walls=True):
#     SCREEN_WIDTH = SCREEN_DIMS[0]
#     SCREEN_HEIGHT = SCREEN_DIMS[1]
#     TIME_STEP = 1.0 / FPS
    
    
#     # --- pygame setup ---
#     screen = py.display.set_mode((SCREEN_WIDTH, 
#                                        SCREEN_HEIGHT), 0, 32)
#     py.display.set_caption(GAME_NAME)
#     clock = py.time.Clock()
    
#     clock = py.time.Clock()
#     world = b2.world(gravity=(0, -g), doSleep=True)
#     colors = {
#         b2.staticBody: (255, 255, 255, 255),
#         b2.dynamicBody: (127, 127, 127, 255),
#         b2.kinematicBody: (0, 0, 255, 255),
        
#     } 
#     b2BodyDef = b2.bodyDef
#     b2FixtureDef = b2.fixtureDef
#     b2JointDef = b2.jointDef
    
#     if ground:
#         # And a static body to hold the ground shape
#         ground_body = world.CreateStaticBody(
#             position=(0,0),
#             shapes=b2.polygonShape(box=ground_size),
#         )
    
#     if hard_walls:
#         # make hard walls
#         left_wall_body = world.CreateStaticBody(
#             position=(0,0),
#             shapes=b2.polygonShape(box=(1,SCREEN_HEIGHT/PPM)),
#         )            
    
#         right_wall_body = world.CreateStaticBody(
#             position=(SCREEN_WIDTH/PPM,0),
#             shapes=b2.polygonShape(box=(1,SCREEN_HEIGHT/PPM)),
#         )  
    
#         ceiling_body = world.CreateStaticBody(
#             position=(0,SCREEN_HEIGHT/PPM),
#             shapes=b2.polygonShape(box=ground_size),
#         )  
#     return world, screen
    
def make_distance_joint(w, myBody1, myBody2, 
                        worldAnchorOnBody1, worldAnchorOnBody2):
    
    # joint_def = w.b2JointDef()
    
    # joint_def.bodyA = myBody1
    # joint_def.bodyB = myBody2
    # joint_def.anchorA = worldAnchorOnBody1
    # joint_def.anchorB = worldAnchorOnBody2
    # joint_def.collideConnected = True
    # joint_def.dampingRatio = 0.0
    # joint_def.frequencyHz = 0.0
    # joint_def.length = b2.vec2(1,1).length
    # joint_def.type = 3 #b2.distanceJoint
    # joint = w.world.CreateJoint(joint_def)
    

    
    joint = w.world.CreateDistanceJoint(bodyA=myBody1,
     	bodyB=myBody2,
     	anchorA=worldAnchorOnBody1,
     	anchorB=worldAnchorOnBody2,
     	collideConnected=True, dampingRatio=0, frequencyHz=0, length=b2.vec2(1,1).length)

    # joint = w.world.CreateRevoluteJoint(
    #     bodyA=myBody1,
    #     bodyB=myBody2,
    #     anchor=myBody1.worldCenter)    
    return joint
    
def make_body(w, pos, vel=(0,0), angle=0, ang_vel=0, density=1, friction=0.3, 
             restitution=0, shape=b2.polygonShape, radius=0.5,
             verticies=[(-1,-1),(-1,1),(1,-1),(1,1)], type=b2.dynamicBody, bullet=False):
       
    body_def = w.b2BodyDef(
        active=True,
        angle=angle,
        angularDamping=0.0,
        angularVelocity=ang_vel,
        awake=True,
        bullet=bullet,
        fixedRotation=False,
        linearDamping=0.0,
        linearVelocity=vel,
        position=pos,
        type=type,
        userData=None)
    
    body = w.world.CreateBody(body_def)  

    body_fix = w.b2FixtureDef(
        shape=shape(),
        density=density,
        friction=friction,
        restitution=restitution,
        )
    
    if shape==b2.circleShape:
        body_fix.shape.radius = radius
    if shape==b2.polygonShape:
        body_fix.shape.vertices = verticies
        
    obj = body.CreateFixture(body_fix)   
    return obj
        
        
        
        
        
        
        
        