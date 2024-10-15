from sentence_transformers import SentenceTransformer

class embeddings:
    model: SentenceTransformer

    def __init__(self):
        self.model = SentenceTransformer(model_name_or_path='paraphrase-multilingual-MiniLM-L12-v2',cache_folder='/Model')
    
    def getEmbeddings(self,contenido:str|list[str]):
        embeded = self.model.encode(sentences=contenido,normalize_embeddings=True)
        return embeded.tolist()