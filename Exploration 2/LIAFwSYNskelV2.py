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

# Parameters
area = 20000*umetre**2
Cm = 1*ufarad*cm**-2
El = -60*mV
gl = 0.7*msiemens/cm**2

tau_ampa=0.3*ms
g_synpk=0.5
g_synmaxval=(g_synpk)

eqs_il = '''
il = gl * (El-v) :amp/meter**2
'''

eqs = '''
dv/dt = (il +GAMPA*msiemens/cm**2*(10*mV-v)+I/area )/Cm:  volt
#dg_ampa/dt = -g_ampa/tau_ampa: 1
GAMPA:1
I : amp
'''
eqs += (eqs_il) 

# Threshold and refractoriness are only used for spike counting
group = NeuronGroup(num_neurons, eqs, clock=Clock(defaultclock.dt),threshold='v > -45*mV',reset='v = -60*mV', method='euler')
group.v = El

Sr = Synapses(group, group, clock=group.clock,model='''
                g_synmax:1 
                dg_ampa/dt = -g_ampa/tau_ampa : 1
                GAMPA_post=g_ampa :1 (summed)''',
		on_pre='''
		g_ampa+= g_synmax 
		
		''')

Sr.connect(i=[0,1],j=[1,0])
Sr.g_synmax=g_synmaxval
Sr.delay=1*ms #introduces a fixed delay between the firing of the pre cell  and the postsynaptic response

monitor2=StateMonitor(group,('v', 'GAMPA'),record=True)
group.I[0] = 0*nA
group.I[1] = 0*nA
run(5.0*ms,report='text')
group.I[0] = 8*nA
group.I[1] = 0*nA
run(.5*ms, report='text')
group.I[0] = 0*nA
group.I[1] = 0*nA
run(10.0*ms)


figure(3)
subplot(4,1,1)
plot(monitor2.t/ms, monitor2.v[0]/mV)

subplot(4,1,2)
plot(monitor2.t/ms, monitor2.GAMPA[0])
subplot(4,1,3)
plot(monitor2.t/ms, monitor2.GAMPA[1],'r')
subplot(4,1,4)
plot(monitor2.t/ms, monitor2.v[1]/mV,'r')