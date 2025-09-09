import streamlit as st
from transformers import pipeline
from datetime import datetime
import time

# Set page config
st.set_page_config(
    page_title="Advanced AI Text Summarizer",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.3rem;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .summary-box {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        margin-top: 15px;
    }
    .metric-box {
        background-color: #ffffff;
        padding: 12px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin: 8px 0;
    }
    .stButton button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
    }
    /* Reduced font sizes for efficiency */
    .stTextArea textarea {
        font-size: 14px;
    }
    /* Compact mode */
    .compact .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Add compact class to parent container
st.markdown('<div class="compact">', unsafe_allow_html=True)

# App title
st.markdown('<p class="main-header">Advanced AI Text Summarizer</p>', unsafe_allow_html=True)
st.write("Transform long articles into concise summaries using efficient NLP models - completely free!")

# Initialize session state for history and text input
if 'history' not in st.session_state:
    st.session_state.history = []
if 'text_input' not in st.session_state:
    st.session_state.text_input = ""

# Use LRU cache to avoid reloading models (reduces memory usage)
@st.cache_resource(show_spinner=False, max_entries=1)
def load_summarizer(model_name):
    """Load summarization model with efficient settings"""
    if model_name == "BART (Recommended)":
        return pipeline(
            "summarization", 
            model="facebook/bart-large-cnn",
            # Use these settings to reduce memory footprint
            dtype='auto',
            device_map='auto'
        )
    else:  # T5-small as a lighter alternative
        return pipeline(
            "summarization",
            model="t5-small",
            tokenizer="t5-small",
            dtype='auto',
            device_map='auto'
        )

# Sidebar for controls
with st.sidebar:
    st.header("Settings")
    
    # Model selection - using efficient models only
    model_option = st.selectbox(
        "Choose summarization model:",
        ("BART (Recommended)", "T5-Small (Faster)")
    )
    
    # Summary length control
    summary_length = st.slider(
        "Target summary length:",
        min_value=30,
        max_value=150,  # Reduced max to save computation
        value=80,
        step=5
    )
    
    # Text preprocessing options
    st.subheader("Text Preprocessing")
    remove_redundancy = st.checkbox("Remove redundant sentences", value=True)
    
    # Info about cost-free operation
    st.info("💡 This app uses efficient models and caching to operate completely free of charge!")

# Main content area
tab1, tab2, tab3 = st.tabs(["Summarize", "History", "About"])

