import torch
import numpy as np
import random
import pygame
from collections import deque

#from snake import Snake
#from  game import Game

from constants     import *
from ai.model      import Linear_QNet, QTrainer
from ai.helper     import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self,game):
        self.game  = game
        self.snake = game.snake
        self.frame_iteration = 0

        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma   = 0.9 # discount rate
        self.memory  = deque(maxlen=MAX_MEMORY) # popleft()
        file_name    = f"model{self.game.get_variation_code()}.pth"
        self.model   = Linear_QNet(11, 256, 3,file_name)
        self.model.load()
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma) 
        self.frame_iteration = 0

    def get_state(self):
        state = self.snake.get_state()
        return np.array(state)  

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        #for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def move(self,action):
        #[straight,right,left]
        #print('action:',action)
        cmd = -1
        if np.array_equal(action,[0,1,0]):
            cmd = CMD_T_RIGHT

        elif np.array_equal(action,[0,0,1]):
           cmd = CMD_T_LEFT

        if cmd >= 0:
            self.game.commands.append(cmd)

        return self.game.step()

    def reset(self):
         self.frame_iteration = 0
         self.game.start()
 
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        #for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done) 

    def play_step(self, action):
        self.frame_iteration += 1
        reward = 0
        ret  = self.move(action) # update the head
        done = False
        score =  self.snake.get_size()
        if not is_ok(ret) or self.frame_iteration >= 1000:
            reward = -10
            done = True
        elif ret == FOOD_VAL:
            score += self.snake.grow_by_food_size
            reward += 10
        self.draw()
        return reward, done, score
    
    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games
        final_move = [0,0,0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move  
    
    def draw(self):
        self.game.window.fill(BK)
        self.game.draw_play(self.game.window)
        pygame.display.update()

class Q_AI_PLayer :
    def __init__(self,game):
        self.game = game
        self.snake = self.game.snake
        self.agent = None
        #self.agent = Agent(self.game)
    
    def init(self):
        if self.agent == None:
            self.agent = Agent(self.game)

    def move(self):

        state  = self.agent.get_state()
        action = self.agent.get_action(state)
        #[straight,right,left]
        if np.array_equal(action,[0,1,0]):
            (self.snake.x_velocity,self.snake.y_velocity) = self.game.snake.turn_right()

        elif np.array_equal(action,[0,0,1]):
            (self.snake.x_velocity,self.snake.y_velocity)= self.game.snake.turn_left()

    def train(self):
        plot_scores = []
        plot_mean_scores = []
        total_score = 0
        record = 0
        agent = self.agent
        agent.reset()
        while True:
            # get old state
            state_old = agent.get_state()


            # get move
            final_move = agent.get_action(state_old)

            # perform move and get new state
            reward, done, score = agent.play_step(final_move)
            state_new = agent.get_state()

            # train short memory
            agent.train_short_memory(state_old, final_move, reward, state_new, done)

            # remember
            agent.remember(state_old, final_move, reward, state_new, done)

            if done:
                # train long memory, plot result
                agent.reset()
                agent.n_games += 1
                agent.train_long_memory()

                if score > record:
                    record = score
                    agent.model.save()            
                    print('Game', agent.n_games, 'Score', score, 'Record:', record, ' New record !')
                else:
                    print('Game', agent.n_games, 'Score', score, 'Record:', record)

                plot_scores.append(score)
                total_score += score
                mean_score = total_score / agent.n_games
                plot_mean_scores.append(mean_score)
                plot(plot_scores, plot_mean_scores)   
                if agent.n_games >= 10000:
                    break 
                    
        agent.modal.load()                 
         