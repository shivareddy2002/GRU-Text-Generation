# GRU-Text-Generation
# 📝 Text Generation Using GRU Model

A deep learning project that generates text sequences using a **Gated Recurrent Unit (GRU)** based Recurrent Neural Network (RNN).
This project demonstrates **Text Generation** using a **GRU-based Recurrent Neural Network**.  
It learns from a given text corpus and generates new text word-by-word. 
The project includes data preprocessing, model training, text generation, and deployment via a **Streamlit** web app. 🚀

---

## 🔗 Live Demo
Try the deployed Streamlit app here:  
**Text Generation using GRU Model** — [🌐 Live Demo](https://text-generation-using-gru-model.streamlit.app/)


---

## 💡 Project Overview
This project generates text sequences by learning patterns from a given text dataset using a GRU-based neural network — efficient, fast, and effective for sequential data. ⚙️

Key steps include:

1. **Data Preprocessing** ✂️  
   - Tokenization: Converts text into sequences of integers.  
   - Padding: Ensures all sequences have the same length for model input.  
   - Input-Output Pair Creation: Prepares sequences by using the first N words as input and the next word as the target.

2. **Model Building** 🏗️  
   - GRU Layer(s): Captures sequential dependencies.  
   - Dense Layer: Predicts the next word from the vocabulary.  
   - Compilation: Uses categorical crossentropy loss and Adam optimizer.

3. **Text Generation** ✍️  
   - Seed text is provided by the user.  
   - Next words are predicted iteratively to form sequences.  
   - Supports **beam search** for higher-quality generation by exploring multiple candidate sequences.

4. **Deployment** 🚀  
   - Integrated into a **Streamlit** app.  
   - Users can interactively input seed text and generate new text sequences.

---

## ⚙️ Usage
1. Open the Streamlit app.  
2. Enter a seed text (starting phrase). 📝  
3. Specify the number of words to generate. 🔢  
4. Click **Generate** to see the output text. ▶️

**Example Output:**  
Seed text: `"Once upon a time"`  
Generated text: `"Once upon a time in a land far away there lived a wise king..."` ✨

---

## 📊 Model Details
- **Architecture:** GRU layer(s) + Dense output layer  
- **Input:** Tokenized and padded sequences of text  
- **Output:** Probability distribution over the vocabulary for next word prediction  
- **Loss:** Categorical Crossentropy  
- **Optimizer:** Adam  

**Why GRU?**  
- Fewer parameters than LSTM → faster training ⚡  
- Retains capability to capture long-term dependencies ✅  
- Ideal when you need a lightweight RNN for text generation

---

## 🔎 Beam Search
- Considers multiple candidate sequences during generation  
- Produces more coherent and contextually relevant text  
- Useful for improved quality when generating longer passages 🧭

---

## 💾 Dataset
- Any text corpus can be used (books, articles, plays, custom corpora). 📚  
- Preprocessing steps: tokenization, sequence creation, padding.  
- Replace the dataset to generate text in different styles/tones.

---

## 🎨 Author
Created by **[LOMADA SIVA GANGI REDDY]**  

---

## 🖼️ Visual Workflow

```mermaid
   flowchart LR
    %% --- Data Preparation Stage ---
    subgraph DP[📂 Data Preparation]
        A["📦 Importing Required Libraries"]
        B["📚 Loading Input Text Corpus"]
        C["✂️ Preprocessing\n(Cleaning + Tokenization + Creating Sequences + Padding)"]
    end

    %% --- Modeling & Training Stage ---
    subgraph MT[🤖 Modeling & Training]
        D["🏗️ GRU Model\n(RNN Layers + Dense)"]
        E["⚡ Training\n(Categorical Crossentropy + Adam)"]
    end

    %% --- Text Generation Stage ---
    subgraph TG[🚀 Text Generation ]
        F["✍️ Text Generation\n(Seed + Predicted Words)"]
    end

    %% --- Deployment Stage ---
    subgraph DS[🚀  Deployment]
        G["🌐 Streamlit Deployment\n(Interactive Web App)"]
    end

    %% --- Flow Connections ---
    A --> B --> C --> D --> E --> F --> G













