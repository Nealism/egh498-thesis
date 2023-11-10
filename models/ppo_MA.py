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

class PPOBufferPerception:
    """
    A buffer for storing trajectories experienced by a PPO agent interacting
    with the environment, and using Generalized Advantage Estimation (GAE-Lambda)
    for calculating the advantages of state-action pairs.
    """

    def __init__(self, ob_size, im_size, ac_size, size, gamma=0.99, lam=0.95):
        self.obs_buf = np.zeros(core.combined_shape(size, ob_size), dtype=np.float32)
        self.im_buf = np.zeros(core.combined_shape(size, im_size), dtype=np.float32)
        self.act_buf = np.zeros(core.combined_shape(size, ac_size), dtype=np.float32)
        self.adv_buf = np.zeros(size, dtype=np.float32)
        self.rew_buf = np.zeros(size, dtype=np.float32)
        self.ret_buf = np.zeros(size, dtype=np.float32)
        self.val_buf = np.zeros(size, dtype=np.float32)
        self.logp_buf = np.zeros(size, dtype=np.float32)
        self.gamma, self.lam = gamma, lam
        self.ptr, self.path_start_idx, self.max_size = 0, 0, size

    def store(self, obs, im, act, rew, val, logp):
        """
        Append one timestep of agent-environment interaction to the buffer.
        """
        assert self.ptr < self.max_size     # buffer has to have room so you can store
        self.obs_buf[self.ptr] = obs
        self.im_buf[self.ptr] = im
        self.act_buf[self.ptr] = act
        self.rew_buf[self.ptr] = rew
        self.val_buf[self.ptr] = val
        self.logp_buf[self.ptr] = logp
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

            self.buffers=tuple([PPOBuffer(ob_size, ac_size, size, gamma=gamma, lam=lam) for Robot in range(num_robots)])

            #print("b",tuple(self.buffers), type(self.buffers))
            
            
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
                # getting=getting.append(buffer.get())
                # #print("buf_get",buffer.get())
                # #return buffer.get()
                # return getting



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

    # Special function to avoid certain slowdowns from PyTorch + MPI combo.
    setup_pytorch_for_mpi()

    lenbuffers = [deque(maxlen=100) for _ in range(robot_number)] # rolling buffer for episode lengths
    # rewbuffer = deque(maxlen=100) # rolling buffer for episode rewards
    rewbuffers = [deque(maxlen=100) for _ in range(robot_number)] # rolling buffer for episode rewards

    # Set up logger and save configuration
    loggers = [EpochLogger(**logger_kwargs) for _ in range(robot_number)]
    # TODO: Can't save locals() if using robotics toolbox (needed for joint goal), need to fix this, don't need to save all "locals()"
    # logger.save_config(locals())

    # Random seed
    seed += 10000 * proc_id()
    torch.manual_seed(seed)
    np.random.seed(seed)

    ob_size = env.observation_space.shape
    ac_size = env.action_space.shape
    print(ob_size,ac_size)
    #print("obs",env.observation_space,"action",env.action_space)
    

    # Create actor-critic module
    if use_perception:
        actor_critic=core.MLPActorCriticPerception
        im_size = env.im_size
        if load_path != "":
            ac = torch.load(load_path)
            print("Loading saved weights: ", load_path)
        else:
            ac = actor_critic(env.observation_space, im_size, env.action_space, **ac_kwargs)
        train_pi_iters = 10
        train_v_iters = 10
    else:    
        actor_critic=core.MLPActorCritic
        if load_path != "":
            ac = torch.load(load_path)
            print("Loading saved weights: ", load_path)
        else:
            ac = actor_critic(env.observation_space, env.action_space, **ac_kwargs)
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
        buf = PPOBufferPerception(ob_size, im_size, ac_size, local_steps_per_epoch, gamma, lam)
    else:
        buf = MA_PPOBuffer(ob_size, ac_size, local_steps_per_epoch, gamma, lam, robot_number)
    #print("buf",buf)
    # Set up function for computing PPO policy loss
    def compute_loss_pi(data):
        if use_perception:
            obs, im, act, adv, logp_old = data['obs'], data['im'], data['act'], data['adv'], data['logp']
        else:
            obs, act, adv, logp_old = data['obs'], data['act'], data['adv'], data['logp']

        # Policy loss
        if use_perception:
            pi, logp = ac.pi(obs, im, act)
        else:
            pi, logp = ac.pi(obs, act)
        ratio = torch.exp(logp - logp_old)
        clip_adv = torch.clamp(ratio, 1-clip_ratio, 1+clip_ratio) * adv
        loss_pi = -(torch.min(ratio * adv, clip_adv)).mean()

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
            lrlocal = (local_rew, local_len) # local values
            listoflrpairs = MPI.COMM_WORLD.allgather(lrlocal) # list of tuples
            rews, lens = map(flatten_lists, zip(*listoflrpairs))
            rewbuffer.extend(rews)
            lenbuffer.extend(lens)
            process = psutil.Process(os.getpid())


            if proc_id() == 0:
                # print()
                # print("Robot ", num)
                # print("="*20)
                writer.add_scalar("ARews/robot_" + str(num), np.mean(rewbuffer), epoch)
                writer.add_scalar("ALens/robot_" + str(num), np.mean(lenbuffer), epoch)
                writer.add_scalar("Stds/robot_" + str(num), np.mean(ac.pi.std.data.numpy()), epoch)
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
            logger.log_tabular('Std', np.mean(ac.pi.std.data.numpy()))
            # logger.log_tabular('Lr_pi', learning_rate_pi)
            # logger.log_tabular('Lr_vf', learning_rate_vf)
            logger.log_tabular('Time per ep', time.time() - t1)
            logger.log_tabular('Time', time.time()-start_time)
            logger.dump_tabular()

    # Prepare for interaction with environment
    start_time = time.time()
    o, ep_rets, ep_lens = env.reset(), [0] * robot_number, [0]*robot_number
    #print("o",o)
    if use_perception:
        im = env.get_image()

    local_lens = [[] for _ in range(robot_number)]
    local_rews = [[] for _ in range(robot_number)]
    t1 = time.time()
    #print("os",np.array(o))
    #ep_ret_list=[]
    # Main loop: collect experience in env and update/log each epoch
    for epoch in range(epochs):
        for t in range(local_steps_per_epoch):
            if use_perception:
                a, v, logp = ac.step(torch.as_tensor(np.array(o), dtype=torch.float32), torch.as_tensor(im, dtype=torch.float32))
            else:
                a, v, logp = ac.step(torch.as_tensor(np.array(o), dtype=torch.float32))
            #print("a",a)
            next_o, r, d, _ = env.step(a)
            #print(r)
            # print(d)
            #print("Value_before",v)
            # v = [0 if collision else value for collision, value in zip(d, v)]
            # v=torch.tensor(v, dtype=torch.float32)
            # print("after v",v)
            #print("DONE",d)
            if use_perception:
                next_im = env.get_image()
            
            # if robot_number > 1:

            #ep_ret += sum(r) / len(r)

            
            
            # else:
            # for single_r in r:
            #     ep_ret += [single_r] #sum(r) / len(r)
            #     ep_ret_list.append(ep_ret)

            for i in range(robot_number):
                ep_rets[i] += r[i]
                ep_lens[i] += 1

            #print(ep_rets)
            #print(ep_ret_list, len(ep_ret_list))
            #print(len(ep_ret_list),(ep_ret_list))

            #print(len(r_list), r_list)



            # save and log
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
            if use_perception:
                im = next_im
            #print(ep_lens)
            #print(d)
            timeout = ep_lens[0] == env.args.max_ep_len
            #print("Done",d)
            if all(d):
                terminal = True
            else:
                terminal = timeout
            #print("terminal",terminal)
            
            #print(terminal)                      #CHECK that Part
            epoch_ended = t==local_steps_per_epoch-1
            
            if terminal or epoch_ended:
                # if trajectory didn't reach terminal state, bootstrap value target
                if (timeout or epoch_ended) and not all(d):
                    if use_perception:
                        _, v, _ = ac.step(torch.as_tensor(o, dtype=torch.float32), torch.as_tensor(im, dtype=torch.float32))
                    else:
                        _, v, _ = ac.step(torch.as_tensor(np.array(o), dtype=torch.float32))
                        #print("what is that tensor with 2 element",v.detach().numpy(), type(v.detach().numpy()))
                        v = v.detach().numpy()
                else:
                    #v = 0
                    v=np.zeros(robot_number)
                    

                #print("complete v",v)
                

                

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
                if use_perception:
                    im = env.get_image()
        if (epoch % save_freq == 0) or (epoch == epochs-1):
            if proc_id() == 0:
                print("Saving model")
                torch.save(ac, PATH + "model.pt")
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


        

        # Perform PPO update!
        data_list= buf.get(robot_number)
        #print("datalist",data_list)
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
    if use_perception:
        im = env.get_image()
    done = False
    while True:
        if use_perception:
            act, _, _ = ac.step(torch.as_tensor(ob, dtype=torch.float32), torch.as_tensor(im, dtype=torch.float32), stochastic=False)
        else:
            act, _, _ = ac.step(torch.as_tensor(ob, dtype=torch.float32), stochastic=False)
        ob, rew, done, _ = env.step(act)
        if use_perception:
            im = env.get_image()
        if done or env.steps > env.args.max_ep_len:
            break
    success = env.get_success()
    successes = MPI.COMM_WORLD.allgather(success)
    env.args.record_sim = True
    return successes

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