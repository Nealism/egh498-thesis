import numpy as np
import torch
from torch.optim import Adam
import gym
import time
import models.core as core
from utils.logx import EpochLogger
from utils.mpi_pytorch import setup_pytorch_for_mpi, sync_params, mpi_avg_grads
from utils.mpi_tools import mpi_fork, mpi_avg, proc_id, mpi_statistics_scalar, num_procs
from collections import deque
from mpi4py import MPI
comm = MPI.COMM_WORLD
import os
import psutil
import pandas as pd
import default_arguments
import cv2
from gym import spaces
import torch.nn as nn


from scipy.ndimage import label, generate_binary_structure

import time
import matplotlib.pyplot as plt
import os

argus = default_arguments.get_defaults() 


class PPOBufferPerception:
    """
    A buffer for storing trajectories experienced by a PPO agent interacting
    with the environment, and using Generalized Advantage Estimation (GAE-Lambda)
    for calculating the advantages of state-action pairs.
    """

    def __init__(self, ob_size, im_size, ac_size, size, gamma=0.99, lam=0.95):
        # print("PPO_AC",ac_size)
        self.obs_buf = np.zeros(core.combined_shape(size, ob_size), dtype=np.float32)
        #print("im_size",type(im_size))
        self.im_buf = np.zeros(core.combined_shape(size, im_size), dtype=np.float32)
        #print("im_size_after",self.im_buf)
        self.act_buf = np.zeros(core.combined_shape(size, ac_size), dtype=np.float32)
        self.adv_buf = np.zeros(size, dtype=np.float32)
        self.rew_buf = np.zeros(size, dtype=np.float32)
        self.ret_buf = np.zeros(size, dtype=np.float32)
        self.val_buf = np.zeros(size, dtype=np.float32)
        self.logp_buf = np.zeros(size, dtype=np.float32)
        if argus.cloning:
            self.exp_buf = np.zeros(core.combined_shape(size, ac_size), dtype=np.float32)
        self.gamma, self.lam = gamma, lam
        self.ptr, self.path_start_idx, self.max_size = 0, 0, size

    def store(self, obs, im, act, rew, val, logp, exp=0):
        """
        Append one timestep of agent-environment interaction to the buffer.
        """
        assert self.ptr < self.max_size     # buffer has to have room so you can store
        #print("store_im",im)
        # print("PPO_STORE!",self.act_buf[self.ptr] )
        # print("PPO_Store_act",act)
        # print("act",type(act),act)
        # print("exp",type(exp),exp)
        self.obs_buf[self.ptr] = obs
        self.im_buf[self.ptr] = im
        self.act_buf[self.ptr] = act
        self.rew_buf[self.ptr] = rew
        self.val_buf[self.ptr] = val
        self.logp_buf[self.ptr] = logp
        if argus.cloning:
            self.exp_buf[self.ptr] = exp
        self.ptr += 1

    def finish_path(self, last_val=0):
        """
        Call this at the end of a trajectory, or when one gets cut off
        by an epoch ending. This looks back in the buffer to where the
        trajectory started, and uses rewards and value estimates from
        the whole trajectory to compute advantage estimates with GAE-Lambda,
        as well as compute the rewards-to-go for each state, to use as
        the targets for the value function.

        The "last_val" argument should be 0 if the trajectory ended
        because the agent reached a terminal state (died), and otherwise
        should be V(s_T), the value function estimated for the last state.
        This allows us to bootstrap the reward-to-go calculation to account
        for timesteps beyond the arbitrary episode horizon (or epoch cutoff).
        """

        path_slice = slice(self.path_start_idx, self.ptr)
        rews = np.append(self.rew_buf[path_slice], last_val)
        vals = np.append(self.val_buf[path_slice], last_val)
        
        # the next two lines implement GAE-Lambda advantage calculation
        deltas = rews[:-1] + self.gamma * vals[1:] - vals[:-1]
        self.adv_buf[path_slice] = core.discount_cumsum(deltas, self.gamma * self.lam)
        
        # the next line computes rewards-to-go, to be targets for the value function
        self.ret_buf[path_slice] = core.discount_cumsum(rews, self.gamma)[:-1]
        
        self.path_start_idx = self.ptr

    def get(self):
        """
        Call this at the end of an epoch to get all of the data from
        the buffer, with advantages appropriately normalized (shifted to have
        mean zero and std one). Also, resets some pointers in the buffer.
        """
        assert self.ptr == self.max_size    # buffer has to be full before you can get
        self.ptr, self.path_start_idx = 0, 0
        # the next two lines implement the advantage normalization trick
        adv_mean, adv_std = mpi_statistics_scalar(self.adv_buf)
        self.adv_buf = (self.adv_buf - adv_mean) / adv_std

        if argus.cloning:
            data = dict(obs=self.obs_buf, im=self.im_buf, act=self.act_buf, ret=self.ret_buf,
                        adv=self.adv_buf, logp=self.logp_buf,exp=self.exp_buf)
            
        else:
            data = dict(obs=self.obs_buf, im=self.im_buf, act=self.act_buf, ret=self.ret_buf,
                        adv=self.adv_buf, logp=self.logp_buf)
        return {k: torch.as_tensor(v, dtype=torch.float32) for k,v in data.items()}



class PPOBuffer:
    """
    A buffer for storing trajectories experienced by a PPO agent interacting
    with the environment, and using Generalized Advantage Estimation (GAE-Lambda)
    for calculating the advantages of state-action pairs.
    """

    def __init__(self, ob_size, ac_size, size, gamma=0.99, lam=0.95):
        self.obs_buf = np.zeros(core.combined_shape(size, ob_size), dtype=np.float32)
        self.act_buf = np.zeros(core.combined_shape(size, ac_size), dtype=np.float32)
        self.adv_buf = np.zeros(size, dtype=np.float32)
        self.rew_buf = np.zeros(size, dtype=np.float32)
        self.ret_buf = np.zeros(size, dtype=np.float32)
        self.val_buf = np.zeros(size, dtype=np.float32)
        self.logp_buf = np.zeros(size, dtype=np.float32)
        self.gamma, self.lam = gamma, lam
        self.ptr, self.path_start_idx, self.max_size = 0, 0, size

    def store(self, obs, act, rew, val, logp):
        """
        Append one timestep of agent-environment interaction to the buffer.
        """
        #print("ptr store",self.ptr,self.max_size, self)
        assert self.ptr < self.max_size     # buffer has to have room so you can store
        self.obs_buf[self.ptr] = obs
        self.act_buf[self.ptr] = act
        self.rew_buf[self.ptr] = rew
        self.val_buf[self.ptr] = val
        self.logp_buf[self.ptr] = logp
        self.ptr += 1

    def finish_path(self, last_val=()):
        """
        Call this at the end of a trajectory, or when one gets cut off
        by an epoch ending. This looks back in the buffer to where the
        trajectory started, and uses rewards and value estimates from
        the whole trajectory to compute advantage estimates with GAE-Lambda,
        as well as compute the rewards-to-go for each state, to use as
        the targets for the value function.

        The "last_val" argument should be 0 if the trajectory ended
        because the agent reached a terminal state (died), and otherwise
        should be V(s_T), the value function estimated for the last state.
        This allows us to bootstrap the reward-to-go calculation to account
        for timesteps beyond the arbitrary episode horizon (or epoch cutoff).
        """
        #print("rw buf",self.rew_buf,type(self.rew_buf))
        #print("only self",self, 'lastval',last_val)
        #print("Debug",self)
        path_slice = slice(self.path_start_idx, self.ptr)
        #print("path_slice_shape",type(path_slice), path_slice, "adv_buff",self.adv_buf,self.adv_buf.shape)
        #print("last_val",last_val)
        rews = np.append(self.rew_buf[path_slice], last_val)
        vals = np.append(self.val_buf[path_slice], last_val)
        #print("owch",self,rews.shape,vals.shape)
        
        
        # the next two lines implement GAE-Lambda advantage calculation
        deltas = rews[:-1] + self.gamma * vals[1:] - vals[:-1]
        #print("rews[:-1]",rews[:-1],"val[1:]",vals[1:],"vals[:-1]",vals[:-1],"deltas_shape",deltas.shape)
        self.adv_buf[path_slice] = core.discount_cumsum(deltas, self.gamma * self.lam)

        # the next line computes rewards-to-go, to be targets for the value function
        self.ret_buf[path_slice] = core.discount_cumsum(rews, self.gamma)[:-1]
        #print("finishinfg",self,len(self.adv_buf),len(self.ret_buf))
        
        
        self.path_start_idx = self.ptr


    

    def get(self):
        """
        Call this at the end of an epoch to get all of the data from
        the buffer, with advantages appropriately normalized (shifted to have
        mean zero and std one). Also, resets some pointers in the buffer.
        """

        #print("check prt buffer",self.ptr, self.max_size, self)
        
        assert self.ptr == self.max_size    # buffer has to be full before you can get
        self.ptr, self.path_start_idx = 0, 0

        # the next two lines implement the advantage normalization trick
        adv_mean, adv_std = mpi_statistics_scalar(self.adv_buf)
        self.adv_buf = (self.adv_buf - adv_mean) / adv_std


        #print("get",self,self.obs_buf,self.act_buf,self.ret_buf,self.adv_buf,self.logp_buf)

        
        data = dict(obs=self.obs_buf, act=self.act_buf, ret=self.ret_buf,
                    adv=self.adv_buf, logp=self.logp_buf)
        #print("data",data)
        #print("return",{k: torch.as_tensor(v, dtype=torch.float32) for k,v in data.items()})
        
        return {k: torch.as_tensor(v, dtype=torch.float32) for k,v in data.items()}
    
