import argparse
import pybullet as p
from assets.env_mocap import EnvExp

def run(args): 

    # env = EnvExp(args=args, frameless=False, master=True)
    # env = EnvExp(args=args, render=args.render, frameless=False, master=True, with_feet=False)
    env = EnvExp(args=args, render=args.render, frameless=False, master=True)

    env.reset()

    print([name + "_target" for name, j in zip(env.motor_names, env.ordered_joints)])

    # joint_target = {}
    # for name, j in zip(env.motor_names, env.ordered_joints):
    #     print(name, j)
    #     joint_target[name] = {'target': p.addUserDebugParameter(name + "_target",j[1],j[2],0)}
    pos_name = ["x", "y", "z"]
    pos_loc = [[0,20,0],[5,5,0],[0,2,1.2]]
    # pos_target = {name: {'pos': p.addUserDebugParameter(name + "_pos", pos_loc[num][0],pos_loc[num][1],pos_loc[num][2])} for num, name in enumerate(pos_name)}
    joint_target = {name: {'target': p.addUserDebugParameter(name + "_target",j[1],j[2],0)} for name, j in zip(env.motor_names, env.ordered_joints)}

    while True:
        orn = [0,0,0,1]
        actions = [0]*env.ac_size
        for i,j in enumerate(env.motor_names):
            actions[i] = p.readUserDebugParameter(joint_target[j]['target'])
        pos = [0,0,0]
        # for i, j in enumerate(pos_name): 
            # pos[i] = p.readUserDebugParameter(pos_target[j]['target'])
	
        env.set_position([0,0,1.2], orn, actions)
        p.stepSimulation()

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--render', default=True, action="store_false")
    parser.add_argument('--perception', default=False, action="store_true")
    parser.add_argument('--urdf', default=False, action="store_true")
    parser.add_argument('--test', default=True, action="store_false")
    args = parser.parse_args()

    run(args)