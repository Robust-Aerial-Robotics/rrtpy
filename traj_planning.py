#%%
import sys
import os
sys.path.insert(0, os.getcwd())
import bswarm.trajectory as tgen
import numpy as np
import json
import matplotlib.pyplot as plt
import rrt

with open('rrt_result.csv', 'r') as f:
    lines = f.readlines()

M = []
for line in lines:
    values = line.split(',')
    row1 = [0,0,0,values[3]]
    row = []
    for value in values:
        row.append(value)
    M.append(row)
final_row = [row[0], row[1], 0, row[3]]
M.append(final_row)
M.insert(0, row1)

waypoints = np.array(M)
    # x, y, z, yaw

T = 10*np.ones(len(waypoints) - 1)
traj = tgen.min_snap_4d(waypoints, T, stop=True)
res = traj.compute_inputs()
print(res.max_data())

#%%
plt.figure()
tgen.plot_trajectories([traj])
plt.show()

#%%
#plt.figure()
#tgen.plot_trajectory_derivatives([traj])
#plt.show()

data = tgen.trajectories_to_json([traj])

#%%
check_with_other_library = True
if check_with_other_library:
    try:
        import bswarm.third_party.plot_trajectory as other
        traj.write_csv('test_data.csv')
        other.plot_uav_trajectory('test_data.csv')
        plt.show()
    except ImportError:
        print('requires plot_uav_trajectory module')

with open('testPlan.json', 'w') as f:
    json.dump(data, f)