import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
import json
import pytz
from datetime import datetime

by_mh = np.load('by_mh.npy')

data = np.load('data_by_cams_filtered.npy')
data[10, 6, 17:22] = 0
data_with_clouds = np.copy(data)
for i in range(18):
    for frame in range(40):
        hour_here = int(np.floor(3 + frame/2))
        data_with_clouds[i, :, frame] = data_with_clouds[i, :, frame]*(100-by_mh[:, hour_here])/100

fig1 = plt.figure(1) # , figsize=(3,3)
avg_by_road = np.max(data[12:, :, :], axis=0)
plt.imshow(avg_by_road*100, interpolation='bicubic', cmap='inferno', aspect = 1.5)
plt.yticks(range(12), ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек'])
plt.xticks(range(0, 40, 2), range(3, 24, 1))
plt.xlabel('Время суток, часы')
plt.ylabel('Время года, месяц')
# plt.colorbar()
fig1.savefig('figures/noclouds_nocolorbar_parking.png', dpi=600)
# plt.show()

fig2 = plt.figure(2)
plt.imshow(by_mh, interpolation='bicubic', cmap='inferno', aspect = 0.9, vmin=0, vmax=100)
plt.yticks(range(12), ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек'])
# plt.xticks(range(0, 40, 2), range(3, 24, 1))
plt.xlabel('Время суток, часы')
plt.ylabel('Время года, месяц')
# plt.colorbar()
fig2.savefig('figures/clouds_cover_parking.png', dpi=600)

fig3 = plt.figure(3)
avg_by_road = np.max(data_with_clouds[12:, :, :], axis=0)
plt.imshow(avg_by_road*100, interpolation='bicubic', cmap='inferno', aspect = 1.5, vmax=100)
plt.yticks(range(12), ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек'])
plt.xticks(range(0, 40, 2), range(3, 24, 1))
plt.xlabel('Время суток, часы')
plt.ylabel('Время года, месяц')
# plt.colorbar()
fig3.savefig('figures/with_clouds_parking.png', dpi=600)


print(np.sum(avg_by_road*0.5*30))
plt.show()
print(1)




