import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import os
import streamlit as st

MODEL_PATH = os.path.join("models", "gru_model.h5")
TOKENIZER_PATH = os.path.join("data", "tokenizer.pickle")


@st.cache_resource(show_spinner="Loading GRU model...")
def load_model_and_tokenizer():

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

    if not os.path.exists(TOKENIZER_PATH):
        raise FileNotFoundError(f"Tokenizer not found: {TOKENIZER_PATH}")

    model = tf.keras.models.load_model(MODEL_PATH)

    with open(TOKENIZER_PATH, "rb") as handle:
        tokenizer = pickle.load(handle)

    max_sequence_len = model.input_shape[1]

    index_word = {index: word for word, index in tokenizer.word_index.items()}

    return model, tokenizer, max_sequence_len, index_word


def gpt_sample(probs, temperature=1.0):

    probs = np.asarray(probs).astype("float64")

    if temperature <= 0:
        temperature = 1.0

    probs = np.log(probs + 1e-9) / temperature
    probs = np.exp(probs)
    probs /= np.sum(probs)

    return np.random.choice(len(probs), p=probs)


def generate_text(
    seed_text,
    next_words,
    model,
    tokenizer,
    max_sequence_len,
    index_word,
    temperature=1.0,
):

    text = seed_text.strip()

    for _ in range(next_words):

        token_list = tokenizer.texts_to_sequences([text])[0]

        token_list = pad_sequences(
            [token_list],
            maxlen=max_sequence_len - 1,
            padding="pre"
        )

        probs = model.predict(token_list, verbose=0)[0]

        next_index = gpt_sample(probs, temperature)

        next_word = index_word.get(next_index, "")

        if next_word == "":
            break

        text += " " + next_word

    return text
