import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
from scipy.signal import savgol_filter
import matplotlib as mpl
from scipy.ndimage import gaussian_filter

reflections = np.load('reflections.npy')
angles = np.load('angles.npy')

data = np.vstack((angles, reflections)).T


sorted_data = data[data[:,0].argsort()]
sorted_data = np.delete(sorted_data, 3, 0)


fig = plt.figure(1, figsize=(5,4))
plt.scatter(sorted_data[:,0]/np.pi*180, sorted_data[:,1]*100)


# Fresnel for glass
def get_R_glass(theta_i):
    n1 = 1
    n2 = 1.5
    cos_theta_i = np.cos(theta_i)
    cos_theta_t = np.sqrt(1 - (n1/n2*np.sin(theta_i))**2)
    R_s = ((n1*cos_theta_i - n2*cos_theta_t)/\
          (n1*cos_theta_i + n2*cos_theta_t))**2
    R_p = ((n1*cos_theta_t - n2*cos_theta_i)/\
          (n1*cos_theta_t + n2*cos_theta_i))**2
    rho = (R_p + R_s)/2
    return 2*rho/(1+rho)

xs = np.linspace(np.min(sorted_data[:-1]),
                 np.max(sorted_data[:-1]), 100)
ys = np.array([get_R_glass(x) for x in xs])
plt.plot(xs/np.pi*180, ys*100, color='C1')


fig.savefig('figures/angular_dependence.png', dpi=300)

plt.show()

# np.save('reflections', reflections)
# np.save('angles', angles)
# # c_ax=plt.subplot(199)
# # cb = mpl.colorbar.ColorbarBase(c_ax,orientation='vertical')
# # c_ax.yaxis.set_ticks_position('left')
# plt.colorbar(im)
# # fig.savefig('figures/39_deg_example_scale.png', dpi=300)
#
# f2, ax = plt.subplots(figsize=(5.1*0.8,2.5*0.8))
# xs = np.linspace(0, 2.2, ref_graph.shape[0])
# ax.plot(xs, ref_graph/np.max(ref_graph)-0.05, label='Источник света')
# ax.plot(xs, test_graph, label='Отражение в кассете')
# plt.xlabel('Координата, угловые градусы')
# plt.ylabel('Интенсивность, отн. ед.')
# plt.ylim(0, 1)
# # plt.legend()
# # f2.savefig('figures/comparison_graph.png', dpi=300)
# plt.show()