class MA_PPOBuffer:
        def __init__(self, ob_size, ac_size, size, gamma=0.99, lam=0.95, num_robots=None):
            #self.args = args
            #self.ptr, self.path_start_idx, self.max_size = 0, 0, size
            #self.ptr, self.path_start_idx, self.max_size = 0, 0, size
            # for ac_s in ac_size:
            self.buffers=tuple([PPOBuffer(ob_size, ac_size, size, gamma=gamma, lam=lam) for Robot in range(num_robots)])
            
            
            
        def store(self, obs, acts, rews, vals, logps):
            
            #num_robots=tuple(range(num_robots))
            #print(num_robots,type(num_robots))
            #for Robot in range(num_robots):
            #robot_id_number=tuple(range(num_robots))
            for buffer, ob, act,rew,val,logp in zip(self.buffers, tuple(obs),tuple(acts),tuple(rews),tuple(vals.tolist()),tuple(logps.tolist())):
                    #self.ptr += 1
                #print("store buffer.ptr",buffer.ptr)
                #print(buffer,Robot,rew)
                #print("bf",buffer,"ob", ob, "act",act,"rw",rew,"vl",val,"lgp",logp)
                #print("buffer store",buffer.store(ob,act,rew,val,logp))
                #print("ob_size_mabuf",len(tuple(obs)))
                buffer.store(ob,act,rew,val,logp)
            

        def finish_path(self, last_vals=()):
            #print("initial_lastval",[last_vals],type([last_vals]))
            #robot_id_number=tuple(range(num_robots))
            #print("early last vals v",tuple(last_vals), type(last_vals))
            #print("Life is full of problems,",last_vals.detach().numpy())

            for buffer, last_val in zip(self.buffers,last_vals):
                #print(buffer,Robot,rew)
                #print("MA",self.buffers,last_vals)
                #print("MA_Single",buffer, last_val,Robot)
                #print("f_buf",buffer, "type1",type(buffer), "f_self_buf",self.buffers)


                #print("fininsh path",buffer.finish_path(last_val))
                buffer.finish_path(last_val)

        
        def get(self,num_robots=None):
            
            get_list=[]
            buffer_list=[]
            robot_id_number=tuple(range(num_robots))
            for buffer,Robot in zip(self.buffers,robot_id_number):
                #print("g_buf",buffer,"type1",type(buffer), "r", Robot)
                #print("buf_get",buffer.get())
                #print("self",self,"buf",buffer, "self buf",self.buffers)
                #print("buf_get",buffer.get())
                #print(buffer)
                b=buffer
                p=buffer.get()
                get_list.append(p)
                buffer_list.append(b)
                #print(p)
                #print("getting list", get_list)
            return get_list
                

class MA_PPOBufferPerception:
        def __init__(self, ob_size,im_size, ac_size, size, gamma=0.99, lam=0.95, num_robots=None):
            #self.args = args
            #self.ptr, self.path_start_idx, self.max_size = 0, 0, size
            #self.ptr, self.path_start_idx, self.max_size = 0, 0, size
            #print("im",type(im_size))
            # print("ac_size",ac_size)
            # for buffer, ob,im, act,rew,val,logp in zip(self.buffers, tuple(obs),tuple(im),tuple(acts),tuple(rews),tuple(vals.tolist()),tuple(logps.tolist())):
            
            
            
            
            # print("MA_AC",ac_size)
            # print(self);exit()
            if argus.heterogeneous or argus.titanheads or argus.IHPPO:
                self.buffer1=PPOBufferPerception(ob_size,im_size, ac_size[0], size, gamma=gamma, lam=lam)
                self.buffer2=PPOBufferPerception(ob_size,im_size, ac_size[1], size, gamma=gamma, lam=lam)
                self.buffers=self.buffer1,self.buffer2
                # self.buffers=[PPOBufferPerception(ob_size,im_size, ac_size[0], size, gamma=gamma, lam=lam)]
            else:
                self.buffers=tuple([PPOBufferPerception(ob_size,im_size, ac_size, size, gamma=gamma, lam=lam) for Robot in range(num_robots)])
            # # print("self.buffers",self.buffers,type(self.buffers))

            # # # self.buffers [(<models.ppo_MA.PPOBufferPerception object at 0x7fd8566ec8b0>,), (<models.ppo_MA.PPOBufferPerception object at 0x7fd8566ec910>,)]
            
            # # # for ac_s in ac_size:
            # # # self.buffers=tuple([PPOBuffer(ob_size, ac_s, size, gamma=gamma, lam=lam) for ac_s in ac_size])

            # # # print("b",tuple(self.buffers), type(self.buffers))
            # # print("b",tuple(self.buffers), type(self.buffers))
            
            
        def store(self, obs,im, acts, rews, vals, logps, exps=[]):
            
            #num_robots=tuple(range(num_robots))
            #print(num_robots,type(num_robots))
            #for Robot in range(num_robots):
            #robot_id_number=tuple(range(num_robots))
            # print("check",len((obs)),len((im)),len((acts)),len((rews)),len((vals.tolist())),len((logps)),(rews[1]))
            # # for buffer, ob,im, act,rew,val,logp in zip(self.buffers, tuple(obs[1]),tuple(im[1]),tuple(acts[1]),tuple(rews[1]),tuple(vals.tolist()[1]),tuple(logps[1])):
            if argus.cloning:
                for buffer, ob,im, act,rew,val,logp,exp in zip(self.buffers, tuple(obs),tuple(im),tuple(acts),tuple(rews),tuple(vals.tolist()),tuple(logps),exps):
                    buffer.store(ob,im,act,rew,val,logp,exp)
            else:
            
                for buffer, ob,im, act,rew,val,logp in zip(self.buffers, tuple(obs),tuple(im),tuple(acts),tuple(rews),tuple(vals.tolist()),tuple(logps)):
                    buffer.store(ob,im,act,rew,val,logp)
                    #self.ptr += 1
                # km= buffer, ob,im, act,rew,val,logp
                # print("store_arguments", buffer, ob,im, act,rew,val,logp,len(km))
                # print("store_acts",act)
                #print("store buffer.ptr",buffer.ptr)
                #print(buffer,Robot,rew)
                #print("bf",buffer,"ob", ob, "act",act,"rw",rew,"vl",val,"lgp",logp)
                #print("buffer store",buffer.store(ob,act,rew,val,logp))
                #print("ob_size_mabuf",len(tuple(obs)))

                
            # self.buffers[0].store(obs[1],im[1],acts[1],rews[1],vals[1],logps[1])
            
            
            # print(buffer.store);exit()
            

        def finish_path(self, last_vals=()):
            #print("initial_lastval",[last_vals],type([last_vals]))
            #robot_id_number=tuple(range(num_robots))
            #print("early last vals v",tuple(last_vals), type(last_vals))
            #print("Life is full of problems,",last_vals.detach().numpy())

            for buffer, last_val in zip(self.buffers,last_vals):
                #print(buffer,Robot,rew)
                #print("MA",self.buffers,last_vals)
                #print("MA_Single",buffer, last_val,Robot)
                #print("f_buf",buffer, "type1",type(buffer), "f_self_buf",self.buffers)


                #print("fininsh path",buffer.finish_path(last_val))
                buffer.finish_path(last_val)

        
        def get(self,num_robots=None):
            
            get_list=[]
            buffer_list=[]
            robot_id_number=tuple(range(num_robots))
            for buffer,Robot in zip(self.buffers,robot_id_number):
                #print("g_buf",buffer,"type1",type(buffer), "r", Robot)
                #print("buf_get",buffer.get())
                #print("self",self,"buf",buffer, "self buf",self.buffers)
                #print("buf_get",buffer.get())
                #print(buffer)
                b=buffer
                p=buffer.get()
                get_list.append(p)
                buffer_list.append(b)
                #print(p)
                #print("getting list", get_list)
            return get_list
                # getting=getting.append(buffer.get())
                # #print("buf_get",buffer.get())
                # #return buffer.get()
                # return getting


