            Initialising_action_linear_velocity = 0.15
            Initialising_action_angular_velocity = 0.7*np.clip(self.heading_error_gapwp1, -1, 1)
            
            for robot_bbox in self.robots_bbox:
            #print("k",robot_bbox,"whole",self.robots_bbox)
                # if str(robot_bbox[0])==str(self):
                #     #print(str(robot_bbox[0]),str(self))
                #     self.robot1_near_robot2=False
                if str(robot_bbox[0]) != str(self):
                    self.robot1_near_robot2=False
                    self.intersection_hline_rbbox,_= self.intersection_check(self.head_line_MA,robot_bbox[1])
                    self.intersection_s1line_rbbox,_= self.intersection_check(self.side_line1g_MA,robot_bbox[1])
                    self.intersection_s2line_rbbox,_= self.intersection_check(self.side_line2g_MA,robot_bbox[1])
                    self.int_check_lines_vs_rbbox=[self.intersection_hline_rbbox,self.intersection_s1line_rbbox,self.intersection_s2line_rbbox]
                    #print(self.int_check_lines_vs_rbbox,self)
                    #print(num,robot_bbox[0]);exit()
                    # print("checking",self.turn_both)

                    if any(self.int_check_lines_vs_rbbox):
                        self.robot1_near_robot2=True
                        # print("self.robot1_near_robot2",self.robot1_near_robot2,self)
                        action_linear_velocity = 0
                        action_angular_velocity = 0
                        if self.turn_both and self==self.All_Robot_ID[0]:
                            action_linear_velocity = -1
                            action_angular_velocity = 0.5
                        elif self.turn_both and self==self.All_Robot_ID[1]:
                            action_linear_velocity = -0.5
                            action_angular_velocity = -0.5


                
                # if self==self.All_Robot_ID[1]:    
                #     print(self.robot1_near_robot2,self)
                        #break

            # if self.intersection_r1_r:
            #     print("TRRRRRRUUEEE")
            #     action_linear_velocity = 0
            #     action_angular_velocity = 0

        
            if self.gapwp1_reach:
                action_linear_velocity = 0.15
                action_angular_velocity = 0.7*np.clip(self.heading_error_gapwp2, -1, 1)
                for robot_bbox in self.robots_bbox:
            #print("k",robot_bbox,"whole",self.robots_bbox)
                # if str(robot_bbox[0])==str(self):
                #     #print(str(robot_bbox[0]),str(self))
                #     self.robot1_near_robot2=False
                    if str(robot_bbox[0]) != str(self):
                        self.robot1_near_robot2=False
                        self.intersection_hline_rbbox,_= self.intersection_check(self.head_line_MA,robot_bbox[1])
                        self.intersection_s1line_rbbox,_= self.intersection_check(self.side_line1g_MA,robot_bbox[1])
                        self.intersection_s2line_rbbox,_= self.intersection_check(self.side_line2g_MA,robot_bbox[1])
                        self.int_check_lines_vs_rbbox=[self.intersection_hline_rbbox,self.intersection_s1line_rbbox,self.intersection_s2line_rbbox]
                        #print(self.int_check_lines_vs_rbbox,self)
                        #print(num,robot_bbox[0]);exit()
                        # print("checking",self.turn_both)

                        if any(self.int_check_lines_vs_rbbox):
                            self.robot1_near_robot2=True
                            # print("self.robot1_near_robot2",self.robot1_near_robot2,self)
                            action_linear_velocity = 0
                            action_angular_velocity = 0
                            if self.turn_both and self==self.All_Robot_ID[0]:
                                action_linear_velocity = -1
                                action_angular_velocity = 0.5
                            elif self.turn_both and self==self.All_Robot_ID[1]:
                                action_linear_velocity = -0.5
                                action_angular_velocity = -0.5
                

            
                if self.gapwp2_reach:
                    action_linear_velocity = 0.15
                    action_angular_velocity = 0.7*np.clip(self.heading_error, -1, 1)
                    for robot_bbox in self.robots_bbox:
            #print("k",robot_bbox,"whole",self.robots_bbox)
                # if str(robot_bbox[0])==str(self):
                #     #print(str(robot_bbox[0]),str(self))
                #     self.robot1_near_robot2=False
                        if str(robot_bbox[0]) != str(self):
                            self.robot1_near_robot2=False
                            self.intersection_hline_rbbox,_= self.intersection_check(self.head_line_MA,robot_bbox[1])
                            self.intersection_s1line_rbbox,_= self.intersection_check(self.side_line1g_MA,robot_bbox[1])
                            self.intersection_s2line_rbbox,_= self.intersection_check(self.side_line2g_MA,robot_bbox[1])
                            self.int_check_lines_vs_rbbox=[self.intersection_hline_rbbox,self.intersection_s1line_rbbox,self.intersection_s2line_rbbox]
                            #print(self.int_check_lines_vs_rbbox,self)
                            #print(num,robot_bbox[0]);exit()
                            # print("checking",self.turn_both)

                            if any(self.int_check_lines_vs_rbbox):
                                self.robot1_near_robot2=True
                                # print("self.robot1_near_robot2",self.robot1_near_robot2,self)
                                action_linear_velocity = 0
                                action_angular_velocity = 0
                                if self.turn_both and self==self.All_Robot_ID[0]:
                                    action_linear_velocity = -1
                                    action_angular_velocity = 0.5
                                elif self.turn_both and self==self.All_Robot_ID[1]:
                                    action_linear_velocity = -0.5
                                    action_angular_velocity = -0.5
            #print(self.exp_actions,self)