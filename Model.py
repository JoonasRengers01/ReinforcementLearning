import keras
from keras import layers
import tensorflow as tf
Num_of_actions = 3

def generate_snake_model():

    model = keras.Sequential()

    model.add(keras.Input((6,)))
    model.add(layers.Dense(8, activation= 'linear'))
    model.add(layers.Dense(16, activation= 'linear'))
    model.add(layers.Dense(8, activation= 'linear'))
    model.add(layers.Dense(Num_of_actions, activation= 'linear'))

    model.summary()

    return model