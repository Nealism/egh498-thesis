import numpy as np
import scipy.signal
from gym.spaces import Box, Discrete
import torch.nn.functional as F
import torch
import torch.nn as nn
from torch.distributions.normal import Normal
from torch.distributions.categorical import Categorical

def combined_shape(length, shape=None):
    if shape is None:
        return (length,)
    return (length, shape) if np.isscalar(shape) else (length, *shape)

def mlp(sizes, activation, output_activation=nn.Identity):
    layers = []
    #print("sizes",sizes)
    for j in range(len(sizes)-1):
        act = activation if j < len(sizes)-2 else output_activation
        layers += [nn.Linear(sizes[j], sizes[j+1]), act()]
        #print("j",j,sizes[j],"j+1",sizes[j+1],"act",act())

    return nn.Sequential(*layers)


# TODO: build CNN from arguments
class CNN(nn.Module):
    def __init__(self, im_dim):
        super().__init__()
        self.im_dim = list(im_dim)
        self.conv1 = nn.Conv2d(in_channels=1,out_channels=4,kernel_size=8,stride=4,padding='valid')
        self.conv2 = nn.Conv2d(in_channels=4,out_channels=8,kernel_size=4,stride=2,padding='valid')
        # #original
        # self.conv1 = nn.Conv2d(in_channels=1,out_channels=8,kernel_size=8,stride=4,padding='valid')
        # self.conv2 = nn.Conv2d(in_channels=8,out_channels=16,kernel_size=4,stride=2,padding='valid')

        # Lazy initialisation of linear layer without knowing input dimensions. Requires a 'dry' run to initialise the size
        self.fc = nn.LazyLinear(64)

    def forward(self, x):
        x = torch.reshape(x, [-1] + self.im_dim)
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = torch.flatten(x, 1) 
        x = torch.tanh(self.fc(x))
        return x

def count_vars(module):
    return sum([np.prod(p.shape) for p in module.parameters()])


def discount_cumsum(x, discount):
    """
    magic from rllab for computing discounted cumulative sums of vectors.

    input: 
        vector x, 
        [x0, 
         x1, 
         x2]

    output:
        [x0 + discount * x1 + discount^2 * x2,  
         x1 + discount * x2,
         x2]
    """
    return scipy.signal.lfilter([1], [1, float(-discount)], x[::-1], axis=0)[::-1]

# ==========================================================================================================
# # perception 
# ==========================================================================================================
class ActorPerception(nn.Module):
    
    def _distribution(self, obs, im):
        raise NotImplementedError

    def _log_prob_from_distribution(self, pi, act):
        raise NotImplementedError

    def forward(self, obs, im, act=None):
        # Produce action distributions for given observations, and 
        # optionally compute the log likelihood of given actions under
        # those distributions.
        pi = self._distribution(obs, im)
        logp_a = None
        if act is not None:
            logp_a = self._log_prob_from_distribution(pi, act)
        return pi, logp_a

class MLPGaussianActorPerception(ActorPerception):

    def __init__(self, obs_dim, im_dim, act_dim, hidden_sizes, activation):
        super().__init__()
        self.obs_dim = obs_dim
        self.im_dim = im_dim
        # log_std = -0.5 * np.ones(act_dim, dtype=np.float32)
        log_std = -0.0 * np.ones(act_dim, dtype=np.float32)
        self.log_std = torch.nn.Parameter(torch.as_tensor(log_std))
        self.z_net = CNN(im_dim)
        # Need to do a dry run to initialise Lazy module
        self.z_net(torch.zeros(self.im_dim))
        self.mu_net = mlp([obs_dim + 64] + list(hidden_sizes) + [act_dim], activation)

    def _distribution(self, obs, im):
        obs = torch.reshape(obs, [-1, self.obs_dim])
        z = self.z_net(im)
        self.mu = self.mu_net(torch.concat((obs, self.z_net(im)), -1))
        self.std = torch.exp(self.log_std)
        return Normal(self.mu, self.std)

    def _log_prob_from_distribution(self, pi, act):
        return pi.log_prob(act).sum(axis=-1)    # Last axis sum needed for Torch Normal distribution

class MLPCriticPerception(nn.Module):

    def __init__(self, obs_dim, hidden_sizes, activation, z_net):
        super().__init__()
        self.obs_dim = obs_dim
        self.z_net = z_net
        self.v_net = mlp([obs_dim + 64] + list(hidden_sizes) + [1], activation)

    def forward(self, obs, im):  
        obs = torch.reshape(obs, [-1, self.obs_dim])
        return torch.squeeze(self.v_net(torch.concat((obs, self.z_net(im)), -1)), -1) # Critical to ensure v has right shape.


