from assets.env_mocap import EnvExp
import default_arguments

def run(args): 
    env = EnvExp(args=args, render=args.render, master=True)
    env.reset()
    while True:
        env.step()

if __name__=="__main__":
    args = default_arguments.get_defaults() 
    args.render = True
    run(args)