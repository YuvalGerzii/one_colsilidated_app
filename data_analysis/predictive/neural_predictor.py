"""
Neural Network Predictive Modeling Module
==========================================

Deep learning models for prediction including MLP, LSTM,
GRU, and Transformer architectures.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Union
import warnings

warnings.filterwarnings('ignore')


class NeuralPredictor:
    """
    Neural network-based predictor with multiple architectures.
    """

    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.history = {}
        self.metrics = {}

    def train_mlp(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: np.ndarray = None,
        y_val: np.ndarray = None,
        hidden_layers: List[int] = [64, 32],
        activation: str = 'relu',
        dropout: float = 0.2,
        epochs: int = 100,
        batch_size: int = 32,
        learning_rate: float = 0.001
    ) -> Dict:
        """
        Train Multi-Layer Perceptron.

        Args:
            X_train: Training features
            y_train: Training target
            X_val: Validation features
            y_val: Validation target
            hidden_layers: Units per hidden layer
            activation: Activation function
            dropout: Dropout rate
            epochs: Training epochs
            batch_size: Batch size
            learning_rate: Learning rate

        Returns:
            Training results
        """
        try:
            import tensorflow as tf
            from tensorflow.keras.models import Sequential
            from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
            from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
            from tensorflow.keras.optimizers import Adam
            from sklearn.preprocessing import StandardScaler
        except ImportError:
            return {"error": "tensorflow not installed"}

        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        if X_val is not None:
            X_val_scaled = scaler.transform(X_val)
        self.scalers['mlp'] = scaler

        # Build model
        model = Sequential()
        model.add(Dense(hidden_layers[0], activation=activation, input_shape=(X_train.shape[1],)))
        model.add(BatchNormalization())
        model.add(Dropout(dropout))

        for units in hidden_layers[1:]:
            model.add(Dense(units, activation=activation))
            model.add(BatchNormalization())
            model.add(Dropout(dropout))

        model.add(Dense(1))

        model.compile(optimizer=Adam(learning_rate=learning_rate), loss='mse', metrics=['mae'])

        # Callbacks
        callbacks = [
            EarlyStopping(monitor='val_loss', patience=15, restore_best_weights=True),
            ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5)
        ]

        # Train
        validation_data = (X_val_scaled, y_val) if X_val is not None else None
        history = model.fit(
            X_train_scaled, y_train,
            validation_data=validation_data,
            epochs=epochs,
            batch_size=batch_size,
            callbacks=callbacks,
            verbose=0
        )

        self.models['mlp'] = model
        self.history['mlp'] = history.history

        return {
            'model': 'MLP',
            'architecture': hidden_layers,
            'total_params': model.count_params(),
            'final_loss': round(history.history['loss'][-1], 6),
            'final_val_loss': round(history.history['val_loss'][-1], 6) if validation_data else None,
            'epochs_trained': len(history.history['loss'])
        }

    def train_lstm_regressor(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: np.ndarray = None,
        y_val: np.ndarray = None,
        lstm_units: List[int] = [64, 32],
        dropout: float = 0.2,
        epochs: int = 100,
        batch_size: int = 32
    ) -> Dict:
        """
        Train LSTM for regression.

        Args:
            X_train: Training sequences (samples, timesteps, features)
            y_train: Training target
            X_val: Validation sequences
            y_val: Validation target
            lstm_units: Units per LSTM layer
            dropout: Dropout rate
            epochs: Training epochs
            batch_size: Batch size

        Returns:
            Training results
        """
        try:
            import tensorflow as tf
            from tensorflow.keras.models import Sequential
            from tensorflow.keras.layers import LSTM, Dense, Dropout
            from tensorflow.keras.callbacks import EarlyStopping
        except ImportError:
            return {"error": "tensorflow not installed"}

        # Ensure 3D input
        if X_train.ndim == 2:
            X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
        if X_val is not None and X_val.ndim == 2:
            X_val = X_val.reshape((X_val.shape[0], X_val.shape[1], 1))

        # Build model
        model = Sequential()

        for i, units in enumerate(lstm_units):
            return_seq = i < len(lstm_units) - 1
            if i == 0:
                model.add(LSTM(units, return_sequences=return_seq,
                              input_shape=(X_train.shape[1], X_train.shape[2])))
            else:
                model.add(LSTM(units, return_sequences=return_seq))
            model.add(Dropout(dropout))

        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mse')

        # Callbacks
        callbacks = [EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)]

        # Train
        validation_data = (X_val, y_val) if X_val is not None else None
        history = model.fit(
            X_train, y_train,
            validation_data=validation_data,
            epochs=epochs,
            batch_size=batch_size,
            callbacks=callbacks,
            verbose=0
        )

        self.models['lstm'] = model
        self.history['lstm'] = history.history

        return {
            'model': 'LSTM',
            'architecture': lstm_units,
            'input_shape': X_train.shape[1:],
            'total_params': model.count_params(),
            'final_loss': round(history.history['loss'][-1], 6),
            'epochs_trained': len(history.history['loss'])
        }

    def train_gru_regressor(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: np.ndarray = None,
        y_val: np.ndarray = None,
        gru_units: List[int] = [64, 32],
        dropout: float = 0.2,
        epochs: int = 100,
        batch_size: int = 32
    ) -> Dict:
        """
        Train GRU for regression.

        Args:
            X_train: Training sequences
            y_train: Training target
            X_val: Validation sequences
            y_val: Validation target
            gru_units: Units per GRU layer
            dropout: Dropout rate
            epochs: Training epochs
            batch_size: Batch size

        Returns:
            Training results
        """
        try:
            import tensorflow as tf
            from tensorflow.keras.models import Sequential
            from tensorflow.keras.layers import GRU, Dense, Dropout
            from tensorflow.keras.callbacks import EarlyStopping
        except ImportError:
            return {"error": "tensorflow not installed"}

        # Ensure 3D input
        if X_train.ndim == 2:
            X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
        if X_val is not None and X_val.ndim == 2:
            X_val = X_val.reshape((X_val.shape[0], X_val.shape[1], 1))

        # Build model
        model = Sequential()

        for i, units in enumerate(gru_units):
            return_seq = i < len(gru_units) - 1
            if i == 0:
                model.add(GRU(units, return_sequences=return_seq,
                             input_shape=(X_train.shape[1], X_train.shape[2])))
            else:
                model.add(GRU(units, return_sequences=return_seq))
            model.add(Dropout(dropout))

        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mse')

        # Train
        validation_data = (X_val, y_val) if X_val is not None else None
        callbacks = [EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)]

        history = model.fit(
            X_train, y_train,
            validation_data=validation_data,
            epochs=epochs,
            batch_size=batch_size,
            callbacks=callbacks,
            verbose=0
        )

        self.models['gru'] = model
        self.history['gru'] = history.history

        return {
            'model': 'GRU',
            'architecture': gru_units,
            'total_params': model.count_params(),
            'final_loss': round(history.history['loss'][-1], 6),
            'epochs_trained': len(history.history['loss'])
        }

    def train_cnn_regressor(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: np.ndarray = None,
        y_val: np.ndarray = None,
        filters: List[int] = [32, 64],
        kernel_size: int = 3,
        epochs: int = 100,
        batch_size: int = 32
    ) -> Dict:
        """
        Train 1D CNN for regression.

        Args:
            X_train: Training sequences
            y_train: Training target
            X_val: Validation sequences
            y_val: Validation target
            filters: Filters per conv layer
            kernel_size: Convolution kernel size
            epochs: Training epochs
            batch_size: Batch size

        Returns:
            Training results
        """
        try:
            import tensorflow as tf
            from tensorflow.keras.models import Sequential
            from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, Dropout
            from tensorflow.keras.callbacks import EarlyStopping
        except ImportError:
            return {"error": "tensorflow not installed"}

        # Ensure 3D input
        if X_train.ndim == 2:
            X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
        if X_val is not None and X_val.ndim == 2:
            X_val = X_val.reshape((X_val.shape[0], X_val.shape[1], 1))

        # Build model
        model = Sequential()

        for i, f in enumerate(filters):
            if i == 0:
                model.add(Conv1D(f, kernel_size, activation='relu',
                                input_shape=(X_train.shape[1], X_train.shape[2])))
            else:
                model.add(Conv1D(f, kernel_size, activation='relu'))
            model.add(MaxPooling1D(2))

        model.add(Flatten())
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.2))
        model.add(Dense(1))

        model.compile(optimizer='adam', loss='mse')

        # Train
        validation_data = (X_val, y_val) if X_val is not None else None
        callbacks = [EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)]

        history = model.fit(
            X_train, y_train,
            validation_data=validation_data,
            epochs=epochs,
            batch_size=batch_size,
            callbacks=callbacks,
            verbose=0
        )

        self.models['cnn'] = model
        self.history['cnn'] = history.history

        return {
            'model': 'CNN',
            'filters': filters,
            'kernel_size': kernel_size,
            'total_params': model.count_params(),
            'final_loss': round(history.history['loss'][-1], 6),
            'epochs_trained': len(history.history['loss'])
        }

    def train_transformer(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: np.ndarray = None,
        y_val: np.ndarray = None,
        d_model: int = 64,
        num_heads: int = 4,
        num_layers: int = 2,
        epochs: int = 100,
        batch_size: int = 32
    ) -> Dict:
        """
        Train Transformer for time series.

        Args:
            X_train: Training sequences
            y_train: Training target
            X_val: Validation sequences
            y_val: Validation target
            d_model: Model dimension
            num_heads: Number of attention heads
            num_layers: Number of transformer layers
            epochs: Training epochs
            batch_size: Batch size

        Returns:
            Training results
        """
        try:
            import tensorflow as tf
            from tensorflow.keras.models import Model
            from tensorflow.keras.layers import (
                Input, Dense, Dropout, LayerNormalization,
                MultiHeadAttention, GlobalAveragePooling1D
            )
            from tensorflow.keras.callbacks import EarlyStopping
        except ImportError:
            return {"error": "tensorflow not installed"}

        # Ensure 3D input
        if X_train.ndim == 2:
            X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
        if X_val is not None and X_val.ndim == 2:
            X_val = X_val.reshape((X_val.shape[0], X_val.shape[1], 1))

        # Build Transformer model
        inputs = Input(shape=(X_train.shape[1], X_train.shape[2]))

        # Project input
        x = Dense(d_model)(inputs)

        # Transformer blocks
        for _ in range(num_layers):
            # Multi-head attention
            attn_output = MultiHeadAttention(
                num_heads=num_heads,
                key_dim=d_model // num_heads
            )(x, x)
            attn_output = Dropout(0.1)(attn_output)
            x = LayerNormalization()(x + attn_output)

            # Feed-forward
            ff_output = Dense(d_model * 4, activation='relu')(x)
            ff_output = Dense(d_model)(ff_output)
            ff_output = Dropout(0.1)(ff_output)
            x = LayerNormalization()(x + ff_output)

        # Output
        x = GlobalAveragePooling1D()(x)
        x = Dense(32, activation='relu')(x)
        outputs = Dense(1)(x)

        model = Model(inputs, outputs)
        model.compile(optimizer='adam', loss='mse')

        # Train
        validation_data = (X_val, y_val) if X_val is not None else None
        callbacks = [EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)]

        history = model.fit(
            X_train, y_train,
            validation_data=validation_data,
            epochs=epochs,
            batch_size=batch_size,
            callbacks=callbacks,
            verbose=0
        )

        self.models['transformer'] = model
        self.history['transformer'] = history.history

        return {
            'model': 'Transformer',
            'd_model': d_model,
            'num_heads': num_heads,
            'num_layers': num_layers,
            'total_params': model.count_params(),
            'final_loss': round(history.history['loss'][-1], 6),
            'epochs_trained': len(history.history['loss'])
        }

    def predict(
        self,
        model_name: str,
        X: np.ndarray
    ) -> np.ndarray:
        """
        Make predictions.

        Args:
            model_name: Name of model
            X: Input data

        Returns:
            Predictions
        """
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not trained")

        model = self.models[model_name]

        # Scale if necessary
        if model_name == 'mlp' and model_name in self.scalers:
            X = self.scalers[model_name].transform(X)

        # Ensure 3D for sequential models
        if model_name in ['lstm', 'gru', 'cnn', 'transformer'] and X.ndim == 2:
            X = X.reshape((X.shape[0], X.shape[1], 1))

        return model.predict(X, verbose=0).flatten()

    def evaluate(
        self,
        model_name: str,
        X_test: np.ndarray,
        y_test: np.ndarray
    ) -> Dict[str, float]:
        """
        Evaluate model.

        Args:
            model_name: Name of model
            X_test: Test features
            y_test: Test target

        Returns:
            Dictionary of metrics
        """
        y_pred = self.predict(model_name, X_test)

        mae = np.mean(np.abs(y_test - y_pred))
        mse = np.mean((y_test - y_pred) ** 2)
        rmse = np.sqrt(mse)

        # R2
        ss_res = np.sum((y_test - y_pred) ** 2)
        ss_tot = np.sum((y_test - np.mean(y_test)) ** 2)
        r2 = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0

        metrics = {
            'MAE': round(mae, 4),
            'MSE': round(mse, 4),
            'RMSE': round(rmse, 4),
            'R2': round(r2, 4)
        }

        self.metrics[model_name] = metrics
        return metrics

    def get_training_history(
        self,
        model_name: str
    ) -> Dict:
        """
        Get training history.

        Args:
            model_name: Name of model

        Returns:
            Training history
        """
        return self.history.get(model_name, {})

    def save_model(
        self,
        model_name: str,
        path: str
    ) -> None:
        """
        Save model to disk.

        Args:
            model_name: Name of model
            path: Save path
        """
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not found")

        self.models[model_name].save(path)

    def load_model(
        self,
        model_name: str,
        path: str
    ) -> None:
        """
        Load model from disk.

        Args:
            model_name: Name for loaded model
            path: Model path
        """
        try:
            import tensorflow as tf
            self.models[model_name] = tf.keras.models.load_model(path)
        except ImportError:
            raise ImportError("tensorflow not installed")

    def compare_models(
        self,
        X_test: np.ndarray,
        y_test: np.ndarray
    ) -> pd.DataFrame:
        """
        Compare all trained models.

        Args:
            X_test: Test features
            y_test: Test target

        Returns:
            Comparison DataFrame
        """
        results = []

        for model_name in self.models.keys():
            metrics = self.evaluate(model_name, X_test, y_test)
            metrics['Model'] = model_name
            results.append(metrics)

        return pd.DataFrame(results).sort_values('RMSE')
