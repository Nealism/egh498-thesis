import numpy as np
import scipy.signal
from gym.spaces import Box, Discrete
import torch.nn.functional as F
import torch
import torch.nn as nn
from torch.distributions.normal import Normal
from torch.distributions.categorical import Categorical
import default_arguments

args = default_arguments.get_defaults() 
def combined_shape(length, shape=None):
    if shape is None:
        return (length,)
    return (length, shape) if np.isscalar(shape) else (length, *shape)

def mlp(sizes, activation, output_activation=nn.Identity):
    layers = []
    # print("mlp_sizes",sizes,"len_size-1",len(sizes)-1);exit()
    for j in range(len(sizes)-1):
        act = activation if j < len(sizes)-2 else output_activation
        # print("mlp_size",range(len(sizes)-1),sizes,j)
        # print(nn.Linear(sizes[j], sizes[j+1]), act())
        layers += [nn.Linear(sizes[j], sizes[j+1]), act()]
    # print("layers:",*layers)
        
        
        # print("j",j,sizes[j],"j+1",sizes[j+1],"act",act())
        # print("sequencial",nn.Sequential(*layers))
    # print("ended_loop");exit()
    return nn.Sequential(*layers)

def output_layer(input, output):
    # layers = []
    # print(input,"sep",output)
    layers=nn.Linear(input,output)
    # layers_r2=nn.Linear(input_r2,output[1])
    # print(layers_r1,"la")
    # if output[0]==3:
    #     return layers_r1,layers_r2
    # elif output[0]==2:
    #     return layers_r2,layers_r1

    return layers

def output_layer_r1(input_r1, output_r1):
    # layers = []
    layers_r1=nn.Linear(input_r1,output_r1)
    # layers_r2=nn.Linear(input_r2,output[1])
    # print(layers_r1,"la")
    # if output[0]==3:
    #     return layers_r1,layers_r2
    # elif output[0]==2:
    #     return layers_r2,layers_r1

    return layers_r1

def output_layer_r2(input_r2, output_r2):
    # layers = []
    layers_r2=nn.Linear(input_r2,output_r2)
    # layers_r2=nn.Linear(input_r2,output[1])
    # print(layers_r1,"la")
    # if output[0]==3:
    #     return layers_r1,layers_r2
    # elif output[0]==2:
    #     return layers_r2,layers_r1

    return layers_r2


# # TODO: build CNN from arguments
class CNN(nn.Module):
    def __init__(self, im_dim):
        super().__init__()
        self.im_dim = list(im_dim)
        # print("CNN_im_dim",self.im_dim)
        self.conv1 = nn.Conv2d(in_channels=1,out_channels=4,kernel_size=8,stride=4,padding='valid')
        self.conv2 = nn.Conv2d(in_channels=4,out_channels=8,kernel_size=4,stride=2,padding='valid')
        # #original
        # self.conv1 = nn.Conv2d(in_channels=1,out_channels=8,kernel_size=8,stride=4,padding='valid')
        # self.conv2 = nn.Conv2d(in_channels=8,out_channels=16,kernel_size=4,stride=2,padding='valid')

        # Lazy initialisation of linear layer without knowing input dimensions. Requires a 'dry' run to initialise the size
        self.fc = nn.LazyLinear(64)

    def forward(self, x):
        # print("CNN_X",x,len(x),type(self.im_dim),self.im_dim,x.shape)
        x = torch.reshape(x, [-1] + self.im_dim)
        # print("CNN_X_after",x,len(x),type(self.im_dim),self.im_dim,x.shape)
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        # print("CNN_Beyond",x,len(x),len(x[0]),(x.shape))
        x = torch.flatten(x, 1) 
        # print("CNN_flatten",x,len(x),len(x[0]),(x.shape));exit()
        x = torch.tanh(self.fc(x))
        # print("CNN_FC",x,len(x),len(x[0]),(x.shape))
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
        # print("checkpoint1")
        pi = self._distribution(obs, im)
        # print("checkpoint2")
        # pi_spot,pi_titan = self._distribution(obs, im)
        # print(pi);exit()
        # logp_a_spot = None
        # logp_a_titan = None
        # if act is not None:
        #     logp_a_spot = self._log_prob_from_distribution(pi_spot, act)
        #     logp_a_titan = self._log_prob_from_distribution(pi_titan, act)
        # return pi_spot,pi_titan, logp_a_spot, logp_a_titan
        logp_a = None
        # print("pi_check",pi,act)
        if act is not None:
            logp_a = self._log_prob_from_distribution(pi, act)
            
        return pi, logp_a




