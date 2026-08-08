import keras

gamma = 0.99  # Past reward discount
epsilon = 1.0  # Epsilon greedy parameter
epsilon_min = 0.1  
epsilon_max = 1.0  
epsilon_diff = (epsilon_max - epsilon_min)  # Difference between max and min, scaling factor for epsilon as training goes

max_steps_per_episode = 10000

optimizer = keras.optimizers.Adam(learning_rate=0.001)

action_log = []
state_log = []
reward_log = []
episode_reward_log = []
frame_count_log = []
running_reward = 0
episode_count = 0
frame_count = 0

#Number of frames of gauranteed random actions
epsilon_random_frames = 10000.0
#Number of frames for exploration
epsilon_greedy = 1000000.0
#maximum length of log
max_history = 1000000

#Number of actions between training
actions_before_update = 4

#Number of actions before updating target network
update_target_network = 10000

lossfunction = keras.losses.huber()