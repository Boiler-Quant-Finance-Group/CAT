import numpy as np
import pandas
import pandas as pd
import matplotlib.pyplot as plt
from xgboost import XGBRegressor, plot_importance
from ast import literal_eval
from sklearn.metrics import mean_squared_error


def forecast(data: pandas.DataFrame, column: str, key: str):
    df = data.copy()

    # Extract relevant key in each cell
    for col in df.columns:
        df[col] = df[col].apply(lambda x: x[key])

    # Remove all columns which have None in the dataset
    df.dropna(axis=1, inplace=True)

    # Split data into features and target variable
    X = df.drop(columns=[column])
    y = df[column]

    # Split data into training and testing sets
    train_size = int(0.8 * len(df))
    X_train, X_test = X[:train_size - 1], X[train_size:len(X)-1]
    y_train, y_test = y[1:train_size], y[train_size+1:]

    # Initialize and train XGBoost model
    model = XGBRegressor(eta=0.3)
    model.fit(X_train, y_train)
    plt.axes(plot_importance(model, max_num_features=5))
    plt.show()

    # Make predictions
    predictions = model.predict(X_test)

    # Evaluate the model
    mse = mean_squared_error(y_test, predictions)
    print('Mean Squared Error:', mse)

    # Visualize actual vs predicted values
    plt.plot(y_test.values, label='Actual')
    plt.plot(predictions, label='Predicted')
    plt.legend()
    plt.show()

    plt.plot(df.index, df[column])
    plt.show()


if __name__ == '__main__':
    # Import the time series data
    df = pd.read_csv('timeseries/processed/bequant_processed_time_series_order_book.csv')

    # Format the time series column
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s')

    # Set timestamp as the index
    df.set_index('Timestamp', inplace=True)

    # Convert all JSON strings to dictionaries
    for col in df.columns:
        df[col] = df[col].apply(literal_eval)

    # Change the column name and key here
    forecast(df, 'ETH/TUSD', 'mean_ask_price')
