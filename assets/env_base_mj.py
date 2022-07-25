from .env_base import EnvBase

class EnvBaseMJ(EnvBase):

    def restore_env_state(self, params):
        if params:
            for key in params:
                self.__dict__[key] = params[key]
        self.set_position(self.state) 

    def get_env_state(self):
        self.state = self.sim.get_state()

    def set_position(self, state):
        # self.sim.set_state_from_flattened(state)
        self.sim.set_state(state)        
        # self.sim.step()
        # sim_state = self.sim.get_state()
        # sim_state = self.sim.set_state()
