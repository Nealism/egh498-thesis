import argparse
from assets.env_mocap import EnvExp
import numpy as np

def run(args): 
    env = EnvExp(args=args, render=args.render, master=True)
    env.reset()
    env.terrain = np.random.random(env.terrain_size)
    env.load_terrain()
    i = 0
    while True:
        env.step()
        if i > 1000:
            env.reset()
            env.terrain = np.random.random(env.terrain_size)
            env.load_terrain()
            i = 0
        i += 1


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--render', default=True, action="store_false")
    parser.add_argument('--urdf', default=False, action="store_true")
    parser.add_argument('--sleep', default=0.01, type=float)
    args = parser.parse_args()

    run(args)