class MLPGaussianActorPerception(ActorPerception):

    def __init__(self, base, obs_dim, im_dim, act_dim, hidden_sizes, activation):
        super().__init__()
        self.obs_dim = obs_dim
        self.im_dim = im_dim
        self.base_model=base
        if args.heterogeneous or args.titanheads:
            self.obs_dim=6
            obs_dim=6
        # print("base",base)
        # print("CHEKJDASLJDHJL",act_dim)
        # print("self.obs_dim",self.obs_dim,act_dim);exit()
        # print(act_dim);exit()
        # act_dim=[3,3]
        # print("act_dim______________________________->>",act_dim)
        # print(args.robots);exit()
        # if (act_dim==(2,3) or act_dim==(3,2)) and args.heterogeneous or args.titanheads:
        if (act_dim==(2,3) or act_dim==(3,2)) and args.heterogeneous:
            # print("OR NOT")
            # spot_act_dim=3
            spot_act_dim=3
            titan_act_dim=2
            # log_std = -0.5 * np.ones(act_dim, dtype=np.float32)
            # log_std_r1 = -0.0 * np.ones(act_dim[0], dtype=np.float32)
            # log_std_r2 = -0.0 * np.ones(act_dim[1], dtype=np.float32)
            # # log_std = -0.0 * np.ones(act_dim, dtype=np.float32)
            # self.log_std_r1 = torch.nn.Parameter(torch.as_tensor(log_std_r1))
            # self.log_std_r2 = torch.nn.Parameter(torch.as_tensor(log_std_r2))

            log_std_spot = -0.0 * np.ones(spot_act_dim, dtype=np.float32)
            log_std_titan = -0.0 * np.ones(titan_act_dim, dtype=np.float32)
            # log_std = -0.0 * np.ones(act_dim, dtype=np.float32)

            if args.transfer_learning:
                # log_std = -0.0 * np.ones(act_dim, dtype=np.float32)
                self.log_std_spot = torch.nn.Parameter(torch.as_tensor(log_std_spot))
                self.log_std_titan = base.pi.log_std
            else:
                self.log_std_spot = torch.nn.Parameter(torch.as_tensor(log_std_spot))
                self.log_std_titan = torch.nn.Parameter(torch.as_tensor(log_std_titan))


            
            
            
            if args.transfer_learning:
                self.z_net = base.pi.z_net
            else:
                self.z_net = CNN(im_dim)
            # Need to do a dry run to initialise Lazy module
            self.z_net(torch.zeros(self.im_dim))
            # self.mu_net1 = mlp([obs_dim + 64] + list(hidden_sizes) + [act_dim[0]], activation)
            # self.mu_net2 = mlp([obs_dim + 64] + list(hidden_sizes) + [act_dim[1]], activation)
            # self.mu_net = mlp([obs_dim + 64] + list(hidden_sizes) + [act_dim], activation)
            feature_shape=256
            feature_shape_r1=256
            feature_shape_r2=256
            # print(obs_dim);exit()
            if args.transfer_learning:
                self.feature_layers = base.pi.mu_net[:-2]
                if args.spot_additional_layer:
                    self.spot_additional_layer=base.pi.mu_net[-2:]
                    # self.titan_additional_layer=base.pi.mu_net[-2:]
                # print("base.pi.mu_net",base.pi.mu_net[-2:])
            else:
                self.feature_layers = mlp([obs_dim + 64] + list(hidden_sizes), activation)
            # self.spot_output_layer = output_layer(feature_shape,3)
            # # self.titan_output_layer = output_layer(feature_shape,2)
            # # print("tensor-Sizes",self.spot_output_layer)
            # # self.spot_output_layer = base.pi.mu_net[-2:]
            # self.titan_output_layer = base.pi.mu_net[-2:]
            if args.transfer_learning:
                
                if args.spot_additional_layer:
                    self.spot_output_layer = output_layer(2,3)
                else:
                    self.spot_output_layer = output_layer(feature_shape,3)
                
                if args.feature_only:
                    self.titan_output_layer = output_layer(feature_shape,2)
                else:
                    self.titan_output_layer = base.pi.mu_net[-2:]
                
                
            else:
                self.spot_output_layer = output_layer(feature_shape,3)
                self.titan_output_layer = output_layer(feature_shape,2)
        elif (act_dim==(2,2)) and args.titanheads:
            spot_act_dim=2
            titan_act_dim=2
            
            log_std_spot = -0.0 * np.ones(spot_act_dim, dtype=np.float32)
            log_std_titan = -0.0 * np.ones(titan_act_dim, dtype=np.float32)
            # log_std = -0.0 * np.ones(act_dim, dtype=np.float32)
            if args.transfer_learning:
                # log_std = -0.0 * np.ones(act_dim, dtype=np.float32)
                self.log_std_spot = base.pi.log_std
                self.log_std_titan = base.pi.log_std
            else:
                self.log_std_spot = torch.nn.Parameter(torch.as_tensor(log_std_spot))
                self.log_std_titan = torch.nn.Parameter(torch.as_tensor(log_std_titan))
            if args.transfer_learning:
                self.z_net = base.pi.z_net
            else:
                self.z_net = CNN(im_dim)
            # Need to do a dry run to initialise Lazy module
            self.z_net(torch.zeros(self.im_dim))
            
            feature_shape=256
            feature_shape_r1=256
            feature_shape_r2=256
            # print(obs_dim);exit()
            if args.transfer_learning:
                self.feature_layers = base.pi.mu_net[:-2]
            else:
                self.feature_layers = mlp([obs_dim + 64] + list(hidden_sizes), activation)
            if args.transfer_learning:
                self.spot_output_layer = base.pi.mu_net[-2:]
                
                self.titan_output_layer = base.pi.mu_net[-2:]
            else:
                self.spot_output_layer = output_layer(feature_shape,2)
                self.titan_output_layer = output_layer(feature_shape,2)
            # print("layer",self.spot_output_layer,self.titan_output_layer)
            # feature_shape=256
            # self.output_layer = output_layer(feature_shape,act_dim)
        # elif (act_dim==(2,2)) and args.IHPPO:
        #     dtr_act_dim=2
        #     titan_act_dim=2
            

        #     log_std_dtr = -0.0 * np.ones(dtr_act_dim, dtype=np.float32)
        #     log_std_titan = -0.0 * np.ones(titan_act_dim, dtype=np.float32)
        #     # log_std = -0.0 * np.ones(act_dim, dtype=np.float32)
        #     self.log_std_dtr = torch.nn.Parameter(torch.as_tensor(log_std_dtr))
        #     self.log_std_titan = torch.nn.Parameter(torch.as_tensor(log_std_titan))
        #     self.z_net = CNN(im_dim)
        #     # Need to do a dry run to initialise Lazy module
        #     self.z_net(torch.zeros(self.im_dim))
        #     # self.mu_net1 = mlp([obs_dim + 64] + list(hidden_sizes) + [act_dim[0]], activation)
        #     # self.mu_net2 = mlp([obs_dim + 64] + list(hidden_sizes) + [act_dim[1]], activation)
        #     # self.mu_net = mlp([obs_dim + 64] + list(hidden_sizes) + [act_dim], activation)
        #     feature_shape=256
        #     feature_shape_r1=256
        #     feature_shape_r2=256
        #     self.feature_layers = mlp([obs_dim + 64] + list(hidden_sizes), activation)
        #     self.dtr_output_layer = output_layer(feature_shape,2)
        #     self.titan_output_layer = output_layer(feature_shape,2)
        #     # feature_shape=256
        #     # self.output_layer = output_layer(feature_shape,act_dim)
        # elif (act_dim==(2,2) or act_dim==(3,3)):
        #     act_dim=act_dim
        #     # print("DID IT COME HERE",act_dim)
        #     log_std = -0.0 * np.ones(act_dim, dtype=np.float32)
        #     self.log_std = torch.nn.Parameter(torch.as_tensor(log_std))
        #     self.z_net = CNN(im_dim)
        #     # Need to do a dry run to initialise Lazy module
        #     self.z_net(torch.zeros(self.im_dim))
        #     self.feature_layers = mlp([obs_dim + 64] + list(hidden_sizes), activation)
        #     feature_shape=256
        #     self.output_layer = output_layer(feature_shape,act_dim)

        # elif len(act_dim)==1 and (args.IHPPO or args.heterogeneous or args.titanheads):
        #     print("th");exit()
        #     spot_act_dim=2
        #     titan_act_dim=2

        #     log_std_spot = -0.0 * np.ones(spot_act_dim, dtype=np.float32)
        #     log_std_titan = -0.0 * np.ones(titan_act_dim, dtype=np.float32)
        #     # log_std = -0.0 * np.ones(act_dim, dtype=np.float32)
        #     self.log_std_spot = torch.nn.Parameter(torch.as_tensor(log_std_spot))
        #     self.log_std_titan = torch.nn.Parameter(torch.as_tensor(log_std_titan))
        #     self.z_net = CNN(im_dim)
        #     # Need to do a dry run to initialise Lazy module
        #     self.z_net(torch.zeros(self.im_dim))
            
        #     feature_shape=256
        #     feature_shape_r1=256
        #     feature_shape_r2=256
        #     # print(obs_dim);exit()
        #     self.feature_layers = mlp([obs_dim + 64] + list(hidden_sizes), activation)
        #     self.spot_output_layer = output_layer(feature_shape,2)
        #     self.titan_output_layer = output_layer(feature_shape,2)
        #     # act_dim=act_dim[0]
        #     # # print("ISITCOMING")
        #     # # print("DID IT COME HERE",act_dim)
        #     # log_std = -0.0 * np.ones(act_dim, dtype=np.float32)
        #     # self.log_std = torch.nn.Parameter(torch.as_tensor(log_std))
        #     # self.z_net = CNN(im_dim)
        #     # # Need to do a dry run to initialise Lazy module
        #     # self.z_net(torch.zeros(self.im_dim))
        #     # self.feature_layers = mlp([obs_dim + 64] + list(hidden_sizes), activation)
        #     # feature_shape=256
        #     # self.output_layer = output_layer(feature_shape,act_dim)
        else:
            # print("th");exit()
            act_dim=act_dim[0]
            # print("NextCOMING",[act_dim])
            self.obs_dim = obs_dim
            self.im_dim = im_dim
            # log_std = -0.5 * np.ones(act_dim, dtype=np.float32)
            

            if args.transfer_learning:
                # log_std = -0.0 * np.ones(act_dim, dtype=np.float32)
                self.log_std = base.pi.log_std
            else:
                log_std = -0.0 * np.ones(act_dim, dtype=np.float32)
                self.log_std = torch.nn.Parameter(torch.as_tensor(log_std))
            if args.transfer_learning:
                self.z_net = base.pi.z_net
            else:
                self.z_net = CNN(im_dim)
            # Need to do a dry run to initialise Lazy module
            self.z_net(torch.zeros(self.im_dim))
            if args.transfer_learning:
                self.mu_net= base.pi.mu_net
                # print()
            else:
                self.mu_net = mlp([obs_dim + 64] + list(hidden_sizes) + [act_dim], activation)
            # if args.transfer_learning:
            #     self.feature_layers = base.pi.mu_net[:-2]
            # else:
            #     self.feature_layers = mlp([obs_dim + 64] + list(hidden_sizes), activation)
            #     # self.mu_net = mlp([obs_dim + 64] + list(hidden_sizes), activation)
            # # self.mu_net = mlp([obs_dim + 64] + list(hidden_sizes) + [act_dim], activation)
            # feature_shape=256
            # self.mu_net = output_layer(feature_shape,2)

        # # self.output_layer = output_layer(feature_shape_r1,feature_shape_r2,act_dim)
        # # self.output_layer = [output_layer_r1(feature_shape_r1,act_dim[0]),output_layer_r2(feature_shape_r2,act_dim[1])]
        # # self.output_layer_r1 = output_layer_r1(feature_shape_r1,act_dim[0])
        # # self.output_layer_r2 =output_layer_r2(feature_shape_r2,act_dim[1])

    def _distribution(self, obs, im):
        # print("obs_before",obs,len(obs),im,len(im))
        # obs=obs[0]
        # print("core_obs",int(obs[1][0]))
        if args.heterogeneous or args.titanheads:
            ob = obs
            self.obs_dim=6
            # if len(obs)==2:
                # obs =  torch.tensor([np.array(obs[0][1:]), np.array(obs[1][1:])], dtype=torch.float32)
            # print("obs_before",obs)
            obs = torch.tensor([np.array(observ[1:]) for observ in obs]) 
            # print("checkhpc_obs",obs)
            
            # li = [observ[1:] for observ in obs]
            # # print("checkhpc_li",li)
            # li=np.array(li)
            # # print("li_array",li)
            # obs = torch.tensor(li) 
            # # print("obs_twoone",obs,type(obs))
            
        
        obs = torch.reshape(obs, [-1, self.obs_dim])
        # print("obs_after",obs,len(obs),im,len(im))

        # z = self.z_net(im)
        # print("dis_im_1",im[0],len(im[0]))
        # z = self.z_net(im[0:1])
        # print("dimention_match",im.shape,obs.shape,len(obs))
        # print("dimention_match_1",im[0:1].shape,obs.shape)
        # z2 = self.z_net(im[1])
        # print("self.z_net(im)",self.z_net(im[0:1]),self.z_net(im[0:1]).shape)
        t=torch.concat((obs, self.z_net(im)), -1)
        # print("concate_shape",t,t.shape)

        # model = nn.Sequential(
        #         nn.Linear(70, 256),   # Linear layer: 70 input features, 256 output features
        #         nn.Tanh(),            # Tanh activation
        #         nn.Linear(256, 256),  # Linear layer: 256 input features, 256 output features
        #         nn.Tanh(),            # Tanh activation
        #         nn.Linear(256, 3),    # Linear layer: 256 input features, 3 output features
        #         nn.Identity()         # Identity function (no activation for final output)
        #     )
        # self.mu = self.mu_net(torch.concat((obs, self.z_net(im)), -1))
        # print("self.feature_extraction",self.feature_extraction,self.feature_extraction.shape)
        if args.heterogeneous or args.titanheads:
            self.feature_extraction = self.feature_layers(torch.concat((obs, self.z_net(im)), -1))
            
            if args.spot_additional_layer:
                # self.mu_spot=self.spot_output_layer(self.feature_extraction)
                # print("self.feature_extraction",self.feature_extraction.shape)
                self.intermediate=self.spot_additional_layer(self.feature_extraction)
                # print("self.intermediate",self.intermediate.shape)

                self.mu_spot=self.spot_output_layer(self.intermediate)
                # print("self.mu_spot",self.mu_spot,type(self.mu_spot),self.mu_spot.shape)
                self.mu_titan=self.titan_output_layer(self.feature_extraction)
            else:
                self.mu_spot=self.spot_output_layer(self.feature_extraction)
                self.mu_titan=self.titan_output_layer(self.feature_extraction)

            self.std_spot = torch.exp(self.log_std_spot)
            self.std_titan = torch.exp(self.log_std_titan)
            # print("self.std_titan",self.std_titan)
            # print("OB_CHEKC",ob)
            if len(obs)==2:            
                return Normal(self.mu_spot, self.std_spot),Normal(self.mu_titan, self.std_titan)
        
            elif (int(ob[0][0]) == 0 and not len(obs)==2) and (args.heterogeneous or args.titanheads):    
                        
                return Normal(self.mu_titan, self.std_titan)
        
            elif (int(ob[0][0]) == 1 and not len(obs)==2) and (args.heterogeneous or args.titanheads):   
                # print("f");exit()         
                return Normal(self.mu_spot, self.std_spot)
        
        # elif len(obs)==2 and args.IHPPO:
        #     self.feature_extraction = self.feature_layers(torch.concat((obs, self.z_net(im)), -1))

        #     self.mu_dtr=self.dtr_output_layer(self.feature_extraction)
        #     # print("self.mu_dtr",self.mu_dtr,type(self.mu_dtr),self.mu_dtr.shape)
        #     self.mu_titan=self.titan_output_layer(self.feature_extraction)
        #     # print(self.feature_extraction[0:1],self.feature_extraction[0:1].shape,self.feature_extraction[1:2].shape,self.feature_extraction.shape)
        #     # self.mu_dtr,self.mu_titan=self.output_layer(self.feature_extraction[0:1],self.feature_extraction[1:2])
            
            
        #     # self.mu_r1,self.mu_r2=self.output_layer_r1(self.feature_extraction[0:1]),self.output_layer_r2(self.feature_extraction[1:2])
            


        #     # # self.mu = model(torch.concat((obs, self.z_net(im)), -1))
        #     # # print("mu_regular",self.mu)
        #     # self.mu1 = self.mu_net1(torch.concat((obs[0:1], self.z_net(im[0:1])),-1))
        #     # self.mu2 = self.mu_net2(torch.concat((obs[1:2], self.z_net(im[1:2])),-1))

        #     # # Compare feature dimensions (second dimension)
        #     # if self.mu1.shape[1] < self.mu2.shape[1]:
        #     #     # Pad self.mu1 to match the feature size of self.mu2
        #     #     padding_size = self.mu2.shape[1] - self.mu1.shape[1]
        #     #     self.mu1_padded = F.pad(self.mu1, (0, padding_size))  # Pads self.mu1 on the right (feature dimension)
        #     #     self.mu = torch.cat((self.mu1_padded, self.mu2), dim=0)  # Concatenate along the batch dimension
        #     # elif self.mu2.shape[1] < self.mu1.shape[1]:
        #     #     # Pad self.mu2 to match the feature size of self.mu1
        #     #     padding_size = self.mu1.shape[1] - self.mu2.shape[1]
        #     #     self.mu2_padded = F.pad(self.mu2, (0, padding_size))  # Pads self.mu2 on the right (feature dimension)
        #     #     self.mu = torch.cat((self.mu1, self.mu2_padded), dim=0)  # Concatenate along the batch dimension
        #     # else:
        #     #     # If both have the same feature size, concatenate them directly
        #     #     self.mu = torch.cat((self.mu1, self.mu2), dim=0)
        #     # # self.mu = torch.cat((self.mu1, self.mu2), dim=0)
        #     # print("mu_concate",self.mu)
        #     # self.mu = self.mu_net(torch.concat((obs, self.z_net(im)), -1))
        #     # print("self.mu",self.mu,"self.mu2",self.mu2)
        #     # self.std = torch.exp(self.log_std)
        #     # self.std_r1 = torch.exp(self.log_std_r1)
        #     # self.std_r2 = torch.exp(self.log_std_r2)

        #     self.std_dtr = torch.exp(self.log_std_dtr)
        #     self.std_titan = torch.exp(self.log_std_titan)

        #     # print("NORMALDIM",self.mu.shape,self.std.shape,self.std,Normal(self.mu, self.std))
        #     return Normal(self.mu_dtr, self.std_dtr),Normal(self.mu_titan, self.std_titan)
        
        # elif len(obs)==1 and (args.IHPPO or args.heterogeneous or args.titanheads): 
        #     self.feature_extraction = self.feature_layers(torch.concat((obs, self.z_net(im)), -1))

        #     self.mu=self.output_layer(self.feature_extraction)
        #     self.std = torch.exp(self.log_std)
        #     return Normal(self.mu, self.std)
        else:
            # print("GGCMING")
            # print("CHEKINGLOPP");exit()
            self.mu = self.mu_net(torch.concat((obs, self.z_net(im)), -1))
            # print("self.log_std",self.log_std)

            # if args.transfer_learning:
            #     # self.std=self.base_model.pi.std
            #     self.std = torch.exp(self.log_std)
            # else:                           
            self.std = torch.exp(self.log_std)
            # self.std = std_dev
            # print("Base_STD",self.std)
            # # self.std = 0.1164
            
            # print("STD",self.std)
            return Normal(self.mu, self.std)
    
    def _distribution_clipped(self, obs, im):
        obs = torch.reshape(obs, [-1, self.obs_dim])
        z = self.z_net(im)
        self.mu = self.mu_net(torch.concat((obs, self.z_net(im)), -1))
        self.std = torch.exp(self.log_std)

        


        # Sample a raw action from the multivariate Gaussian distribution
        raw_action = Normal(self.mu, self.std)

        # Define the bounds for each dimension
        bounds = [(-0.5, 1), (-1.5, 1.5)]

        # Apply the tanh squashing function and scale to the desired bounds for each dimension
        bounded_action = np.zeros_like(raw_action)
        
        for i in range(len(raw_action)):
            lower_bound, upper_bound = bounds[i]
            squashed_action = np.tanh(raw_action[i])  # Squash to [-1, 1]
            scaled_action = (squashed_action + 1) / 2  # Scale to [0, 1]
            bounded_action[i] = scaled_action * (upper_bound - lower_bound) + lower_bound
        
        return bounded_action

    def _log_prob_from_distribution(self, pi, act):
        # print("pi",pi,"act",act,"self",self)
        return pi.log_prob(act).sum(axis=-1)    # Last axis sum needed for Torch Normal distribution

