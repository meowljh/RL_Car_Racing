import gymnasium as gym
import sys
import numpy as np
import random
import math
import matplotlib.pyplot as plt


class Agent:
    def __init__(self):
        self.env = gym.make('carRace:carRace/NamCTrack-v0')
        self.observe_space_max = self.env.observation_space.high
        self.observe_space_shape = self.env.observation_space.shape
        self.num_buckets = tuple((self.observe_space_max + np.ones(self.observe_space_shape)).astype(np.uint))
        self.num_actions = self.env.action_space.n
        self.state_bounds = list(zip(self.env.observation_space.low, self.observe_space_max))
        
        self.min_explore_rate = 0.001
        self.min_learning_rate = 0.2
        self.decay_factor = np.prod(self.num_buckets, dtype=float) / 10.0
        
        self.num_episodes = 99999999
        self.max_T = 2000
        
        self.q_table = np.zeros(self.num_buckets + (self.num_actions, ), dtype=float)
        
    def select_action(self, state, explore_rate):
        if random.random() < explore_rate:
            action = self.env.action_space.sample()
        else:
            action = int(np.argmax(self.q_table[state]))
        return action
    
    def get_learning_rate(self, episode):
        return max(self.min_learning_rate, min(0.8, 1.0 - math.log10((episode + 1) / self.decay_factor)))

    def get_explore_rate(self, episode):
        return max(self.min_explore_rate, min(0.8, 1.0 - math.log10((episode + 1) / self.decay_factor)))
    
    def state_to_bucket(self, state):
        # state is continuous, while the state should be discrete to save
        # there are methods of reinforcement learning for continous state spaces, but in this implementation, we will change by binning 
        bucket_indice = []
        for i in range(len(state)):
            if state[i] <= self.state_bounds[i][0]:
                bucket_index = 0
            elif state[i] >= self.state_bounds[i][1]:
                bucket_index = self.num_buckets[i] - 1
            else:
                bound_width = self.state_bounds[i][1] - self.state_bounds[i][0]
                offset = (self.num_buckets[i] - 1) * self.state_bounds[i][0] / bound_width
                scaling = (self.num_buckets[i]-1) / bound_width
                bucket_index = int(round(scaling * state[i] - offset))
            bucket_indice.append(bucket_index)
            
        return tuple(bucket_indice)
          
        
    def simulate(self):
        learning_rate = self.get_learning_rate(0)
        explore_rate =  self.get_explore_rate(0)
        discount_factor = 0.99
        total_reward = 0
        total_rewards = []
        training_done = False
        threshold = 1000

        for episode in range(self.num_episodes):
            total_rewards.append(total_reward)
            if episode == 50000:
                plt.plot(total_rewards)
                plt.ylabel("rewards")
                plt.show()
                self.env.save_memory("50000")
                break
            obs = self.env.reset()
            print("RESET!! ", obs)
            state_init = self.state_to_bucket(obs)
            total_reward = 0
            
            if episode >= threshold:
                explore_rate = 0.01
             
            for t in range(self.max_T):
                action = self.select_action(state_init, explore_rate)
                print("action ", action)
                obs, reward, done, _, _ = self.env.step(action)
                state = self.state_to_bucket(obs)
                self.env.remember(state_init, action, reward, state, done)
                total_reward += reward
                print("state ", state)
                print("observed ", obs)
                # update Q table #
                best_q = np.amax(self.q_table[state]) # new state #
                print("best Q ", best_q)
                self.q_table[state_init + (action,)] += learning_rate * (reward + (best_q) * discount_factor - self.q_table[state_init + (action,)])
                
                # setup state for next iteration #
                state_init = state
                self.env.render()
                if done or t >= self.max_T - 1:
                    print(f"Episode {episode} finished after {t} time steps with total reward {total_reward}")
                    break
            
            learning_rate = self.get_learning_rate(episode)
            explore_rate = self.get_explore_rate(episode)


if __name__ == "__main__":
    agent = Agent()
    agent.simulate()