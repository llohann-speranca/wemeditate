from typing import List, Union

from wemeditate.constants import MEDITATION_INDEX_PATH, SEARCH_RESULT_LOG_PATH, K, QUERY_PREFIX
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from wemeditate.syretriever.vectorestore_manager import parse_search_result
from csv import DictWriter


# TODO: Change the path to a config file
def load_index_database():
    """Return the FAISS database with the meditation descriptions.
    Load from the MEDITATION_INDEX_PATH in wemeditate/constants.py"""
    embeddings = OpenAIEmbeddings()
    meditation_faiss_database = FAISS.load_local(MEDITATION_INDEX_PATH, embeddings)
    return meditation_faiss_database


def get_search_results(query: str,
                       database: FAISS):
    query_extended = '\n'.join([QUERY_PREFIX, query])
    search_results = database.similarity_search_with_score(query_extended, k=K)
    data_urls = []
    to_log = []
    for result in [parse_search_result(r) for r in search_results]:
        data_url, index, score = result
        data_urls.append(data_url)
        to_log.extend([index, score])

    log_search_result(query_extended, to_log)

    return data_urls


def log_search_result(query_extended: str,
                      to_log: List[Union[int, float]]):
    field_names = ['query_extended'] + sum([[f'result_{i}', f'score_{i}'] for i in range(1, K+1)], [])
    row_dict = {'query_extended': query_extended}
    row_dict.update({key: value for key, value in zip(field_names[1:], to_log)})

    # Open CSV file in append mode
    with open(SEARCH_RESULT_LOG_PATH, 'a', newline='') as f_object:
        dict_writer_object = DictWriter(f_object, fieldnames=field_names)
        dict_writer_object.writerow(row_dict)
