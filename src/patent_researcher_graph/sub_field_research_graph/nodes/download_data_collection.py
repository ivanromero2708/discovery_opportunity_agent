class DownloadDataCollection:
    def __init__(self):
        pass

    def run(self, state, config=None) -> dict:
        # Return an empty list for patent_documents.
        return {"patent_documents": []}
