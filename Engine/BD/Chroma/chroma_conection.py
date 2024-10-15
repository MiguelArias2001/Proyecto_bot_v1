import chromadb
from Engine.Utils.embeddings import embeddings
import Engine.Utils.lector_JSON as lector

class bd_chroma:

    def __init__(self):
        self._cliente = chromadb.PersistentClient(path="./Engine/BD/Chroma/Collections")
        self.coleccion = None
        self.embeddings = embeddings()

    def getColleccion(self, name:str):
        self.coleccion = self._cliente.get_collection(name=name)
        return self.coleccion
    
    def setColeccion(self, name:str):
        print("Estoy creando la colleccion")
        self.coleccion = self._cliente.get_or_create_collection(name=name, metadata={"hnsw:space": "l2"})
        if self.coleccion == None:
            print("No se creo")

    def insert(self, path:str):
        id, content, meta = lector.extractData(path)
        if(meta!=None and id!=None and content!=None):
            embedding = self.embeddings.getEmbeddings(contenido = content)
            try:
                self.coleccion.add(
                    ids = id,
                    embeddings = embedding,
                    metadatas = meta,
                    documents = content
                )
                cant = self.coleccion.count()
                print(f"Se insertaron '{cant}' datos en la coleccion")
            except ValueError:
                print("Se provoco un error al insertar:"+ValueError)
        else:
            print("No hay datos extraidos del JSON")

    def format_str(self, list:list):
        response = ""
        for l in list:
            response +=  f"* {l}\n"
        return response

    
    def query(self, question:str, results:int):
        embedding = self.embeddings.getEmbeddings(contenido = question.split(" "))
        print(embedding)
        try:
            response = self.coleccion.query(
                query_embeddings = embedding,
                n_results = results,
                include = ["metadatas","documents"]
            )
            documents = self.format_str(response.get("documents")[0])
            metadata = self.format_str(response.get("metadatas")[0])

            return documents, metadata
        except ValueError:
            print("Se presento un error al hacer la consulta: "+str(ValueError))
