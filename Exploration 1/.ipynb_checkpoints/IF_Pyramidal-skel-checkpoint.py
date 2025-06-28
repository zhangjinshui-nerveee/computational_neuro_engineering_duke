from brian2 import *

num_neurons = 100
duration = 3.0*second

# Parameters
area = 20000*umetre**2
Cm = (1*ufarad*cm**-2)
defaultclock.dt=.02*ms
div=defaultclock.dt


# The model

ENa=50.0 *mV
gnabar=50*msiemens*cm**-2
VT1=-61.5
VT=-61.5
EK=-90.0*mV
gkbar=4.8*msiemens*cm**-2
EKm=-90.0*mV
glbar= 0.0205*msiemens/cm**2
El=-70*mV


eqs_na = """
ina = gnabar*m**3*h*(ENa-v) : amp/meter**2
dm/dt  = (am1*(1-m)-bm1*m): 1
dh/dt  = (ah1*(1-h)-bh1*h): 1
am1=0.32*(13-(vu-VT))/(exp((13-(vu-VT))/4.0)-1.0)/ms: Hz
bm1=(0.28*((vu-VT)-40)/(exp(((vu-VT)-40)/5.0)-1.0))/ms: Hz
ah1 = 0.128*exp(-(vu-17-VT)/18)/ms: Hz
bh1 = 4/(1+exp(-(vu-40-VT)/5))/ms: Hz
"""

# IM channel ()
eqs_m = """
im = gmbar*c*(EKm-v) : amp/meter**2


"""



# K channel 
eqs_k = """
ik = gkbar*b**4*(EK-v): amp/meter**2
db/dt  = (ab*(1-b)-bb*b): 1
ab=0.032*(vu-15-VT1)/(1.0 - exp(-(vu-15-VT1)/5.0))/ms:Hz
bb=0.5*exp(-(vu-10-VT1)/40)/ms : Hz

"""

# Leak
eqs_leak = """
il = glbar*(El-v) : amp/meter**2
"""



eqs = """
dv/dt = (il + ik+ +ina+ im + I/area)/Cm : volt
vu = v/mV : 1  # unitless v 
I: amp
"""
eqs += eqs_leak + eqs_k + eqs_na +eqs_m


# Threshold and refractoriness are only used for spike counting
P1 = NeuronGroup(num_neurons, eqs,clock=Clock(defaultclock.dt),
                    threshold='v > -40*mV',refractory='v > -40*mV',method='euler')
                    

P1.I='1.3*nA * i / num_neurons'

                    

monitor = SpikeMonitor(P1)
monitor2=StateMonitor(P1, ('v'), record=True)
net = Network(P1, monitor, monitor2)
net.run(duration)

figure(1)
subplot(2,1,1)
plot(monitor2.t/ms, monitor2.v[20]/mV)
subplot(2,1,2)
#Idata=I(numpy.arange(0,duration/ms,(div/ms))*ms)
#plt.plot((numpy.arange(0,duration/ms,div/ms)),Idata)
plot(P1.I/nA, monitor.count / duration)
xlabel('I (nA)')
ylabel('Firing rate (sp/s)')
show()