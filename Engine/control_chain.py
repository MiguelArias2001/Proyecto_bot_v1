from Engine.LLM.LLM_manager import LLM_Manager
from Engine.Utils.prompt_templates import prompt_control_contexto_valido, prompt_control_generar_respuesta, prompt_control_historial, prompt_control_mensaje_salida, prompt_control_pregunta_valida, prompt_control_respuesta_invalida
from Engine.BD.Chroma.chroma_conection import bd_chroma

class Control_Chain:
    def __init__(self):
        self.col = bd_chroma()
        self.llm_manager = LLM_Manager()

    def call_llm(self, prompt):
        response = ""
        for part in self.llm_manager.ask(prompt):
            response += part
        return response
    
    def generate_prompt(self, template, **kwargs):
        return template.format(**kwargs)
    
    def pregunta_valida(self, question):
        prompt = self.generate_prompt(prompt_control_pregunta_valida, question=question)
        self.llm_manager.set_config(len(prompt))
        return self.call_llm(prompt)
    
    def contexto_valido(self, question):
        prompt = self.generate_prompt(prompt_control_contexto_valido, question=question)
        self.llm_manager.set_config(len(prompt))
        return self.call_llm(prompt)
    
    def generar_respuesta(self, question, context):
        prompt = self.generate_prompt(prompt_control_generar_respuesta, question=question, context=context)
        self.llm_manager.set_config(len(prompt))
        return self.call_llm(prompt)
    
    def historial_respuesta(self, question, history):
        prompt = self.generate_prompt(prompt_control_historial, question=question, history=history)
        self.llm_manager.set_config(len(prompt))
        return self.call_llm(prompt)
    
    def mensaje_salida(self, question, context, history):
        prompt = self.generate_prompt(prompt_control_mensaje_salida, question=question, context=context, history=history)
        self.llm_manager.set_config(len(prompt))
        return self.call_llm(prompt)

    def respuesta_invalida(self) -> str:
        return prompt_control_respuesta_invalida

    def __call__(*,self, question, history="") -> str:

        collections = {
            "evento": 'db_eventos', 
            "fecha": 'db_fecha',
            "norma": 'db_normatividad'
        }

        # Verificar si la pregunta es válida
        validez = self.pregunta_valida(question).strip().lower()
        if validez != "sí":
            return self.respuesta_invalida()

        # Verificar el contexto de la pregunta
        tipo_contexto = self.contexto_valido(question).strip().lower()
        
        if tipo_contexto in list(collections.keys()):
            # escoge la coleccion que tiene mas sentido en la consulta y extrae la informacion
            self.col.getColleccion(collections[tipo_contexto])
            context, metadata = self.col.query(question=question, results=4)

            # Generar respuesta basada en el contexto
            respuesta = self.generar_respuesta(question, context)
            
            # Generar respuesta basada en el historial
            respuesta_historial = self.historial_respuesta(question, history)
            
            # Generar mensaje de salida final
            mensaje_final = self.mensaje_salida(question, respuesta, respuesta_historial)

            # Se agrega la metadata de la informacion usada en la respuesta
            met = "\nLa informacion para generar la respuesta fue dada de los siguientes documentos: \n"+metadata.__str__()
            return mensaje_final+met
        else:
            # Se devuelve el mensaje de respuesta invalida
            return self.respuesta_invalida()