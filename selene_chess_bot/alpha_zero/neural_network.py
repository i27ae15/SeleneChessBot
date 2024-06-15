from tensorflow.keras import layers, models

from core.printing import __print__ as pprint


def create_chess_cnn(input_shape=(8, 8, 12)):

    input_layer = layers.Input(shape=input_shape)

    x = layers.Conv2D(32, (3, 3), padding='same', activation='relu')(input_layer)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling2D((2, 2))(x)

    x = layers.Conv2D(64, (3, 3), padding='same', activation='relu')(x)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling2D((2, 2))(x)

    x = layers.Conv2D(128, (3, 3), padding='same', activation='relu')(x)
    x = layers.BatchNormalization()(x)

    x = layers.Flatten()(x)
    x = layers.Dense(256, activation='relu')(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.5)(x)

    # Policy head
    policy_head = layers.Dense(64, activation='softmax', name='policy_head')(x)  # Adjust the output shape if necessary

    # Value head
    value_head = layers.Dense(1, activation='tanh', name='value_head')(x)

    model = models.Model(inputs=input_layer, outputs=[policy_head, value_head])
    model.compile(
        optimizer='adam',
        loss={'policy_head': 'categorical_crossentropy', 'value_head': 'mean_squared_error'},
        metrics={'policy_head': 'accuracy', 'value_head': 'mse'}
    )
    # Create the model
    model.summary()
    pprint('Model created successfully!')

    return model
