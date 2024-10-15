from Engine.control_chain import Control_Chain

if __name__ == "__main__":
    print("Ejecutando")
#    chroma = bd_chroma()
#    chroma.setColeccion("db_normatividad")
#    if chroma.coleccion.count() == 0:
#        chroma.insert("./Engine/BD/Chroma/Data/acuerdos.json")

    cc = Control_Chain()
    pregunta = input("Digite su peregunta aqui: ")
    respuesta = cc(question=pregunta,history="")

    