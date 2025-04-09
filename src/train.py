from data_preparation import load_data, preprocess
from model import build_model
from sklearn.model_selection import train_test_split
import tensorflow as tf

# Load and preprocess
df = load_data()
X, y, le_team, le_tour = preprocess(df)

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Convert to float32 tensors
X_train = X_train.values.astype('float32')
X_test = X_test.values.astype('float32')
y_train = y_train.values.astype('float32')
y_test = y_test.values.astype('float32')

# Build model
model = build_model(input_shape=X.shape[1])

# Train
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=50, batch_size=64)

# Save model
model.save("model/score_predictor.keras")

# Evaluate
loss, mae = model.evaluate(X_test, y_test)
print(f"Test Loss: {loss:.2f}, MAE: {mae:.2f}")
