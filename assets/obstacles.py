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

    def add_straight_world(self, difficulty=10, height_coeff=0.07, terrain_type="mix", base=False, base_before=False, initial_pos=[0,0,0], baseline=False, num_artifacts=1, rand_flat=False, args=None, obstacle_types=None, dqn=False):
        self.args = args
        height_coeff = (0.085/10)*difficulty 
        if terrain_type == "flat":
            initial_size = [np.random.uniform(0.18,0.22), np.random.uniform(0.55,0.85) - difficulty*0.01, 0.5]
        else:
            initial_size = [np.random.uniform(0.18,0.22), np.random.uniform(0.55,0.85), 0.5]
        size = copy.copy(initial_size)
        pos = [-initial_size[0]-0.5+initial_pos[0],0+initial_pos[1],initial_size[2]+initial_pos[2]]
        prev_size = copy.copy(initial_size)
        prev_yaw = 0
        if terrain_type == "mix":
            # Make sure not same terrain type twice in a row
            rand_order = []
            if obstacle_types == None:
                obstacle_types = ["flat","jumps","gaps","stairs","steps","high_jumps"]
            all_options = obstacle_types
            rand_order.append(np.random.choice(all_options))
            while len(rand_order) < 7:
                choice = np.random.choice(all_options)
                while choice == rand_order[-1]:
                    choice = np.random.choice(all_options)
                rand_order.append(choice)
        # elif terrain_type == "dqn":
        #     rand_order = [np.random.choice(["jumps","gaps","stairs"]) for _ in range(15)]
        # elif terrain_type == "multi":
        #     rand_order = ["jumps","gaps","stairs"]
        elif terrain_type == "zero":
            rand_order = []
        else:
            if baseline:
                rand_order = [terrain_type for _ in range(7)]
            else:
                rand_order = [terrain_type for _ in range(num_artifacts)]
        # if not args.train_multi and terrain_type in ["high_jumps", "hard_high_jumps", "one_leg_hop"]:
        # print(rand_order, num_artifacts)
        if self.args.run_state in ["train_single", "run_single"]:
            order = []
            pol_order = []
            yaws = []
        else:
            order = ["flat","flat","flat","flat","flat"]
            pol_order = ["flat","flat","flat","flat","flat"]
            yaws = [0.0, 0.0, 0.0, 0.0, 0.0]
        pre_artifact_box = []
        if base:
            order = ["flat"]*(3*2 + 7*7)
            pol_order = ["flat"]*(3*2 + 7*7)
        else:
            prev_yaw = 0.0
            yaw = 0.0
            curve = np.random.choice([-1,1])
            for r in rand_order:
                if r == "stairs":
                    up_down = np.random.choice(["up", "down"])
                if r == "high_jumps":
                    artifact_size = 2
                elif r in ["hard_high_jumps"]:
                    artifact_size = 4
                elif r in ["flat","hop"]:
                    artifact_size = np.random.randint(7,9)
                elif r in ["hard_steps"]:
                    artifact_size = np.random.randint(8,10)
                elif r in ["steps", "hard_steps", "one_leg_hop","stairs", "hard_stairs","up_stairs","down_stairs"]:
                    artifact_size = np.random.randint(6,8)
                # elif r in ["stairs", "hard_stairs"]:
                #     artifact_size = np.random.randint(4,6)
                else:
                    # artifact_size = np.random.randint(2,4)
                    artifact_size = 2
                placement = 1
                pre_artifact_box.append(len(order)) 
                if r == "flat": 
                    curve = -1*curve
                for i in range(artifact_size):
                    if r in ["flat","hop"]:
                        order.append("flat")
                        if i == 0:
                            yaw = 0
                        else:
                            yaw = curve*0.03*difficulty
                        if args.easy_flat:
                            yaws.append(0)
                        else:
                            yaws.append(yaw)
                    elif r in ["hard_high_jumps"] and i > 0:
                        order.append("hard_high_jumps")
                    elif r in ["jumps", "gaps", "high_jumps", "steps", "stairs", "hard_high_jumps", "hard_stairs", "hard_steps", "one_leg_hop","up_stairs","down_stairs"]:
                        if (i == placement) or (r in ["steps", "stairs", "hard_steps", "hard_stairs", "one_leg_hop","up_stairs","down_stairs"] and i > 0):
                            # if r in ["stairs"]:
                            #     order.append(np.random.choice(["up", "down"]))
                            # else:
                            order.append(r)
                        else:
                            order.append("flat")
                    # else:
                    #     if terrain_type == "mix":
                    #         if i >= placement:
                    #             order.append(np.random.choice(["up", "down"]))
                    #         else:
                    #             order.append("flat")
                    #     else:
                    #         if i >= placement and i != artifact_size - 1:
                    #             if args.stair_thing:
                    #                 up_down = np.random.choice(["up", "down"])
                    #                 order.extend([up_down, up_down])
                    #             else:
                    #                 order.append(np.random.choice(["up", "down"]))
                    #                 order.append(np.random.choice(["up", "down"]))
                    #             pol_order.append(r)
                    #             yaws.append(0.0)
                    #         else:
                    #             order.append("flat")
                    pol_order.append(r)
                    if not r in ["flat"] or args.easy_flat:
                        yaws.append(0.0)
                    prev_yaw = yaw
                # pol_order.append("flat")
                # order.append("flat")
                # yaws.append(0.0)
                # if self.args.run_state in ["train_single"]:
                #     order.extend(["flat"])
                #     pol_order.extend(["zero"])
                #     yaws.extend([0.0])
                # else:
                if not self.args.run_state in ["train_single","run_single"]:
                    order.extend(["flat"]*15)
                    pol_order.extend(["flat"]*14 + ["zero"])
                    yaws.extend([0.0]*15)
            

            if self.args.run_state in ["train_single","run_single"]:
                order.extend(["flat","flat"])
                pol_order.extend(["flat","zero"])
                yaws.extend([0.0,0.0])

        colours = []
        
        for i,pol in enumerate(order):
            if args.show_detection and i in pre_artifact_box:
                colours.append([0.7,0.8,0.7,1])
            elif pol in ["stairs","up","down", "hard_stairs","up_stairs","down_stairs"]:
                colours.append([0.8,0.5,0.8,1])
            elif pol == "jumps":
                colours.append([0.8,0.3,0.3,1])
            elif pol == "high_jumps":
                colours.append([0.8,0.4,0.3,1])
            elif pol == "hard_high_jumps":
                colours.append([0.7,0.3,0.2,1])
            elif pol == "steps":
                colours.append([0.6,0.4,0.7,1])
            elif pol == "hard_steps":
                colours.append([0.5,0.3,0.6,1])
            elif pol == "gaps":
                colours.append([0.3,0.8,0.3,1])
            elif pol == "zero":
                colours.append([0.8,0.5,0.3,1])
            elif pol in ["flat","hop"]:
                colours.append([0.3,0.3,0.8,1])
            elif pol in ["one_leg_hop"]:
                colours.append([0.2,0.6,0.2,1])
            else:
                print("obstacle_not _found")

        count = 0
        lowest = 0
        for name in order:
            if name in ["down_stairs","down"]: count += 1
            if name in ["up_stairs","up"]: count -= 1
            if count > lowest:
                    lowest = count
        prev_height = (lowest + 2)*height_coeff + 0.4
        pos[2] = prev_height
        size[2] = prev_height
        prev_size = copy.copy(size)
        prev_pos = copy.copy(pos)
        yaw_count = 0
        prev_o = "flat"
        self.first_step = 0
        prev_yaw = 0
        last_artifact_box = 0
        for i,(o, yaw) in enumerate(zip(order, yaws)): 
            if o == terrain_type:
                # print(o, i)
                last_artifact_box = i       
            if pol_order[i] == "zero":
                initial_size = [0.8, initial_size[1], 0.5]
            elif i in pre_artifact_box:
                initial_size = [args.detection_dist/2, initial_size[1], 0.5]
            else:
                initial_size = [np.random.uniform(0.18,0.22), initial_size[1], 0.5]
            if o == "stairs":
                up_down = np.random.choice(["up", "down"])
                if up_down == "down":
                    height = prev_height - height_coeff
                    pos[2] = height
                    size = [initial_size[0], initial_size[1], height]
                elif up_down == "up":
                    height = prev_height + height_coeff
                    pos[2] = height
                    size = [initial_size[0], initial_size[1], height]
            elif o == "up_stairs":
                height = prev_height + height_coeff
                pos[2] = height
                size = [initial_size[0], initial_size[1], height]
            elif o == "down_stairs":
                height = prev_height - height_coeff
                pos[2] = height
                size = [initial_size[0], initial_size[1], height]
            elif o == "jumps":
                pos = [pos[0], pos[1], pos[2] + 0.05 + difficulty*0.014]
                size = [0.05+1*0.03, size[1], pos[2]]
            elif o == "hard_high_jumps":    
                if prev_o != "hard_high_jumps" or order[i+1] != "hard_high_jumps":
                    pos = [pos[0], pos[1], 0.01]
                    size = [0.03 + difficulty*0.022, size[1], pos[2]]
                else:
                    pos = [pos[0], pos[1], pos[2] + (difficulty)*0.02 + 0.5]
                    size = [0.2, initial_size[1], pos[2]]
            elif o == "high_jumps":
                if i in pre_artifact_box:
                    # pos = [pos[0], pos[1], pos[2] + (difficulty)*0.035]
                    pos = [pos[0], pos[1], pos[2] + (difficulty)*self.args.jump_height/20]
                    size = [initial_size[0], initial_size[1], height]
                else:
                    # pos = [pos[0], pos[1], pos[2] + (difficulty)*0.025]            
                    pos = [pos[0], pos[1], pos[2] + (difficulty)*self.args.jump_height/20]
                    # pos = [pos[0], pos[1], pos[2] + (difficulty)*0.03]            
                    # pos = [pos[0], pos[1], pos[2] + (difficulty)*0.035]            
                    size = [0.15, initial_size[1], pos[2]]
            elif o == "hard_steps":
                step_width = 0.1
                if prev_o != "hard_steps":
                    self.first_step = step_pos = np.random.choice([-1,1])*(0.15)
                    little_bit = np.random.choice([-1,1])*(0.5)
                else:
                    step_pos = -1*step_pos + np.random.uniform(-difficulty/200, difficulty/200)
                pos[1] = step_pos
                height = prev_height 
                pos = [pos[0], pos[1], height]
                size = [initial_size[0], step_width, height]
            elif o == "steps":
                if difficulty == 10:
                    step_width = 0.1
                else:
                    step_width = -0.022*10 + 0.322
                if prev_o != "steps":
                    self.first_step = step_pos = np.random.choice([-1,1])*(0.1)
                else:
                    step_pos = -1*step_pos
                pos[1] = step_pos*(1+difficulty*0.2)
                height = prev_height 
                pos = [pos[0], pos[1], height]
                size = [initial_size[0], step_width, height]
            elif o == "gaps":
                pos = [pos[0], pos[1], 0.01]
                size = [difficulty*0.05, size[1], pos[2]]
            elif o == "one_leg_hop":
                step_width = -0.022*10 + 0.422
                if prev_o != "one_leg_hop":
                    self.first_step = step_pos = np.random.choice([-1,1])*(0.15)
                else:
                    step_pos = -1*step_pos
                pos[1] = step_pos
                height = prev_height + 0.02*difficulty
                pos = [pos[0], pos[1], height]
                size = [0.18, step_width, height]
            elif o == "hard_stairs":
                step_width = initial_size[1]
                step_pos = 0.0
                pos[1] = step_pos
                height = prev_height + 0.015*difficulty
                pos = [pos[0], pos[1], height]
                size = [initial_size[0], step_width, height]
            else:
                height = prev_height
                if prev_o in ["high_jumps"]:
                    size =[0.45, initial_size[1], height]
                elif prev_o in ["hard_high_jumps"]:
                    size =[0.25, initial_size[1], height]
                elif prev_o in ["one_leg_hop"]:
                    height = prev_height + 0.015*difficulty
                    size =[0.25, initial_size[1], height]
                else:
                    size = [initial_size[0], initial_size[1], height]
                pos[2] = height
            prev_height = height
            pos, prev_yaw = self.add_curved_box(pos, prev_yaw=prev_yaw, prev_size=prev_size, size=size, yaw=yaw, colour=colours[i], centre=False, prev_pos=prev_pos)
            prev_size = copy.copy(size)
            prev_pos = copy.copy(pos)
            prev_o = o
        
        return pol_order, self.first_step, last_artifact_box

    def add_curved_box(self, pos=[0,0,0], prev_yaw=0.0, prev_size=[1,0.25,0.5], size=[1,0.25,0.5], yaw=-0.25, colour=[0.8,0.3,0.3,1], centre=False, prev_pos=[0,0,0]):
        if (prev_size[1] > 0.35 and size[1] < 0.35) or size[1] < 0.35 or prev_size[1] < 0.35:      
            if prev_size[1] > 0.35 and size[1] < 0.35:      
                length, width = size[0]+prev_size[0], pos[1]
                self.prev_steps_pos = width
                self.step_fact = np.sign(pos[1])
            elif size[1] < 0.35:
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
            pos = [cnr[0] + x, cnr[1] + y, cnr[2]]
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
    # parser.add_argument("--render", default=False, action="store_true")
    parser.add_argument("--render", default=True, action="store_false")
    parser.add_argument("--use_env", default=False, action="store_true")
    parser.add_argument("--display_im", default=False, action="store_true")
    parser.add_argument("--show_detection", default=False, action="store_true")
    parser.add_argument("--train_multi", default=False, action="store_true")
    parser.add_argument("--easy_flat", default=False, action="store_true")
    args = parser.parse_args()
    np.random.seed(83)

    if args.use_env:
        from assets.env_base import Env
        env = Env(render=args.render, display_im=args.display_im, obstacle_type="mix")
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
        obstacles.add_straight_world(args=args,terrain_type="mix", obstacle_types=["gaps","steps"])
        while True:
            pass
