class AssessPatentCollection:
    def __init__(self, patent_collection, patent_collection_script):
        self.patent_collection = patent_collection
        self.patent_collection_script = patent_collection_script

    def __eq__(self, other):
        return self.patent_collection == other.patent_collection and self.patent_collection_script == other.patent_collection_script

    def __hash__(self):
        return hash((self.patent_collection, self.patent_collection_script))

    def __repr__(self):
        return f'AssessPatentCollectionScript(patent_collection={self.patent_collection}, patent_collection_script={self.patent_collection_script})'