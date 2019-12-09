import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
import json
import pytz
from datetime import datetime

def has_refl(target_filename):
    image = ndimage.imread(target_filename, mode='RGB')
    image[image < 50] = 0
    plt.imshow(image)
    maxes = np.amax(image, axis=(0,1))
    means = np.mean(image, axis=(0,1))
    if np.any(maxes > 220):
        if means[2] > means[0] + means[1]:
            return True
        else:
            return False
    else:
        return False

# target_filename = 'data/3d/by_month/03/direct_vB__Camera0080029.jpg'
# target_filename = 'data/3d/by_month/03/direct_vB__Camera0050010.jpg'
# target_filename = 'data/3d/by_month/03/direct_vB__Camera0040040.jpg'


# fig = plt.figure(1)
# months = 2*np.arange(5)
# data_by_cams = []
# for camera_id in 1+np.arange(18):
#     data_for_cam = np.zeros(shape=(12, 40), dtype=float)
#     for month in months:
#         for frame in range(40):
#             target_filename = 'data/3d/by_month/{0:02d}/direct_vB__Camera{1:03d}{2:04d}.jpg'.format(month+1, camera_id, frame)
#             if has_refl(target_filename):
#                 data_for_cam[month, frame] = 1
#     for month in [1,3,5,7,9]:
#         data_for_cam[month] = (data_for_cam[month-1] + data_for_cam[month+1])/2
#     data_for_cam[11] = (data_for_cam[10] + data_for_cam[0]) / 2
#     plt.imshow(data_for_cam)
#     fig.savefig('figures/by_cam/{0:03d}.png'.format(camera_id))
#     plt.cla()
#     data_by_cams.append(np.copy(data_for_cam))
# np.save('data_by_cams_filtered', data_by_cams)
#
# # print(has_refl(target_filename))
# plt.show()


# # ================ Parsing weather data
# with open('data/weather/moscow_weather_history.json') as json_file:
#     wdata = json.load(json_file)
#
# by_mh = list()
# for i in range(12):
#     temp_ = []
#     for j in range(24):
#         temp_.append(list())
#     by_mh.append(temp_.copy())
# for r in wdata:
#     dt = r['dt']
#     clouds = r['clouds']['all']
#     loctime = datetime.fromtimestamp(dt, tz=pytz.timezone('America/New_York'))
#     month = int(loctime.strftime('%m'))
#     hour = int(loctime.strftime('%H'))
#     by_mh[month-1][hour].append(clouds)
# for i in range(12):
#     for j in range(24):
#         temp_ = np.array(by_mh[i][j])
#         by_mh[i][j] = np.mean(temp_)
# # by_mh_2 = np.mean(by_mh, axis=2)
# by_mh = np.array(by_mh)
# np.save('by_mh', by_mh)
# print(1)


## ====================== main plotting

by_mh = np.load('by_mh.npy')

data = np.load('data_by_cams_filtered.npy')
data[10, 6, 17:22] = 0
data_with_clouds = np.copy(data)
for i in range(18):
    for frame in range(40):
        hour_here = int(np.floor(3 + frame/2))
        data_with_clouds[i, :, frame] = data_with_clouds[i, :, frame]*(100-by_mh[:, hour_here])/100

fig1 = plt.figure(1) # , figsize=(3,3)
avg_by_road = np.max(data[:11, :, :], axis=0)
plt.imshow(avg_by_road*100, interpolation='bicubic', cmap='inferno', aspect = 1.5)
plt.yticks(range(12), ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек'])
plt.xticks(range(0, 40, 2), range(3, 24, 1))
plt.xlabel('Время суток, часы')
plt.ylabel('Время года, месяц')
# plt.colorbar()
fig1.savefig('figures/noclouds_nocolorbar.png', dpi=600)
# plt.show()

fig2 = plt.figure(2)
plt.imshow(by_mh, interpolation='bicubic', cmap='inferno', aspect = 0.9, vmin=0, vmax=100)
plt.yticks(range(12), ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек'])
# plt.xticks(range(0, 40, 2), range(3, 24, 1))
plt.xlabel('Время суток, часы')
plt.ylabel('Время года, месяц')
# plt.colorbar()
fig2.savefig('figures/clouds_cover.png', dpi=600)

fig3 = plt.figure(3)
avg_by_road = np.max(data_with_clouds[:11, :, :], axis=0)
plt.imshow(avg_by_road*100, interpolation='bicubic', cmap='inferno', aspect = 1.5, vmax=100)
plt.yticks(range(12), ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек'])
plt.xticks(range(0, 40, 2), range(3, 24, 1))
plt.xlabel('Время суток, часы')
plt.ylabel('Время года, месяц')
# plt.colorbar()
fig3.savefig('figures/with_clouds.png', dpi=600)


print(np.sum(avg_by_road*0.5*30))
plt.show()
print(1)




