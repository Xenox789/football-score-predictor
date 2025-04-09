from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Input

def build_model(input_shape):
    model = Sequential([
        Input(shape=(input_shape,)),
        Dense(128, activation='relu'),
        Dropout(0.2),
        Dense(64, activation='relu'),
        Dropout(0.1),
        Dense(2, activation='linear')  # Output: [home_score, away_score]
    ])

    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])
    return model
