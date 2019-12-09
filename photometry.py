import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
from scipy.signal import savgol_filter
import matplotlib as mpl

fig,axarr = plt.subplots(2,2, figsize=(5,5))

center_pos = (np.round(np.array([8639, 5848])/1000*300)).astype(int)
box_size = 400
image = ndimage.imread('data/optical/reference.tif')
image1 = image[center_pos[1]-box_size:center_pos[1]+box_size,
               center_pos[0]-box_size:center_pos[0]+box_size, :]
image1 = np.sum(image1, axis=2)
image1 = image1 - np.min(image1)
refmax = np.max(image1)
ref_graph = np.copy(image1[box_size,:])
ref_graph = savgol_filter(ref_graph, 31, 2)
# image1 = image[500:, :, :]
axarr[0,0].imshow(image1, cmap='gray', vmax = refmax)
axarr[0,0].axis('off')
axarr[0,0].set_aspect('equal')
axarr[1,0].imshow(image1, cmap='plasma', vmax = refmax)
axarr[1,0].axis('off')
axarr[1,0].set_aspect('equal')

aspects = np.loadtxt('data/optical/aspects.txt', skiprows=1)
# get angles
def get_angles(aspects):
    angles = []
    width_to_height_normal = 150/60
    for n in range(10):
        assert n == aspects[n, 1]
        width, height = aspects[n, 2:4]
        angle_here = np.arccos(width / (height * width_to_height_normal) )
        angles.append(angle_here)
    return np.array(angles)
angles = get_angles(aspects)
print(angles/np.pi*180)
n = 1
box_size = 400
center_pos = (aspects[n,4:]/1000*300).astype(int)
image = ndimage.imread('data/optical/angle_{0:d}.tif'.format(n))
image1 = image[center_pos[1]-box_size:center_pos[1]+box_size,
               center_pos[0]-box_size:center_pos[0]+box_size, :]
image1 = np.sum(image1, axis=2)
image1 = (image1 - np.min(image1))/refmax
test_graph = np.copy(image1[box_size,:])
test_graph = savgol_filter(test_graph, 31, 2)
# image1 = image[500:, :, :]
axarr[0,1].imshow(image1, cmap='gray', vmax = 1)
axarr[0,1].axis('off')
axarr[0,1].set_aspect('equal')
im = axarr[1,1].imshow(image1, cmap='plasma', vmax = 1)
axarr[1,1].axis('off')
axarr[1,1].set_aspect('equal')

# c_ax=plt.subplot(199)
# cb = mpl.colorbar.ColorbarBase(c_ax,orientation='vertical')
# c_ax.yaxis.set_ticks_position('left')
plt.colorbar(im)
fig.savefig('figures/39_deg_example_scale.png', dpi=300)

f2, ax = plt.subplots(figsize=(5.1*0.8,2.5*0.8))
xs = np.linspace(0, 2.2/1.4, ref_graph.shape[0])
ax.plot(xs, ref_graph/np.max(ref_graph)-0.05, label='Источник света')
ax.plot(xs, test_graph, label='Отражение в кассете')
plt.xlabel('Координата, угловые градусы')
plt.ylabel('Интенсивность, отн. ед.')
plt.ylim(0, 1)
# plt.legend()
f2.savefig('figures/comparison_graph.png', dpi=300)
plt.show()