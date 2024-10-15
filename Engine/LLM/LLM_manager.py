from ctransformers import AutoModelForCausalLM
from ctransformers import Config, AutoConfig

class LLM_Manager:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LLM_Manager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            config=Config(
                    temperature=0.3,
                    gpu_layers=50,
                    context_length=2040,
                    repetition_penalty=1.0,
                    stream=True
                )
            self.conf = AutoConfig(config)
            self.load_model()
            self._initialized = True

    def load_model(self):
        self.llm = AutoModelForCausalLM.from_pretrained(
            model_path_or_repo_id="./Engine/LLM/Llama-2/llama-2-7b-chat_Q4_K_M.gguf", 
            model_type="llama",
            config=self.conf, 
            lib="avx2", 
            local_files_only=True
        )
    
    def get_config(self):
        return self.conf
    
    def set_config(self, context_length: int):
        config=Config(
                temperature=0.3,
                gpu_layers=50,
                context_length=context_length,
                repetition_penalty=1.0,
                stream=True
            )
        self.conf = AutoConfig(config)
        self.load_model()

    def ask(self, prompt:str):
        response = ""
        result = self.llm(prompt=prompt)
        for r in result:
            response = r
            yield response