class MLPActorCriticPerception(nn.Module):

    def __init__(self, observation_space,  im_dim, action_space,
                 hidden_sizes=(64,64), activation=nn.Tanh):
        super().__init__()
        obs_dim = observation_space.shape[0]
        # # policy builder depends on action space
        if isinstance(action_space, Box):
            self.pi = MLPGaussianActorPerception(obs_dim, im_dim, action_space.shape[0], hidden_sizes, activation)
        # print("self.pi",self.pi)
        # build value function
        self.v  = MLPCriticPerception(obs_dim, hidden_sizes, activation, self.pi.z_net)


    def step(self, obs, im, stochastic=True):
        pi = self.pi._distribution(obs, im)
        
        # print(pi)

        if stochastic:
            a = pi.sample()
            # print(a)
        else:
            a = self.pi.mu
        # print("policy_vel",a)
        logp_a = self.pi._log_prob_from_distribution(pi, a)
        v = self.v(obs, im)

        # Memory leak happens here somewhere. Copying the arrays seem to help??
        v_copy = v.cpu().detach().data.numpy().copy()
        a_copy = a.cpu().detach().data.numpy().copy()
        logp_a_copy = logp_a.cpu().detach().data.numpy().copy()
        return a_copy, v_copy, logp_a_copy

    def act(self, obs, im):
        return self.step(obs, im)[0]

# ==========================================================================================================
# Without perception 
# ==========================================================================================================
class Actor(nn.Module):

    def _distribution(self, obs):
        raise NotImplementedError

    def _log_prob_from_distribution(self, pi, act):
        raise NotImplementedError

    def forward(self, obs, act=None):
        # Produce action distributions for given observations, and 
        # optionally compute the log likelihood of given actions under
        # those distributions.
        pi = self._distribution(obs)
        logp_a = None
        if act is not None:
            logp_a = self._log_prob_from_distribution(pi, act)
        return pi, logp_a

class MLPCategoricalActor(Actor):
    
    def __init__(self, obs_dim, act_dim, hidden_sizes, activation):
        super().__init__()
        self.logits_net = mlp([obs_dim] + list(hidden_sizes) + [act_dim], activation)

    def _distribution(self, obs):
        logits = self.logits_net(obs)
        return Categorical(logits=logits)

    def _log_prob_from_distribution(self, pi, act):
        return pi.log_prob(act)

class MLPGaussianActor(Actor):

    def __init__(self, obs_dim, act_dim, hidden_sizes, activation):
        super().__init__()
        #print("action_dim",act_dim)
        # log_std = -0.5 * np.ones(act_dim, dtype=np.float32)
        log_std = -0.0 * np.ones(act_dim, dtype=np.float32)
        #print("log_std",log_std)
        self.log_std = torch.nn.Parameter(torch.as_tensor(log_std))
        self.mu_net = mlp([obs_dim] + list(hidden_sizes) + [act_dim], activation)

    def _distribution(self, obs):
        #print(obs)
        self.mu = self.mu_net(obs)
        #print(self.mu)
        self.std = torch.exp(self.log_std)
        #print(self.std)
        #print("NORMAL",Normal(self.mu, self.std))
        return Normal(self.mu, self.std) ## multivariate normal dist. with self.mu=means and self.std=standard devs.

    def _log_prob_from_distribution(self, pi, act):
        return pi.log_prob(act).sum(axis=-1)    # Last axis sum needed for Torch Normal distribution

class MLPCritic(nn.Module):

    def __init__(self, obs_dim, hidden_sizes, activation):
        super().__init__()
        self.v_net = mlp([obs_dim] + list(hidden_sizes) + [1], activation)

    def forward(self, obs):        
        return torch.squeeze(self.v_net(obs), -1) # Critical to ensure v has right shape.

class MLPActorCritic(nn.Module):

    def __init__(self, observation_space, action_space, 
                 hidden_sizes=(64,64), activation=nn.Tanh):
        super().__init__()

        obs_dim = observation_space.shape[0]
        #print(obs_dim,action_space.shape[0])
        # # policy builder depends on action space
        if isinstance(action_space, Box):
            self.pi = MLPGaussianActor(obs_dim, action_space.shape[0], hidden_sizes, activation)
        elif isinstance(action_space, Discrete):
            self.pi = MLPCategoricalActor(obs_dim, action_space.n, hidden_sizes, activation)

        # build value function
        self.v  = MLPCritic(obs_dim, hidden_sizes, activation)


    def step(self, obs, stochastic=True):
        pi = self.pi._distribution(obs)
        if stochastic:
            a = pi.sample() ## sample from normal dist.
        else:
            a = self.pi.mu ## just take mean of dist. as the value
        logp_a = self.pi._log_prob_from_distribution(pi, a)
        v = self.v(obs)

        # Memory leak happens here somewhere. Copying the arrays seems to help??
        a_copy = a.cpu().detach().data.numpy().copy()
        # return a_copy, v.item(), logp_a.item()
        return a_copy, v, logp_a

    def act(self, obs):
        return self.step(obs)[0]