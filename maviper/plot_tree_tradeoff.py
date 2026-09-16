import numpy as np
import matplotlib.pyplot as plt

depths_rt = [2,3,4,5,6,7,8,9,10,32]
depths_e_titan = [2,3,4,5,6,7,8,9,10,32,34]
depths_e_spot = [2,3,4,5,6,7,8,9,10,32,35]


titan_nodes_rt = [7,15,31,63,127,251,469,845,1423,12669]
titan_mae_rt = [0.387507, 0.315411, 0.269525, 0.237303, 0.218529, 0.199486, 0.184669, 0.171436, 0.163019, 0.161846]
titan_mse_rt = [0.266057, 0.186961, 0.134013, 0.108009, 0.094847, 0.083959, 0.075469, 0.071282, 0.068905, 0.087721]
titan_r2_rt = [0.673283, 0.770506, 0.836543, 0.868497, 0.885043, 0.899642, 0.909776, 0.914913, 0.917184, 0.895669]

spot_nodes_rt = [7, 15, 31, 63, 125, 231, 401, 677, 1105, 12669]
spot_mae_rt = [0.482365, 0.428681, 0.391687, 0.341412, 0.325550, 0.308307, 0.296028, 0.290836, 0.292358, 0.337920]
spot_mse_rt = [0.465540, 0.365941, 0.315619, 0.266715, 0.243458, 0.218691, 0.207582, 0.206480, 0.215829, 0.316552]
spot_r2_rt = [0.401447, 0.498282, 0.569094, 0.688418, 0.713573, 0.751977, 0.765150, 0.771422, 0.768036, 0.670911]

titan_nodes_e = [7,15,31,63,127,255,487,881,1477,12523,12527]
titan_mae_e = [0.421177, 0.359167, 0.306193, 0.291673, 0.261331, 0.260295, 0.260924, 0.254630, 0.267379, 0.283200, 0.285107]
titan_mse_e = [0.287355, 0.206108, 0.167630, 0.161252, 0.133423, 0.138378, 0.141336, 0.137333, 0.153339, 0.170556, 0.171412]
titan_r2_e = [0.668871, 0.758575, 0.806854, 0.814905, 0.848488, 0.844402, 0.841906, 0.846961, 0.828927, 0.809516, 0.808780]

spot_nodes_e = [7,15,31,63,125,241,443,735,1165,12495,12527]
spot_mae_e = [0.458824, 0.407276, 0.362624, 0.330293, 0.309953, 0.293929, 0.288824, 0.279255, 0.284271, 0.344071, 0.337835]
spot_mse_e = [0.447417, 0.350251, 0.282625, 0.252419, 0.227236, 0.210689, 0.213971, 0.204334, 0.211921, 0.301202, 0.288339]
spot_r2_e = [0.436, 0.535328, 0.615371, 0.691180, 0.728561, 0.760975, 0.765169, 0.773989, 0.768330, 0.674952, 0.683413]



#===================
# Random Timestep
#===================
# R2 vs depth

plt.figure()
plt.plot(depths_rt, titan_r2_rt, marker="o", label="Titan")
plt.plot(depths_rt, spot_r2_rt, marker="o", label="Spot")

plt.xlabel("Decision Tree Depth")
plt.ylabel("R2")
plt.title("R2 vs Decision Tree Depth (Random-Timestep)")

plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("maviper/data/r2_vs_depth_rt.png", dpi=300)
plt.show()


# node count vs depth

plt.figure()
plt.plot(depths_rt, titan_nodes_rt, marker="o", label="Titan")
plt.plot(depths_rt, spot_nodes_rt, marker="o", label="Spot")

plt.xlabel("Decision Tree Depth")
plt.ylabel("Node Count")
plt.title("Decision Tree Complexity vs Depth (Random-Timestep)")

plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("maviper/data/nodes_vs_depth_rt.png", dpi=300)
plt.show()

# node count vs r2

plt.figure()
plt.plot(titan_nodes_rt, titan_r2_rt, marker="o", label="Titan")
plt.plot(spot_nodes_rt, spot_r2_rt, marker="o", label="Spot")

plt.xlabel("Decision Tree Complexity")
plt.ylabel("R2")
plt.title("R2 vs Decision Tree Complexity (Random-Timestep)")

plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("maviper/data/r2_vs_nodes_rt.png", dpi=300)
plt.show()


#=================
# Episodic Split
#=================
# R2 vs depth

plt.figure()
plt.plot(depths_e_titan, titan_r2_e, marker="o", label="Titan")
plt.plot(depths_e_spot, spot_r2_e, marker="o", label="Spot")

plt.xlabel("Decision Tree Depth")
plt.ylabel("R2")
plt.title("R2 vs Decision Tree Depth (Episodic Split)")

plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("maviper/data/r2_vs_depth_e.png", dpi=300)
plt.show()


# node count vs depth

plt.figure()
plt.plot(depths_e_titan, titan_nodes_e, marker="o", label="Titan")
plt.plot(depths_e_spot, spot_nodes_e, marker="o", label="Spot")

plt.xlabel("Decision Tree Depth")
plt.ylabel("Node Count")
plt.title("Decision Tree Complexity vs Depth (Episodic Split)")

plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("maviper/data/nodes_vs_depth_e.png", dpi=300)
plt.show()

# node count vs r2

plt.figure()
plt.plot(titan_nodes_e, titan_r2_e, marker="o", label="Titan")
plt.plot(spot_nodes_e, spot_r2_e, marker="o", label="Spot")

plt.xlabel("Decision Tree Complexity")
plt.ylabel("R2")
plt.title("R2 vs Decision Tree Complexity (Episodic Split)")

plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("maviper/data/r2_vs_nodes_e.png", dpi=300)
plt.show()