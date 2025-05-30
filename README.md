# StoryTube

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/shouryank/StoryTube/pulls)

**Transform your short stories into animated videos.**

StoryTube is an innovative tool that takes a short story as input and generates an animated video, bringing narratives to life through automation.

## ✨ Features

- **Natural Language Processing**: Utilizes NLP techniques for coreference resolution and clause extraction.
- **Dialogue Generation**: Automatically generates dialogues from narratives.
- **Animation Rendering**: Creates animations based on the processed story content.
- **Audio Integration**: Incorporates generated dialogues into the animation as audio.

## 📁 Project Structure

```
StoryTube/
├── animation/           # Animation scripts and assets
├── assets/              # Static assets like images and audio
├── clausIE/             # Clause extraction module
├── coref_resolution/    # Coreference resolution module
├── dialogue/            # Dialogue generation scripts
├── extras/              # Additional utilities and scripts
├── utils/               # Helper functions and utilities
├── constants.py         # Constant values used across modules
├── main.py              # Entry point of the application
├── requirements.txt     # Python dependencies
└── test_pipeline.py     # Test scripts for the pipeline
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/shouryank/StoryTube.git
   cd StoryTube
   ```

2. **Create a Virtual Environment (Optional but Recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## 📝 Usage

1. **Prepare Your Story**

   Create a text file containing your short story.

2. **Run the Application**

   ```bash
   python main.py --input path_to_your_story.txt
   ```

   Replace `path_to_your_story.txt` with the actual path to your story file.

3. **Output**

   The generated animated video will be saved in the `output/` directory.

## 🧪 Testing

To run the test pipeline:

```bash
python test_pipeline.py
```

This will execute a series of tests to ensure each module functions correctly.

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request. For major changes, open an issue first to discuss what you would like to change.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
