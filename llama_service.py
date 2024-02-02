import os
from llama_index import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)
os.environ['OPENAI_API_KEY'] = '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'
PERSIST_DIR = "./storage"
index = None

def initialize_index():
    global index
    if not os.path.exists(PERSIST_DIR):
        documents = SimpleDirectoryReader("data").load_data()
        index = VectorStoreIndex.from_documents(documents)
        index.storage_context.persist(persist_dir=PERSIST_DIR)
    else:
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        index = load_index_from_storage(storage_context)

# initialize_index()
def search_for_long_term_memory(message):
    global index
    if index is None:
        initialize_index()
    query_engine = index.as_query_engine()
    return str(query_engine.query(message))

# print(search_for_long_term_memory("你知道奶奶要干嘛吗？"))