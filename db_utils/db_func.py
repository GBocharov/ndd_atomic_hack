from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import DirectoryLoader, TextLoader
import pprint as pp
import chromadb
from db_utils import model
from text_utils.prepare_text import prepare_text_for_db
from file_proccesing.file_transform import trans_file

def create_db(persist_directory  : str = 'vdb_langchain_doc_small', file_directory : str = 'data'):
    loader = DirectoryLoader(file_directory, glob = "./*.txt")
    docs = loader.load()

    # text preapare
    for doc in docs:
        doc.page_content = prepare_text_for_db(doc.page_content)

   #embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")


    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 350, chunk_overlap = 30)
    texts = text_splitter.split_documents(docs)

    for text in texts:
        text.page_content = text.page_content.replace(r'\n', ' ')

    ids = [str(i) for i in range(1, len(texts)+ 1) ]
    vectordb = Chroma.from_documents(
                                    documents = texts,
                                    embedding = model,
                                    ids = ids
                                    ,persist_directory = persist_directory

                                     )
    return vectordb

def print_db(vectordb):
    data = vectordb._collection.get(include = ['documents'])
    print('DB_size -> ', len(data['documents']))

def get_db(persist_directory  : str = 'vdb_langchain_doc_small'):
    vectordb = Chroma(persist_directory=persist_directory, embedding_function=model)
    return vectordb

def get_db_response(query, db):
    docs = db.similarity_search_with_score(query, k = 8)
    return docs

def add_file_to_db(vectordb , file_path : str = "3.txt"):

    file_path = trans_file(file_path)

    if file_path == 0:
        print('Неподдерживаемый формат файла')
        return

    loader = TextLoader(file_path, encoding='utf-8')

    docs = loader.load()

    for doc in docs:
        doc.page_content = prepare_text_for_db(doc.page_content)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 300, chunk_overlap = 20)
    texts = text_splitter.split_documents(docs)

    for text in texts:
        text.page_content = text.page_content.replace(r'\n', ' ')

    last_ids = int(vectordb._collection.get()['ids'][-1])+1

    new_ids = [str(i) for i in range(last_ids , len(texts) + last_ids + 1) ]
    print('База успешно обновлена')
    print_db(vectordb)
    vectordb.add_documents(documents = docs, ids = new_ids)


