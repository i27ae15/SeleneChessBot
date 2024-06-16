import tensorflow as tf
import numpy as np


from core.printing import __print__ as pprint


def set_seed(seed: int = None):
    if seed is None:
        seed = np.random.randint(1, 10**6)
    tf.random.set_seed(seed)


def create_chess_cnn(input_shape: tuple = (8, 8, 12), seed: int = None):

    set_seed(seed)

    input_layer = tf.keras.layers.Input(shape=input_shape)

    # First convolutional layer
    x = tf.keras.layers.Conv2D(32, (3, 3), padding='same', activation='relu')(input_layer)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.MaxPooling2D((2, 2))(x)

    # Second convolutional layer
    x = tf.keras.layers.Conv2D(64, (3, 3), padding='same', activation='relu')(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.MaxPooling2D((2, 2))(x)

    # Third convolutional layer
    x = tf.keras.layers.Conv2D(128, (3, 3), padding='same', activation='relu')(x)
    x = tf.keras.layers.BatchNormalization()(x)

    # Flatten the output
    x = tf.keras.layers.Flatten()(x)

    # Fully connected layers
    x = tf.keras.layers.Dense(256, activation='relu')(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Dropout(0.5)(x)

    # Policy head
    policy_head = tf.keras.layers.Dense(64, activation='softmax', name='policy_head')(x)  # Adjust the output shape if necessary

    # Value head
    value_head = tf.keras.layers.Dense(1, activation='tanh', name='value_head')(x)

    # Creating the model
    model = tf.keras.models.Model(inputs=input_layer, outputs=[policy_head, value_head])

    # Compile the models
    model.compile(
        optimizer='adam',
        loss={'policy_head': 'categorical_crossentropy', 'value_head': 'mean_squared_error'},
        metrics={'policy_head': 'accuracy', 'value_head': 'mse'}
    )
    # Create the model
    model.summary()
    pprint('Model created successfully!')

    return model
