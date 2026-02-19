import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import os
import streamlit as st

# --------------------------------------------------
# Paths
# --------------------------------------------------
MODEL_PATH = os.path.join("models", "gru_model.h5")
TOKENIZER_PATH = os.path.join("data", "tokenizer.pickle")


# --------------------------------------------------
# 🔒 Load model & tokenizer once
# --------------------------------------------------
@st.cache_resource(show_spinner="Loading GRU model...")
def load_model_and_tokenizer():
    """
    Load GRU model and tokenizer from disk.

    Returns:
        model: Trained Keras model
        tokenizer: Keras Tokenizer
        max_sequence_len: int
        index_word: dict
    """

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

    if not os.path.exists(TOKENIZER_PATH):
        raise FileNotFoundError(f"Tokenizer not found: {TOKENIZER_PATH}")

    model = tf.keras.models.load_model(MODEL_PATH)

    with open(TOKENIZER_PATH, "rb") as handle:
        tokenizer = pickle.load(handle)

    max_sequence_len = model.input_shape[1]

    # Reverse lookup dictionary
    index_word = {index: word for word, index in tokenizer.word_index.items()}

    return model, tokenizer, max_sequence_len, index_word


# --------------------------------------------------
# 🔹 GPT-style sampling
# --------------------------------------------------
def gpt_sample(
    probs,
    temperature=1.0,
    top_k=0,
    top_p=1.0,
    repetition_penalty=1.0,
    generated_indices=None,
):
    """
    GPT-like decoding:
    - temperature scaling
    - top-k sampling
    - nucleus (top-p)
    - repetition penalty
    """

    probs = np.asarray(probs).astype("float64")

    # Repetition penalty
    if generated_indices and repetition_penalty != 1.0:
        for idx in generated_indices:
            probs[idx] /= repetition_penalty

    # Temperature
    if temperature <= 0:
        temperature = 1.0

    probs = np.log(probs + 1e-9) / temperature
    probs = np.exp(probs)
    probs /= np.sum(probs)

    # Top-K
    if top_k > 0:
        top_k_indices = np.argsort(probs)[-top_k:]
        mask = np.zeros_like(probs)
        mask[top_k_indices] = probs[top_k_indices]
        probs = mask / np.sum(mask)

    # Top-P (nucleus)
    if top_p < 1.0:
        sorted_indices = np.argsort(probs)[::-1]
        cumulative_probs = np.cumsum(probs[sorted_indices])

        cutoff = cumulative_probs > top_p
        if np.any(cutoff):
            cutoff_index = np.where(cutoff)[0][0]
            allowed = sorted_indices[: cutoff_index + 1]

            mask = np.zeros_like(probs)
            mask[allowed] = probs[allowed]
            probs = mask / np.sum(mask)

    return np.random.choice(len(probs), p=probs)


# --------------------------------------------------
# 🔹 Text generation (GPT-like GRU)
# --------------------------------------------------
def generate_text(
    seed_text: str,
    next_words: int,
    model,
    tokenizer,
    max_sequence_len: int,
    index_word: dict,
    temperature: float = 1.0,
    top_k: int = 0,
    top_p: float = 1.0,
    repetition_penalty: float = 1.0,
    stop_token: str = None,
):
    """
    Generate text using GRU with GPT-like decoding.

    Args:
        seed_text: starting text
        next_words: words to generate
        model: keras model
        tokenizer: tokenizer
        max_sequence_len: sequence length
        index_word: reverse dictionary
        temperature: randomness
        top_k: restrict to k words
        top_p: nucleus probability
        repetition_penalty: reduce repeats
        stop_token: optional stop word

    Returns:
        Generated text
    """

    text = seed_text.strip()
    generated_indices = []

    for _ in range(next_words):
        token_list = tokenizer.texts_to_sequences([text])[0]

        token_list = pad_sequences(
            [token_list],
            maxlen=max_sequence_len - 1,
            padding="pre"
        )

        probs = model.predict(token_list, verbose=0)[0]

        next_index = gpt_sample(
            probs,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            repetition_penalty=repetition_penalty,
            generated_indices=generated_indices,
        )

        next_word = index_word.get(next_index, "")

        if next_word == "":
            break

        text += " " + next_word
        generated_indices.append(next_index)

        if stop_token and next_word == stop_token:
            break

    return text
