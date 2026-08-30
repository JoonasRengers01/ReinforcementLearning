import keras
import numpy as np
import tensorflow as tf
from Main import snakeGame
epsilon = 1e-6
model = keras.models.load_model('ModelArchive/'+'snake_model_no_walls.h5')
seeds = [25,42,100,146]
results = []
for j in seeds:
    np.random.seed(j)
    randomlist = []
    for i in range(50):
        randomlist.append((np.random.randint(2,17),np.random.randint(2,17)))

    for episode in range(25):
        game = snakeGame(randomlist)
        state = game.observe()
        state = np.array(state)
        while game.running:
            if epsilon >= np.random.rand(1)[0]:
                action = np.random.choice(3)
            else:
                state_tensor = keras.ops.convert_to_tensor(state, dtype=tf.float32)
                state_tensor = keras.ops.expand_dims(state,0)
                action_probability = model(state_tensor, training = False)
                action = tf.argmax(action_probability[0]).numpy()
            future_state,reward, running = game.step(action)
            future_state = np.array(future_state)
            state = future_state
            if game.snakeHead.Length >= 50:
                break
        print(f"Episode: {episode}, Seed: {j}, Length: {game.snakeHead.Length}")
        results.append((game.snakeHead.Length,episode))

print(f"Results: {results}")

print(f"Evaluation complete. Total games played: {len(results)} \n")

print(f"Max Length: {max([result[0] for result in results])} \n Min Length: {min([result[0] for result in results])} \n Average Length: {np.mean([result[0] for result in results])} \n standard deviation: {np.std([result[0] for result in results])}")