class MLPCriticPerception(nn.Module):



    def __init__(self, base, obs_dim, hidden_sizes, activation, z_net):
        super().__init__()
        self.obs_dim = obs_dim
        if args.heterogeneous or args.titanheads:
            self.obs_dim = 6
            obs_dim = 6

        if args.transfer_learning:
            self.z_net=base.v.z_net
        else:
            self.z_net = z_net
        if args.transfer_learning:
            self.v_net=base.v.v_net
        else:
            self.v_net = mlp([obs_dim + 64] + list(hidden_sizes) + [1], activation)

    def forward(self, obs, im):
        if args.heterogeneous or args.titanheads:
            # if len(obs)==2:
            #     obs =  torch.tensor([np.array(obs[0][1:]), np.array(obs[1][1:])], dtype=torch.float32)
            # else:
            #     # print("CHECK",obs[0][1:])
            #     obs =  torch.tensor(np.array(obs[0][1:]), dtype=torch.float32) 
            # if len(obs)==2:
                # obs =  torch.tensor([np.array(obs[0][1:]), np.array(obs[1][1:])], dtype=torch.float32)
                # print("V_obs_before",obs)
                # obs = torch.tensor([np.array(observ[1:]) for observ in obs]) 
            obs = torch.tensor([np.array(observ[1:]) for observ in obs]) 
            # li = [observ[1:] for observ in obs]
            # li=np.array(li)
            # obs = torch.tensor(li) 
              
        obs = torch.reshape(obs, [-1, self.obs_dim])
        return torch.squeeze(self.v_net(torch.concat((obs, self.z_net(im)), -1)), -1) # Critical to ensure v has right shape.



    

