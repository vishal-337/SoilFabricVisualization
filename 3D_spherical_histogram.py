

import math
import numpy as np
import matplotlib as mpl
from matplotlib import cm
import plotly.graph_objects as go

with open('normals_Iso.txt') as f:
    contents = f.readlines()
fig = go.Figure()
long_div = 36
lat_div = 18
ic = []
for i in range(1, long_div + 2):
    ic.append((i - 1) * 2 * math.pi / long_div)
jc = []
for i in range(1, lat_div + 2):
    jc.append(math.acos(1 - ((2 * (i - 1)) / lat_div)))

#print(len(ic))
#print(jc)
c = []
for i in contents[1:]:
    x = i.split(" ")
    c.append([float(x[0]), float(x[1]), float(x[2])])
for i in contents[1:]:
    x = i.split(" ")
    c.append([-1 * float(x[0]), -1 * float(x[1]), -1 * float(x[2])])


def function(data):
    x = np.array([i[0] for i in c])
    y = np.array([i[1] for i in c])
    z = np.array([i[2] for i in c])
    R = np.sqrt(np.square(x) + np.square(y) + np.square(z))
    theta = np.arccos(np.divide(z, R))
    phi = np.arccos(np.divide(x, np.sqrt(np.square(x) + np.square(y))))
    for i in range(len(phi)):
        if (y[i] < 0):
            x = (2 * math.pi) - phi[i]
            phi[i] = x

    return [R, theta, phi]

fun = function(c)

A = []
for i in range(len(ic) - 1):
    for j in range(len(jc) - 1):
        lent = len([k for k in range(len(fun[1])) if (
                    (fun[2][k] >= ic[i]) and (fun[2][k] < ic[i + 1]) and (fun[1][k] >= jc[j]) and (
                        fun[1][k] < jc[j + 1]))])
        A.append([ic[i], ic[i + 1], jc[j], jc[j + 1], lent])
M = max([i[4] for i in A])
mn=min([i[4] for i in A])
Total_vec = sum([i[4] for i in A])

norm = mpl.colors.Normalize(vmin=0, vmax=M)
cmap = mpl.cm.ScalarMappable(norm=norm, cmap=mpl.cm.RdYlGn_r)
cmap.set_array([])

#fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
line_marker = dict(color='black', width=4)
line_marker2 = dict(color='black', width=1)
for i in range(len(A)):
    theta1 = A[i][2]
    theta2 = A[i][3]
    phi1 = A[i][0]
    phi2 = A[i][1]

    r = A[i][4]
    x1 = r * math.sin(theta1) * math.cos(phi1)
    y1 = r * math.sin(theta1) * math.sin(phi1)
    z1 = r * math.cos(theta1)

    x2 = r * math.sin(theta2) * math.cos(phi1)
    y2 = r * math.sin(theta2) * math.sin(phi1)
    z2 = r * math.cos(theta2)

    x3 = r * math.sin(theta2) * math.cos(phi2)
    y3 = r * math.sin(theta2) * math.sin(phi2)
    z3 = r * math.cos(theta2)

    x4 = r * math.sin(theta1) * math.cos(phi2)
    y4 = r * math.sin(theta1) * math.sin(phi2)
    z4 = r * math.cos(theta1)

    X = [0,x1, x2, x3,x4]
    Y = [0,y1, y2, y3,y4]
    Z = [0,z1, z2, z3,z4]

    X1=[0, x1, x2, 0]
    Y1 = [0, y1, y2, 0]
    Z1 = [0, z1, z2, 0]

    X2 = [0, x3, x2,0]
    Y2 = [0, y3, y2,0]
    Z2 = [0, z3, z2,0]

    X3 = [0, x4, x3]
    Y3 = [0, y4, y3]
    Z3 = [0, z4, z3]

    X4 = [x4, x1]
    Y4 = [y4, y1]
    Z4 = [z4, z1]
    
    X5 = [g * ((M+10)/r) for g in [x1,x2,x3,x4,x1]]
    Y5 = [g * ((M+10)/r) for g in [y1,y2,y3,y4,y1]]
    Z5 = [g * ((M+10)/r) for g in [z1,z2,z3,z4,z1]]



    fig.add_scatter3d(x=X5, y=Y5, z=Z5, mode='lines', line=line_marker2,showlegend=False)
    fig.add_scatter3d(x=X1, y=Y1, z=Z1, mode='lines', line=line_marker,showlegend=False)
    fig.add_scatter3d(x=X2, y=Y2, z=Z2, mode='lines', line=line_marker,showlegend=False)
    fig.add_scatter3d(x=X3, y=Y3, z=Z3, mode='lines', line=line_marker,showlegend=False)
    fig.add_scatter3d(x=X4, y=Y4, z=Z4, mode='lines', line=line_marker,showlegend=False)
    fig.add_mesh3d(x=X, y=Y, z=Z, i=[0, 0, 0, 0, 1, 1], j=[1, 1, 2, 3,2,3], k=[4, 2, 3, 4,3,4],intensity=[r,r,r,r,r,r],intensitymode='cell',colorscale="rdylgn_r",cmin=mn,cmax=M)

fig.update_layout(showlegend=False)
fig.update_layout(
    scene=dict(
        xaxis=dict(visible= False,showticklabels=False),
        yaxis=dict(visible= False,showticklabels=False),
        zaxis=dict(visible= False,showticklabels=False),
    )
)


fig.show()
