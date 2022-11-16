import os
import meilisearch as meilisearch

from indexers.IndexDriver import IndexDriver


class Meilisearch(IndexDriver):
    def __init__(self):
        super().__init__()
        master_key = os.getenv("MEILISEARCH_MASTER_KEY")
        meilisearch_url = os.getenv("MEILISEARCH_URL")
        self.client = meilisearch.Client(meilisearch_url, master_key)

    def search(self, index_name, query):
        index = self.client.index(index_name)
        return index.search(query)

    def index(self, index_name, uuid, data, word_cloud):
        index = self.client.index(index_name)
        print(word_cloud)
        index.add_documents([{
            'id': uuid,
            'search_data': data,
            'word_cloud': word_cloud
        }])
        return True
