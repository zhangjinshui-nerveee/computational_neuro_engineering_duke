from brian2 import *

num_neurons = 100
defaultclock.dt=0.01*ms
duration = 2000*ms

# Parameters
area = 20000*umetre**2
Cm = 1*ufarad*cm**-2
El = 
EK = 
ENa = 

gl =
gNa = 
gK = 


#The model
eqs_ina = '''

'''

eqs_ik = '''
ik=gK * n**4 * (EK-v):amp/meter**2
dn/dt = alphan * (1-n) - betan * n : 1
alphan = (0.01/mV) * (-(v)+10*mV) / (exp((-(v)+10*mV) / (10*mV)) - 1)/ms : Hz
betan = 0.125*exp(-(v)/(80*mV))/ms : Hz
'''

eqs_il = '''
il = gl * (El-v) :amp/meter**2
'''

eqs = '''
dv/dt = (ina+ik+il +I/area)/Cm:  volt
I: amp
'''
eqs += (eqs_ina+eqs_ik+eqs_il) 

# Threshold and refractoriness are only used for spike counting
group = NeuronGroup(num_neurons,  eqs,
                    threshold='v > 40*mV',
                    refractory='v > 40*mV',
                    clock=Clock(defaultclock.dt),method='euler')
group.v = 0*mV
group.m=0.0529
group.n=0.3177
group.h=0.596
monitor2=StateMonitor(group,'v',record=True)
run(duration, report='text')

group.I = '(7.0*nA * i) / num_neurons'

monitor = SpikeMonitor(group)
monitor2=StateMonitor(group,'v',record=True)

run(duration)

figure(1)
plot(group.I/nA, monitor.count / duration)
xlabel('I (nA)')
ylabel('Firing rate (sp/s)')

figure(2)
plot(monitor2.t/ms, monitor2.v[24]/mV) #plot the voltage for neuron 0 (index starts at 0)
ylim(-80,60) #set axes limits

show()
