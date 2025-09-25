import time
import streamlit as st
from generate import (
    generate_text,                  # Your GRU text generation function
    load_model_and_tokenizer         # Loads model, tokenizer, max_sequence_len
)

# -----------------------------------------------------
# 🔒 Cache model/tokenizer so they load only once
# -----------------------------------------------------
@st.cache_resource(show_spinner="Loading GRU model...")
def get_model_tokenizer():
    # Returns three values: model, tokenizer, max_sequence_len
    return load_model_and_tokenizer()

# -----------------------------------------------------
# 🚀 Main App
# -----------------------------------------------------
def main():
    st.set_page_config(
        page_title="Text Generator using GRU Model",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # ---------- Custom CSS (mimic gradient & dark mode) ----------
    st.markdown("""
        <style>
        body, .stApp {
            background: linear-gradient(-45deg, #e0f7fa, #e1bee7, #bbdefb, #ffe0b2);
            background-size: 400% 400%;
            animation: gradientBG 500s ease infinite;
        }
        @keyframes gradientBG {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }
        .main-card {
            background-color: rgba(255,255,255,0.85);
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
            max-width: 850px;
            margin: auto;
        }
        .history-box {
            max-height: 200px;
            overflow-y: auto;
            padding-right: 5px;
        }
        </style>
    """, unsafe_allow_html=True)

    # ---------- Sidebar ----------
    st.sidebar.title("🚀 Siva ")
    st.sidebar.markdown("### Navigation")
    nav = st.sidebar.radio("", ["Home", "About", "How It Works", "Contact"])
    st.sidebar.markdown("---")
    #st.sidebar.caption("🌙 Toggle dark mode in browser settings (Streamlit theme).")
    
    # ---------- Content ----------
    if nav == "Home":
        show_home()
    elif nav == "About":
        show_about()
    elif nav == "How It Works":
        show_how()
    else:
        show_contact()

# ---------- Sections ----------
def show_home():

    st.title("🤖 Text Generation using GRU Model")

    seed = st.text_input("Seed Text", placeholder="Enter starting text")
    col1, col2 = st.columns(2)
    with col1:
        length = st.number_input("Number of Words", 1, 5000, 20)
    with col2:
        temperature = st.slider("Temperature (controls creativity)", 0.1, 2.0, 0.7, 0.1)

    generate_btn = st.button("✨ Generate Text")

    if "history" not in st.session_state:
        st.session_state.history = []

    if generate_btn:
        if not seed.strip():
            st.warning("⚠️ Please enter seed text.")
        else:
            # ✅ Correct unpacking for 3 returned values
            model, tokenizer, max_sequence_len = get_model_tokenizer()
            with st.spinner("Generating text..."):
                t0 = time.time()
                generated = generate_text(
                    seed_text=seed.strip(),
                    next_words=length,
                    model=model,
                    tokenizer=tokenizer,
                    max_sequence_len=max_sequence_len
                )
                t1 = time.time()

            st.success(f"✅ Text generated in {t1 - t0:.2f} seconds.")
            st.subheader("✨ Generated Text")
            st.write(generated)
            st.text_area("Copy / Edit", generated, height=100)
            st.download_button("📥 Download as TXT", generated, file_name="generated_text.txt")

            # Save to history
            st.session_state.history.insert(0, generated)

    if st.session_state.history:
        st.markdown("### 📝 History")
        with st.container():
            st.markdown('<div class="history-box">', unsafe_allow_html=True)
            for i, txt in enumerate(st.session_state.history, 1):
                with st.expander(f"Result {i}"):
                    st.write(txt)
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


def show_about():
    st.title("🤖 Text Generation using GRU Model")

    st.header("ℹ️ About")
    st.write(
        """
        This project demonstrates **Text Generation** using a **GRU-based Neural Network**.  
        The model learns from sequences of text and predicts the next word step-by-step to create new text. ✍️✨

        Key ideas:
        - Learn patterns in text sequences (tokens/words) 🔎
        - Predict the most likely next token at each step ▶️
        - Generate coherent sentences by sampling repeatedly 🔁
        """
    )

    with st.expander("📊 Data details (click to expand)"):
        st.write("**Dataset**: A corpus of raw text (books/articles/your data). 🗂️")
        st.write("**Typical preprocessing**:")
        st.markdown(
            """
            - 🔤 Lowercasing, punctuation removal (optional)
            - ➗ Tokenization (words / subwords / chars)
            - 🔁 Sliding-window sequences of fixed `seq_length`
            - 🧾 Convert tokens → integer ids (vocabulary)
            - 🔀 Train / validation split (e.g., 90% / 10%)
            """
        )
        st.write("**What the model needs**:")
        st.markdown(
            """
            - 📦 `num_sequences` (how many training sequences)
            - 🧠 `vocab_size` (unique tokens)
            - 📏 `seq_length` (tokens per input)
            - 🔁 `batch_size` used during training
            """
        )
        st.info("Tip: If you'd like, pass actual dataset stats to show real numbers here. ✅")


def show_how():
    st.title("🤖 Text Generation using GRU Model")
    st.header("⚡ How It Works")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("📜 Step 1")
        st.write("Enter your **Seed Text** to begin the generation process.")
    with col2:
        st.subheader("✍️ Step 2")
        st.write("Adjust **parameters** like word count and temperature.")
    with col3:
        st.subheader("🤖 Step 3")
        st.write("The GRU model predicts and generates text continuing your idea.")
    st.markdown('</div>', unsafe_allow_html=True)

def show_contact():
    st.title("🤖 Text Generation using GRU Model")
    st.header("📬 Contact")
    st.write("👤 **Name :**  Lomada Siva Gangi Reddy ")
    st.write("📧 Email: [lomadasivagangireddy3@gmail.com](mailto:lomadasivagangireddy3@gmail.com)")
    st.write("🌐 GitHub: [github.com/shivareddy2002](https://github.com/shivareddy2002)")
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------
if __name__ == "__main__":
    main()
