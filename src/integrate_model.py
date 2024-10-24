import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from src.data_collection import collect_game_data
from src.chess_game import ChessGame
import os

def preprocess_data(game_data):
    board_fen = game_data['board']
    current_turn = 1 if game_data['current_turn'] == 'white' else 0
    white_timer = game_data['white_timer']
    black_timer = game_data['black_timer']
    captured_pieces = len(game_data['captured_pieces'])
    move_history = len(game_data['move_history'])

    features = np.array([current_turn, white_timer, black_timer, captured_pieces, move_history])
    return features

def create_model(input_shape):
    model = Sequential([
        Dense(128, input_shape=(input_shape,), activation='relu'),
        Dropout(0.2),
        Dense(64, activation='relu'),
        Dropout(0.2),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer=Adam(), loss='binary_crossentropy', metrics=['accuracy'])
    return model

def train_model(game_data_list):
    X = np.array([preprocess_data(data) for data in game_data_list])
    y = np.array([1 if data['current_turn'] == 'white' else 0 for data in game_data_list])

    model = create_model(X.shape[1])

    model.fit(X, y, epochs=10, batch_size=32, validation_split=0.2)

    project_dir = os.path.abspath(os.path.dirname(__file__))
    models_dir = os.path.join(project_dir, 'models')
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)

    model_path = os.path.join(models_dir, 'chess_model.h5')
    model.save(model_path)

    return model

if __name__ == '__main__':
    game = ChessGame()
    game_data_list = [collect_game_data(game) for _ in range(100)]
    model = train_model(game_data_list)
