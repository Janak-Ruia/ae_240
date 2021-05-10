import math
import numpy
import matplotlib.pyplot as plt

def V_grav_t(g0, Isp, M0, beta, t, v0,g):
    return (g0*(-Isp*math.log((M0-beta*t)/M0))-g*t+v0)

def beta(thrust, g0, Isp):
    return thrust/(g0*Isp)

def height_t(m0, g0, Isp, beta, v0, t, g, h0):
    lamda=(m0-beta*t)/m0
    return ((m0*g0*Isp/beta)*((lamda)*math.log(lamda)-lamda + 1) - 0.5*g*t**2 + v0*t +h0)

Re = 6378000

def modifiy_g(h):
    g_prime = g0*(1-2*h/Re)
    return (g0+g_prime)/2
#constant pitch rate
def theta(t, rate):
    return rate*t

theta_0 = 45*math.pi/180

def height_theta(g, theta_0, V0, theta, h0):
    q0 = g*math.sin(theta_0)/V0
    return (g/4*q0**2)*(math.cos(2*theta_0)-math.cos(2*theta))+h0


m_total = 103217
mp1 = 76000
ms1 = 7530
mp2 = 15000
ms1 = 1500
mp3 = 3200
ms3 = 0
m_payload = 1080
ft1 = 1188000
ft2 = 180000
ft3 = 6500
g0 = 9.81
isp1 = 300
isp2 = 341.5
isp3 = 306.9

beta1 = beta(ft1, g0, isp1)
beta2 = beta(ft2, g0, isp2)
beta3 = beta(ft3, g0, isp3)

#final height at stage 1
h_fin_1 = height_t(m_total, g0, isp1, beta1, 0, 188, 9.81, 0) 
new_g = modifiy_g(h_fin_1)
h_fin_1_g = height_t(m_total, g0, isp1, beta1, 0, 188, new_g, 0)
V_fin_1_g=V_grav_t(9.81, 300, m_total, beta1, 188, 0, new_g)
print("h: ", h_fin_1_g,"and V: ", V_fin_1_g)


t = numpy.linspace(0,300, 30000)
h=[]
v=[]

h_req = 538100 - h_fin_1_g  #height required from h2 and h3
hr = []

#function to calculate h2
def h2(t1):
    return height_t(m_total-mp1-ms1, g0, isp2, beta2, V_fin_1_g, t1, 9.81, h_fin_1) #letting stage 2 run straight for 150s

#function to calculate h3
def h3(t1):
    V0 = V_grav_t(9.81, isp2, m_total-mp1-ms1, beta2, t1, V_fin_1_g, new_g) #vel at start of turn
    q0 = 0.028
    return (g0/4*q0**2)*(math.cos(2*theta_0)-math.cos(math.pi))

#propellant used in stage 2 part 1
def m2(t, beta):
    return beta*t

#propellant used in stage 2 part 2
def m3(t, m_2, isp):
    V0 = V_grav_t(9.81, isp2, m_total-mp1-ms1, beta2, t1, V_fin_1_g, new_g)
    q0 = g0*math.sin(theta_0)/V0
    return (m_total-mp1-ms1-m_2)*(1-math.exp(2*(math.sin(theta_0)-1)/(q0*isp)))


t1 = 157

#burn profile for stage 2 part 2
def mass_3(t,m_2,isp):
    q0 = 0.0028 
    theta = theta_0 + t*q0
    if theta>=math.pi/2:
        print(t)
    return (m_2)*(math.exp(2*(math.sin(theta_0)-math.sin(theta))/(q0*isp)))




H_final = h2(t1)+h3(t1)+h_fin_1_g

'''
STAGE 1 BURN PROFILE
'''
stage_1_mass = []
time = numpy.linspace(0, 188, 5000)
for t in time:
    stage_1_mass.append(m_total - m2(t, beta1))

stage_1_mass_final = stage_1_mass[-1]
plt.plot(time, stage_1_mass)
plt.legend(['Stage 1 burn profile'])
plt.xlabel('time (s)')
plt.ylabel('mass (kg)')
plt.show()

'''
STAGE 2 BURN PROFILE
'''
stage_2_mass = []
time = numpy.linspace(0, 437.5, 10000)

mass_t_157 = m_total - ms1 - mp1 - m2(157, beta2)
print("mass m 157 : ", mass_t_157)
for t in time:
    if t<157:
        stage_2_mass.append(m_total - ms1 - mp1 - m2(t, beta2))
    else:
        td = t-157
        stage_2_mass.append(mass_3(td, mass_t_157, isp2))
    


plt.plot(time, stage_2_mass)
plt.legend(['Stage 2 burn profile'])
plt.xlabel('time (s)')
plt.ylabel('mass (kg)')
plt.show()

'''----------------------------------------------------------------------------------------'''
'''Side code for finding t1'''

# m = []
# mthe3 = []
# mthe2 = []
# mreq = []
# for t1 in t:
#     h.append(h2(t1)+h3(t1))
#     hr.append(h_req)
#     m_2 = m2(t1, beta2)
#     mthe2.append(m_2)
#     m_3 = m3(t1, m_2, isp2)
#     mthe3.append(m_3)
#     m.append(m_2 + m_3)
#     mreq.append(15000)



# plt.plot(t, m)
# plt.plot(t, mthe3)
# plt.plot(t, mthe2)

# # plt.legend("")
# plt.plot(t, mreq)
# plt.legend(["m2+m3","m3","m2","propellant available"])
# plt.xlabel("t1 (s)")
# plt.ylabel("mass (kg)")
# plt.show()

# plt.plot(t, h)
# plt.plot(t, hr)
# plt.xlabel("t1 (s)")
# plt.ylabel("Height (m)")
# plt.legend(["h2+h3","Required Height"])
# plt.show()