#changed save freq 10 to 1 to save at each epoch
def ppo(env, ac_kwargs=dict(), seed=0, 
        steps_per_epoch=4000, epochs=50, gamma=0.99, clip_ratio=0.2, pi_lr=3e-4,
        vf_lr=1e-3, train_pi_iters=100, train_v_iters=100, lam=0.97, max_ep_len=2048, local_epoch_len=2048,
        target_kl=0.01, logger_kwargs=dict(), save_freq=10, PATH=None, writer=None, use_perception=False, load_path="",robot_number=None):
    """
    Proximal Policy Optimization (by clipping), 

    with early stopping based on approximate KL

    Args:
        env_fn : A function which creates a copy of the environment.
            The environment must satisfy the OpenAI Gym API.

        actor_critic: The constructor method for a PyTorch Module with a 
            ``step`` method, an ``act`` method, a ``pi`` module, and a ``v`` 
            module. The ``step`` method should accept a batch of observations 
            and return:

            ===========  ================  ======================================
            Symbol       Shape             Description
            ===========  ================  ======================================
            ``a``        (batch, ac_size)  | Numpy array of actions for each 
                                           | observation.
            ``v``        (batch,)          | Numpy array of value estimates
                                           | for the provided observations.
            ``logp_a``   (batch,)          | Numpy array of log probs for the
                                           | actions in ``a``.
            ===========  ================  ======================================

            The ``act`` method behaves the same as ``step`` but only returns ``a``.

            The ``pi`` module's forward call should accept a batch of 
            observations and optionally a batch of actions, and return:

            ===========  ================  ======================================
            Symbol       Shape             Description
            ===========  ================  ======================================
            ``pi``       N/A               | Torch Distribution object, containing
                                           | a batch of distributions describing
                                           | the policy for the provided observations.
            ``logp_a``   (batch,)          | Optional (only returned if batch of
                                           | actions is given). Tensor containing 
                                           | the log probability, according to 
                                           | the policy, of the provided actions.
                                           | If actions not given, will contain
                                           | ``None``.
            ===========  ================  ======================================

            The ``v`` module's forward call should accept a batch of observations
            and return:

            ===========  ================  ======================================
            Symbol       Shape             Description
            ===========  ================  ======================================
            ``v``        (batch,)          | Tensor containing the value estimates
                                           | for the provided observations. (Critical: 
                                           | make sure to flatten this!)
            ===========  ================  ======================================


        ac_kwargs (dict): Any kwargs appropriate for the ActorCritic object 
            you provided to PPO.

        seed (int): Seed for random number generators.

        steps_per_epoch (int): Number of steps of interaction (state-action pairs) 
            for the agent and the environment in each epoch.

        epochs (int): Number of epochs of interaction (equivalent to
            number of policy updates) to perform.

        gamma (float): Discount factor. (Always between 0 and 1.)

        clip_ratio (float): Hyperparameter for clipping in the policy objective.
            Roughly: how far can the new policy go from the old policy while 
            still profiting (improving the objective function)? The new policy 
            can still go farther than the clip_ratio says, but it doesn't help
            on the objective anymore. (Usually small, 0.1 to 0.3.) Typically
            denoted by :math:`\epsilon`. 

        pi_lr (float): Learning rate for policy optimizer.

        vf_lr (float): Learning rate for value function optimizer.

        train_pi_iters (int): Maximum number of gradient descent steps to take 
            on policy loss per epoch. (Early stopping may cause optimizer
            to take fewer than this.)

        train_v_iters (int): Number of gradient descent steps to take on 
            value function per epoch.

        lam (float): Lambda for GAE-Lambda. (Always between 0 and 1,
            close to 1.)

        max_ep_len (int): Maximum length of trajectory / episode / rollout.

        target_kl (float): Roughly what KL divergence we think is appropriate
            between new and old policies after an update. This will get used 
            for early stopping. (Usually small, 0.01 or 0.05.)

        logger_kwargs (dict): Keyword args for EpochLogger.

        save_freq (int): How often (in terms of gap between epochs) to save
            the current policy and value function.

    """
    if env.args.cloning:
        save_freq=1
    # Special function to avoid certain slowdowns from PyTorch + MPI combo.
    setup_pytorch_for_mpi()

    lenbuffers = [deque(maxlen=100) for _ in range(robot_number)] # rolling buffer for episode lengths
    # rewbuffer = deque(maxlen=100) # rolling buffer for episode rewards
    rewbuffers = [deque(maxlen=100) for _ in range(robot_number)] # rolling buffer for episode rewards

    # Set up logger and save configuration
    loggers = [EpochLogger(**logger_kwargs) for _ in range(robot_number)]
    # TODO: Can't save locals() if using robotics toolbox (needed for joint goal), need to fix this, don't need to save all "locals()"
    # logger.save_config(locals())
    # base_model_path="/home/kom018/behaviour_rl/Saved_models/Turtle_titan/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/model.pt"
    base_model_path="/home/kom018/behaviour_rl/Saved_models/Turtle_titan/choosen_models/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/model.pt"
    
    base_model=torch.load(base_model_path)

    # if env.args.transfer_learning:
    #     for name, param in base_model.named_parameters():
    #         if 'weight' in name:  # Filter to get only weights, not biases
    #             # std_dev = torch.std(param.data)  
    #             std_dev = param.data

    # # print("Base_STD",std_dev) 

    # print("BAAAAAAAAAAAAAAAAAAAAA",base_model.pi.std);exit()

    model_mu=torch.load("/home/kom018/behaviour_rl/Saved_models/Turtle_titan/choosen_models/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/mu_net_simul.jit")
    model_z=torch.load("/home/kom018/behaviour_rl/Saved_models/Turtle_titan/choosen_models/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/z_net_simul.jit")
    # print(model_mu,"model_mu")
    # Random seed
    seed += 10000 * proc_id()
    torch.manual_seed(seed)
    np.random.seed(seed)

    # ob_size = env.observation_space.shape
    # ac_size = env.action_space.shape
    

    if env.args.heterogeneous or env.args.titanheads:
        # print("OB",env.ob_size)
        ob_size = (env.ob_size,)
        ac_size = tuple(env.ac_size)
    else:
        ob_size = env.observation_space.shape
        ac_size = env.action_space.shape
    # print(ob_size,ac_size,type(ob_size),type(ac_size));exit()
    # print("obs",env.observation_space,"action",env.action_space)
    
    # print(base_model.pi)
    # Create actor-critic module
    if use_perception:
        actor_critic=core.MLPActorCriticPerception
        im_size = env.im_size

        
        
        if load_path != "":
            ac = torch.load(load_path)
            print("Loading saved weights: ", load_path)


        
                        
        elif env.args.transfer_learning:
            ac = actor_critic(base_model, env.observation_space, im_size, env.action_space, **ac_kwargs)
            # ac = torch.load(base_model_path)
            # print("ac",ac)
            
            # print("self.pi",ac.pi.z_net)
            if not env.args.freezing_off:
                for param in ac.pi.z_net.parameters():
                    param.requires_grad = False
                if env.args.heterogeneous or env.args.titanheads:

                    for param in ac.pi.feature_layers.parameters():
                        param.requires_grad = False

                    


                    if env.args.spot_additional_layer:
                        for param in ac.pi.spot_additional_layer.parameters():
                            param.requires_grad = False

                    # for param in ac.pi.spot_output_layer.parameters():
                    #     param.requires_grad = True
                    if env.args.titan_frozen_layer:
                        for param in ac.pi.titan_output_layer.parameters():
                            param.requires_grad = False

                    if env.args.spot_frozen_layer:
                        for param in ac.pi.spot_output_layer.parameters():
                            param.requires_grad = False

                if env.args.multi_titans:
                    for param in ac.pi.mu_net.parameters():
                        param.requires_grad = False

            
        else:
            ac = actor_critic(None, env.observation_space, im_size, env.action_space, **ac_kwargs)
        # print("ac",ac);exit()
        # for name, param in ac.pi.named_parameters():
        #     if param.requires_grad:
        #         print(name, param.data)
            
        train_pi_iters = 10
        train_v_iters = 10
    else:    
        actor_critic=core.MLPActorCritic
        if load_path != "":
            ac = torch.load(load_path)
            print("Loading saved weights: ", load_path)
        # elif env.args.transfer_learning:
        #     ac = actor_critic(base_model, env.observation_space, env.action_space, **ac_kwargs)
        else:
            ac = actor_critic(env.observation_space, env.action_space, **ac_kwargs)


        
            # print("AC",ac);exit()
        train_pi_iters = 100
        train_v_iters = 100

    # Sync params across processes
    sync_params(ac)

    # Count variables
    var_counts = tuple(core.count_vars(module) for module in [ac.pi, ac.v])
    # logger.log('\nNumber of parameters: \t pi: %d, \t v: %d\n'%var_counts)

    # Set up experience buffer
    # local_steps_per_epoch = int(steps_per_epoch / num_procs())
    local_steps_per_epoch = local_epoch_len
    #print(local_steps_per_epoch)
    steps_per_epoch = local_epoch_len * num_procs()
    if use_perception:
        #print("type",im_size)
        # print("ob_size",ob_size,(ob_size[0]+1,))
        buf = MA_PPOBufferPerception(ob_size, im_size, ac_size, local_steps_per_epoch, gamma, lam, robot_number)
    else:
        buf = MA_PPOBuffer(ob_size, ac_size, local_steps_per_epoch, gamma, lam, robot_number)
    #print("buf",buf)
    # Set up function for computing PPO policy loss
    def compute_loss_pi(data):

        if env.args.cloning:
            if use_perception:
                obs, im, act, adv, logp_old,exp= data['obs'], data['im'], data['act'], data['adv'], data['logp'],data['exp']
            else:
                obs, act, adv, logp_old = data['obs'], data['act'], data['adv'], data['logp']
            # print("EXP",len(exp),len(act))
        else:
            if use_perception:
                obs, im, act, adv, logp_old= data['obs'], data['im'], data['act'], data['adv'], data['logp']
            else:
                obs, act, adv, logp_old = data['obs'], data['act'], data['adv'], data['logp']

        # exps=data['exp']
        
        # print( " data['act']",data['act']);exit()
        # Policy loss
        # ac_space=spaces.Box(-10000.0, 10000.0, (len(act[0]),))
        # ac_space=spaces.Box(-10000.0, 10000.0, (len(act[0]),))
        # if env.args.heterogeneous or env.args.titanheads:
        # ac = actor_critic(env.observation_space, im_size, ac_space, **ac_kwargs)
        # print("obs",len(obs),env.observation_space,env.action_space,ac_space,len(act),len(act[0]),len(act[1]),act)
        # print(act,len(act[0]))
        # print(obs)
        
        if use_perception:
            # if (env.args.heterogeneous or env.args.titanheads or env.args.IHPPO) and not env.args.multi_titans:
            #     ac = actor_critic(env.observation_space, im_size, ac_space, **ac_kwargs)
            # else:
            #     ac = actor_critic(env.observation_space, im_size, env.action_space, **ac_kwargs)
            # if env.args.separate_node and "spot" in str(env.robots[1]):

            #     # if "titan" in str(env.robots[0]):
            #     print("ENv",str(env.robots[0]))
            #     pi, logp_linang,logp_lat = ac.pi(obs, im, act)
            # else:
            pi, logp = ac.pi(obs, im, act)
            # pi_spot,pi_titan, logp_spot,logp_titan = ac.pi(obs, im, act)
        else:
            pi, logp = ac.pi(obs, act)

        
        # print("AC.PI",pi)
        # if isinstance(logp, list):
        #     # print(type(logp),type(logp_old))
        #     ratio_linang = torch.exp(logp[0] - logp_old)
        #     ratio_lat = torch.exp(logp[1] - logp_old)
        #     clip_adv_linang = torch.clamp(ratio_linang, 1-clip_ratio, 1+clip_ratio) * adv
        #     clip_adv_lat = torch.clamp(ratio_lat, 1-clip_ratio, 1+clip_ratio) * adv
        #     loss_pi_linang = -(torch.min(ratio_linang * adv, clip_adv_linang)).mean()
        #     loss_pi_lat = -(torch.min(ratio_lat * adv, clip_adv_lat)).mean()
        #     loss_pi = (loss_pi_linang + loss_pi_lat) / 2
        #     # print("loss",loss_pi_linang,loss_pi_lat,loss_pi)

        #     # Useful extra info
        #     approx_kl_linang = (logp_old - logp[0]).mean().item()
        #     approx_kl_lat = (logp_old - logp[1]).mean().item()
        #     approx_kl = (approx_kl_linang + approx_kl_lat) / 2
        #     ent_linang = pi[0].entropy().mean().item()
        #     ent_lat = pi[0].entropy().mean().item()
        #     ent=(ent_linang + ent_lat) / 2
        #     clipped_linang = ratio_linang.gt(1+clip_ratio) | ratio_linang.lt(1-clip_ratio)
        #     clipped_lat = ratio_lat.gt(1+clip_ratio) | ratio_lat.lt(1-clip_ratio)
        #     clipfrac_linang = torch.as_tensor(clipped_linang, dtype=torch.float32).mean().item()
        #     clipfrac_lat = torch.as_tensor(clipped_lat, dtype=torch.float32).mean().item()
        #     clipfrac = (clipfrac_linang + clipfrac_lat) / 2
        #     pi_info = dict(kl=approx_kl, ent=ent, cf=clipfrac)
        if env.args.cloning:
            predicted_action_deterministic = ac.pi.mu
            # print("predicted_action_deterministic",predicted_action_deterministic)
            criterion = nn.MSELoss()
            # print("EXP",exp,act)
            loss_clone = criterion(predicted_action_deterministic, exp)
            # print("lc",((predicted_action_deterministic - exp)**2).mean(),loss_clone)
            # mse_loss = loss_clone / (loss_clone.detach().mean() + 1e-6)  # Normalise

            # print("MSE", mse_loss)
        # else:
        ratio = torch.exp(logp - logp_old)
        clip_adv = torch.clamp(ratio, 1-clip_ratio, 1+clip_ratio) * adv
        
        if env.args.cloning:
            loss_pi=loss_clone
        else:
            
            loss_pi = -(torch.min(ratio * adv, clip_adv)).mean()


        # print("loss",loss_pi)
        # Useful extra info
        approx_kl = (logp_old - logp).mean().item()
        ent = pi.entropy().mean().item()
        clipped = ratio.gt(1+clip_ratio) | ratio.lt(1-clip_ratio)
        clipfrac = torch.as_tensor(clipped, dtype=torch.float32).mean().item()
        pi_info = dict(kl=approx_kl, ent=ent, cf=clipfrac)

        return loss_pi, pi_info

    # Set up function for computing value loss
    def compute_loss_v(data):
        if use_perception:
            obs, im, ret = data['obs'], data['im'], data['ret']
            # print("critic_loss",((ac.v(obs, im) - ret)**2).mean())
            return ((ac.v(obs, im) - ret)**2).mean()
        else: 
            obs, ret = data['obs'], data['ret']
            return ((ac.v(obs) - ret)**2).mean()

    # Set up optimizers for policy and value function
    # optimizer = Adam(list(ac.pi.parameters()) + list(ac.v.parameters()), lr=pi_lr)
    pi_optimizer = Adam(ac.pi.parameters(), lr=pi_lr)
    vf_optimizer = Adam(ac.v.parameters(), lr=vf_lr)

    # Set up model saving
    # logger.setup_pytorch_saver(ac)

    


    def update(data, epoch, logger):

        
        pi_l_old, pi_info_old = compute_loss_pi(data)
        pi_l_old = pi_l_old.item()
        v_l_old = compute_loss_v(data).item()

        for g in pi_optimizer.param_groups:
            g['lr'] = max((1 - epoch / epochs) * pi_lr, 0.000001)

        for g in vf_optimizer.param_groups:
            g['lr'] = max((1 - epoch / epochs) * vf_lr, 0.000001)

        # Train policy with multiple steps of gradient descent
        for i in range(train_pi_iters):
            pi_optimizer.zero_grad()
            loss_pi, pi_info = compute_loss_pi(data)
            kl = mpi_avg(pi_info['kl'])
            if kl > 1.5 * target_kl:
                logger.log('Early stopping at step %d due to reaching max kl.'%i)
                break
            loss_pi.backward()
            # print(ac.pi);exit()
            mpi_avg_grads(ac.pi)    # average grads across MPI processes
            pi_optimizer.step()

        logger.store(StopIter=i)

        # Value function learning
        for i in range(train_v_iters):
            vf_optimizer.zero_grad()
            loss_v = compute_loss_v(data)
            loss_v.backward()
            mpi_avg_grads(ac.v)    # average grads across MPI processes
            vf_optimizer.step()

        # Log changes from update
        kl, ent, cf = pi_info['kl'], pi_info_old['ent'], pi_info['cf']
        logger.store(LossPi=pi_l_old, LossV=v_l_old,
                     KL=kl, Entropy=ent, ClipFrac=cf,
                     DeltaLossPi=(loss_pi.item() - pi_l_old),
                     DeltaLossV=(loss_v.item() - v_l_old))
        
    def print_results(env, writer, num, logger, data, epoch, local_rew, local_len, rewbuffer, lenbuffer, learning_rate_pi, learning_rate_vf, t1):
            
            update(data,epoch, logger)
            # print("local",local_len)
            lrlocal = (local_rew, local_len) # local values
            listoflrpairs = MPI.COMM_WORLD.allgather(lrlocal) # list of tuples
            rews, lens = map(flatten_lists, zip(*listoflrpairs))
            rewbuffer.extend(rews)
            lenbuffer.extend(lens)
            process = psutil.Process(os.getpid())
            
            # if not env.args.Dagger:
            #     test_success = run_test(env, PATH + "model.pt", use_perception=use_perception)
            if proc_id() == 0:
                # print()
                # print("Robot ", num)
                # print("="*20)

                
            #     
            #         print("Test success:", test_success)
                # if not env.args.Dagger:
                #     writer.add_scalar("SuccessTest"+ str(num), np.mean(test_success[0]), epoch)
                #     writer.add_scalar("SuccessTest"+ str(num), np.mean(test_success[1]), epoch)
                writer.add_scalar("ARews/robot_" + str(num), np.mean(rewbuffer), epoch)
                writer.add_scalar("ALens/robot_" + str(num), np.mean(lenbuffer), epoch)
                if env.args.multi_titans or env.args.multi_spots:
                    writer.add_scalar("Stds/robot_" + str(num), np.mean(ac.pi.std.data.numpy()), epoch)
                elif env.args.heterogeneous or env.args.titanheads:
                    # print("AGEDEKH",ac.pi.std_spot)
                    # if "titan" in str(env.robots[0]):
                    #     print("titanAGEDEKH",ac.pi.std_spot)
                    #     writer.add_scalar("Stds/spot_lin" + str(num), np.mean(ac.pi.std_spot[1][0].data.numpy()), epoch)
                    #     writer.add_scalar("Stds/spot_ang" + str(num), np.mean(ac.pi.std_spot[1][1].data.numpy()), epoch)
                    #     writer.add_scalar("Stds/spot_lat" + str(num), np.mean(ac.pi.std_spot[1][2].data.numpy()), epoch)
                    #     writer.add_scalar("Stds/titan_lin" + str(num), np.mean(ac.pi.std_titan[0][0].data.numpy()), epoch)
                    #     writer.add_scalar("Stds/titan_ang" + str(num), np.mean(ac.pi.std_titan[0][1].data.numpy()), epoch)
                        
                    # # elif ac_size==(3,2):
                    # elif "spot" in str(env.robots[0]):
                    #     print("SpotAGEDEKH",ac.pi.std_spot)
                    writer.add_scalar("Stds/spot_lin" + str(num), np.mean(ac.pi.std_spot[0].data.numpy()), epoch)
                    writer.add_scalar("Stds/spot_ang" + str(num), np.mean(ac.pi.std_spot[2].data.numpy()), epoch)
                    writer.add_scalar("Stds/spot_lat" + str(num), np.mean(ac.pi.std_spot[1].data.numpy()), epoch)
                    writer.add_scalar("Stds/titan_lin" + str(num), np.mean(ac.pi.std_titan[0].data.numpy()), epoch)
                    writer.add_scalar("Stds/titan_ang" + str(num), np.mean(ac.pi.std_titan[1].data.numpy()), epoch)
                        
                # print("ac.pi.std_titan.data",ac.pi.std_titan.data,ac.pi.std_spot.data.numpy())
                writer.add_scalar("RAM/robot_" + str(num), process.memory_info().rss/(1024.0 ** 3)*num_procs(), epoch)
                writer.add_scalar("Lr_pi/robot_" + str(num), learning_rate_pi, epoch)
                writer.add_scalar("Lr_vf/robot_" + str(num), learning_rate_vf, epoch)
                writer.add_scalar("time_per_rollout/robot_" + str(num), time.time() - t1, epoch)

            local_len = []
            local_rew = []

            # Log info about epoch
            logger.log_tabular('Epoch', epoch)
            logger.log_tabular('Rews', np.mean(rewbuffer))
            logger.log_tabular('Lens', np.mean(lenbuffer))

            env.log_stuff(logger, num, writer, epoch)

            logger.log_tabular("RAM", process.memory_info().rss/(1024.0 ** 3)*num_procs())
            # logger.log_tabular('Std', np.mean(ac.pi.std.data.numpy()))
            # logger.log_tabular('Lr_pi', learning_rate_pi)
            # logger.log_tabular('Lr_vf', learning_rate_vf)
            logger.log_tabular('Time per ep', time.time() - t1)
            logger.log_tabular('Time', time.time()-start_time)
            logger.dump_tabular()

    # Prepare for interaction with environment
    start_time = time.time()


    o, ep_rets, ep_lens = env.reset(), [0] * robot_number, [0]*robot_number
    # print(o[1],"o",o[0])
    
    if env.args.heterogeneous or env.args.titanheads:
        # if ac_size==(2,3):
        if "titan" in str(env.robots[0]):
            # print("O_before",len(o[0]),o)
            o[0] = np.insert(o[0], 0, 0)
            o[1] = np.insert(o[1], 0, 1)
            # print("O_after",len(o[0]),o)
        # elif ac_size==(3,2):
        elif "spot" in str(env.robots[0]):
            # print("O_before",len(o[0]),o)
            o[0] = np.insert(o[0], 0, 1)
            o[1] = np.insert(o[1], 0, 0)
    # print("O_after",len(o),o)
        
        #print(im);exit()
    if use_perception:
        im = env.get_image()
        

    local_lens = [[] for _ in range(robot_number)]
    local_rews = [[] for _ in range(robot_number)]
    t1 = time.time()
    #print("os",np.array(o))
    #ep_ret_list=[]
    # Main loop: collect experience in env and update/log each epoch
    
    # time_saving=[]
    # action_saving1=[]
    # action_saving2=[]
    # action_saving3=[]
    # action_saving4=[]

    
    for epoch in range(epochs):
        st=time.time()
        # print("checking how many observation",o, len(o))
        for t in range(local_steps_per_epoch):
            if use_perception:
                # print(o)

                if (env.args.heterogeneous or env.args.titanheads) and not env.args.cloning:
                    
                    a_spot,a_titan, v, logp_spot, logp_titan = ac.step(torch.as_tensor(np.array(o), dtype=torch.float32), torch.as_tensor(im, dtype=torch.float32))
                
                # if (env.args.heterogeneous or env.args.titanheads) and not env.args.separate_node:
                    
                #     a_spot,a_titan, v, logp_spot, logp_titan = ac.step(torch.as_tensor(np.array(o), dtype=torch.float32), torch.as_tensor(im, dtype=torch.float32))
                
                # elif (env.args.heterogeneous or env.args.titanheads) and env.args.separate_node:
                #     # print("acc",ac.step(torch.as_tensor(np.array(o), dtype=torch.float32), torch.as_tensor(im, dtype=torch.float32)))
                #     a_spot,a_spot_lateral, a_titan, v, logp_spot,logp_spot_lateral, logp_titan = ac.step(torch.as_tensor(np.array(o), dtype=torch.float32), torch.as_tensor(im, dtype=torch.float32))
                # elif env.args.IHPPO:
                #     a_dtr,a_titan, v, logp_dtr, logp_titan = ac.step(torch.as_tensor(np.array(o), dtype=torch.float32), torch.as_tensor(im, dtype=torch.float32))
                
                elif env.args.cloning:
                    a, v, logp = ac.step(torch.as_tensor(np.array(o), dtype=torch.float32), torch.as_tensor(im, dtype=torch.float32), stochastic=False)
                
                else:
                    a, v, logp = ac.step(torch.as_tensor(np.array(o), dtype=torch.float32), torch.as_tensor(im, dtype=torch.float32))
                
            
            else:
                a, v, logp = ac.step(torch.as_tensor(np.array(o), dtype=torch.float32))


            if env.args.Pretrained_cur:
            # obs = MUL.reset()
            # im = MUL.get_image()
                model_mu=torch.load("/home/kom018/behaviour_rl/Saved_models/Turtle_titan/choosen_models/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/mu_net_simul.jit")
                model_z=torch.load("/home/kom018/behaviour_rl/Saved_models/Turtle_titan/choosen_models/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/z_net_simul.jit")
                if env.args.multi_titans or env.args.multi_spots:
                    a_r1=torch.as_tensor(np.array([o[0]]), dtype=torch.float32).unsqueeze(dim=0)
                elif env.args.heterogeneous:
                    a_r1=torch.as_tensor(np.array([o[0][1:]]), dtype=torch.float32).unsqueeze(dim=0)
                b_r1=model_z(torch.as_tensor(im[0], dtype=torch.float32))
                # print(a_r1[0],"br1",b_r1)
                # print(np.array(a_r1[0].detach().numpy()).shape,np.array(b_r1.detach().numpy()).shape)
                concatenate_part_r1=torch.concat((a_r1[0],b_r1),-1)        
                action_r1 = model_mu(concatenate_part_r1)

                if env.args.num_robots==2:

                    if env.args.multi_titans or env.args.multi_spots:
                        a_r2=torch.as_tensor(np.array([o[1]]), dtype=torch.float32).unsqueeze(dim=0)
                    elif env.args.heterogeneous:
                        a_r2=torch.as_tensor(np.array([o[1][1:]]), dtype=torch.float32).unsqueeze(dim=0)
                    # a_r2=torch.as_tensor(np.array([o[1]]), dtype=torch.float32).unsqueeze(dim=0)
                    b_r2=model_z(torch.as_tensor(im[1], dtype=torch.float32))
                    # print(a_r2[0],"br2",b_r2)
                    # print(np.array(a_r2[0].detach().numpy()).shape,np.array(b_r2.detach().numpy()).shape)
                    concatenate_part_r2=torch.concat((a_r2[0],b_r2),-1)        
                    action_r2 = model_mu(concatenate_part_r2)
                    # print("ar1",action_r1,"ar2",action_r2)
                
                r1_clipped_linear_vel_command=np.clip(action_r1[0][0].detach().numpy(), -0.75, 0.75)
                r1_clipped_angular_vel_command=np.clip(action_r1[0][1].detach().numpy(), -0.75, 0.75)
                action_r=torch.tensor([[r1_clipped_linear_vel_command,r1_clipped_angular_vel_command]])

                if env.args.num_robots==2:
                    r2_clipped_linear_vel_command=np.clip(action_r2[0][0].detach().numpy(), -0.75, 0.75)
                    r2_clipped_angular_vel_command=np.clip(action_r2[0][1].detach().numpy(), -0.75, 0.75)

                    # action=[[r1_clipped_linear_vel_command,r1_clipped_angular_vel_command],[r2_clipped_linear_vel_command,r2_clipped_angular_vel_command]]
                    # action=np.array([[r1_clipped_linear_vel_command,r1_clipped_angular_vel_command],[r2_clipped_linear_vel_command,r2_clipped_angular_vel_command]])
                    action_r=torch.tensor([[r1_clipped_linear_vel_command,r1_clipped_angular_vel_command],[r2_clipped_linear_vel_command,r2_clipped_angular_vel_command]])
                # pol=torch.load("/home/kom018/behaviour_rl/Saved_models/Turtle_titan/choosen_models/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/model.pt")
                # sp_ac = pol.step(torch.as_tensor(np.array(o), dtype=torch.float32), torch.as_tensor(im, dtype=torch.float32), stochastic=False)[0]
                sp_ac=action_r
                # print("sp_ac",sp_ac)
            else: 
                sp_ac=np.array([[0., 0.],[0., 0.]])
            # print("action_bef",a_spot,a_titan, v, logp_spot, logp_titan)
            # print(ac_size);exit()
            # print(env.robots);exit()
            # if env.args.heterogeneous or env.args.titanheads:
            #     if ac_size==(2,3):
            #         a=a_titan[0],a_spot[1]
            #         logp=[logp_titan[0],logp_spot[1]]
            #     elif ac_size==(3,2):
            #         a=a_spot[0],a_titan[1]
            #         logp=[logp_spot[0],logp_titan[1]]
            # print("action",a,len(a));exit()
            if env.args.heterogeneous or env.args.titanheads:
                # if ac_size==(2,3):

                # if env.args.separate_node:
                #     if "titan" in str(env.robots[0]):
                #         # print("spoot",logp_spot[0],np.array((a_spot[1][0],a_spot_lateral[1][0],a_spot[1][1])),type(a_spot[1]))
                #         a=a_titan[0],np.array((a_spot[1][0],a_spot_lateral[1][0],a_spot[1][1]))
                #         logp=[logp_titan[0],logp_spot[1],logp_spot_lateral[1]]
                #         print("sepa",a_spot,a_spot_lateral,a_titan)
                #     # elif ac_size==(3,2):
                #     elif "spot" in str(env.robots[0]):
                        
                #         # a=a_spot[0],a_spot_lateral[0],a_titan[1]
                #         a=np.array((a_spot[0][0],a_spot_lateral[0][0],a_spot[0][1])),a_titan[1]
                #         # logp=[logp_spot[0],logp_titan[1]]
                #         logp=[logp_spot[0],logp_spot_lateral[0],logp_titan[1]]
                if env.args.individual_policy:
                    if "titan" in str(env.robots[0]):
                        a=a_titan[0],a_spot[0]
                        logp=[logp_titan[0],logp_spot[0]]
                    # elif ac_size==(3,2):
                    elif "spot" in str(env.robots[0]):
                        a=a_spot[0],a_titan[0]
                        logp=[logp_spot[0],logp_titan[0]]
                    # print(a)
                else:
                    if "titan" in str(env.robots[0]):
                        a=a_titan[0],a_spot[1]
                        logp=[logp_titan[0],logp_spot[1]]
                    # elif ac_size==(3,2):
                    elif "spot" in str(env.robots[0]):
                        a=a_spot[0],a_titan[1]
                        logp=[logp_spot[0],logp_titan[1]]
                    # print(a)
            # elif env.args.IHPPO:
            #     # if ac_size==(2,3):
            #     if "titan" in str(env.robots[0]):
            #         a=a_titan[0],a_dtr[1]
            #         logp=[logp_titan[0],logp_dtr[1]]
            #     # elif ac_size==(3,2):
            #     elif "dtr" in str(env.robots[0]):
            #         a=a_dtr[0],a_titan[1]
            #         logp=[logp_dtr[0],logp_titan[1]]
            # # print("val",v)
            # print(a)
            tt=time.time()
            # if env.args.Pretrained_cur:

            if env.args.cloning:
                next_o, r, d,termination, _,exps = env.step(a,sp_ac)
                # exps = np.vstack(exps)
                # print("exp_before",exps)
                # exps=exps[0][0],exps[0][1],exps[1][0],exps[1][1]
                # print("exp_after",exps)
                # print("EXXXX",type(exps),type(a))
            else:
                next_o, r, d,termination, _ = env.step(a,sp_ac)
            # print("ch",exps,r)
            # else:
            #     next_o, r, d,termination, _ = env.step(a,0)
            # print("td", time.time()-tt)
            tt=time.time()
            #print("O_len",len(next_o),len(next_o[0]),"o",next_o)

            #print(r)
            # print(d)
            #print("Value_before",v)
            # v = [0 if collision else value for collision, value in zip(d, v)]
            # v=torch.tensor(v, dtype=torch.float32)
            # print("after v",v)
            #print("DONE",d)
            st1=time.time()
            # current_time=0
            # and time.time() - st1 == 0.2
            if use_perception:
                # if time.time() - st1 == 0.2:
                next_im = env.get_image()
                # print("next_im",len(next_im),next_im.shape)
                
                if env.args.map_show:
                    r1_occupancy_map = next_im[0, 0, :, :]
                    

                    # r1_occupancy_map = next_im[0, :, :]
                    # r2_occupancy_map = next_im[1, :, :]

                    # r1_occupancy_map=next_im[0, 0, :, :]
                    # # r2_occupancy_map=next_im[1, 0, :, :]

                    r1_occupancy_map_array = np.array(r1_occupancy_map)
                    # print("r1_occupancy_map_array.shape",r1_occupancy_map_array.shape)
                    # Determine the dimensions of the occupancy map
                    rows, cols = r1_occupancy_map_array.shape
                    
                    # Create an empty image with the same dimensions as the occupancy map
                    image_r1 = np.zeros((rows, cols, 3), dtype=np.uint8)
                    
                    # Assign grey color where occupancy_map is 0
                    image_r1[r1_occupancy_map_array == 0] = (128, 128, 128)  # Grey
                    
                    # Assign red color where occupancy_map is 1
                    image_r1[r1_occupancy_map_array == 1] = (0, 0, 255)  # Red

                    image_r1 = image_r1 #occupancy_map_to_image(im_ocupancy)


                    # # Create a window with the specified name
                    cv2.namedWindow("R1 Occupancy Map", cv2.WINDOW_NORMAL)

                    # Resize the window to a desired size
                    cv2.resizeWindow("R1 Occupancy Map", 800, 600)

                    # Define the save path directory
                    save_dir = '/home/kom018/behaviour_rl/Results_plots/Action_plots'
                    os.makedirs(save_dir, exist_ok=True)  # Ensure the directory exists

                    # Save the Robot 1 occupancy map
                    save_path_r1 = os.path.join(save_dir, 'R1_occupancy_map.png')
                    cv2.imwrite(save_path_r1, image_r1)

                    # Display the image
                    cv2.imshow("R1 Occupancy Map", image_r1)

                    if env.args.num_robots==2:
                        r2_occupancy_map = next_im[1, 0, :, :]
                        r2_occupancy_map_array = np.array(r2_occupancy_map)
                        # print("r2_occupancy_map_array.shape",r2_occupancy_map_array.shape)
                        # Determine the dimensions of the occupancy map
                        rows_r2, cols_r2 = r2_occupancy_map_array.shape
                        
                        # Create an empty image with the same dimensions as the occupancy map
                        image_r2 = np.zeros((rows_r2, cols_r2, 3), dtype=np.uint8)
                        
                        # Assign grey color where occupancy_map is 0
                        image_r2[r2_occupancy_map_array == 0] = (128, 128, 128)  # Grey
                        
                        # Assign red color where occupancy_map is 1
                        image_r2[r2_occupancy_map_array == 1] = (0, 0, 255)  # Red

                        image_r2 = image_r2 #occupancy_map_to_image(im_ocupancy)


                        # # Create a window with the specified name
                        cv2.namedWindow("R2 Occupancy Map", cv2.WINDOW_NORMAL)

                        # Resize the window to a desired size
                        cv2.resizeWindow("R2 Occupancy Map", 800, 600)

                        # Save the Robot 2 occupancy map
                        save_path_r2 = os.path.join(save_dir, 'R2_occupancy_map.png')
                        cv2.imwrite(save_path_r2, image_r2)
                        # Display the image
                        cv2.imshow("R2 Occupancy Map", image_r2)
                    

                    cv2.waitKey(1)

                #-------------------------------------------------------------------

                # def mark_edge_cells(occupancy_map):
                #     # Define a structure for connected components (8-connected neighborhood)
                #     structure = generate_binary_structure(2, 1)
                    
                #     # Label connected components
                #     labeled_map, num_labels = label(occupancy_map, structure)
                    
                #     # Find the unique labels (excluding background label 0)
                #     unique_labels = np.unique(labeled_map)[1:]
                    
                #     # Create a new array for the modified occupancy map
                #     modified_occupancy_map = np.zeros_like(occupancy_map)
                    
                #     # Iterate over each unique label (connected component)
                #     for labela in unique_labels:
                #         # Extract the mask for the current connected component
                #         component_mask = (labeled_map == labela).astype(np.uint8)
                        
                #         # Find edge cells that are adjacent to unoccupied cells (0)
                #         edge_mask = np.zeros_like(component_mask)
                #         edge_mask[1:-1, 1:-1] = (component_mask[1:-1, 1:-1] > 0) & \
                #                                 ((component_mask[:-2, 1:-1] == 0) | (component_mask[2:, 1:-1] == 0) | \
                #                                 (component_mask[1:-1, :-2] == 0) | (component_mask[1:-1, 2:] == 0))
                        
                #         # Mark edge cells as 2 in the modified map
                #         modified_occupancy_map[edge_mask > 0] = 1
                        
                #     return modified_occupancy_map

                # r_output_dir_occupancy ="/home/kom018/behaviour_rl/Results_plots/Action_plots/Pybullet/Merged_Occupancy.png"
                # # Get the modified occupancy maps
                # modified_r1_occupancy_map = mark_edge_cells(r1_occupancy_map)
                # modified_r2_occupancy_map = mark_edge_cells(r2_occupancy_map)

                # # Create a figure with two subplots
                # fig, axes = plt.subplots(1, 2, figsize=(30, 15))

                # # Plotting the modified occupancy map for Robot 1
                # axes[0].imshow(modified_r1_occupancy_map, cmap='Reds', origin='upper')
                # axes[0].set_title("Robot 1 Occupancy Map")

                # for i in range(modified_r1_occupancy_map.shape[0]):
                #     for j in range(modified_r1_occupancy_map.shape[1]):
                #         cell_value = int(modified_r1_occupancy_map[i, j])
                #         color = 'blue' if cell_value == 2 else 'red' if cell_value == 1 else 'black'
                #         axes[0].text(j, i, cell_value, ha='center', va='center', color=color)

                # # Customizing the subplot for Robot 1
                # axes[0].set_xticks(np.arange(modified_r1_occupancy_map.shape[1]))
                # axes[0].set_yticks(np.arange(modified_r1_occupancy_map.shape[0]))
                # axes[0].grid(True, which='both', color='black', linestyle='-', linewidth=0.5)
                # axes[0].set_xticks(np.arange(-0.5, modified_r1_occupancy_map.shape[1], 1), minor=True)
                # axes[0].set_yticks(np.arange(-0.5, modified_r1_occupancy_map.shape[0], 1), minor=True)
                # axes[0].grid(which='minor', color='black', linestyle='-', linewidth=0.5)
                # axes[0].tick_params(which='minor', size=0)

                # # Plotting the modified occupancy map for Robot 2
                # axes[1].imshow(modified_r2_occupancy_map, cmap='Greens', origin='upper')
                # axes[1].set_title("Robot 2 Occupancy Map")

                # for i in range(modified_r2_occupancy_map.shape[0]):
                #     for j in range(modified_r2_occupancy_map.shape[1]):
                #         cell_value = int(modified_r2_occupancy_map[i, j])
                #         color = 'blue' if cell_value == 2 else 'red' if cell_value == 1 else 'black'
                #         axes[1].text(j, i, cell_value, ha='center', va='center', color=color)

                # # Customizing the subplot for Robot 2
                # axes[1].set_xticks(np.arange(modified_r2_occupancy_map.shape[1]))
                # axes[1].set_yticks(np.arange(modified_r2_occupancy_map.shape[0]))
                # axes[1].grid(True, which='both', color='black', linestyle='-', linewidth=0.5)
                # axes[1].set_xticks(np.arange(-0.5, modified_r2_occupancy_map.shape[1], 1), minor=True)
                # axes[1].set_yticks(np.arange(-0.5, modified_r2_occupancy_map.shape[0], 1), minor=True)
                # axes[1].grid(which='minor', color='black', linestyle='-', linewidth=0.5)
                # axes[1].tick_params(which='minor', size=0)

                # plt.savefig(r_output_dir_occupancy, bbox_inches='tight')
                # print(next_im)
                # else:
                #     pass 
                #print(len(im))
                #np.savetxt('im1.txt', im[0])
            current_time = time.time()
            new_time=current_time-st1

            # print("time_before",st1) 
            
            st1=time.time()
            # print("time",new_time)
            # if robot_number > 1:

            #ep_ret += sum(r) / len(r)
            
            
            
            # else:
            # for single_r in r:
            #     ep_ret += [single_r] #sum(r) / len(r)
            #     ep_ret_list.append(ep_ret)

            # print("reward",r)
            # print("robot_number",robot_number)
                
            # print("a",a,"O-shape",np.array(o).shape)
                
            # current_time = time.time() - st
            # print(current_time)
            # st=time.time()
            # time_saving.append(current_time)
            # action_saving1.append([a[0][0]])
            # action_saving2.append([a[0][1]])
            # action_saving3.append([a[1][0]])
            # action_saving4.append([a[1][1]])
            # print("act",action_saving)
            # print("actions",a)
            # column0=pd.DataFrame(time_saving)
            # column1=pd.DataFrame(action_saving1)
            # column2=pd.DataFrame(action_saving2)
            # column3=pd.DataFrame(action_saving3)
            # column4=pd.DataFrame(action_saving4)
            # datafrm=pd.concat([column1,column2,column3,column4],axis=1)
            # datafrm=pd.concat([column0,column1,column2],axis=1)
            # # print("datafrm",datafrm)
            # datafrm.to_csv("/home/kom018/behaviour_rl/action_time.csv")


            for i in range(robot_number):
                #print("ep_ret_before",ep_rets)
                ep_rets[i] += r[i]
                # print("ep_ret",ep_rets)

                ep_lens[i] += 1

            # print(ep_rets,ep_lens)
            #print(ep_ret_list, len(ep_ret_list))
            #print(len(ep_ret_list),(ep_ret_list))

            #print(len(r_list), r_list)
            
            # print("obse",o,exps[0][0])
            # save and log
            # print("STORE_O",o)
            if env.args.cloning:
                # print('actions',a,'ex',exps)
                if use_perception:
                    buf.store(o, im, a, r, v, logp,exps)
                else:
                    buf.store(o, a, r, v, logp,exps)

            else:
                if use_perception:
                    buf.store(o, im, a, r, v, logp)
                else:
                    buf.store(o, a, r, v, logp)

            #_,_,_,j,_,_=buf.store(o, a, r, v, logp, robot_number)
            
            #print("obs_size",len(o))
            for logger, val in zip(loggers, v):
                logger.store(VVals=val)
            
            # Update obs (critical!)
            o = next_o

            if env.args.heterogeneous or env.args.titanheads:
                # if ac_size==(2,3):
                if "titan" in str(env.robots[0]):
                    # print("O_before",len(o[0]),o)
                    o[0] = np.insert(o[0], 0, 0)
                    o[1] = np.insert(o[1], 0, 1)
                    # print("O_after",len(o[0]),o)
                # elif ac_size==(3,2):
                elif "spot" in str(env.robots[0]):
                    # print("O_before",len(o[0]),o)
                    o[0] = np.insert(o[0], 0, 1)
                    o[1] = np.insert(o[1], 0, 0)
                    # print("O_after",len(o[0]),o)
            # print("updated_O",o)
            
            if use_perception:
                im = next_im
            #print(ep_lens)
            #print(d)
            #print("im",im)
            timeout = (ep_lens[0] == env.args.max_ep_len)  or all(termination) 
            # print("Done",d)
            
            argus = default_arguments.get_defaults() 
            if argus.single_done and any(d):
                terminal=True

            elif all(d):
            # if any(d):
                terminal = True
            # elif all(termination):
            #     # print("tham");exit()
            #     terminal = timeout
            else:
                terminal = timeout
            #print("terminal",terminal)
            
            #print(terminal)                      #CHECK that Part
            epoch_ended = t==local_steps_per_epoch-1
            
            if terminal or epoch_ended:
                # if trajectory didn't reach terminal state, bootstrap value target
                #if (timeout or epoch_ended) and not all(d):
                if (timeout or epoch_ended) and not (all(d) or ( argus.single_done and any(d))):
                    if use_perception:
                        if (env.args.heterogeneous or env.args.titanheads or env.args.IHPPO) and not env.args.cloning:
                        
                            _,_, v,_, _ = ac.step(torch.as_tensor(np.array(o), dtype=torch.float32), torch.as_tensor(im, dtype=torch.float32))

                        # if (env.args.heterogeneous or env.args.titanheads or env.args.IHPPO) and not env.args.separate_node:
                        
                        #     _,_, v,_, _ = ac.step(torch.as_tensor(np.array(o), dtype=torch.float32), torch.as_tensor(im, dtype=torch.float32))

                        # elif (env.args.heterogeneous or env.args.titanheads or env.args.IHPPO) and env.args.separate_node:
                        
                        #     _,_,_, v,_,_, _ = ac.step(torch.as_tensor(np.array(o), dtype=torch.float32), torch.as_tensor(im, dtype=torch.float32))
                        
                        
                        elif env.args.cloning:
                           _, v, _ = ac.step(torch.as_tensor(np.array(o), dtype=torch.float32), torch.as_tensor(im, dtype=torch.float32), stochastic=False)
                        else:
                            _, v, _ = ac.step(torch.as_tensor(np.array(o), dtype=torch.float32), torch.as_tensor(im, dtype=torch.float32))
                    else:
                        _, v, _ = ac.step(torch.as_tensor(np.array(o), dtype=torch.float32))
                        #print("what is that tensor with 2 element",v.detach().numpy(), type(v.detach().numpy()))
                        v = v.detach().numpy()
                else:
                    #v = 0
                    v=np.zeros(robot_number)
                    

                # print("complete v",v)
                

                

                #print("what is v",v, type(v))
                buf.finish_path(v)
                #print("finish",buf.finish_path(v))
                if terminal:
                    # only save EpRet / EpLen if trajectory finished
                    for logger, ep_ret, ep_len, local_rew, local_len in zip(loggers, ep_rets, ep_lens, local_rews, local_lens):
                        logger.store(EpRet=ep_ret, EpLen=ep_len)
                    #local_rews.append(ep_ret[int(len(ep_ret)/1)-1])
                        #print(ep_ret)
                        local_rew.append(ep_ret)
                        local_len.append(ep_len)
                    #print("LR",local_rews)

                    #print("local",len(local_rews.append(ep_ret[int(len(ep_ret)/2)])))
                
                o, ep_rets, ep_lens = env.reset(), [0] * robot_number, [0]*robot_number
                if env.args.heterogeneous or env.args.titanheads:
                    # if ac_size==(2,3):
                    if "titan" in str(env.robots[0]):
                        # print("O_before",len(o[0]),o)
                        o[0] = np.insert(o[0], 0, 0)
                        o[1] = np.insert(o[1], 0, 1)
                        # print("O_after",len(o[0]),o)
                    # elif ac_size==(3,2):
                    elif "spot" in str(env.robots[0]):
                        # print("O_before",len(o[0]),o)
                        o[0] = np.insert(o[0], 0, 1)
                        o[1] = np.insert(o[1], 0, 0)
                        # print("O_after",len(o[0]),o)
                # print("updated_O",o);exit()
                if use_perception:
                    im = env.get_image()
        if (epoch % save_freq == 0) or (epoch == epochs-1):
            if proc_id() == 0:
                

                # if env.args.cloning and not env.args.Dagger:
                print("Saving model_checkpoint",epoch)
                
                model_state = {
                    'epoch': epoch,
                    'model': ac,
                    'state_dict': ac.state_dict(),
                    'optimizer': pi_optimizer.state_dict()
                }
                torch.save(model_state, PATH + f'model_{epoch}.pt')

                # else:
                #     print("Saving model")
                #     torch.save(ac, PATH + "model.pt")
            # Wait for all processes before doing an update
            comm.Barrier()
            # Currently runnning a test shuts the physics server for PyBullet, unsure why
            # if "pb" not in env.args.env:
            #     save_state = env.get_env_state()
            #     restore_state = [env.pos, env.orn, env.joints]
            #     test_success = run_test(env, PATH + "model.pt", use_perception=use_perception)
            #     if proc_id() == 0:
            #         print("Test success:", test_success)
            #         writer.add_scalar("SuccessTest", np.mean(test_success), epoch)
            #     env.reset(test=True, restore_state=restore_state)
            #     if use_perception:
            #         im = env.get_image()
            #     env.restore_env_state(save_state)


        

        # Perform PPO update is inside print results function below!
        data_list= buf.get(robot_number)
        # print("datalist",data_list);exit()
        for g in pi_optimizer.param_groups:
            learning_rate_pi = g['lr']

        for g in vf_optimizer.param_groups:
            learning_rate_vf = g['lr']
        
        for num, (data,logger, local_rew, local_len, rewbuffer,lenbuffer) in enumerate(zip(data_list, loggers, local_rews, local_lens, rewbuffers, lenbuffers)):
            print_results(env, writer, num, logger, data, epoch, local_rew, local_len, rewbuffer, lenbuffer, learning_rate_pi, learning_rate_vf, t1)


        loggers = [EpochLogger(**logger_kwargs) for _ in range(robot_number)]
        t1 = time.time()
    
        



