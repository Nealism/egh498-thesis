import numpy as np
import scipy.signal
from gym.spaces import Box, Discrete
import torch.nn.functional as F
import torch
import torch.nn as nn
from torch.distributions.normal import Normal
from torch.distributions.categorical import Categorical
# from spinup.utils.mpi_running_mean_std_torch import RunningMeanStdTorch

def combined_shape(length, shape=None):
    if shape is None:
        return (length,)
    return (length, shape) if np.isscalar(shape) else (length, *shape)

def mlp(sizes, activation, output_activation=nn.Identity):
    layers = []
    for j in range(len(sizes)-1):
        act = activation if j < len(sizes)-2 else output_activation
        layers += [nn.Linear(sizes[j], sizes[j+1]), act()]
    return nn.Sequential(*layers)

# x = tf.nn.relu(TF_U.conv2d(im, 16, "vis_l1", [8, 8], [4, 4], pad="VALID"))
# x = tf.nn.relu(TF_U.conv2d(x, 32, "vis_l2", [4, 4], [2, 2], pad="VALID"))

# def cnn(sizes, activation, output_activation=nn.Identity):
# def cnn():
#     # layers = []
#     # for j in range(len(sizes)-1):
#     #     act = activation if j < (sizes) - 2 else output_activation
#     #     layers += [nn.Conv2d(1, sizes[j], 5), act()]
#     layers = []
#     layers += [nn.Conv2d(1, 16, 5), nn.ReLU()]
#     layers += [nn.Conv2d(16, 32, 5), nn.ReLU()]
#     layers += [nn.Flatten()]
#     layers += [nn.Linear(13888, 64), nn.Tanh()]
#     return nn.Sequential(*layers)


class CNN(nn.Module):
    def __init__(self, im_dim):
        super().__init__()
        self.im_dim = im_dim
        # self.conv1 = nn.Conv2d(1, 16, 5)
        # # self.pool = nn.MaxPool2d(2, 2)
        # self.conv2 = nn.Conv2d(16, 32, 5)
        # # self.fc1 = nn.Linear(16 * 5 * 5, 120)
        # # self.fc2 = nn.Linear(120, 84)
        # # self.fc = nn.Linear(13888, 64)61504
        # self.fc = nn.Linear(61504, 64)
        
        self.conv1 = nn.Conv2d(in_channels=1,out_channels=8,kernel_size=8,stride=4,padding='valid')
        self.conv2 = nn.Conv2d(in_channels=8,out_channels=16,kernel_size=4,stride=2,padding='valid')

        # self.conv1 = nn.Conv2d(1, 6, 5)
        # self.pool = nn.MaxPool2d(2, 2)
        # self.conv2 = nn.Conv2d(6, 16, 5)
        # self.fc1 = nn.Linear(16 * 5 * 5, 120)
        # self.fc2 = nn.Linear(120, 84)
        # self.fc = nn.Linear(524288, 64)

        # Gross
        # print(self.conv2.shape)
        self.fc = nn.Linear(2880, 64)
        # self.fc = nn.LazyLinear(64)

        # self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        # x = F.relu(self.conv1(x))
        # x = F.relu(self.conv2(x))
        # x = torch.flatten(x, 1) # flatten all dimensions except batch
        # x = F.tanh(self.fc(x))
        # return x
        x = torch.reshape(x, [-1] + self.im_dim)

        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = torch.flatten(x, 1) # flatten all dimensions except batch
        # x = F.relu(self.fc1(x))
        # x = F.relu(self.fc2(x))
        x = F.tanh(self.fc(x))
        return x

# class CNN(nn.Module):
#     def __init__(self):
#         super(CNN, self).__init__()
#         self.conv1 = nn.Sequential(         
#             nn.Conv2d(
#                 in_channels=1,              
#                 out_channels=16,            
#                 kernel_size=5,              
#                 stride=1,                   
#                 padding=2,                  
#             ),                              
#             nn.ReLU(),                      
#             nn.MaxPool2d(kernel_size=2),    
#         )
#         self.conv2 = nn.Sequential(         
#             nn.Conv2d(16, 32, 5, 1, 2),     
#             nn.ReLU(),                      
#             nn.MaxPool2d(2),                
#         )
#         # fully connected layer, output 10 classes
#         self.out = nn.Linear(32 * 7 * 7, 10)

