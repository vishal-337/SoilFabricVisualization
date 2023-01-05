import math
import numpy as np
import plotly.graph_objects as go

with open('normals_iso.txt') as f:
    contents = f.readlines()

##creating empty dictionary to store values
dic = {}
dicf = {}
for num in range(72):
    if num % 2 != 0:
        dic[num * 5] = 0
        dicf[num * 5] = 0  # dic to store force

f = []
##Calculating angle of each vector and storing it in theta
theta = []
for i in contents[1:-1]:
    x = i.split(" ")
    d = math.degrees(math.atan2(float(x[1]), float(x[0])))  # atan2(y,x)
    if (d < 0):
        d = 360 + d
    theta.append(d)
    f.append(float(x[3]))  # adding force
for i in contents[1:-1]:
    x = i.split(" ")
    g = math.degrees(math.atan2(-1 * float(x[1]), -1 * float(x[0])))  # atan2(y,x)
    if (g < 0):
        g = 360 + g
    theta.append(g)
    f.append(float(x[3]))  # adding force

##Calculating number of vectors in 10 degree window and storing in dic
for i in dic.keys():
    for j in range(len(theta)):
        if theta[j] >= i - 5 and theta[j] < i + 5:
            dic[i] = dic[i] + 1
            dicf[i] = dicf[i] + f[j]
# calculating avg force in each bucket
for i in dicf.keys():
    dicf[i] = dicf[i] / dic[i]

# Fourier Series

# List of z values
zList = []
for i in dic.keys():
    z = (dic[i] / (2 * len(contents[1:-1]) * math.radians(10))) - (1 / (2 * math.pi))
    zList.append(z)
# List of x values
xList = []
for i in dic.keys():
    x = (math.cos(2 * math.radians(i)))
    xList.append(x)
# List of y values
yList = []
for i in dic.keys():
    y = (math.sin(2 * math.radians(i)))
    yList.append(y)

# Least Square Plane for z = C1(x) + C2(y) to find A & thetaA
data = np.c_[xList, yList, zList]
A = np.c_[data[:, 0], data[:, 1], np.ones(data.shape[0])]
C, _, _, _ = np.linalg.lstsq(A, data[:, 2])

aVal = (2 * math.pi) * math.sqrt(C[0] ** 2 + C[1] ** 2)
thetaA = math.radians(math.degrees(0.5 * math.asin((2 * math.pi * C[1]) / aVal)))
thetax = np.zeros(360)
Etheta = np.zeros(360)
rad_con=650
for i in range(360):
    Etheta[i] = rad_con * (1 / 2 * math.pi) * (1 + (aVal * math.cos(2 * (math.radians(i) - thetaA))))
    thetax[i] = i

# creating layout
layout = go.Figure()

# creating bar polar and adding to layout
barpolar_plots = [go.Barpolar(
    r=list(dic.values()),
    theta=list(dic.keys()),
    width=[10],
    marker_line_color="black",
    marker_line_width=0.5,
    opacity=1,
    marker_color=list(dicf.values()),
    marker_colorscale="ice", marker_colorbar_thickness=20,
    marker_cmin=min(list(dicf.values())), marker_cmax=max(list(dicf.values())))]

layout.add_traces(barpolar_plots)

# creating scatter polar and adding to layout
scat = [go.Scatterpolar(r=Etheta, theta=thetax, mode='lines')]

layout.add_traces(scat)

layout.update_layout(
    title='Shperical Histogram',
    template=None,
    polar=dict(
        radialaxis=dict(range=[0, max(dic.values()) + 200], showticklabels=True),
        angularaxis=dict(showticklabels=True, nticks=36, )
    )
)
layout.show()