def run_test(env, model, use_perception=False):
    # Test policy without any randomness
    try:
        ac = torch.load(model)
        load_successful = True
    except Exception as e:
        print("Failed to load saved torch file, trying again", e)
        load_successful = False
        
    # Make sure everyone was able to load the weights
    if (np.array(MPI.COMM_WORLD.allgather(load_successful)) == False).any():
        print("Load failed, try again next time.")
        return [0.0] * env.ac_size
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
    # print("success",success)
    # success=[0,0]
    successes1 = MPI.COMM_WORLD.allgather(success[0])
    successes2 = MPI.COMM_WORLD.allgather(success[1])
    env.args.record_sim = True
    # return successes
    return successes1,successes2

def flatten_lists(listoflists):
        return [el for list_ in listoflists for el in list_]

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--env', type=str, default='HalfCheetah-v2')
    parser.add_argument('--hid', type=int, default=64)
    parser.add_argument('--l', type=int, default=2)
    parser.add_argument('--gamma', type=float, default=0.99)
    parser.add_argument('--seed', '-s', type=int, default=0)
    parser.add_argument('--cpu', type=int, default=4)
    parser.add_argument('--steps', type=int, default=4000)
    parser.add_argument('--epochs', type=int, default=50)
    parser.add_argument('--exp_name', type=str, default='ppo')
    args = parser.parse_args()

    mpi_fork(args.cpu)  # run parallel code with mpi

    from utils.run_utils import setup_logger_kwargs
    logger_kwargs = setup_logger_kwargs(args.exp_name, args.seed)

    ppo(lambda : gym.make(args.env), actor_critic=core.MLPActorCritic,
        ac_kwargs=dict(hidden_sizes=[args.hid]*args.l), gamma=args.gamma, 
        seed=args.seed, steps_per_epoch=args.steps, epochs=args.epochs,
        logger_kwargs=logger_kwargs)
    

    def mark_edge_cells(occupancy_map):
            # Define a structure for connected components (8-connected neighborhood)
            structure = generate_binary_structure(2, 1)
            
            # Label connected components
            labeled_map, num_labels = label(occupancy_map, structure)
            
            # Find the unique labels (excluding background label 0)
            unique_labels = np.unique(labeled_map)[1:]
            
            # Create a new array for the modified occupancy map
            modified_occupancy_map = np.zeros_like(occupancy_map)
            
            # Iterate over each unique label (connected component)
            for labela in unique_labels:
                # Extract the mask for the current connected component
                component_mask = (labeled_map == labela).astype(np.uint8)
                
                # Find edge cells that are adjacent to unoccupied cells (0)
                edge_mask = np.zeros_like(component_mask)
                edge_mask[1:-1, 1:-1] = (component_mask[1:-1, 1:-1] > 0) & \
                                        ((component_mask[:-2, 1:-1] == 0) | (component_mask[2:, 1:-1] == 0) | \
                                        (component_mask[1:-1, :-2] == 0) | (component_mask[1:-1, 2:] == 0))
                
                # Mark edge cells as 2 in the modified map
                modified_occupancy_map[edge_mask > 0] = 1
                