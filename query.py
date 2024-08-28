import glob
import os

from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI

from history import History

openai_client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
openai_embeddings = OpenAIEmbeddings()


def read_pages(folder):
    pages = []
    paths = os.path.join(folder, "*.txt")
    for path in glob.glob(paths):
        loader = TextLoader(path, encoding="utf-8")
        pages.extend(loader.load_and_split())
    return pages


def query_dataset(path: str, query: str, k: int):

    # read pages of dataset
    pages = read_pages(path)
    print(len(pages))
    # find top 10 most similar passages for query
    new_db = FAISS.from_documents(pages, openai_embeddings)
    documents = new_db.similarity_search(query, k=k)

    # load documents into a history and using LLM to get answer to query
    history = History()
    for document in documents:
        print(document.page_content)
        history.system(document.page_content)

    history.user(query)

    answer = llm_chat(history)
    return answer


def llm_chat(message_log: History, model_name: str = "gpt-4o-mini"):
    # Use OpenAI's ChatCompletion API to get the chatbot's response
    response = openai_client.chat.completions.create(
        model=model_name,  # The name of the OpenAI chatbot model to use
        messages=message_log.logs,   # The conversation history up to this point, as a list of dictionaries
        max_tokens=1000,        # The maximum number of tokens (words or subwords) in the generated response
        stop=None,              # The stopping sequence for the generated response, if any (not used here)
        temperature=0.0,        # The "creativity" of the generated response (higher temperature = more creative)
    )

    # Find the first response from the chatbot that has text in it (some responses may not have text)
    for choice in response.choices:
        if "text" in choice:
            return choice.text

    # If no response with text is found, return the first response's content (which may be empty)
    return response.choices[0].message.content
