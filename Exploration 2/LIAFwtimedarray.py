#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 15:30:32 2020

@author: chenriq
"""

from brian2 import *
defaultclock.dt=.01*ms
num_neurons = 2
duration = 2*second
div=defaultclock.dt


# Parameters
area = 20000*umetre**2
Cm = 1*ufarad*cm**-2
El = -60*mV
gl = 0.7*msiemens/cm**2

tau_ampa=0.3*ms
g_synpk=2.0
g_synmaxval=(g_synpk)


B=numpy.concatenate([0*sin(30*Hz*2*pi*numpy.arange(0,duration/ms/2,div/ms)*ms),
   1*sin(5*Hz*2*pi*numpy.arange(1500,2500,div/ms)*ms)])   

I=TimedArray(B,dt=defaultclock.dt)

# stimlist=numpy.zeros(2000)
# pulselist=numpy.array([10,50,130,290,410])
# stimlist[pulselist]=1    
# B=stimlist
# #duration = .02*second

# I=TimedArray(stimlist,dt=1*ms)
 


eqs_il = '''
il = gl * (El-v) :amp/meter**2
'''

eqs = '''
dv/dt = (il +g_ampa*msiemens/cm**2*(10*mV-v)+mag*I(t)/area )/Cm:  volt
dg_ampa/dt = -g_ampa/tau_ampa: 1
mag: amp
'''
eqs += (eqs_il) 

# Threshold and refractoriness are only used for spike counting
group = NeuronGroup(num_neurons, eqs, clock=Clock(defaultclock.dt),threshold='v > 450*mV',reset='v = -60*mV', method='euler')
group.v = El
group.mag=20*nA

Sr = Synapses(group, group, clock=group.clock,model='''
                g_synmax:1 ''',
		on_pre='''
		g_ampa+= g_synmax
		
		''')

Sr.connect(i=[0,1],j=[1,0])
Sr.g_synmax=g_synmaxval
Sr.delay=1*ms #introduces a fixed delay between the firing of the pre cell  and the postsynaptic response

monitor2=StateMonitor(group,('v', 'g_ampa'),record=True)


run(duration,report='text')


figure(1)
subplot(5,1,1)
plot(monitor2.t/ms, monitor2.v[0]/mV)

subplot(5,1,2)
plot(monitor2.t/ms, monitor2.g_ampa[0])
subplot(5,1,3)
plot(monitor2.t/ms, monitor2.g_ampa[1],'r')
subplot(5,1,4)
plot(monitor2.t/ms, monitor2.v[1]/mV,'r')
subplot(5,1,5)
Idata=I(numpy.arange(0,duration/ms,(div/ms))*ms)
plot((numpy.arange(0,duration/ms,div/ms)),Idata)

