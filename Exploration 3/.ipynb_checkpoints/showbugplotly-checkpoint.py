#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 21:58:23 2018

@author: chenriq
"""

from brian2 import *
import numpy as np

import plotly.graph_objects as go

import numpy as np

import plotly.io as pio

pio.renderers.default='browser'

Ox=np.load('outbugx.npy')
Oy=np.load('outbugy.npy')
srx=np.load('outsrx.npy')
sry=np.load('outsry.npy')
slx=np.load('outslx.npy')
sly=np.load('outsly.npy')
Ba=np.load('outbugang.npy')
Fx=np.load('outfoodx.npy')
Fy=np.load('outfoody.npy')

bug_x_coords=np.zeros((500,3))
bug_y_coords=np.zeros((500,3))

for i in range(0,500):
           # Remove the last bug's position from the figure window
    bug_x_coords[i] = [Ox[i], Ox[i]-4*cos(Ba[i]), Ox[i]-8*cos(Ba[i])]
    bug_y_coords[i] = [Oy[i], Oy[i]-4*sin(Ba[i]), Oy[i]-8*sin(Ba[i])]

# Create figure
fig = go.Figure(
    data=[go.Scatter(x=Fx, y=Fy,
                     mode="lines",
                     line=dict(width=2, color="blue"))],
    
    
    layout=go.Layout(
        xaxis=dict(range=[-100, 100], autorange=False, zeroline=False),
        yaxis=dict(range=[-100, 100], autorange=False, zeroline=False),
        height=600,
        width=600,
        title_text="Kinematic Generation of a Planar Curve", hovermode="closest",
        updatemenus=[dict(type="buttons",
                          buttons=[dict(
                                        label="Play",
                                        method="animate",
                                        args = [None, {"frame": {"duration": 10, 
                                                                        "redraw": False},
                                                              "fromcurrent": True, 
                                                              "transition": {"duration": 0}}])])]),
    frames=[
        # go.Frame(
        # data=[go.Scatter(
        #     x=[bug_x_coords[k][0],bug_x_coords[k][1]],
        #     y=[bug_y_coords[k][0],bug_y_coords[k][1]],
        #     mode="markers",
        #     marker=dict(color=["red","blue"], size=[20,20]))])
        go.Frame(
        data=[go.Scatter(
            x=np.concatenate((bug_x_coords[k],[srx[k], slx[k]],[Fx[k]] )),
            y=np.concatenate((bug_y_coords[k],[sry[k], sly[k]], [Fy[k]])),
            mode="markers+markers+markers+markers+markers+markers",
            marker=dict(color=["black","black","black","blue","red","green"], size=[10,10,10,8,8,20]))])
        for k in range(1,500)]
                       
                                                   
                       
)
fig.show()
