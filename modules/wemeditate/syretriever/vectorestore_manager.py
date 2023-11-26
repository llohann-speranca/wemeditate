from typing import Tuple
from langchain.schema import Document
from autoscraper import AutoScraper
import pandas as pd
from wemeditate.constants import MEDITATIONS_CSV_PATH, MEDITATION_INDEX_PATH
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings


def parse_search_result(search_result: Tuple[Document, float]) -> (str, float):
    doc, score = search_result
    data_url = doc.metadata['data_url']
    index = doc.metadata['index']
    return data_url, index, score


def scrap_meditations():
    model_url = 'https://media.sydevelopers.com/meditations/70/edit'

    # We can add one or multiple candidates here.
    # You can also put urls here to retrieve urls.
    wanted_list = ['Morning meditation', 'general, happy, relaxed, content, morning, morning-general',
                   "https://media.sydevelopers.com/meditations/c798b19f1c.json"]
    scraper = AutoScraper()
    result = scraper.build(model_url, wanted_list)
    print(result)

    # Retrieving exact information
    meditations_data = pd.DataFrame(columns=['title', 'tags', 'data_url'])
    for i in range(250):
        url = f'https://media.sydevelopers.com/meditations/{i}/edit'
        result = scraper.get_result_exact(url)
        if len(result) == 3:
            meditations_data.loc[i] = result
        else:
            print(f'{url}\n{result}')

    # Saving the loot
    meditations_data.reset_index().to_csv(MEDITATIONS_CSV_PATH, index=False)
    return meditations_data


# TODO: Scrap and create vectorestore
def scrap_and_create_vectorestore():
    loader = CSVLoader(file_path=MEDITATIONS_CSV_PATH, metadata_columns=['index', 'data_url'])
    data = loader.load()

    embeddings = OpenAIEmbeddings()

    db = FAISS.from_documents(data, embedding=embeddings)
    db.save_local(MEDITATION_INDEX_PATH)
