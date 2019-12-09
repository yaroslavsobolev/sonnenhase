import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
import json
import pytz
from datetime import datetime
from scipy import interpolate

by_mh = np.load('by_mh.npy')

data = np.load('data_by_cams_filtered.npy')
data[10, 6, 17:22] = 0
data_with_clouds = np.copy(data)
by_cam = []
for i in range(18):
    for frame in range(40):
        hour_here = int(np.floor(3 + frame/2))
        data_with_clouds[i, :, frame] = data_with_clouds[i, :, frame]*(100-by_mh[:, hour_here])/100
    by_cam.append(np.sum(data_with_clouds[i, :, :]))

by_cam = np.array(by_cam)
cam_coords = np.loadtxt('data/3d/cam_coords.txt', skiprows=1)

plt.plot(by_cam*0.5*30)
# plt.show()

# for_plot = np.vstack((by_cam, by_cam))[:,:12]
# x = cam_coords[:,1]
# y = by_cam[:12]*0.5*30
# f = interpolate.interp1d(x, y, kind='quadratic')
# xnew = np.linspace(np.min(x), np.max(x), 50)
# ynew = f(xnew)   # use interpolation function returned by `interp1d`
# ynew[ynew <= 0] = 0
# plt.plot(x, y, 'o', xnew, ynew, '-')
# plt.show()
#
# for_plot = np.vstack((ynew, ynew))
# fig = plt.figure(1)
# plt.imshow(for_plot, cmap='inferno', interpolation='bicubic', vmin=0, vmax=160, aspect=5)
# fig.savefig('figures/road_map.png', dpi=500)
#
# plt.show()
# print(1)

park_coords = np.loadtxt('data/3d/parking_cams.txt', skiprows=1)
# plt.plot(np.array(by_cam)*0.5*30)
fig, ax = plt.subplots()
xs = park_coords[:,1]
ys = park_coords[:,2]
zs = by_cam[12:]*0.5*30
f = interpolate.interp2d(xs, ys, zs, kind='linear',fill_value=0)

xnew = np.linspace(np.min(xs), np.max(xs), 100)
ynew = np.linspace(np.min(ys), np.max(ys), 100)
znew = f(xnew, ynew)

from scipy.interpolate import Rbf
# , d = np.random.rand(4, 50)
rbfi = Rbf(xs, ys, zs)  # radial basis function interpolator instance
# xi = yi = zi = np.linspace(0, 1, 20)
xv, yv = np.meshgrid(xnew, ynew)
znew = rbfi(xv, yv)   # interpolated values
# di.shape
coeff = 1/365*60
# plt.plot(x, znew[0, :], 'ro-', xnew, znew[0, :], 'b-')
ims = ax.imshow(znew*coeff, cmap='inferno', extent=(np.min(xs), np.max(xs), np.min(ys), np.max(ys)), origin='lower',
          vmin=0, vmax=160*coeff)
# plt.scatter(xs, ys, s=zs)
fig.savefig('figures/parking_map.png', dpi=500)

plt.colorbar(ims, orientation='horizontal')
fig.savefig('figures/parking_map_with_legend.png', dpi=500)
plt.show()

