import os
import meilisearch as meilisearch

from indexers.IndexDriver import IndexDriver


class Meilisearch(IndexDriver):
    def __init__(self):
        super().__init__()
        master_key = os.getenv("MEILISEARCH_KEY")
        meilisearch_url = os.getenv("MEILISEARCH_HOST")
        self.client = meilisearch.Client(meilisearch_url, master_key)


    def search(self, index_name, query = ""):
        index = self.client.index(index_name)
        return index.search(query)

    def index(self, index_name, uuid, data, word_cloud, title, author):
        index = self.client.index(index_name)
        index.add_documents([{
            'id': uuid,
            'search_data': data,
            'word_cloud': word_cloud,
            'title': title,
            'author': author
        }])
        return True
