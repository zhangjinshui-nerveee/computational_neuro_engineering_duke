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
g_synpk=1.5

eqs_il = '''
il = gl * (El-v) :amp/meter**2
'''

eqs = '''
dv/dt = (il +GAMPA*g_synpk*msiemens/cm**2*(0*mV-v)+I/area )/Cm:  volt
I : amp
GAMPA:1
'''
eqs += (eqs_il) 

# Threshold and refractoriness are only used for spike counting
group = NeuronGroup(num_neurons, eqs, clock=Clock(defaultclock.dt),threshold='v > -45*mV',reset='v = -60*mV', method='euler')
group.v = El

Sr = Synapses(group, group, clock=group.clock,method='euler',model='''
                Trpre=.25*(tanh((t/ms-tspike/ms)/.005)-tanh((t/ms-(tspike/ms +.3))/.005)):1
                aAMPA=0.94/ms :Hz
                bAMPA=0.18/ms: Hz 
                tspike: second
                dsAMPA_syn/dt = aAMPA*Trpre*(1-sAMPA_syn)-bAMPA*sAMPA_syn:1                               
                GAMPA_post=sAMPA_syn : 1 (summed)''',on_pre='''
                tspike=t''')

Sr.connect(i=[0],j=[1])
Sr.tspike[0]=-.5*ms # needed to get rid of spurious first tspike
Sr.delay=0*ms #introduces a fixed delay between the firing of the pre cell  and the postsynaptic response

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