with tab1:
    # Use session state for text input to persist across reruns
    text_input = st.text_area(
        "Paste your text here:",
        height=200,
        value=st.session_state.text_input,
        placeholder="Enter text to summarize (minimum 100 characters for best results)...",
        help="For best results, provide well-structured text with complete sentences.",
        key="text_input_area"
    )
    
    col1, col2 = st.columns([1, 2])
    with col1:
        summarize_btn = st.button("Generate Summary", type="primary", use_container_width=True)
    with col2:
        if st.button("Clear Text", use_container_width=True):
            # Clear text by updating session state
            st.session_state.text_input = ""
            st.rerun()  # Fixed: Use st.rerun() instead of st.experimental_rerun()
    
    # Update session state with current text input
    if text_input != st.session_state.text_input:
        st.session_state.text_input = text_input
    
    if summarize_btn:
        if st.session_state.text_input.strip() and len(st.session_state.text_input.split()) > 15:
            with st.spinner("Loading model and generating summary..."):
                try:
                    # Load model
                    summarizer = load_summarizer(model_option)
                    
                    # Preprocess text if options are selected
                    processed_text = st.session_state.text_input
                    if remove_redundancy:
                        # Simple redundancy removal (keeps first occurrence of each sentence)
                        sentences = processed_text.split('.')
                        unique_sentences = []
                        seen_sentences = set()
                        for sentence in sentences:
                            trimmed = sentence.strip()
                            if trimmed and trimmed not in seen_sentences:
                                unique_sentences.append(trimmed)
                                seen_sentences.add(trimmed)
                        processed_text = '. '.join(unique_sentences)
                    
                    # Generate summary
                    start_time = time.time()
                    
                    # Adjust length based on model
                    if model_option == "T5-Small (Faster)":
                        max_len = min(summary_length + 20, 100)  # Conservative limits for T5-small
                        min_len = max(summary_length - 20, 30)
                    else:
                        max_len = summary_length + 30
                        min_len = max(summary_length - 30, 30)
                    
                    summary = summarizer(
                        processed_text, 
                        max_length=max_len,
                        min_length=min_len,
                        do_sample=False
                    )
                    
                    processing_time = time.time() - start_time
                    summary_text = summary[0]['summary_text']
                    
                    # Display results
                    st.markdown('<div class="summary-box">', unsafe_allow_html=True)
                    st.markdown(f'<p class="sub-header">Summary</p>', unsafe_allow_html=True)
                    st.success(summary_text)
                    
                    # Calculate and display metrics
                    orig_word_count = len(st.session_state.text_input.split())
                    summary_word_count = len(summary_text.split())
                    compression_ratio = orig_word_count / max(summary_word_count, 1)
                    
                    st.markdown("### Summary Metrics")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
                        st.metric("Original Words", orig_word_count)
                        st.markdown('</div>', unsafe_allow_html=True)
                    with col2:
                        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
                        st.metric("Summary Words", summary_word_count)
                        st.markdown('</div>', unsafe_allow_html=True)
                    with col3:
                        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
                        st.metric("Compression Ratio", f"{compression_ratio:.1f}x")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.markdown(f"Processing time: {processing_time:.2f} seconds")
                    
                    # Add to history
                    st.session_state.history.append({
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M"),
                        'original': st.session_state.text_input[:300] + "..." if len(st.session_state.text_input) > 300 else st.session_state.text_input,
                        'summary': summary_text,
                        'model': model_option,
                        'word_count': summary_word_count,
                        'compression': f"{compression_ratio:.1f}x"
                    })
                    
                    # Keep only last 10 history items to save memory
                    if len(st.session_state.history) > 10:
                        st.session_state.history = st.session_state.history[-10:]
                    
                    # Export options
                    st.download_button(
                        label="Download Summary",
                        data=summary_text,
                        file_name="summary.txt",
                        mime="text/plain"
                    )
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}. Please try with shorter text.")
        
        elif not st.session_state.text_input.strip():
            st.warning("Please enter some text first.")
        else:
            st.warning("Text is too short. Please provide at least 15 words for meaningful summarization.")

with tab2:
    st.header("Summary History")
    if st.session_state.history:
        for i, item in enumerate(reversed(st.session_state.history)):
            with st.expander(f"{item['timestamp']} - {item['model']} ({item['word_count']} words, {item['compression']})"):
                st.write("**Original text (excerpt):**")
                st.info(item['original'])
                st.write("**Summary:**")
                st.success(item['summary'])
                
                # Add delete button for each history item
                if st.button(f"Delete", key=f"delete_{i}"):
                    # Remove item from history
                    index_to_remove = len(st.session_state.history) - 1 - i
                    st.session_state.history.pop(index_to_remove)
                    st.rerun()
    else:
        st.info("No summarization history yet. Generate some summaries to see them here.")

with tab3:
    st.header("About This App")
    st.write("""
    This Advanced Text Summarizer uses efficient NLP models to generate concise summaries completely free of charge.
    
    **Cost-Free Features:**
    - Efficient model selection (BART and T5-Small)
    - Model caching to reduce reloading
    - Memory-optimized settings
    - Text preprocessing options
    - Summary quality metrics
    - Export functionality
    - Session history
    
    **Models used:**
    - Facebook BART-large-CNN: High-quality summarization model
    - T5-Small: Faster, lighter model for quick summaries
    
    **Optimizations:**
    - Models are loaded only when needed
    - Caching prevents redundant model loading
    - Memory-efficient settings
    - History limited to 10 entries to conserve resources
    """)
    
    st.info("""
    💡 This app is designed to run completely free on platforms like Streamlit Community Cloud,
    Hugging Face Spaces, and other free hosting services.
    """)

st.markdown('</div>', unsafe_allow_html=True)  