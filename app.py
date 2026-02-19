# import time
# import streamlit as st
# from generate import (
#     generate_text,                  # Your GRU text generation function
#     load_model_and_tokenizer         # Loads model, tokenizer, max_sequence_len
# )

# # -----------------------------------------------------
# # 🔒 Cache model/tokenizer so they load only once
# # -----------------------------------------------------
# @st.cache_resource(show_spinner="Loading GRU model...")
# def get_model_tokenizer():
#     # Returns three values: model, tokenizer, max_sequence_len
#     return load_model_and_tokenizer()

# # -----------------------------------------------------
# # 🚀 Main App
# # -----------------------------------------------------
# def main():
#     st.set_page_config(
#         page_title="Text Generator using GRU Model",
#         page_icon="🤖",
#         layout="wide",
#         initial_sidebar_state="expanded"
#     )

#     # ---------- Custom CSS (mimic gradient & dark mode) ----------
#     st.markdown("""
#         <style>
#         body, .stApp {
#             background: linear-gradient(-45deg, #e0f7fa, #e1bee7, #bbdefb, #ffe0b2);
#             background-size: 400% 400%;
#             animation: gradientBG 500s ease infinite;
#         }
#         @keyframes gradientBG {
#             0% {background-position: 0% 50%;}
#             50% {background-position: 100% 50%;}
#             100% {background-position: 0% 50%;}
#         }
#         .main-card {
#             background-color: rgba(255,255,255,0.85);
#             padding: 2rem;
#             border-radius: 20px;
#             box-shadow: 0 4px 20px rgba(0,0,0,0.15);
#             max-width: 850px;
#             margin: auto;
#         }
#         .history-box {
#             max-height: 200px;
#             overflow-y: auto;
#             padding-right: 5px;
#         }
#         </style>
#     """, unsafe_allow_html=True)

#     # ---------- Sidebar ----------
#     st.sidebar.title("🚀 Siva ")
#     st.sidebar.markdown("### Navigation")
#     nav = st.sidebar.radio("", ["Home", "About", "How It Works", "Contact"])
#     st.sidebar.markdown("---")
#     #st.sidebar.caption("🌙 Toggle dark mode in browser settings (Streamlit theme).")
    
#     # ---------- Content ----------
#     if nav == "Home":
#         show_home()
#     elif nav == "About":
#         show_about()
#     elif nav == "How It Works":
#         show_how()
#     else:
#         show_contact()

# # ---------- Sections ----------
# def show_home():

#     st.title("🤖 Text Generation using GRU Model")

#     seed = st.text_input("Seed Text", placeholder="Enter starting text")
#     col1, col2 = st.columns(2)
#     with col1:
#         length = st.number_input("Number of Words", 1, 5000, 20)
#     with col2:
#         temperature = st.slider("Temperature (controls creativity)", 0.1, 2.0, 0.7, 0.1)

#     generate_btn = st.button("✨ Generate Text")

#     if "history" not in st.session_state:
#         st.session_state.history = []

#     if generate_btn:
#         if not seed.strip():
#             st.warning("⚠️ Please enter seed text.")
#         else:
#             # ✅ Correct unpacking for 3 returned values
#             model, tokenizer, max_sequence_len = get_model_tokenizer()
#             with st.spinner("Generating text..."):
#                 t0 = time.time()
#                 generated = generate_text(
#                     seed_text=seed.strip(),
#                     next_words=length,
#                     model=model,
#                     tokenizer=tokenizer,
#                     max_sequence_len=max_sequence_len
#                 )
#                 t1 = time.time()

#             st.success(f"✅ Text generated in {t1 - t0:.2f} seconds.")
#             st.subheader("✨ Generated Text")
#             st.write(generated)
#             st.text_area("Copy / Edit", generated, height=100)
#             st.download_button("📥 Download as TXT", generated, file_name="generated_text.txt")

#             # Save to history
#             st.session_state.history.insert(0, generated)

#     if st.session_state.history:
#         st.markdown("### 📝 History")
#         with st.container():
#             st.markdown('<div class="history-box">', unsafe_allow_html=True)
#             for i, txt in enumerate(st.session_state.history, 1):
#                 with st.expander(f"Result {i}"):
#                     st.write(txt)
#             st.markdown('</div>', unsafe_allow_html=True)

#     st.markdown('</div>', unsafe_allow_html=True)


