import torch
import os
import matplotlib.pyplot as plt

import numpy as np


def run_test(env, model, use_perception=False):
    # Test policy without any randomness
    try:
        ac = torch.load(model)
        load_successful = True
    except Exception as e:
        print("Failed to load saved torch file, trying again", e)
        load_successful = False
        
    # # Make sure everyone was able to load the weights
    # if (np.array(MPI.COMM_WORLD.allgather(load_successful)) == False).any():
    #     print("Load failed, try again next time.")
    #     return [0.0] * env.ac_size
    ac.eval()
    env.args.cur = False
    env.args.disturbances = False
    env.args.record_sim = False
    ob = env.reset()
    sp_ac=np.array([[0., 0.],[0., 0.]])
    if use_perception:
        im = env.get_image()
    done = False
    while True:
        if use_perception:
            act, _, _ = ac.step(torch.as_tensor(ob, dtype=torch.float32), torch.as_tensor(im, dtype=torch.float32), stochastic=False)
        else:
            act, _, _ = ac.step(torch.as_tensor(ob, dtype=torch.float32), stochastic=False)
        # ob, rew, done, _= env.step(act,sp_ac)
        if env.args.cloning:
            ob, rew, done, termination, _,exp= env.step(act,sp_ac)
        else:
            ob, rew, done, termination, _= env.step(act,sp_ac)
        if use_perception:
            im = env.get_image()
        if done or env.steps > env.args.max_ep_len:
            break
    # success = env.get_success()
    success = env.success_list
    # # print("success",success)
    # # success=[0,0]
    # successes1 = MPI.COMM_WORLD.allgather(success[0])
    # successes2 = MPI.COMM_WORLD.allgather(success[1])
    env.args.record_sim = True
    # return successes
    # return successes1,successes2
    return success[0],success[1]

def load_and_test(checkpoint_dir):
    success_rates = []
    epochs = []

    # Load all checkpoint files sorted by epoch number
    checkpoint_files = sorted([f for f in os.listdir(checkpoint_dir) if f.endswith('.pth')], key=lambda x: int(x.split('_')[3].split('.')[0]))
    
    for filename in checkpoint_files:
        epoch_number = int(filename.split('_')[3].split('.')[0])
        checkpoint_path = os.path.join(checkpoint_dir, filename)
        checkpoint = torch.load(checkpoint_path)
        
        # Assuming the model setup is known and consistent
        model = YourModel()  # Make sure to define your model class correctly
        model.load_state_dict(checkpoint['state_dict'])
        
        # Test the model
        success_rate = run_test(model)
        success_rates.append(success_rate)
        epochs.append(epoch_number)

    return epochs, success_rates


def plot_success(epochs, success_rates):
    plt.figure(figsize=(10, 5))
    plt.plot(epochs, success_rates, marker='o', linestyle='-', color='b')
    plt.title('Model Success Rate per Epoch')
    plt.xlabel('Epoch')
    plt.ylabel('Success Rate')
    plt.grid(True)
    plt.show()


checkpoint_dir = 'path_to_your_checkpoints'  # Update this path
epochs, success_rates = load_and_test(checkpoint_dir)
plot_success(epochs, success_rates)

