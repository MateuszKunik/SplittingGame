import numpy as np
from gym import Env
from gym.spaces import MultiDiscrete, Box

from utils import *

class SplittingGame(Env):
    def __init__(self, d, k, joker, score, max_steps):
        super(SplittingGame, self).__init__()
        self.d = d
        self.k = k
        self.joker = joker
        self.score = score
        self.max_steps = max_steps
        
        # Initialize trivial code V = [[***], [], [], ...]
        self.code = generate_trivial_code(self.joker, self.d, self.score)
        # Initialize number of steps
        self.current_step = 0

        # Action space: item, index
        self.action_space = MultiDiscrete([self.score, self.d])
        # Observation space: binary items
        self.observation_space = Box(low=0, high=1, shape=(self.score, self.d))
        

    def decode(self):
        decoded = []
        char_mapping = {1: '0', 2: '1', self.joker: '*'}

        for item in self.code:
            if item[0] != 0:
                decoded.append(''.join(list(map(char_mapping.get, item))))

        return decoded

    def step(self, action):
        self.current_step += 1
        reward = -1
        done = False

        # Main splitting game code
        v0 = self.code[action[0]]
        # Check if chosen item is non-trivial
        if len(v0) == self.d:
            index = action[1]
            
            # Create new strings v1, v2 if chosen index is joker '*'
            if v0[index] == self.joker:
                v1, v2 = replace_joker(v0, index)

                # Check if the new items satisfy the requirements
                if all((k_neighborly(item, v1, self.k)) and (k_neighborly(item, v2, self.k)) for item in self.code):
                    # Remove chosen item and one trivial string
                    self.code = remove_string(self.code, v0)
                    self.code = remove_string(self.code, np.zeros(self.d, dtype=int))
                    # Add new strings to code V
                    self.code = np.vstack([self.code, v1])
                    self.code = np.vstack([self.code, v2])

                    # Charge the reward
                    reward = 1

                    # Render code progress
                    # self.render()
                

        # Check the number of steps and number of non-trivial elements
        if (self.current_step >= self.max_steps) or (sum(1 for item in self.code if item[0] != 0) == self.score):
            done = True
        
        # Placeholder for info
        info = {}

        return self.code, reward, done, info


    def render(self):
        # Implement visualization
        # to_render = self.decode()
        # print(to_render)
        pass


    def reset(self):
        # Reset code -> trivial code
        self.code = generate_trivial_code(self.joker, self.d, self.score)
        # Reset number of steps
        self.current_step = 0

        return self.code