# def show_about():
#     st.title("🤖 Text Generation using GRU Model")

#     st.header("ℹ️ About")
#     st.write(
#         """
#         This project demonstrates **Text Generation** using a **GRU-based Neural Network**.  
#         The model learns from sequences of text and predicts the next word step-by-step to create new text. ✍️✨

#         Key ideas:
#         - Learn patterns in text sequences (tokens/words) 🔎
#         - Predict the most likely next token at each step ▶️
#         - Generate coherent sentences by sampling repeatedly 🔁
#         """
#     )

#     with st.expander("📊 Data details (click to expand)"):
#         st.write("**Dataset**: A corpus of raw text (books/articles/your data). 🗂️")
#         st.write("**Typical preprocessing**:")
#         st.markdown(
#             """
#             - 🔤 Lowercasing, punctuation removal (optional)
#             - ➗ Tokenization (words / subwords / chars)
#             - 🔁 Sliding-window sequences of fixed `seq_length`
#             - 🧾 Convert tokens → integer ids (vocabulary)
#             - 🔀 Train / validation split (e.g., 90% / 10%)
#             """
#         )
#         st.write("**What the model needs**:")
#         st.markdown(
#             """
#             - 📦 `num_sequences` (how many training sequences)
#             - 🧠 `vocab_size` (unique tokens)
#             - 📏 `seq_length` (tokens per input)
#             - 🔁 `batch_size` used during training
#             """
#         )
#         st.info("Tip: If you'd like, pass actual dataset stats to show real numbers here. ✅")


# def show_how():
#     st.title("🤖 Text Generation using GRU Model")
#     st.header("⚡ How It Works")
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         st.subheader("📜 Step 1")
#         st.write("Enter your **Seed Text** to begin the generation process.")
#     with col2:
#         st.subheader("✍️ Step 2")
#         st.write("Adjust **parameters** like word count and temperature.")
#     with col3:
#         st.subheader("🤖 Step 3")
#         st.write("The GRU model predicts and generates text continuing your idea.")
#     st.markdown('</div>', unsafe_allow_html=True)

# def show_contact():
#     st.title("🤖 Text Generation using GRU Model")
#     st.header("📬 Contact")
#     st.write("👤 **Name :**  Lomada Siva Gangi Reddy ")
#     st.write("📧 Email: [lomadasivagangireddy3@gmail.com](mailto:lomadasivagangireddy3@gmail.com)")
#     st.write("🌐 GitHub: [github.com/shivareddy2002](https://github.com/shivareddy2002)")
#     st.markdown('</div>', unsafe_allow_html=True)

# # -----------------------------------------------------
# if __name__ == "__main__":
#     main()
import time
import streamlit as st
from generate import (
    generate_text,
    load_model_and_tokenizer
)

# -----------------------------------------------------
# 🔒 Cache model/tokenizer
# -----------------------------------------------------
@st.cache_resource(show_spinner="Loading GRU model...")
def get_model_tokenizer():
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

    # ---------- Custom CSS ----------
    st.markdown("""
        <style>
        body, .stApp {
            background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
            background-size: 400% 400%;
            animation: gradientBG 15s ease infinite;
        }
        @keyframes gradientBG {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }
        .glass-card {
            background: rgba(255, 255, 255, 0.9);
            border-radius: 16px;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(5px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            padding: 20px;
            margin-bottom: 20px;
        }
        .result-box {
            background-color: #f0f2f6;
            border-left: 5px solid #ff4b4b;
            padding: 15px;
            border-radius: 5px;
            font-family: monospace;
            white-space: pre-wrap;
        }
        </style>
    """, unsafe_allow_html=True)

    # ---------- Sidebar ----------
    with st.sidebar:
        st.title("🚀 Siva's AI Lab")
        st.markdown("---")
        st.markdown("### 🧭 Navigation")
        nav = st.radio(
            "Go to",
            ["Home", "About", "How It Works", "Contact"],
            label_visibility="collapsed"
        )
        st.markdown("---")
        st.info("💡 Tip: Decoding controls improve text quality.")

    # ---------- Routing ----------
    if nav == "Home":
        show_home()
    elif nav == "About":
        show_about()
    elif nav == "How It Works":
        show_how()
    else:
        show_contact()


