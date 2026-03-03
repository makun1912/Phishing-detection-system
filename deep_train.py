import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

data = pd.read_csv("../dataset/phishing.csv")

tokenizer = Tokenizer(num_words=5000)
tokenizer.fit_on_texts(data['url'])

X = tokenizer.texts_to_sequences(data['url'])
X = pad_sequences(X, maxlen=50)

y = np.array(data['label'])

model = Sequential()
model.add(Embedding(5000, 64))
model.add(LSTM(64))
model.add(Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(X, y, epochs=5, batch_size=32)

model.save("../model/lstm_model.h5")

print("Deep Learning Model Saved!")
