
# AI Agents

A Framework for Language Model-Powered Applications LangChain is a framework designed for building applications powered by language models. It provides a standard interface for chains, integrates with various tools, and offers end-to-end chains for common applications. The two main features of LangChain are data-awareness and agentic behavior.

Data-awareness enables the language model to connect to other sources of data, while agentic behavior allows the model to interact with its environment. By using agents, LangChain can dynamically decide which tools to call based on user input. This makes agents extremely powerful when used correctly.

## How it works

The application uses Streamlit to create the GUI and Langchain to deal with the LLM.

The PDF demo reads the PDF and splits the text into smaller chunks that can be then fed into a LLM. It uses OpenAI embeddings to create vector representations of the chunks. The application then finds the chunks that are semantically similar to the question that the user asked and feeds those chunks to the LLM to generate a response.

The SQL Database Agent enable users to query databases using natural language. The SQL Database Agent is designed to interact with SQL databases, allowing users to ask questions in natural language and receive answers.
We explored the capabilities of LangChain, SQL Agents, and OpenAI LLMs for natural language database querying. By combining these technologies, we can create powerful applications that allow users to interact with databases using natural language, making data retrieval more efficient and intuitive. 

## Installation

To install the application, please clone this repository and create MakeEnv.mk file
that copy from MakeEnv.example and install the requirements:
```
make install
```

You also need to create .env file that copy from .env.example, then update it.
- OPENAI_API_KEY OpenAI API key
- SERPAPI_API_KEY SerpAPI key
- DATABASE Mysql connection uri

You also install MySQL instance with docker.
```
make docker-network
make mysql-run
```

## Usage

To use the application, run the Home.py file with the streamlit CLI (after having installed streamlit):
```
streamlit run Home.py
```

## Contributing

This project is for demonstration purposes only and is not intended to receive further contributions. It is supposed to be used as support material for Upwork that shows how to build the project.

## Link

- [MySQL Sample Database](https://www.mysqltutorial.org/mysql-sample-database.aspx)
- [ChatGPT for PDF files with LangChain](https://levelup.gitconnected.com/chatgpt-for-pdf-files-with-langchain-ef565c041796)