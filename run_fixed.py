import pybullet as p
import numpy as np
import time

import default_arguments

def run(args): 

    Env, args = default_arguments.get_env(args)   
    args.render = True
    args.test = True
    args.record_sim = False
    args.frameless = False
    env = Env(PATH="", args=args, writer=None)
    env.reset()

    if "pb" in args.env:
        pos_name = ["x", "y", "z"]
        pos_loc = [[0,20,0],[5,5,0],[0,2,1.2]]

        if "franka" in args.env:
            joint_target = {name: {'target': p.addUserDebugParameter(name + "_target",j[1],j[2],i)} for name, j, i in zip(env.motor_names, env.ordered_joints, env.initial_joints)}
            print(env.initial_joints)
            env.insert_sphere()
        else: 
            joint_target = {name: {'target': p.addUserDebugParameter(name + "_target",j[1],j[2],0)} for name, j in zip(env.motor_names, env.ordered_joints)}
        steps = 0

        while True:
            orn = [0,0,0,1]
            actions = [0]*env.ac_size
            for i,j in enumerate(env.motor_names):
                actions[i] = p.readUserDebugParameter(joint_target[j]['target'])
            pos = [0,0,0]
        
            # for i, j in enumerate(pos_name): 
                # pos[i] = p.readUserDebugParameter(pos_target[j]['target'])
            steps += 1            
            env.set_position([0,0,0], orn, actions)
            p.stepSimulation()
            time.sleep(env.simStep)
    else:
        # This doesn't work, not sure how to get the same interaction with Mujoco, for now just importing models into pybullet
        actions = list(np.zeros(env.ac_size))
        env.set_position(actions)

if __name__=="__main__":
    args = default_arguments.get_defaults() 
    run(args)