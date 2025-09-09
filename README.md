# AI Text Summarizer

A sophisticated yet efficient web application that summarizes long articles into concise text using optimized Hugging Face Transformers models.

## Features

* Efficient model selection (BART and T5-Small)
* Model caching to minimize resource usage
* Memory-optimized settings
* Text preprocessing options
* Summary quality metrics
* Export functionality
* Session history (limited to conserve memory)
* Responsive UI with efficient styling

## Tech Stack

* Python, Streamlit
* Hugging Face Transformers (BART, T5-Small)
* Torch with memory-efficient settings
* Custom CSS for compact UI

## Optimizations

1. **Model Caching**: Models are loaded once and cached for the session
2. **Efficient Models**: Using smaller models when possible
3. **Memory Limits**: History limited to 10 entries
4. **Compact UI**: Reduced element sizes for faster rendering
5. **Smart Loading**: Models only loaded when needed

## Run Locally

```bash
git clone https://github.com/your-username/python-text-summarizer.git
cd python-text-summarizer
pip install -r requirements.txt
streamlit run app.py
