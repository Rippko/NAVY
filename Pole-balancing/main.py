import numpy as np
import gym
import matplotlib.pyplot as plt
from collections import deque
import random
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import multiprocessing
import time
import imageio
from PIL import Image

# Detekce zařízení (GPU/CPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Hyperparametry
EPISODES = 500
GAMMA = 0.99
EPSILON_START = 1.0
EPSILON_END = 0.01
EPSILON_DECAY = 0.995
MEMORY_SIZE = 10000
BATCH_SIZE = 64
LEARNING_RATE = 0.001

class QNetwork(nn.Module):
    def __init__(self, state_size, action_size):
        super(QNetwork, self).__init__()
        self.fc1 = nn.Linear(state_size, 24)
        self.fc2 = nn.Linear(24, 24)
        self.fc3 = nn.Linear(24, action_size)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return self.fc3(x)

class ReplayBuffer:
    def __init__(self, capacity):
        self.memory = deque(maxlen=capacity)

    def add(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.epsilon = EPSILON_START
        self.qnetwork = QNetwork(state_size, action_size).to(device)
        self.optimizer = optim.Adam(self.qnetwork.parameters(), lr=LEARNING_RATE)
        self.memory = ReplayBuffer(MEMORY_SIZE)

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        state = torch.FloatTensor(state).unsqueeze(0).to(device)
        self.qnetwork.eval()
        with torch.no_grad():
            action_values = self.qnetwork(state)
        self.qnetwork.train()
        return torch.argmax(action_values).item()

    def remember(self, state, action, reward, next_state, done):
        self.memory.add(state, action, reward, next_state, done)

    def learn(self):
        if len(self.memory) < BATCH_SIZE:
            return

        experiences = self.memory.sample(BATCH_SIZE)
        states, actions, rewards, next_states, dones = zip(*experiences)

        states = torch.FloatTensor(np.array(states)).to(device)
        actions = torch.LongTensor(actions).unsqueeze(1).to(device)
        rewards = torch.FloatTensor(rewards).unsqueeze(1).to(device)
        next_states = torch.FloatTensor(np.array(next_states)).to(device)
        dones = torch.FloatTensor(dones).unsqueeze(1).to(device)

        Q_expected = self.qnetwork(states).gather(1, actions)
        Q_next = self.qnetwork(next_states).detach().max(1)[0].unsqueeze(1)
        Q_targets = rewards + GAMMA * Q_next * (1 - dones)

        loss = F.mse_loss(Q_expected, Q_targets)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        self.epsilon = max(EPSILON_END, self.epsilon * EPSILON_DECAY)

def train_dqn():
    env = gym.make('CartPole-v1')
    state_size = env.observation_space.shape[0]
    action_size = env.action_space.n

    agent = DQNAgent(state_size, action_size)
    scores = []

    for episode in range(EPISODES):
        state, _ = env.reset()
        score = 0
        done = False

        while not done:
            action = agent.act(state)
            next_state, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated

            agent.remember(state, action, reward, next_state, done)
            agent.learn()

            state = next_state
            score += reward

        scores.append(score)
        print(f"Epizoda {episode+1}/{EPISODES} | Skóre: {score:.0f} | Epsilon: {agent.epsilon:.2f}")

        if len(scores) >= 100 and np.mean(scores[-100:]) >= 295.0:
            print(f"Problém vyřešen v epizodě {episode+1}!")
            break

    env.close()
    return agent, scores

def visualize_solution_loop(agent):
    env = gym.make('CartPole-v1', render_mode='human')
    try:
        while True:
            state, _ = env.reset()
            done = False
            total_reward = 0

            while not done:
                action = agent.act(state)
                state, reward, terminated, truncated, _ = env.step(action)
                done = terminated or truncated
                total_reward += reward

            print(f"Vizualizace - skóre: {total_reward}")
            time.sleep(1)
    finally:
        env.close()

def plot_results(scores):
    plt.figure(figsize=(10, 6))
    plt.plot(scores)
    plt.title('Vývoj skóre během tréninku')
    plt.xlabel('Epizoda')
    plt.ylabel('Skóre')
    plt.grid(True)
    plt.savefig('screens/training_results.png')
    plt.show()
    
def record_gif(agent, filename='cartpole_solution.gif', num_episodes=1, fps=30):
    env = gym.make('CartPole-v1', render_mode='rgb_array')
    frames = []
    
    for episode in range(num_episodes):
        state, _ = env.reset()
        done = False
        
        while not done:
            action = agent.act(state)
            next_state, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated
            
            frame = env.render()
            frames.append(Image.fromarray(frame))
            
            state = next_state
    
    env.close()
    
    print(f"Ukládám GIF s {len(frames)} snímky do souboru {filename}...")
    imageio.mimsave(filename, frames, fps=fps)
    print(f"GIF úspěšně uložen do {filename}")

if __name__ == "__main__":
    multiprocessing.set_start_method('spawn')
    agent, scores = train_dqn()
    
    record_gif(agent, filename='screens/cartpole_solution.gif', num_episodes=3)

    vis_process = multiprocessing.Process(target=visualize_solution_loop, args=(agent,))
    vis_process.start()

    plot_results(scores)
    vis_process.terminate()
    vis_process.join()