class MLPActorCriticPerception(nn.Module):

    def __init__(self, base, observation_space,  im_dim, action_space,
                 hidden_sizes=(64,64), activation=nn.Tanh):
        
        super().__init__()
        # action_space=[(-10000.0, 10000.0, (2,)),(-10000.0, 10000.0, (2,))]
        # action_space=Box(-10000.0, 10000.0, (2,3))
        # print("core",action_space.shape);exit()
        obs_dim = observation_space.shape[0]
        # if args.heterogeneous or args.titanheads:
        #     obs_dim=6
        # print("obs_dim",obs_dim)
        # obs_dim = observation_space.shape[0]
        # obs_dim=6
        # im_dim=[1,80,80]
        # print(obs_dim)
        # # # # policy builder depends on action space
        # for action_sp in action_space:
        #     if isinstance(action_sp, Box):
        #         print("core_shape",action_sp,action_sp.shape[0])
        #         self.pi = MLPGaussianActorPerception(obs_dim, im_dim, action_sp.shape[0], hidden_sizes, activation)
        # # # policy builder depends on action space
        
        if isinstance(action_space, Box):
            # print("core_shape",action_space,action_space.shape)
            # self.pi = MLPGaussianActorPerception(obs_dim, im_dim, action_space.shape[0], hidden_sizes, activation)
            self.pi = MLPGaussianActorPerception(base, obs_dim, im_dim, action_space.shape, hidden_sizes, activation)
            # print('attributes',dir(self.pi))
        
        # print("self.pi",self.pi)
        # build value function
        self.v  = MLPCriticPerception(base, obs_dim, hidden_sizes, activation, self.pi.z_net)


    def step(self, obs, im, stochastic=True):
        # print("stepobs",obs.shape)
        # print("lenlen",len(obs),len(im))
        # obs=obs[0]
        # pi = self.pi._distribution(obs, im)
        if args.heterogeneous or args.titanheads:
            pi_spot,pi_titan = self.pi._distribution(obs, im)
        # elif args.IHPPO:
        #     pi_dtr,pi_titan = self.pi._distribution(obs, im)
        else:
            pi = self.pi._distribution(obs, im)
        # pi = self.pi._distribution_clipped(obs, im)
        
        # print(pi_spot,pi_titan);exit()

        if stochastic:
            if args.heterogeneous or args.titanheads:
                a_spot = pi_spot.sample()
                a_titan = pi_titan.sample()
            # elif args.IHPPO:
            #     a_dtr = pi_dtr.sample()
            #     a_titan = pi_titan.sample()
            else:
                a = pi.sample()
            # print("STEPA",a);exit()
        else:
            if args.heterogeneous or args.titanheads:
                a_spot = self.pi.mu_spot
                a_titan = self.pi.mu_titan
            # elif args.IHPPO:
            #     a_dtr = self.pi.mu_dtr
            #     a_titan = self.pi.mu_titan
            else:
                a = self.pi.mu
            
        # # print("action_core",a_spot,"titanaction",a_titan)
        # if args.gausian_clip:
        #     r1_clipped_linear_vel_command=np.clip(a[0][0].detach().numpy(), -0.5, 1)
        #     r1_clipped_angular_vel_command=np.clip(a[0][1].detach().numpy(), -1.5, 1.5)

        #     r2_clipped_linear_vel_command=np.clip(a[1][0].detach().numpy(), -0.5, 1)
        #     r2_clipped_angular_vel_command=np.clip(a[1][1].detach().numpy(), -1.5, 1.5)

        #     a=torch.tensor([[r1_clipped_linear_vel_command,r1_clipped_angular_vel_command],[r2_clipped_linear_vel_command,r2_clipped_angular_vel_command]])
        # # print("policy_vel",a,type(a))

        if args.heterogeneous or args.titanheads:
            logp_a_spot = self.pi._log_prob_from_distribution(pi_spot, a_spot)
            logp_a_titan = self.pi._log_prob_from_distribution(pi_titan, a_titan)
        # elif args.IHPPO:
        #     logp_a_dtr = self.pi._log_prob_from_distribution(pi_dtr, a_dtr)
        #     logp_a_titan = self.pi._log_prob_from_distribution(pi_titan, a_titan)
        else:
            logp_a = self.pi._log_prob_from_distribution(pi, a)
        
        # print(obs[0:1],len(obs[0:1]),len(im[0:1]),im[0:1])

        if ( args.heterogeneous or args.titanheads or args.IHPPO) and not args.combined_value:
            v1 = self.v(obs[0:1], im[0:1])
            v2 = self.v(obs[1:2], im[1:2])
            v= torch.concat((v1,v2), -1)
            # print("value",v)
        elif (args.heterogeneous or args.titanheads or args.IHPPO) and args.combined_value:
            v = self.v(obs, im)
        else:
            v = self.v(obs, im)
            # print("value_regular",v)
        

        # Memory leak happens here somewhere. Copying the arrays seem to help??
        v_copy = v.cpu().detach().data.numpy().copy()
        # print("val",v_copy);exit()

        if args.heterogeneous or args.titanheads:
            a_copy_spot = a_spot.cpu().detach().data.numpy().copy()
            a_copy_titan = a_titan.cpu().detach().data.numpy().copy()
            logp_a_copy_spot = logp_a_spot.cpu().detach().data.numpy().copy()
            logp_a_copy_titan = logp_a_titan.cpu().detach().data.numpy().copy()
        # elif args.IHPPO:
        #     a_copy_dtr = a_dtr.cpu().detach().data.numpy().copy()
        #     a_copy_titan = a_titan.cpu().detach().data.numpy().copy()
        #     logp_a_copy_dtr = logp_a_dtr.cpu().detach().data.numpy().copy()
        #     logp_a_copy_titan = logp_a_titan.cpu().detach().data.numpy().copy()
        else:
            a_copy = a.cpu().detach().data.numpy().copy()
            logp_a_copy = logp_a.cpu().detach().data.numpy().copy()
        # print("val",v_copy);exit()
        if args.heterogeneous or args.titanheads:
            return a_copy_spot, a_copy_titan, v_copy, logp_a_copy_spot, logp_a_copy_titan
        # elif args.IHPPO:
        #     return a_copy_dtr, a_copy_titan, v_copy, logp_a_copy_dtr, logp_a_copy_titan
        else:
            return a_copy, v_copy, logp_a_copy

    def act(self, obs, im):
        return self.step(obs, im)[0]

# # ==========================================================================================================
# # Without perception 
# # ==========================================================================================================
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