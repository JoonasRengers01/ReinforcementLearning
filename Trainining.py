import keras
from Main import snakeGame
import numpy as np
from Model import generate_snake_model
import tensorflow as tf

gamma = 0.95  # Past reward discount
epsilon = 1.0  # Epsilon greedy parameter
epsilon_min = 0.1  
epsilon_max = epsilon  
epsilon_diff = (epsilon_max - epsilon_min)  # Difference between max and min, scaling factor for epsilon as training goes
sample_size = 512
max_steps_per_episode = 10000
max_episodes = 10000

optimizer = keras.optimizers.Adam(learning_rate=0.001)

action_log = []
state_log = []
future_state_log = []
reward_log = []
episode_reward_log = []
frame_count_log = []
running_log = []
length_log = []
running_reward = 0
episode_count = 0
frame_count = 0

num_actions = 3

#Number of frames of gauranteed random actions
epsilon_random_frames = 10000.0
#Number of frames for exploration
epsilon_greedy = 100000.0
#maximum length of log
max_history = 2000000

#Number of actions between training
actions_before_update = 4

#Number of actions before updating target network
update_target_network = 10000

lossfunction = keras.losses.Huber()
model = generate_snake_model()
model_target = generate_snake_model()

while True:
    #Initialize the game and get the initial state
    game = snakeGame()
    state = game.observe()
    state = np.array(state)

    episode_reward = 0

    for frame in range(1,max_steps_per_episode):
        frame_count += 1

        if frame_count <= epsilon_random_frames or epsilon >= np.random.rand(1)[0]:
            np.random.seed(np.random.randint(0,100000))
            #Take a random action
            action = np.random.choice(num_actions)
            # print(f"Framecount: {frame_count}, Random action taken: {action}")
        else:
            #Use the model to predict the next action
            state_tensor = keras.ops.convert_to_tensor(state, dtype=tf.float32)
            state_tensor = keras.ops.expand_dims(state,0)
            action_probability = model(state_tensor, training = False)
            action = tf.argmax(action_probability[0]).numpy()
            # print(f"Framecount: {frame_count}, Action taken from model: {action}")
            

        #Update the epsilon value to reduce the number of random actions taken as training progresses
        epsilon -= epsilon_diff/epsilon_greedy
        epsilon = max(epsilon, epsilon_min)

        #Update the game state and get the reward
        if game.running:
            future_state,reward, running = game.step(action)
            future_state = np.array(future_state)
        else:
            break
        # print(f"Frame: {frame_count}, Reward: {reward}")
        #award action reward to the agent
        episode_reward +=  reward

        #update the logs
        action_log.append(action)
        state_log.append(state)
        future_state_log.append(future_state)
        reward_log.append(reward)
        running_log.append(int(running))
        state = future_state

        if frame_count % actions_before_update == 0 and len(reward_log) > sample_size:

            #Get a random sample of the logs to train the model
            indices = np.random.choice(range(len(reward_log)), size = sample_size)


            state_sample = np.array([state_log[i] for i in indices])
            future_state_sample = np.array([future_state_log[i] for i in indices])
            action_sample = np.array([action_log[i] for i in indices])
            reward_sample = np.array([reward_log[i] for i in indices])
            running_sample = np.array([running_log[i] for i in indices])

            #Calculate the discounted rewards
            future_rewards = model_target.predict(future_state_sample)
            
            updated_q_values = reward_sample + gamma * keras.ops.amax(future_rewards, axis=1)

            updated_q_values = updated_q_values * (1 - running_sample) - running_sample


            masks = keras.ops.one_hot(action_sample, num_actions)

            with tf.GradientTape() as tape:
                q_values = model(state_sample)

                q_action = keras.ops.sum(keras.ops.multiply(q_values, masks), axis=1)
                loss = lossfunction(updated_q_values, q_action)

                grads = tape.gradient(loss, model.trainable_variables)
                optimizer.apply_gradients(zip(grads, model.trainable_variables))

        if frame_count % update_target_network == 0:
            model_target.set_weights(model.get_weights())

        if frame_count % 400 == 0:
            print(f"Episode: {episode_count}, average snake Length: {np.mean(length_log)}, running reward: {running_reward},  episode reward: {episode_reward}, epsilon: {epsilon}, frame count: {frame_count}")

        #limit the size of the logs to prevent memory issues
        if len(reward_log) > max_history:
            del reward_log[:1]
            del state_log[:1]
            del action_log[:1]
            del future_state_log[:1]
            del running_log[:1]
        if not game.running:
            break

    episode_reward_log.append(episode_reward)
    frame_count_log.append(frame_count)
    if len(episode_reward_log) > 50:
        del episode_reward_log[:1]
    running_reward = np.mean(episode_reward_log)

    episode_count += 1

    if episode_count >= max_episodes:
        break
    length_log.append(game.snakeHead.Length)
    if len(length_log) > 50:
        del length_log[:1]
    print(f"Episode: {episode_count}, average snake Length: {np.mean(length_log)}, snake Length: {game.snakeHead.Length}, running reward: {running_reward},  episode reward: {episode_reward}, epsilon: {epsilon}, frame count: {frame_count}")

