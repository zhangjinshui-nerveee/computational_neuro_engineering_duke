import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np


TOT_TIME = 13  # ms
dt = 0.01  # Timestep in ms
NTSTEPS = round(TOT_TIME / dt)  # Number of Timesteps
tvect = [i * dt for i in list(range(1, NTSTEPS))]  # Time Vector


# SET THE STIMULUS PARAMETERS
stimval =  13 # uA/cm2
stimdur = 0.5  # ms (duration)

# Initial Conditions
Cm = 1.0  #uF/cm^2
v = -60.0  #mV (rest potential)

# CALCULATE STEADY STATE VALUES FOR M,N,H at REST

GNA_bar = 125.0  # mS/cm^2
GK_bar = 30.0  # mS/cm^2
GLEAK_bar = 0.3  # mS/cm^2
ENA = 55.0  # mV
EK = -72.0  # mV


def am(vm):
  return 0.1*((25-(vm+60))/(np.exp((25-(vm+60))/10)-1))

def an(vm):
  return 0.01*(10-(vm+60))/((np.exp((10-(vm+60))/10))-1)

def ah(vm):
  return 0.07*np.exp((-(vm+60))/20.0)

def bm(vm):
  return 4.0*np.exp((-(vm+60))/18.0)

def bn(vm):
  return 0.125*np.exp((-(vm+60))/80)

def bh(vm):
  return 1/(np.exp((30-(vm+60))/10)+1)

#def tn(v):
  #return 1/(an(v)+bn(v))

#def tm(v):
  #return 1/(am(v)+bm(v))

#def th(v):
  #return 1/(ah(v)+bh(v))

n = an(-60)/(an(-60)+bn(-60))
 
m = am(-60)/(am(-60)+bm(-60))

h = ah(-60)/(ah(-60)+bh(-60))

# CALCULATE ELEAK

EL = v + (((GK_bar*(n**4)*(v-EK))+(GNA_bar*(m**3)*h*(v-ENA)))/GLEAK_bar)

vout = np.zeros(len(tvect))
mout = np.zeros(len(tvect))
hout = np.zeros(len(tvect))
nout = np.zeros(len(tvect))

iout = np.zeros(len(tvect))

for i in range(0, len(iout)):
  if i*dt < stimdur:
    iout[i] = -stimval
for i in range(0, NTSTEPS-1):
    # Apply square wave stimulus - you will play with this to get multiple pulses
    
    Istim = iout[i]

    # Calculate Iion from INa, IK and Il
    INa = GNA_bar*(m**3)*h*(v-(ENA))
    IK = GK_bar*(n**4)*(v-(EK))
    Il = GLEAK_bar*(v-(EL))
    
    Iion = INa + IK +Il     # this is the total ionic current from HH

    # Calculate next m, n, h using Forward Euler and the ODEs for m, n, h
    m = m + dt*((am(v)*(1-m))-(bm(v)*m))
    n = n + dt*((an(v)*(1-n))-(bn(v)*n))
    h = h + dt*((ah(v)*(1-h))-(bh(v)*h))

    # calculate next v - don't forget istim

    v = v - dt*((1/Cm)*(Iion+Istim))

    # store v
    vout[i] = v
    mout[i]=m
    hout[i]=h
    nout[i]=n

#vout=(vout/(max(vout)-min(vout)))
fig = go.Figure()
fig.add_trace(go.Scatter(x=tvect, y=vout,
                    mode='lines',
                    name='lines',line = dict(width = 7)))
fig2=go.Figure()
fig2.add_trace(go.Scatter(x=tvect, y=mout,
                    mode='lines',
                    name='lines',line = dict(width = 7)))
fig2.add_trace(go.Scatter(x=tvect, y=hout,
                    mode='lines',
                    name='lines',line = dict(width = 7)))
fig2.add_trace(go.Scatter(x=tvect, y=nout,
                    mode='lines',
                    name='lines',line = dict(width = 7)))
fig.update_layout(title='Action Potential',
                   xaxis_title='Time (ms)',
                   yaxis_title='Voltage (mV)', font_size=24,autosize=False,width=1000,height=800)
fig.update_yaxes(color='black',gridcolor='black',tickcolor='black',tickvals=[-90, -70, -60, -50, -40, -30 ,-20 ,-10, 0, 10, 20, 30, 40])
fig.update_xaxes(color='black',gridcolor='black',tickvals=[1,3,5,7,9,11,13,15])
fig.update_layout(plot_bgcolor='white')

fig.show()
fig2.show()
