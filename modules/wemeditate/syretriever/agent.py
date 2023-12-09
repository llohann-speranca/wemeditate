from wemeditate.syretriever import load_index_database, get_search_results

class Agent:
    def __init__(self,
                 meditation_database = None,
                 ):
        if meditation_database is None:
            meditation_database = load_index_database()
        self.database = meditation_database

    def __call__(self, query, k):
        return self._get_search_results(query, k)

    def _get_search_results(self, query, k):
        return get_search_results(query, self.database, k)
