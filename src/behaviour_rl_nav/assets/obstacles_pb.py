import numpy as np
import pybullet as p
import copy

class Obstacles():
  def __init__ (self):
    self.box_id = []
    self.positions = []
    self.sizes = []
    self.colours = []
    
    self.circle_id = []
    self.circle_sizes = []
    self.circle_colours = []

  def remove_obstacles(self):
    if self.box_id:
      for b in self.box_id:
        p.removeBody(b)
      self.box_id = []
      self.positions = []
      self.sizes = []
      self.colours = []

    if self.circle_id:
      for b in self.circle_id:
        p.removeBody(b)
      self.circle_id = []
      self.circle_sizes = []
      self.circle_colours = []


  def add_doors(self, difficulty):
    # Flat box
    # self.add_box([1, -1.5, 1], [0,0,0], [0.2,1,1], colour=[0.8,0.3,0.5,1])
    # self.add_box([1, 1.5, 1], [0,0,0.5], [0.2,1,1], colour=[0.8,0.3,0.5,1])


    # self.add_box([50, -1.5, 1], [0,0,0], [0.2,1,1], colour=[0.8,0.3,0.5,1])
    # self.add_box([50, 1.5, 1], [0,0,0.5], [0.2,1,1], colour=[0.8,0.3,0.5,1])
    for j in range(4):
      y_offset = j*5
      ground_size = [15, np.random.uniform(3, 6), 1]
      ground_pos = [ground_size[0] - 1.0, y_offset, ground_size[2]]
      ground_orn = [0,0,0]
      self.add_box(ground_pos, ground_orn, ground_size, colour=[0.3,0.3,0.8,1])
      
      x_min = ground_pos[0] - ground_size[0] - 0.2
      x_max = ground_pos[0] + ground_size[0] + 0.2
      y_min = ground_pos[1] - ground_size[1] - 0.2 + y_offset
      y_max = ground_pos[1] + ground_size[1] + 0.2 + y_offset
      size_x = [ground_size[0], 0.2, 2]
      size_y = [0.2, ground_size[1] + size_x[1]*2, 2]
      self.add_box([ground_pos[0], y_min, size_x[2]],[0,0,0], size_x, colour=[0.3,0.8,0.5,1])
      self.add_box([ground_pos[0], y_max, size_x[2]], [0,0,0], size_x, colour=[0.3,0.8,0.5,1])
      self.add_box([x_min, ground_pos[1], size_y[2]], [0,0,0], size_y, colour=[0.3,0.8,0.5,1])
      self.add_box([x_max, ground_pos[1], size_y[2]], [0,0,0], size_y, colour=[0.3,0.8,0.5,1])

      # pos = np.
      # for _ in range(10):
      ground_width = ground_size[1]
      z_offset = ground_pos[2] + ground_size[2]
      # x = np.random.uniform(6,8)

      x = 5
      # 1-10   
      for i in range(4):
          #  x += 8
          door_width = -0.078*np.random.uniform(difficulty-1, difficulty) + 1.578

          # door_width = np.random.uniform(0.7, 1.0)
          # size = [0.2, np.random.uniform(ground_width/2-0.4, ground_width/2 + 0.4), 1]
          # size = [0.2, np.random.uniform(ground_width/2-0.3, ground_width/2 + 0.3), 1]
          wall =  (ground_width - door_width*2 - 0.35)
          size = [0.2, wall, 1]
          # print(size)
          pos = [x, size[1] + door_width/2 + y_offset, z_offset + size[2]]

          # orn = [0,0,0.5]
          orn = [0,0,0]
          self.add_box(pos, orn, size, colour=[0.8,0.3,0.5,1])
          size = [size[0], wall, 1]
          # print(size)

          pos = [x, -(size[1] + door_width/2) + y_offset, z_offset + size[2]]
          orn = [0,0,0]
          self.add_box(pos, orn, size, colour=[0.8,0.3,0.5,1])
          x += np.random.uniform(5,7)
    
    return self.get_box_info()
  
  
  def add_steps(self, difficulty=10, height_coeff=0.07, terrain_type='mix', base=False, base_before=False, initial_pos=[0,0,0], baseline=False, two=False, rand_flat=False, foot=True):
    initial_size = [0.18, 0, 0.5]
    # initial_size = [np.random.uniform(0.18,0.22), np.random.uniform(0.55,0.85), 0.5]
    # initial_size = [0.2, 0.7, 0.5]
    # print("fixed size", initial_size)
    size = copy.copy(initial_size)
    # pos = [-initial_size[0]-0.5+initial_pos[0],0+initial_pos[1],initial_size[2]+initial_pos[2]]
    pos = [-initial_size[0] + 0.35 +initial_pos[0],0+initial_pos[1],initial_size[2]+initial_pos[2]]
    prev_size = copy.copy(initial_size)
    prev_yaw = 0
    order = ['steps' for _ in range(15)]
    colours = []
    for pol in order:
      colours.append([0.6,0.4,0.7,1])

    yaws = [0.0]*len(order)

    count = 0
    lowest = 0
    prev_height = (lowest + 2)*height_coeff + 0.4
    pos[2] = prev_height
    size[2] = prev_height
    prev_size = copy.copy(size)
    yaw = 0
    # height_coeff += 0.03
    prev_o = 'flat'
    # step_width = np.random.uniform(-0.04*difficulty + 0.5, -0.04*difficulty + 0.7)
    # step_pos = np.random.choice([-1,1])*np.random.uniform(0,0.2)
    step_width = 0.1
    if foot:
      step_pos = -1*0.15
    else:
      step_pos = 1*0.15
    pos = [pos[0], step_pos, prev_height]
    size = [size[0], step_width, prev_height]
    
      #     elif pol == 'zero':
      #   colours.append([0.8,0.5,0.3,1])
      # elif pol == 'flat':
      #   colours.append([0.3,0.3,0.8,1])
    # size_box = [0.45, 0.55, 0.5]
    # pos, prev_yaw = self.add_curved_box(pos, prev_yaw=prev_yaw, prev_size=prev_size, size=size_box, yaw=yaw, colour=[0.8,0.5,0.3,1], centre=False)
    
    
    # pos, prev_yaw = self.add_curved_box(pos, prev_yaw=prev_yaw, prev_size=prev_size, size=size, yaw=yaw, colour=colours[0], centre=True)
    # pos, prev_yaw = self.add_box(pos, prev_yaw=prev_yaw, prev_size=prev_size, size=size, yaw=yaw, colour=colours[0], centre=True)
    
        
    self.add_box(pos, orn=[0,0,0], size=size, colour=colours[0])
    
    prev_size = copy.copy(initial_size)
    step_pos = -step_pos
    pos = [pos[0], step_pos, prev_height]
    size = [size[0], step_width, prev_height]
    self.add_box(pos, orn=[0,0,0], size=size, colour=colours[0])
    # pos, prev_yaw = self.add_curved_box(pos, prev_yaw=prev_yaw, prev_size=prev_size, size=size, yaw=yaw, colour=colours[0], centre=True)
    for i,o in enumerate(order):        
      step_pos = -1*step_pos
      pos[1] = step_pos
      # height = prev_height + np.random.uniform(-difficulty/100, difficulty/100)
      height = prev_height 
      pos = [pos[0], pos[1], height]
      size = [size[0], step_width, height]
      prev_o = o
      prev_height = height
      yaw = 0.0
      pos2 = [pos[0], -pos[1], height]
      pos, prev_yaw = self.add_curved_box(pos, prev_yaw=prev_yaw, prev_size=prev_size, size=size, yaw=yaw, colour=colours[i], centre=True)
      
      if difficulty < 9:
        size2 = [size[0]*((10-difficulty)/10), step_width, prev_height]
        pos2, prev_yaw = self.add_curved_box(pos2, prev_yaw=prev_yaw, prev_size=prev_size, size=size2, yaw=yaw, colour=colours[i], centre=True)

      prev_size = copy.copy(size)

  def add_straight_world(self, difficulty=10, height_coeff=0.07, terrain_type='mix', base=False, base_before=False, initial_pos=[0,0,0], baseline=False, num_artifacts=1, rand_flat=False, args=None, obstacle_types=None, dqn=False):
    self.args = args
    # difficulty = 10
    # print(terrain_type)
    # if difficulty == 10:
    #   height_coeff = 0.07
    # else:
      # height_coeff = np.random.uniform((0.04/10)*difficulty + 0.02, (0.05/10)*difficulty + 0.02)
      # height_coeff = (0.05/10)*difficulty + 0.02
    # height_coeff = (0.07/10)*difficulty 
    # height_coeff = (0.1/10)*difficulty 
    # Hardest
    # terrain_type='mix'

    height_coeff = (0.085/10)*difficulty 
    # Latest
    # height_coeff = (0.08/10)*difficulty 
    if terrain_type == 'flat':
      initial_size = [np.random.uniform(0.18,0.22), np.random.uniform(0.55,0.85) - difficulty*0.01, 0.5]
    # elif terrain_type == 'mix':
    #   initial_size = [np.random.uniform(0.18,0.22), np.random.uniform(0.55,0.6), 0.5]
    else:
      initial_size = [np.random.uniform(0.18,0.22), np.random.uniform(0.55,0.85), 0.5]

    # initial_size = [np.random.uniform(0.18,0.22), np.random.uniform(0.4,0.5), 0.5]
    # initial_size = [0.2, 0.7, 0.5]
    # initial_size = [np.random.uniform(0.18,0.22), 0.55, 0.5]
    size = copy.copy(initial_size)
    pos = [-initial_size[0]-0.5+initial_pos[0],0+initial_pos[1],initial_size[2]+initial_pos[2]]
    prev_size = copy.copy(initial_size)
    prev_yaw = 0
    if terrain_type == 'mix':
      # Meke sure not same terrain type twice in a row
      rand_order = []
      # all_options = ['jumps','gaps','stairs', 'steps', 'high_jumps']
      # option = np.random.choice(['jumps','gaps','stairs', 'steps', 'high_jumps'])
      # if args.old:
      #   all_options = ['jumps','gaps','stairs']
      # else:
        # all_options = ['flat', 'jumps','gaps','stairs','steps', 'high_jumps', 'hard_steps', 'hard_high_jumps', 'one_leg_hop']
      # all_options = ['flat', 'steps']
      all_options = obstacle_types
      # options = copy.copy(all_options)
      # options.remove('gaps')
      # rand_order.append(np.random.choice(['jumps','stairs']))
      rand_order.append(np.random.choice(all_options))
      # rand_order.append('gaps')
      
      while len(rand_order) < 7:
        choice = np.random.choice(all_options)
        # while choice == rand_order[-1] and ((rand_order[-1] != 'jumps') or (rand_order[-1] == 'jumps' and choice != 'steps')):
        while choice == rand_order[-1]:
          choice = np.random.choice(all_options)
        rand_order.append(choice)
        # choice = 
        # option = np.random.choice(all_options)      
        # option = np.random.choice(options)

      # all_options = obstacle_types
      # # all_options = ['jumps','gaps','stairs','steps']
      # option = np.random.choice(all_options)
      # for i in range(7):
      # # for i in range(1):
      #   rand_order.append(option)
      #   options = copy.copy(all_options)
      #   options.remove(option)
      #   option = np.random.choice(options)
      # # print("fixed rand order")
      # # rand_order = ['high_jumps', 'gaps', 'jumps', 'stairs', 'steps']

    elif terrain_type == 'dqn':
      rand_order = [np.random.choice(['jumps','gaps','stairs']) for _ in range(15)]
    elif terrain_type == 'multi':
      rand_order = ['jumps','gaps','stairs']
    elif terrain_type == 'zero':
      rand_order = []
    else:
      if baseline:
        rand_order = [terrain_type for _ in range(7)]
      else:
        rand_order = [terrain_type for _ in range(num_artifacts)]
    if not args.single_pol and terrain_type in ['high_jumps', 'hard_high_jumps', 'one_leg_hop']:
      order = []
      pol_order = []
      yaws = []
    else:
      order = ['flat','flat','flat','flat','flat']
      pol_order = ['flat','flat','flat','flat','flat']
      yaws = [0.0, 0.0, 0.0, 0.0, 0.0]
    pre_artifact_box = []
    if base:
      order = ['flat']*(3*2 + 7*7)
      pol_order = ['flat']*(3*2 + 7*7)
    else:
      # print(rand_order)
      prev_yaw = 0.0
      yaw = 0.0
      curve = np.random.choice([-1,1])
      # up_down = np.random.choice([0,1])
      for r in rand_order:
        if r == 'stairs':
          up_down = np.random.choice(['up', 'down'])
        # if terrain_type == 'mix':        
        #   artifact_size = np.random.randint(4,7)
        #   # artifact_size = np.random.randint(5,9)
        #   if r == 'stairs':
        #     placement = np.random.randint(0,3)
        #     stair = np.random.choice(['up', 'down'])

        #   else:
        #     if artifact_size == 4:
        #       placement = 2
        #     else:
        #       placement = np.random.randint(2,artifact_size-2)
        #       # placement = np.random.randint(1,artifact_size-3)
        # else:
        # if r in ['stairs', 'steps', 'flat']:
        #   artifact_size = np.random.randint(7,8)
        # else:
        if r == 'high_jumps':
          # artifact_size = 5
          # artifact_size = 4
          artifact_size = 2
        elif r in ['hard_high_jumps']:
          # artifact_size = 5
          artifact_size = 4
          # artifact_size = 3
        elif r in ['flat','hop']:
          # artifact_size = 40
          artifact_size = np.random.randint(7,9)
        elif r in ['hard_steps']:
          artifact_size = np.random.randint(8,10)
        elif r in ['steps', 'hard_steps', 'one_leg_hop']:
          artifact_size = np.random.randint(6,8)
        elif r in ['stairs', 'hard_stairs']:
          artifact_size = np.random.randint(4,6)
          # artifact_size = np.random.randint(7,9)
        # elif r in ['jumps']:
        #   artifact_size = np.random.randint(6,8)
        else:
          # artifact_size = np.random.randint(4,8)
          # artifact_size = np.random.randint(4,6)
          # artifact_size = np.random.randint(3,4)
          artifact_size = 3
        placement = 1
        pre_artifact_box.append(len(order)) 
        if r == 'flat': 
          curve = -1*curve
        # print(r, curve, artifact_size)
        # if r == 'steps':
        
        for i in range(artifact_size):
          # print(r)
          # if r in ['stairs']:
            # print("st")
            # pass
          if r in ['flat','hop']:
            order.append('flat')

            # yaws.extend([curve*0.03*difficulty])
            if i == 0:
              yaw = 0
            else:
              yaw = curve*0.03*difficulty
            if args.easy_flat:
              yaws.append(0)
            else:
              yaws.append(yaw)
          elif r in ['hard_high_jumps'] and i > 0:
            # if i in [1,3]:
            #   order.append('gaps')
            # else:
            order.append('hard_high_jumps')

          # elif r in ['steps', 'hard_steps', 'one_leg_hop']:
          #   order.append(r)
            # pol_order.append('base')
          elif r in ['jumps', 'gaps', 'high_jumps', 'steps', 'hard_high_jumps', 'hard_stairs', 'hard_steps', 'one_leg_hop']:
            # if i == 3:
            if (i == placement) or (r in ['steps', 'hard_steps', 'hard_stairs', 'one_leg_hop'] and i > 0):
            # if (i == placement):
              order.append(r)
            else:
              order.append('flat')
          else:
            if terrain_type == 'mix':
              if i >= placement:
                order.append(np.random.choice(['up', 'down']))
                # order.append('up')
              else:
                order.append('flat')
            else:
              if i >= placement and i != artifact_size - 1:
                # print("areg you here?")
                
                # order.append(np.random.choice(['up', 'down']))
                
                # if args.up_stairs:
                #   order.extend(['up','up'])
                if args.stair_thing:
                  up_down = np.random.choice(['up', 'down'])
                  order.extend([up_down, up_down])
                  # print(order)
                else:
                  order.append(np.random.choice(['up', 'down']))
                  order.append(np.random.choice(['up', 'down']))
                pol_order.append(r)
                yaws.append(0.0)

                # up_down = np.random.choice(['up', 'down'])
                # if (up_down == 'up' and i != placement + 1) or (up_down == 'down' and i == placement + 1):
                # if (up_down == 'up'):
                #   order.append(np.random.choice(['up']))
                # else:
                #   order.append(np.random.choice(['down']))
              else:
                order.append('flat')
          pol_order.append(r)
          # if r in ['steps', 'hard_steps']:
            # yaws.append(prev_yaw)
          # elif not r in ['flat']:
          if not r in ['flat'] or args.easy_flat:
            # yaws.append(prev_yaw)
            yaws.append(0.0)
          prev_yaw = yaw
        
        # extra_flat = 4
        # for _ in range(extra_flat):
        #   pol_order.append('flat')
        #   order.append('flat')
        #   yaws.append(0.0)

        # pol_order.append('flat')
        # order.append('flat')
        # yaws.append(0.0)

        pol_order.append('flat')
        order.append('flat')
        yaws.append(0.0)
        # if self.args.additional_flat:

        # pol_order.append('flat')
        # order.append('flat')
        # yaws.append(0.0)
        # pol_order.append('flat')
        # order.append('flat')
        # yaws.append(0.0)
      # print(args.single_pol, args.dqn)
      # print(args.single_pol, dqn)
      if args.single_pol and dqn:
        # print("in obstacles")
        order.extend(['flat','flat','flat','flat','flat','flat','flat','flat','flat'])
        pol_order.extend(['flat', 'flat','flat','flat', 'flat','flat', 'flat','flat', 'zero'])
        yaws.extend([0.0, 0.0, 0.0])
      else: 
        order.extend(['flat','flat','flat','flat'])
        pol_order.extend(['flat', 'flat','flat', 'zero'])
        yaws.extend([0.0, 0.0, 0.0, 0.0])
    # print(yaws)
    colours = []
    # for pol in pol_order:
    for i,pol in enumerate(order):
      # print(pol)
      if args.show_detection and i in pre_artifact_box:
        colours.append([0.7,0.8,0.7,1])
      elif pol in ['stairs','up','down', 'hard_stairs']:
        colours.append([0.8,0.5,0.8,1])
      elif pol == 'jumps':
        colours.append([0.8,0.3,0.3,1])
      elif pol == 'high_jumps':
        colours.append([0.8,0.4,0.3,1])
      elif pol == 'hard_high_jumps':
        colours.append([0.7,0.3,0.2,1])
      elif pol == 'steps':
        colours.append([0.6,0.4,0.7,1])
      elif pol == 'hard_steps':
        colours.append([0.5,0.3,0.6,1])
      elif pol == 'gaps':
        colours.append([0.3,0.8,0.3,1])
      elif pol == 'zero':
        colours.append([0.8,0.5,0.3,1])
      elif pol in ['flat','hop']:
        colours.append([0.3,0.3,0.8,1])
      elif pol in ['one_leg_hop']:
        colours.append([0.2,0.6,0.2,1])
      else:
        print("obstacle_not _found")

    count = 0
    lowest = 0
    for name in order:
      if name == 'down': count += 1
      if name == 'up': count -= 1
      if count > lowest:
        lowest = count
    prev_height = (lowest + 2)*height_coeff + 0.4
    pos[2] = prev_height
    size[2] = prev_height
    # self.add_box(pos, [0,0,0], size)
    prev_size = copy.copy(size)
    prev_pos = copy.copy(pos)
    yaw_count = 0
    prev_o = 'flat'
    # print(pol_order, order, difficulty)
    # print(pol_order)
    # print(pre_artifact_box)
    # print(yaws)
    self.first_step = 0
    prev_yaw = 0
    for i,(o, yaw) in enumerate(zip(order, yaws)):        
      # initial_size = [np.random.uniform(0.18,0.22), initial_size[1], 0.5]
      # print(pre_artifact_box)
      if pol_order[i] == 'zero':
        # initial_size = [0.8, initial_size[1], 0.5]
        initial_size = [0.8, initial_size[1], 0.5]
      # elif (i > 0 and pol_order[i-1] != pol_order[i]):
      elif i in pre_artifact_box:
      # if i > 1 and ((pol_order[i-2] != pol_order[i]) or (pol_order[i-1] != pol_order[i])):
        
        # initial_size = [0.45, initial_size[1], 0.5]
        initial_size = [args.detection_dist/2, initial_size[1], 0.5]
        # initial_size = [0.225, initial_size[1], 0.5]
        # order_count += 1
        # print("art", order_count)
      else:
        initial_size = [np.random.uniform(0.18,0.22), initial_size[1], 0.5]
        # initial_size = [initial_size[0], initial_size[1], 0.5]

      if o == 'down':
        height = prev_height - height_coeff
        pos[2] = height
        size = [initial_size[0], initial_size[1], height]
      elif o == 'up':
        height = prev_height + height_coeff
        pos[2] = height
        size = [initial_size[0], initial_size[1], height]
      elif o == 'jumps':
        # pos = [pos[0], pos[1], pos[2] + difficulty*0.015]
        # if difficulty == 10:
        #   pos = [pos[0], pos[1], pos[2] + 0.15]
        # else:
          # pos = [pos[0], pos[1], pos[2] + 0.05 + np.random.uniform((difficulty-1)*0.01, difficulty*0.01)]
        # pos = [pos[0], pos[1], pos[2] + 0.05 + difficulty*0.01]
        # Latest
        # pos = [pos[0], pos[1], pos[2] + 0.05 + difficulty*0.0125]
        # Hardest
        # pos = [pos[0], pos[1], pos[2] + 0.05 + difficulty*0.015]
        pos = [pos[0], pos[1], pos[2] + 0.05 + difficulty*0.014]
        size = [0.05+1*0.03, size[1], pos[2]]
      elif o == 'hard_high_jumps':
        # if difficulty == 10:
        #   pos = [pos[0], pos[1], pos[2] + 0.35]
        # else:
          # pos = [pos[0], pos[1], pos[2] + np.random.uniform(0.1 + (difficulty-1)*0.015, 0.1 + (difficulty)*0.015)]
          # pos = [pos[0], pos[1], pos[2] + 0.1 + (difficulty)*0.015]
          # pos = [pos[0], pos[1], pos[2] + (difficulty)*0.025]
        
        # if order[i+1] != 'hard_high_jumps':
        #   pos = [pos[0], pos[1], 0.01]
        #   size = [difficulty*0.025, size[1], pos[2]]
        # print(len(order), i)
        # if prev_o != 'hard_high_jumps' or len(order) > i + 2 and order[i+2] != 'hard_high_jumps':
        if prev_o != 'hard_high_jumps' or order[i+1] != 'hard_high_jumps':
        # if i in pre_artifact_box:
          # size = [initial_size[0], initial_size[1], height]
          pos = [pos[0], pos[1], 0.01]
          size = [0.03 + difficulty*0.022, size[1], pos[2]]
          
          # size = [initial_size[0], initial_size[1], height]
          # pos = [pos[0], pos[1], size[2] ]
          # pos = [pos[0], pos[1], pos[2] ]

          # size = [initial_size[0], initial_size[1], initial_size[2]]

        else:
          pos = [pos[0], pos[1], pos[2] + (difficulty)*0.02 + 0.5]
            
          # pos = [pos[0], pos[1], pos[2] + (difficulty)*0.05]
          # pos = [pos[0], pos[1], pos[2] + (difficulty)*0.04]
          # size = [0.03, initial_size[1], pos[2]]
          size = [0.2, initial_size[1], pos[2]]
      elif o == 'high_jumps':
        # if difficulty == 10:
        #   pos = [pos[0], pos[1], pos[2] + 0.35]
        # else:
          # pos = [pos[0], pos[1], pos[2] + np.random.uniform(0.1 + (difficulty-1)*0.015, 0.1 + (difficulty)*0.015)]
          # pos = [pos[0], pos[1], pos[2] + 0.1 + (difficulty)*0.015]
          # pos = [pos[0], pos[1], pos[2] + (difficulty)*0.025]
        if i in pre_artifact_box:
          # size = [initial_size[0], initial_size[1], height]
          # pos = [pos[0], pos[1], pos[2] + (difficulty)*0.025]
          pos = [pos[0], pos[1], pos[2] + (difficulty)*0.035]
          size = [initial_size[0], initial_size[1], height]
        # elif pol_order[i+1] != 'high_jumps':
        #   # pos = [pos[0], pos[1], pos[2] + (difficulty)*0.035]
        #   size = [0.45, initial_size[1], height]
        else:
          # pos = [pos[0], pos[1], pos[2] + (difficulty)*0.035]
          pos = [pos[0], pos[1], pos[2] + (difficulty)*0.025]
          # pos = [pos[0], pos[1], pos[2] + (difficulty)*0.01]
            
          # pos = [pos[0], pos[1], pos[2] + (difficulty)*0.05]
          # pos = [pos[0], pos[1], pos[2] + (difficulty)*0.04]
          # size = [0.03, initial_size[1], pos[2]]
          size = [0.15, initial_size[1], pos[2]]
      elif o == 'hard_steps':
        # step_width = 0.1 + (10 - difficulty)
        # if difficulty == 10:
        step_width = 0.1
        # else:
          # step_width = np.random.uniform(-0.022*(difficulty-1) + 0.322, -0.022*difficulty + 0.322)
          # step_width = -0.022*difficulty + 0.322
          # step_width = -0.022*10 + 0.322

        # step_width = -0.044*difficulty + 0.544
        # step_width = 0.3
        # print(step_width)
        # step_width = 0.12
        if prev_o != 'hard_steps':
        # if i in pre_artifact_box:
          # self.first_step = step_pos = np.random.choice([-1,1])*(0.15 + np.random.uniform(-10/200, 10/200))
          self.first_step = step_pos = np.random.choice([-1,1])*(0.15)
          little_bit = np.random.choice([-1,1])*(0.5)
          # self.first_step = step_pos = np.random.choice([-1,1])*(0.15 + np.random.uniform(-difficulty/200, difficulty/200))
          # self.first_step = step_pos = np.random.choice([-1,1])*(0.15)
          # step_pos = np.random.choice([-1,1])*(0.15 + np.random.uniform(-10/200, 10/200))
          # step_pos = np.random.choice([-1,1])*(0.1)

          # step_pos = np.random.choice([-1,1])*(0.15)
          # step_pos = np.random.choice([-1,1])*(0.22)
          
          # size = [initial_size[0], initial_size[1], height]
          # size = [np.random.uniform(0.18,0.22), initial_size[1], height]
          # height = prev_height
          # size = [initial_size[0], initial_size[1], height]
          # pos2 = copy.copy(pos)
        else:
          # step_pos = -1*(step_pos + little_bit)
          # step_pos = -1*(step_pos) 
          step_pos = -1*step_pos + np.random.uniform(-difficulty/200, difficulty/200)
          # step_pos = -1*step_pos + np.random.uniform(-difficulty/150, difficulty/150)
        pos[1] = step_pos
        height = prev_height 
        # height = prev_height + np.random.uniform(-0.005*difficulty, 0.005*difficulty)
        # height = prev_height + np.random.uniform(-0.005*10, 0.005*10)
        pos = [pos[0], pos[1], height]
        size = [initial_size[0], step_width, height]
          # if difficulty < 8:
          #   pos2 = [pos[0], -pos[1], height]
          #   size2 = [size[0]*((7-difficulty)/10), size[1], size[2]]
          #   pos2, prev_yaw = self.add_curved_box(pos2, prev_yaw=prev_yaw, prev_size=prev_size, size=size2, yaw=yaw, colour=colours[i], centre=True)
     
      elif o == 'steps':
        # step_width = 0.1 + (10 - difficulty)
        if difficulty == 10:
          step_width = 0.1
        else:
          # step_width = np.random.uniform(-0.022*(difficulty-1) + 0.322, -0.022*difficulty + 0.322)
          # step_width = -0.022*difficulty + 0.322
          step_width = -0.022*10 + 0.322

        # step_width = -0.044*difficulty + 0.544
        # step_width = 0.3
        # print(step_width)
        # step_width = 0.12
        if prev_o != 'steps':
        # if i in pre_artifact_box:
          # step_pos = np.random.choice([-1,1])*(0.15 + np.random.uniform(-difficulty/200, difficulty/200))
          # step_pos = np.random.choice([-1,1])*(0.15 + np.random.uniform(-10/200, 10/200))
          self.first_step = step_pos = np.random.choice([-1,1])*(0.1)
          # step_pos = np.random.choice([-1,1])*(0.15)
          # step_pos = np.random.choice([-1,1])*(0.22)
          # size = [initial_size[0], initial_size[1], height]
          # pos2 = copy.copy(pos)
        else:
          step_pos = -1*step_pos
        pos[1] = step_pos*(1+difficulty*0.2)
        # pos[1] = step_pos*(1+difficulty*0.19)
        # pos[1] = step_pos*(1)
        height = prev_height 
        pos = [pos[0], pos[1], height]
        size = [initial_size[0], step_width, height]

          # if difficulty < 8:
          #   pos2 = [pos[0], -pos[1], height]
          #   size2 = [size[0]*((7-difficulty)/10), size[1], size[2]]
          #   pos2, prev_yaw = self.add_curved_box(pos2, prev_yaw=prev_yaw, prev_size=prev_size, size=size2, yaw=yaw, colour=colours[i], centre=True)
      elif o == 'gaps':
        pos = [pos[0], pos[1], 0.01]
        # size = [difficulty*0.035, size[1], pos[2]]
        size = [difficulty*0.05, size[1], pos[2]]
        # size = [0.1 + difficulty*0.025, size[1], pos[2]]
        # if difficulty == 10:
          # size = [0.1 + difficulty*0.025, size[1], pos[2]]
        # else:
          # size = [0.1 + np.random.uniform((difficulty-1)*0.025, difficulty*0.025), size[1], pos[2]]
      elif o == 'one_leg_hop':
        # step_width = np.random.uniform(0.2, 0.4)
        # step_width = 0.2
        # step_width = -0.022*difficulty + 0.422
        step_width = -0.022*10 + 0.422

        # if i in pre_artifact_box:
        if prev_o != 'one_leg_hop':

          # self.first_step = step_pos = np.random.choice([-1,1])*(0.15 + np.random.uniform(-difficulty/200, difficulty/200))
          self.first_step = step_pos = np.random.choice([-1,1])*(0.15)
          # self.first_step = step_pos = 0.0
          # size = [initial_size[0], initial_size[1], height]
          # pos2 = copy.copy(pos)
        else:
          step_pos = -1*step_pos
        # step_pos = 0.0
        pos[1] = step_pos
        # height = prev_height 
        # height = prev_height + np.random.uniform(0.02*(difficulty-1), 0.02*difficulty)
        # height = prev_height + 0.015*difficulty
        height = prev_height + 0.02*difficulty
        pos = [pos[0], pos[1], height]
        # size = [initial_size[0], step_width, height]
        # size = [np.random.uniform(0.08,0.12), step_width, height]
        size = [0.18, step_width, height]
      elif o == 'hard_stairs':

        step_width = initial_size[1]
        step_pos = 0.0
        pos[1] = step_pos
        # height = prev_height + 0.02*difficulty
        # height = prev_height + 0.007*difficulty
        height = prev_height + 0.015*difficulty
        pos = [pos[0], pos[1], height]
        size = [initial_size[0], step_width, height]
        # size = [0.18, step_width, height]
      else:
        height = prev_height
        # pos[1] = 0
        if prev_o in ['high_jumps']:
          size =[0.45, initial_size[1], height]
        elif prev_o in ['hard_high_jumps']:
          size =[0.25, initial_size[1], height]
        elif prev_o in ['one_leg_hop']:
          height = prev_height + 0.015*difficulty
          size =[0.25, initial_size[1], height]
        else:
          size = [initial_size[0], initial_size[1], height]
        pos[2] = height
      
      prev_height = height
      # yaw = 0.0
      # print(i, len(colours))
      # print(yaw)
      # if o in ['steps', 'hard_steps', 'one_leg_hop'] or prev_o in ['steps', 'hard_steps', 'one_leg_hop']:      
      #   pos, prev_yaw = self.add_curved_box(pos, prev_yaw=prev_yaw, prev_size=prev_size, size=size, yaw=yaw, colour=colours[i], centre=True, prev_pos=prev_pos)
      #   # pos, prev_yaw = self.add_curved_box(pos, prev_yaw=prev_yaw, prev_size=prev_size, size=size, yaw=yaw, colour=colours[i], centre=False)
      # else:
      # pos, prev_yaw = self.add_curved_box(pos, prev_yaw=prev_yaw, prev_size=prev_size, size=size, yaw=yaw, colour=colours[i], centre=True)
      # print(size)

      pos, prev_yaw = self.add_curved_box(pos, prev_yaw=prev_yaw, prev_size=prev_size, size=size, yaw=yaw, colour=colours[i], centre=False, prev_pos=prev_pos)
      # pos, prev_yaw = self.add_curved_box(pos, prev_yaw=prev_yaw, prev_size=prev_size, size=size, yaw=yaw, colour=colours[i], centre=False)
      # self.add_box(pos=pos, orn=[0,0,yaw], size=list(size), colour=colours[i])
      prev_size = copy.copy(size)
      prev_pos = copy.copy(pos)
      prev_o = o
    
    # return pol_order, self.first_step
    return self.get_box_info()

  def add_curved_box(self, pos=[0,0,0], prev_yaw=0.0, prev_size=[1,0.25,0.5], size=[1,0.25,0.5], yaw=-0.25, colour=[0.8,0.3,0.3,1], centre=False, prev_pos=[0,0,0]):
   
    if (prev_size[1] > 0.5 and size[1] < 0.5) or size[1] < 0.5 or prev_size[1] < 0.5:      
      if prev_size[1] > 0.5 and size[1] < 0.5:      
        length, width = size[0]+prev_size[0], pos[1]
        self.prev_steps_pos = width
        self.step_fact = np.sign(pos[1])
      elif size[1] < 0.5:
        self.step_fact *= -1
        length, width = size[0]+prev_size[0], 2*pos[1]
      elif prev_size[1] < 0.5:
        length, width = size[0]+prev_size[0], -self.step_fact * abs(self.prev_steps_pos)
      diag = np.sqrt(length**2 + width**2)
      if yaw >= 0:
        phi = np.arctan2(width, length) 
      else:
        phi = np.arctan2(-width, length)
      yaw = yaw + prev_yaw
      x = diag*np.cos(yaw + phi)
      y = diag*np.sin(yaw + phi)
      pos = [prev_pos[0]+x, prev_pos[1] + y , pos[2]]
    else:
      length, width, _ = prev_size
      diag = np.sqrt(length**2 + width**2)
      if yaw >= 0:
        yaw = min(yaw, np.arctan2(length*2, width*2)) 
        psi = np.arctan2(-width, length)
      else:
        yaw = max(yaw, -np.arctan2(length*2, width*2)) 
        psi = np.arctan2(width, length) 
      cnr = [pos[0] + diag*np.cos(psi + prev_yaw), pos[1] + diag*np.sin(psi + prev_yaw), pos[2]]
      length, width, _ = size
      diag = np.sqrt(length**2 + width**2)
      if yaw >= 0:
        phi = np.arctan2(width, length) 
      else:
        phi = np.arctan2(-width, length)
      yaw = yaw + prev_yaw
      x = diag*np.cos(yaw + phi)
      y = diag*np.sin(yaw + phi)
      # print(cnr)
      # if centre:
      #   pos = [cnr[0] + x, pos[1], cnr[2]]
      # else:
      pos = [cnr[0] + x, cnr[1] + y, cnr[2]]
    # print(yaw, prev_yaw, np.arctan2(length*2, width*2))
    if self.args.easy_flat:
      yaw = 0
    self.add_box(pos=pos, orn=[0,0,yaw], size=list(size), colour=colour)
    return pos, yaw

  def add_circle(self, pos, size=[0.1,0.01], colour=[0,0,1,1]):
    visBoxId = p.createVisualShape(p.GEOM_CYLINDER, radius=size[0], length=size[1], rgbaColor=colour)
    circle_id = p.createMultiBody(baseMass=0, baseVisualShapeIndex=visBoxId, basePosition=pos)
    self.circle_id.append(circle_id)
    self.circle_sizes.append(size)
    self.circle_colours.append(colour)

  def add_box(self, pos, orn, size, colour=[0.8,0.3,0.3,1]):
    size = copy.copy(size)
    colBoxId = p.createCollisionShape(p.GEOM_BOX, halfExtents=size)
    visBoxId = p.createVisualShape(p.GEOM_BOX, halfExtents=size, rgbaColor=colour)
    q = p.getQuaternionFromEuler(orn)
    box_id = p.createMultiBody(baseMass=0, baseCollisionShapeIndex=colBoxId, baseVisualShapeIndex=visBoxId, basePosition=pos, baseOrientation=q)
    self.box_id.append(box_id)
    self.positions.append(pos+orn)
    self.sizes.append(size)
    self.colours.append(colour)
    # print(pos, size)

  def get_box_info(self):
    # print(self.sizes)
    return [self.box_id, self.positions, self.sizes, self.colours]

