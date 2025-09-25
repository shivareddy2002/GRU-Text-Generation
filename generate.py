import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import os
import streamlit as st

# Paths to model and tokenizer
MODEL_PATH = os.path.join("models", "gru_model.h5")
TOKENIZER_PATH = os.path.join("data", "tokenizer.pickle")

# -------------------------------
# 🔒 Load model & tokenizer once
# -------------------------------
@st.cache_resource
def load_model_and_tokenizer():
    """
    Load GRU model and tokenizer from disk.
    Returns:
        model: Trained Keras model
        tokenizer: Keras Tokenizer
        max_sequence_len: int, maximum sequence length
    """
    # Load trained model
    model = tf.keras.models.load_model(MODEL_PATH)

    # Load tokenizer
    with open(TOKENIZER_PATH, "rb") as handle:
        tokenizer = pickle.load(handle)

    # Max sequence length used during training
    max_sequence_len = model.input_shape[1]

    return model, tokenizer, max_sequence_len


# -------------------------------
# 🔹 Text generation with temperature
# -------------------------------
def generate_text(
    seed_text,
    next_words,
    model,
    tokenizer,
    max_sequence_len,
    temperature=1.0
):
    """
    Generate text using the trained GRU model.
    Args:
        seed_text (str): Starting text
        next_words (int): Number of words to generate
        model: Keras model
        tokenizer: Keras Tokenizer
        max_sequence_len (int): maximum input sequence length
        temperature (float): creativity factor (>1 = more random)
    Returns:
        str: Generated text
    """
    # Build reverse index for quick word lookup
    index_word = {index: word for word, index in tokenizer.word_index.items()}

    text = seed_text

    for _ in range(next_words):
        token_list = tokenizer.texts_to_sequences([text])[0]
        token_list = pad_sequences([token_list], maxlen=max_sequence_len - 1, padding='pre')
        predicted_probs = model.predict(token_list, verbose=0)[0]

        # Apply temperature scaling
        predicted_probs = np.log(predicted_probs + 1e-9) / temperature
        exp_preds = np.exp(predicted_probs)
        predicted_probs = exp_preds / np.sum(exp_preds)

        # Sample the next word
        predicted_index = np.random.choice(len(predicted_probs), p=predicted_probs)
        next_word = index_word.get(predicted_index, "")

        if next_word == "":
            break

        text += " " + next_word

    return text
