# Writer Murakami

A multi-agent AI system that analyzes Haruki Murakami's literary works and generates responses in his distinctive style using advanced RAG (Retrieval Augmented Generation) techniques.

![Murakami Style](https://i.imgur.com/JQIndFf.png)

## Overview

Writer Murakami uses a distributed agent architecture to analyze PDF documents containing Murakami's works and generate text in his distinctive literary voice. Whether you're seeking inspiration, exploring creative writing styles, or simply appreciating the unique characteristics of Murakami's prose, this system offers an AI-powered lens into his fictional world.

## Features

- **Text Analysis**: Extract and process content from Murakami's works
- **Style Emulation**: Generate text in Murakami's distinctive voice
- **Interactive Interface**: Engage with the system through a command-line interface
- **Multi-agent Architecture**: Distributed processing across specialized agents
- **RAG Technology**: Ground AI responses in actual Murakami text

## Installation

### Prerequisites

- Python 3.9+
- OpenAI API key

### Setup

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/writer-murakami.git
   cd writer-murakami
   ```

2. Install dependencies:
   ```
   pip install uagents langchain-community langchain-openai faiss-cpu
   ```

3. Set your OpenAI API key:
   ```
   export OPENAI_API_KEY=your_api_key_here
   ```

## Usage

1. Start the PDF Agent:
   ```
   python PDFAgent.py
   ```

2. In a new terminal, start the RAG Agent:
   ```
   python RagAgent.py
   ```

3. In a third terminal, start the User Agent:
   ```
   python UserAgent.py
   ```

4. Interact with the system through the User Agent terminal:
   - Enter the path to a PDF containing Murakami's work (or use the default)
   - Ask questions or request story generation
   - Receive responses in Murakami's style

## Example Prompts

- "What themes are present in Norwegian Wood?"
- "Write a 500-word story about a mysterious cat"
- "Describe a rainy Tokyo evening in Murakami's style"
- "What is the significance of wells in Murakami's work?"

## Architecture

The system consists of three specialized agents:

1. **User Agent (`UserAgent.py`)**: Handles user interaction, collecting questions and document references, then displaying the generated Murakami-style responses

2. **PDF Agent (`PDFAgent.py`)**: Processes PDF documents of Murakami's works, extracting and organizing content for analysis

3. **RAG Agent (`RagAgent.py`)**: Implements Retrieval Augmented Generation (RAG) to:
   - Create vector embeddings of Murakami's text
   - Find relevant passages using FAISS similarity search
   - Generate responses with LLMs guided by carefully crafted prompts

## Project Story

### Inspiration

Our project was born from a deep appreciation for Haruki Murakami's distinctive literary voice. His blend of the mundane and the surreal, his simple yet profound observations, and his ability to create dreamlike narratives have captivated readers worldwide. We wondered if artificial intelligence could learn to mimic this unique style - not to replace the irreplaceable, but to understand what makes his writing so compelling and to explore the boundaries of AI-generated creative content. Can technology capture the essence of an author whose work often explores the liminal spaces between reality and dreams?

### What it does

Writer Murakami is a multi-agent AI system that analyzes Haruki Murakami's literary works and generates responses in his distinctive style. Users can ask questions or request stories, and the system draws from Murakami's texts to craft responses that mirror his thematic preoccupations, sentence structures, and imagery. Whether generating short reflections or longer narratives, Writer Murakami attempts to capture the essence of the author's voice - from his references to Western music and mysterious cats to his matter-of-fact descriptions of the surreal and his characteristic melancholic tone.

### How we built it

We designed a distributed system using the uAgents framework with three specialized agents working in concert:

1. **User Agent**: Handles user interaction, collecting questions and document references, then displaying the generated Murakami-style responses
2. **PDF Agent**: Processes PDF documents of Murakami's works, extracting and organizing content for analysis
3. **RAG Agent**: The core of our system, implementing Retrieval Augmented Generation (RAG) to:
   - Create vector embeddings of Murakami's text using OpenAI's embedding model
   - Find relevant passages using FAISS similarity search
   - Generate responses with ChatGPT guided by carefully crafted prompts that encode Murakami's stylistic elements

The agents communicate asynchronously, passing structured messages to coordinate the analysis and generation process. We used LangChain to manage the AI components and designed detailed prompts to guide the model toward Murakami's distinctive voice.

### Challenges we ran into

We encountered several significant challenges:

1. **Agent Communication**: Establishing reliable message passing between our distributed agents proved tricky, requiring careful state management and timeout handling
2. **Capturing Murakami's Voice**: Distilling the essence of Murakami's style into actionable prompts that could guide the LLM was an iterative process of refinement
3. **Technical Issues**: We faced deprecation warnings in LangChain's API that required updates to our code
4. **Balancing Creativity and Accuracy**: Finding the right model temperature setting to balance creative expression with faithfulness to Murakami's style
5. **Response Handling**: Managing the transition from traditional LLM chains to the newer, more efficient runnable sequences paradigm

### Accomplishments that we're proud of

Despite the challenges, we're particularly proud of:

1. Creating a detailed, structured prompt that effectively guides the AI to emulate Murakami's distinctive voice
2. Building a responsive multi-agent system where each component handles a specific aspect of the process
3. Successfully implementing modern RAG techniques to ground the AI's responses in authentic Murakami content
4. Developing a robust error handling and retry mechanism that increases system reliability
5. Creating an interactive experience that allows users to explore Murakami's style through their own questions and requests

### What we learned

This project taught us valuable lessons about:

1. The nuances of literary style and how to encode these qualities in AI systems
2. Building distributed, asynchronous agent-based architectures
3. The power of RAG for grounding AI-generated content in specific knowledge domains
4. Techniques for prompt engineering to guide AI behavior toward specific stylistic outcomes
5. The challenges of maintaining state across distributed components
6. How to balance adherence to source material with creative generation

### What's next for Writer Murakami

We see several exciting directions for the future:

1. **Expanded Corpus**: Incorporating more of Murakami's works to create a more comprehensive stylistic understanding
2. **Web Interface**: Developing a user-friendly web application to make the system accessible beyond the command line
3. **Style Parameters**: Allowing users to adjust aspects of the Murakami style simulation (more surreal, more nostalgic, etc.)
4. **Multi-modal Generation**: Adding the ability to generate Murakami-inspired images alongside text
5. **Contextual Memory**: Implementing conversation history to create more coherent extended interactions
6. **Comparative Analysis**: Adding other author styles to allow users to compare different literary voices
7. **Fine-tuning**: Training a specialized model on Murakami's works for even more accurate style emulation

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Haruki Murakami for his inspiring literary works
- The uAgents framework for enabling multi-agent applications
- LangChain for providing powerful AI integration tools