# -----------------------------------------------------
# 🏠 Home
# -----------------------------------------------------
def show_home():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.title("🤖 GRU Text Generator")
    st.caption("Generate human-like text sequences using Deep Learning.")
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1.5], gap="medium")

    # LEFT COLUMN
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("✍️ Configuration")

        with st.form("generation_form"):
            seed = st.text_area(
                "Seed Text",
                height=150,
                placeholder="Start your story here..."
            )

            with st.expander("⚙️ Generation Parameters", expanded=True):
                length = st.slider("Word Count", 10, 1000, 50)
                temperature = st.slider("Temperature", 0.1, 2.0, 0.8)

            # 🔥 NEW: Decoding Controls
            with st.expander("🧠 Decoding Controls (GPT-style)", expanded=False):
                decoding_mode = st.selectbox(
                    "Decoding Mode",
                    ["GPT (recommended)", "Creative", "Strict", "Greedy"]
                )

                top_k = st.slider("Top-K", 0, 100, 50)
                top_p = st.slider("Top-P (nucleus)", 0.1, 1.0, 0.9)
                repetition_penalty = st.slider("Repetition Penalty", 1.0, 2.0, 1.1)

            generate_btn = st.form_submit_button(
                "🚀 Generate Text",
                use_container_width=True
            )

        st.markdown('</div>', unsafe_allow_html=True)

    # RIGHT COLUMN
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("✨ Result")

        if generate_btn:
            if not seed.strip():
                st.warning("⚠️ Please enter seed text.")
            else:
                model, tokenizer, max_sequence_len, index_word = get_model_tokenizer()

                # Apply preset modes
                if decoding_mode == "Creative":
                    temperature = 1.1
                    top_k = 80
                    top_p = 0.95
                    repetition_penalty = 1.0
                elif decoding_mode == "Strict":
                    temperature = 0.5
                    top_k = 20
                    top_p = 0.8
                    repetition_penalty = 1.2
                elif decoding_mode == "Greedy":
                    temperature = 0.1
                    top_k = 0
                    top_p = 1.0
                    repetition_penalty = 1.0
                # GPT default otherwise

                with st.spinner("Generating text..."):
                    t0 = time.time()
                    generated = generate_text(
                        seed_text=seed.strip(),
                        next_words=length,
                        model=model,
                        tokenizer=tokenizer,
                        max_sequence_len=max_sequence_len,
                        index_word=index_word,
                        temperature=temperature,
                        top_k=top_k,
                        top_p=top_p,
                        repetition_penalty=repetition_penalty
                    )
                    t1 = time.time()

                st.success(f"✅ Generated in {t1 - t0:.2f}s")

                st.markdown(
                    f'<div class="result-box">{generated}</div>',
                    unsafe_allow_html=True
                )

                st.download_button(
                    label="📥 Download Result",
                    data=generated,
                    file_name="generated_text.txt",
                    mime="text/plain"
                )

                if "history" not in st.session_state:
                    st.session_state.history = []

                st.session_state.history.insert(0, generated)

        else:
            st.info("👈 Enter text on the left to start generating!")

        st.markdown('</div>', unsafe_allow_html=True)

    # HISTORY
    if "history" in st.session_state and st.session_state.history:
        st.markdown("---")
        st.subheader("📜 Recent Generations")

        for i, txt in enumerate(st.session_state.history[:3]):
            with st.expander(f"Result #{i+1}"):
                st.code(txt, language="text")


# -----------------------------------------------------
# ℹ️ About
# -----------------------------------------------------
def show_about():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.title("ℹ️ About")
    st.write("""
    This project demonstrates **Text Generation** using a **GRU Neural Network**.

    The model:
    - Learns word sequences
    - Predicts next word probabilities
    - Generates coherent text step-by-step
    """)
    st.markdown('</div>', unsafe_allow_html=True)


# -----------------------------------------------------
# ⚙️ How It Works
# -----------------------------------------------------
def show_how():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.title("⚙️ How It Works")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("📜 Step 1")
        st.write("Enter seed text.")

    with col2:
        st.subheader("⚙️ Step 2")
        st.write("Adjust parameters & decoding.")

    with col3:
        st.subheader("🤖 Step 3")
        st.write("GRU generates text.")

    st.markdown('</div>', unsafe_allow_html=True)


# -----------------------------------------------------
# 📬 Contact
# -----------------------------------------------------
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
