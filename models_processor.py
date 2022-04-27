import io
import base64
import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

SEQ_LEN = 100
URL_DICT = {
    'ADA': 'https://query1.finance.yahoo.com/v7/finance/download/ADA-USD?period1=1516665600&period2=1650672000&interval=1d&events=history&includeAdjustedClose=true',
    'BTC': 'https://query1.finance.yahoo.com/v7/finance/download/BTC-USD?period1=1410912000&period2=1650585600&interval=1d&events=history&includeAdjustedClose=true',
    'LINK': 'https://query1.finance.yahoo.com/v7/finance/download/LINK-USD?period1=1517184000&period2=1650672000&interval=1d&events=history&includeAdjustedClose=true',
    'ETH': 'https://query1.finance.yahoo.com/v7/finance/download/ETH-USD?period1=1445472000&period2=1650585600&interval=1d&events=history&includeAdjustedClose=true',
    'MATIC': 'https://query1.finance.yahoo.com/v7/finance/download/MATIC-USD?period1=1548720000&period2=1650672000&interval=1d&events=history&includeAdjustedClose=true',
    'SOL': 'https://query1.finance.yahoo.com/v7/finance/download/SOL-USD?period1=1548720000&period2=1650672000&interval=1d&events=history&includeAdjustedClose=true'
}


class ModelProcessor:
    def __init__(self, name, model_path):
        self.name = name
        self.model_path = model_path
        self.scaler = MinMaxScaler()

    def get_test(self):
        csv_path = URL_DICT[self.name]
        df = pd.read_csv(csv_path, parse_dates=['Date'])
        df = df.sort_values('Date')

        close_price = df.Close.values.reshape(-1, 1)
        scaled_close = self.scaler.fit_transform(close_price)

        scaled_close = scaled_close[~np.isnan(scaled_close)]
        scaled_close = scaled_close.reshape(-1, 1)

        X_train, y_train, X_test, y_test = preprocess(scaled_close, SEQ_LEN, train_split=0.95)

        return X_test, y_test

    def get_pred(self):
        X_test, y_test = self.get_test()
        model = keras.models.load_model(f'models/{self.model_path}.hdf5')

        y_pred = model.predict(X_test)
        y_pred_transformed = self.scaler.inverse_transform(y_pred)
        y_test_transformed = self.scaler.inverse_transform(y_test)

        return y_pred_transformed, y_test_transformed

    def build_plot(self):
        img = io.BytesIO()

        y_pred_transformed, y_test_transformed = self.get_pred()
        plt.figure(figsize=(12, 8))
        plt.plot(y_test_transformed, color='green', label='Real')
        plt.plot(y_pred_transformed, color='red', label='Prediction')
        plt.title(f'{self.name} Price Prediction')
        plt.legend()
        plt.savefig(img, format='png')
        img.seek(0)

        plot_url = base64.b64encode(img.getvalue()).decode()

        return plot_url


def to_sequences(data, seq_len):
    d = []

    for index in range(len(data) - seq_len):
        d.append(data[index: index + seq_len])

    return np.array(d)


def preprocess( data_raw, seq_len, train_split):
    data = to_sequences(data_raw, seq_len)

    num_train = int(train_split * data.shape[0])

    X_train = data[:num_train, :-1, :]
    y_train = data[:num_train, -1, :]

    X_test = data[num_train:, :-1, :]
    y_test = data[num_train:, -1, :]

    return X_train, y_train, X_test, y_test



