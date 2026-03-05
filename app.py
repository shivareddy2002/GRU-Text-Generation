import time
import streamlit as st
from generate import generate_text, load_model_and_tokenizer

# -----------------------------------------------------
# 🔒 Cache model/tokenizer so they load only once
# -----------------------------------------------------
@st.cache_resource(show_spinner="Loading GRU model...")
def get_model_tokenizer():
    try:
        model, tokenizer, max_sequence_len = load_model_and_tokenizer()
        return model, tokenizer, max_sequence_len
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None, None, None


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

    # ---------- Custom CSS ----------
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

        .history-box {
            max-height: 200px;
            overflow-y: auto;
            padding-right: 5px;
        }
        </style>
    """, unsafe_allow_html=True)

    # ---------- Sidebar ----------
    st.sidebar.title("🚀 Siva")
    st.sidebar.markdown("### Navigation")

    nav = st.sidebar.radio("", ["Home", "About", "How It Works", "Contact"])

    # ---------- Pages ----------
    if nav == "Home":
        show_home()
    elif nav == "About":
        show_about()
    elif nav == "How It Works":
        show_how()
    else:
        show_contact()


# -----------------------------------------------------
# 🏠 HOME PAGE
# -----------------------------------------------------
def show_home():

    st.title("🤖 Text Generation using GRU Model")

    seed = st.text_input("Seed Text", placeholder="Enter starting text")

    col1, col2 = st.columns(2)

    with col1:
        length = st.number_input("Number of Words", 1, 500, 20)

    with col2:
        temperature = st.slider("Temperature (controls creativity)", 0.1, 2.0, 0.7, 0.1)

    generate_btn = st.button("✨ Generate Text")

    if "history" not in st.session_state:
        st.session_state.history = []

    if generate_btn:

        if not seed.strip():
            st.warning("⚠️ Please enter seed text.")
            return

        model, tokenizer, max_sequence_len = get_model_tokenizer()

        if model is None:
            st.error("Model failed to load.")
            return

        with st.spinner("Generating text..."):

            start = time.time()

            generated = generate_text(
                seed_text=seed.strip(),
                next_words=length,
                model=model,
                tokenizer=tokenizer,
                max_sequence_len=max_sequence_len,
                temperature=temperature
            )

            end = time.time()

        st.success(f"✅ Text generated in {end-start:.2f} seconds.")

        st.subheader("Generated Text")
        st.write(generated)

        st.text_area("Copy / Edit", generated, height=120)

        st.download_button(
            "📥 Download as TXT",
            generated,
            file_name="generated_text.txt"
        )

        # Save history
        st.session_state.history.insert(0, generated)

    # ---------- History ----------
    if st.session_state.history:

        st.markdown("### 📝 History")

        with st.container():

            st.markdown('<div class="history-box">', unsafe_allow_html=True)

            for i, txt in enumerate(st.session_state.history, 1):

                with st.expander(f"Result {i}"):
                    st.write(txt)

            st.markdown('</div>', unsafe_allow_html=True)


# -----------------------------------------------------
# ℹ️ ABOUT
# -----------------------------------------------------
def show_about():

    st.title("ℹ️ About")

    st.write(
        """
        A deep learning project that generates text sequences using a **Gated Recurrent Unit (GRU)** based Recurrent Neural Network (RNN).

        This project demonstrates **Text Generation** using a **GRU-based Recurrent Neural Network**. It learns from a given text corpus
        and generates new text word-by-word. The project includes data preprocessing, model training, text generation, and deployment
        via a **Streamlit** web app. 🚀
        """
    )

    st.markdown("### 🚀 Key Features")
    st.markdown("- Efficient **GRU architecture** for sequence learning.")
    st.markdown("- **Beam search style next-word generation controls** with temperature sampling.")
    st.markdown("- Interactive **Streamlit web app** for real-time text generation.")
    st.markdown("- Lightweight and fast training compared to LSTMs.")

    st.markdown("### 🧰 Dependencies")
    st.markdown("- Python")
    st.markdown("- TensorFlow / Keras")
    st.markdown("- NumPy")
    st.markdown("- Pandas")
    st.markdown("- Matplotlib")
    st.markdown("- Streamlit")


# -----------------------------------------------------
# ⚙️ HOW IT WORKS
def show_how():

    st.title("⚙️ How It Works")

    steps = [
        ("1️⃣ Importing Dependencies", "Load TensorFlow/Keras, NumPy, Matplotlib, and utilities for preprocessing and training."),
        ("2️⃣ Loading the Text Corpus", "Provide a custom input text file so the model can learn writing patterns."),
        ("3️⃣ Preprocessing the Data", "Clean text, tokenize words, create numerical sequences, and pad inputs to a fixed length."),
        ("4️⃣ Building the GRU Model", "Use Embedding + GRU layers + Dense softmax output for next-word prediction."),
        ("5️⃣ Training the Model", "Train with Categorical Crossentropy loss and Adam optimizer."),
        ("6️⃣ Generating Text", "Use a seed text and iteratively predict the next words to create a sequence."),
        ("7️⃣ Deploying with Streamlit", "Serve the model with an interactive app for instant text generation."),
    ]

    for step_title, step_desc in steps:
        with st.container(border=True):
            st.subheader(step_title)
            st.write(step_desc)

    st.markdown("### 🌐 Live Demo")
    st.markdown("[Text Generation using GRU Model](https://text-generation-using-gru-model.streamlit.app/)")

    st.markdown("### 🖼️ Visual Workflow")
    st.image(
        "https://github.com/shivareddy2002/GRU-Text-Generation/blob/main/UI_Galary/text_generation_flow.png?raw=true",
        caption="Project workflow from data preparation to Streamlit deployment",
        use_container_width=True,
    )


# -----------------------------------------------------
# 📬 CONTACT
# -----------------------------------------------------
def show_contact():

    st.title("📬 Contact")

    st.write("**Lomada Siva Gangi Reddy**")
    st.write("🎓 B.Tech CSE (Data Science), RGMCET (2021–2025)")
    st.write("💡 Interests: Python | Machine Learning | Deep Learning | Data Science")
    st.write("📍 Open to Internships & Job Offers")

    st.markdown("### Contact Me")
    st.write("📧 Email: lomadasivagangireddy3@gmail.com")
    st.write("📞 Phone: 9346493592")
    st.markdown("💼 [LinkedIn](https://www.linkedin.com/in/lomada-siva-gangi-reddy-a64197280/)")
    st.markdown("🌐 [GitHub](https://github.com/shivareddy2002)")
    st.markdown("🚀 [Portfolio](https://lsgr-portfolio-pulse.lovable.app/)")


# -----------------------------------------------------
if __name__ == "__main__":
    main()
