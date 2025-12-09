# 🤖 AI Text Summarizer: Concise Summary Generator

> A sophisticated yet efficient web application that leverages optimized Hugging Face Transformers models to condense lengthy articles into precise, readable summaries.

<p align="center">
  <img src="https://img.shields.io/badge/Streamlit-Deployment-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit Deployment" />
  <img src="https://img.shields.io/badge/Models-BART%20%7C%20T5--Small-blue?style=for-the-badge" alt="Models: BART | T5-Small" />
</p>

## ✨ Core Features & Benefits

| Icon | Feature | Benefit |
| :---: | :--- | :--- |
| ⚡ | **Efficient Model Selection** | Fast and balanced performance using optimized **BART** and **T5-Small** models. |
| 🧠 | **Memory Optimized** | Features **model caching** and memory-efficient PyTorch settings to minimize resource usage and cost. |
| ✂️ | **Advanced Preprocessing** | Options for custom text preprocessing to ensure high-quality, relevant summaries. |
| 📜 | **Export & History** | Includes export functionality and limited session history (10 entries) for easy reference and management. |
| 📱 | **Responsive UI** | Clean, compact, and responsive Streamlit interface with custom CSS for faster rendering. |

## 💻 Tech Stack

| Category | Technologies |
| :--- | :--- |
| **Backend** | ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) |
| **Framework** | ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white) |
| **AI/ML** | ![Hugging Face](https://img.shields.io/badge/Hugging%20Face-FFB800?style=for-the-badge&logo=huggingface&logoColor=white) ![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white) |
| **Models** | `BART`, `T5-Small` |
| **Styling** | Custom CSS |

## ⚙️ Optimizations for Performance

This application is engineered for speed and efficiency:
1.  **Model Caching**: Models are initialized and cached upon the first use, eliminating redundant loading.
2.  **Efficient Models**: Strategically uses smaller, less resource-intensive models (`T5-Small`) when possible.
3.  **Memory Limits**: Session history is capped at 10 entries to conserve memory during long sessions.
4.  **Compact UI**: Uses custom CSS to reduce element sizes, leading to a faster and more compact user interface.
5.  **Smart Loading**: Models are loaded only when a summarization request is made, optimizing startup time.

## 🚀 Run Locally

```bash
# Clone the repository
git clone [https://github.com/your-username/python-text-summarizer.git](https://github.com/your-username/python-text-summarizer.git)
cd python-text-summarizer

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
