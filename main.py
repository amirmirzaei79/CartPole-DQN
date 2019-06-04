import gym
import time
import tensorflow as tf
import keras
import numpy as np

env = gym.make('CartPole-v1')

# regression neural network to predict action rewards for each state - in this case each state has 2 actions
model = keras.models.Sequential()
model.add(keras.layers.Dense(32, activation='sigmoid', input_dim=env.observation_space.shape[0]))
model.add(keras.layers.Dense(32, activation='sigmoid'))
model.add(keras.layers.Dense(env.action_space.n, activation='linear'))
model.compile(loss='mean_squared_error', optimizer=keras.optimizers.Adam(0.001), metrics=['mae']) # 0.001 is learning rate of Adam

# deep Q learning init
gamma = 0.9
epsilon = 1.0
epsilonMin = 0.01
epsilonDecay = 0.95
episodeLimit = 5000

# deep Q
for episode in range(episodeLimit):
    currentStateArray = env.reset()
    currentState = np.array([currentStateArray])
    done = False
    while not done:
        # env.render()

        if np.random.rand() <= epsilon:
            action = np.random.randint(0, 1)
        else:
            action = np.argmax(model.predict(currentState))

        newStateArray, reward, done, info = env.step(action)
        newState = np.array([newStateArray])
        target = reward + gamma * np.max(model.predict(newState))
        targetLabel = model.predict(currentState)[0]
        targetLabel[action] = target
        model.fit(currentState, targetLabel.reshape(1, 2), epochs=1, verbose=0)
        currentState = newState
    else:
        print(episode)

    if epsilon > epsilonMin:
        epsilon *= epsilonDecay

model.save_weights("weights.h5")

# Play game
print("\nPlaying Game...")
time.sleep(1)

s = env.reset()
done = False
while not done:
    env.render()
    a = np.argmax(model.predict(np.array([s])))
    newS, r, done, _ = env.step(a)
    s = newS
    time.sleep(0.01)
# env.reset()
# env.render()
# observations, reward, done, info = env.step(env.action_space.sample())
# env.render()
#
# print(observations, '\n', Reward, done, '\n', info)
#
# time.sleep(1)