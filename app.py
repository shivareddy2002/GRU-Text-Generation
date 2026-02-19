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
# Cache model
# -----------------------------------------------------
@st.cache_resource(show_spinner="Loading GRU model...")
def get_model_tokenizer():
    return load_model_and_tokenizer()


# -----------------------------------------------------
# MAIN
# -----------------------------------------------------
def main():
    st.set_page_config(
        page_title="GRU Text Generator",
        page_icon="🤖",
        layout="wide"
    )

    # ---------- CLEAN PROFESSIONAL THEME ----------
    st.markdown("""
        <style>
        /* App background */
        .stApp {
            background-color: #f5f7fb;
        }

        /* Center content */
        .block-container {
            max-width: 1100px;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        /* Card */
        .card {
            background: white;
            padding: 24px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            margin-bottom: 20px;
        }

        /* Title */
        .title {
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 0.3rem;
        }

        .subtitle {
            color: #6b7280;
            margin-bottom: 0.5rem;
        }

        /* Result */
        .result-box {
            background: #f9fafb;
            border: 1px solid #e5e7eb;
            padding: 16px;
            border-radius: 8px;
            font-family: monospace;
            white-space: pre-wrap;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #ffffff;
            border-right: 1px solid #e5e7eb;
        }

        </style>
    """, unsafe_allow_html=True)

    # ---------- Sidebar ----------
    with st.sidebar:
        st.title("🤖 GRU Generator")
        st.markdown("---")
        nav = st.radio(
            "Navigation",
            ["Home", "About", "How It Works", "Contact"],
            label_visibility="collapsed"
        )
        st.markdown("---")
        st.caption("Temperature controls creativity.")

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
# HOME
# -----------------------------------------------------
def show_home():

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="title">GRU Text Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Generate human-like text using a GRU neural network</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1.4], gap="large")

    # LEFT
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Configuration")

        with st.form("generation_form"):
            seed = st.text_area(
                "Seed Text",
                height=160,
                placeholder="Start writing here..."
            )

            st.markdown("#### Generation")
            length = st.slider("Word Count", 10, 1000, 50)
            temperature = st.slider("Temperature", 0.1, 2.0, 0.8)

            st.markdown("#### Mode")
            decoding_mode = st.selectbox(
                "Style",
                ["GPT (balanced)", "Creative", "Strict", "Greedy"]
            )

            repetition_penalty = st.slider(
                "Repetition Penalty",
                1.0, 2.0, 1.1
            )

            generate_btn = st.form_submit_button(
                "Generate Text",
                use_container_width=True
            )

        st.markdown('</div>', unsafe_allow_html=True)

    # RIGHT
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Result")

        if generate_btn:
            if not seed.strip():
                st.warning("Please enter seed text.")
            else:
                model, tokenizer, max_sequence_len, index_word = get_model_tokenizer()

                # Mode presets
                if decoding_mode == "Creative":
                    temperature = 1.1
                    repetition_penalty = 1.0
                elif decoding_mode == "Strict":
                    temperature = 0.5
                    repetition_penalty = 1.2
                elif decoding_mode == "Greedy":
                    temperature = 0.1
                    repetition_penalty = 1.0

                with st.spinner("Generating..."):
                    t0 = time.time()
                    generated = generate_text(
                        seed_text=seed.strip(),
                        next_words=length,
                        model=model,
                        tokenizer=tokenizer,
                        max_sequence_len=max_sequence_len,
                        index_word=index_word,
                        temperature=temperature,
                        repetition_penalty=repetition_penalty
                    )
                    t1 = time.time()

                st.success(f"Generated in {t1 - t0:.2f}s")

                st.markdown(
                    f'<div class="result-box">{generated}</div>',
                    unsafe_allow_html=True
                )

                st.download_button(
                    "Download",
                    generated,
                    file_name="generated_text.txt"
                )

                if "history" not in st.session_state:
                    st.session_state.history = []
                st.session_state.history.insert(0, generated)

        else:
            st.info("Enter text and click Generate.")

        st.markdown('</div>', unsafe_allow_html=True)

    # HISTORY
    if "history" in st.session_state and st.session_state.history:
        st.markdown("### Recent Generations")
        for i, txt in enumerate(st.session_state.history[:3]):
            with st.expander(f"Result {i+1}"):
                st.code(txt)

# -----------------------------------------------------
# ABOUT
# -----------------------------------------------------
def show_about():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.title("About")
    st.write("""
    This project demonstrates text generation using a GRU neural network.
    The model predicts next words sequentially to create coherent text.
    """)
    st.markdown('</div>', unsafe_allow_html=True)


# -----------------------------------------------------
# HOW
# -----------------------------------------------------
def show_how():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.title("How It Works")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Step 1")
        st.write("Enter seed text.")
    with col2:
        st.subheader("Step 2")
        st.write("Adjust parameters.")
    with col3:
        st.subheader("Step 3")
        st.write("Model generates text.")

    st.markdown('</div>', unsafe_allow_html=True)


# -----------------------------------------------------
# CONTACT
# -----------------------------------------------------
def show_contact():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.title("Contact")
    st.write("Lomada Siva Gangi Reddy")
    st.write("lomadasivagangireddy3@gmail.com")
    st.write("github.com/shivareddy2002")
    st.markdown('</div>', unsafe_allow_html=True)


# -----------------------------------------------------
if __name__ == "__main__":
    main()