if __name__=="__main__":
  import argparse
  parser = argparse.ArgumentParser()
  # parser.add_argument('--render', default=False, action='store_true')
  parser.add_argument('--render', default=True, action='store_false')
  parser.add_argument('--use_env', default=False, action='store_true')
  parser.add_argument('--display_im', default=False, action='store_true')
  parser.add_argument('--show_detection', default=False, action='store_true')
  parser.add_argument('--single_pol', default=False, action='store_true')
  parser.add_argument('--easy_flat', default=False, action='store_true')
  args = parser.parse_args()
  np.random.seed(83)

  if args.use_env:
    from env import Env
    env = Env(render=args.render, display_im=args.display_im, obstacle_type='mix')
    # env = Env(render=False, display_im=True)
    # physicsClientId = p.connect(p.GUI)
    # obstacles = Obstacles()
    # obstacles.stairs(['down','up','down','up','down'])
    # obstacles.stairs(['up' for _ in range(10)])
    # obstacles.doughnut(size=0.5,width=0.5)
    # obstacles.path(path=[[1,1,0.5,1],[1.1,1,0.5,1],[1,1,0.5,1]])
    # obstacles.path(difficulty=4)
    # obstacles.adversarial_world()
    # obstacles.path(difficulty=10)
    # obstacles.stairs(['up','up','up','up','up','up','up','up','up','down','down','down','down','down','down'], height_coeff=0.07)

    env.reset()
    env.obstacles.remove_obstacles()
    # env.obstacles.test_world()
    env.obstacles.test_world()
    # env.obstacles.path(difficulty=1)
    env.world_map = env.get_world_map(env.obstacles.get_box_info())

    while True:
      env.step(np.random.random(env.ac_size))
      env.get_im()
  else:
    if args.render:
      physicsClientId = p.connect(p.GUI)
    else:
      physicsClientId = p.connect(p.DIRECT) #DIRECT is much faster, but GUI shows the robot
    obstacles = Obstacles()
    p.loadMJCF("./assets/ground.xml")
    print(args)
    # obstacles.add_straight_world(args=args,terrain_type='mix', difficulty=10)
    # obstacles.add_straight_world(args=args,terrain_type='flat')
    obstacles.add_straight_world(args=args,terrain_type='mix', obstacle_types=['gaps','steps'])
    # obstacles.add_straight_world(args=args,terrain_type='mix', obstacle_types=['flat','steps'])
    # obstacles.add_show1()
    # obstacles.add_curved_box()
    # obstacles.add_curves(difficulty=7)
    # obstacles.add_curvey_stairs(order=['flat']*3 + [np.random.choice(['up','down','flat'],p=[0.3,0.3,0.4]) for _ in range(30)], height_coeff=0.07, difficulty=7)
    # obstacles.add_curvey_stairs(order=['flat']*3 + [np.random.choice(['up','down'],p=[0.5,0.5]) for _ in range(40)], height_coeff=0.07, difficulty=1)
    # obstacles.add_domain_training_world()
    # obstacles.large_world()
    # obstacles.add_domain_training_world_no_stairs()
    while True:
      pass