#     def forward(self, x):
#         x = self.conv1(x)
#         x = self.conv2(x)
#         # flatten the output of conv2 to (batch_size, 32 * 7 * 7)
#         x = x.view(x.size(0), -1)       
#         output = self.out(x)
#         return output, x    # return x for visualization

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
        # self.z_net = cnn([im_dim] + list(im_hidden_sizes) + [act_dim], activation)
        self.z_net = CNN(im_dim)
        self.mu_net = mlp([obs_dim + 64] + list(hidden_sizes) + [act_dim], activation)

    def _distribution(self, obs, im):
        obs = torch.reshape(obs, [-1, self.obs_dim])
        z = self.z_net(im)
        # print(torch.reshape(obs, [-1, self.obs_dim]).shape, torch.reshape(im, [-1] + self.im_dim).shape, self.z_net(im).shape)
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

        # build value function
        self.v  = MLPCriticPerception(obs_dim, hidden_sizes, activation, self.pi.z_net)


    def step(self, obs, im, stochastic=True):
        # with torch.no_grad():
        #     pi = self.pi._distribution(obs)
        #     if stochastic:
        #         a = pi.sample()
        #     else:
        #         a = pi.mu
        #     logp_a = self.pi._log_prob_from_distribution(pi, a)
        #     v = self.v(obs)
        # return a.numpy(), v.numpy(), logp_a.numpy()
        pi = self.pi._distribution(obs, im)
        if stochastic:
            a = pi.sample()
        else:
            a = self.pi.mu
        logp_a = self.pi._log_prob_from_distribution(pi, a)
        v = self.v(obs, im)

        # Memory leak happens here somewhere. Copying the arrays seem to help??
        v_copy = v.cpu().detach().data.numpy().copy()
        # a_copy = a.cpu().detach().data.numpy().copy()
        # v_copy = v.item()
        a_copy = a.cpu().detach().data.numpy().copy()[0]
        logp_a_copy = logp_a.cpu().detach().data.numpy().copy()

        # logp_a_copy = logp_a.item()
        # return a.cpu().detach().numpy(), v.cpu().detach().numpy(), logp_a.cpu().detach().numpy()
        # return np.zeros(21), v.cpu().detach().numpy(), 1

        return a_copy, v_copy, logp_a_copy

    def act(self, obs, im):
        return self.step(obs, im)[0]

# ==========================================================================================================
# Non perception 
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
        # log_std = -0.5 * np.ones(act_dim, dtype=np.float32)
        log_std = -0.0 * np.ones(act_dim, dtype=np.float32)
        self.log_std = torch.nn.Parameter(torch.as_tensor(log_std))
        self.mu_net = mlp([obs_dim] + list(hidden_sizes) + [act_dim], activation)

    def _distribution(self, obs):
        self.mu = self.mu_net(obs)
        self.std = torch.exp(self.log_std)
        return Normal(self.mu, self.std)

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
        # # policy builder depends on action space
        if isinstance(action_space, Box):
            self.pi = MLPGaussianActor(obs_dim, action_space.shape[0], hidden_sizes, activation)
        elif isinstance(action_space, Discrete):
            self.pi = MLPCategoricalActor(obs_dim, action_space.n, hidden_sizes, activation)

        # build value function
        self.v  = MLPCritic(obs_dim, hidden_sizes, activation)


    def step(self, obs, stochastic=True):
        # with torch.no_grad():
        #     pi = self.pi._distribution(obs)
        #     if stochastic:
        #         a = pi.sample()
        #     else:
        #         a = pi.mu
        #     logp_a = self.pi._log_prob_from_distribution(pi, a)
        #     v = self.v(obs)
        # return a.numpy(), v.numpy(), logp_a.numpy()
        pi = self.pi._distribution(obs)
        if stochastic:
            a = pi.sample()
        else:
            a = self.pi.mu
        logp_a = self.pi._log_prob_from_distribution(pi, a)
        v = self.v(obs)

        # Memory leak happens here somewhere. Copying the arrays seem to help??
        # v_copy = v.cpu().detach().data.numpy().copy()
        a_copy = a.cpu().detach().data.numpy().copy()
        # logp_a_copy = logp_a.cpu().data.detach().numpy().copy()
        # return a.cpu().detach().numpy(), v.cpu().detach().numpy(), logp_a.cpu().detach().numpy()
        # return np.zeros(21), v.cpu().detach().numpy(), 1
        return a_copy, v.item(), logp_a.item()

    def act(self, obs):
        return self.step(obs)[0]