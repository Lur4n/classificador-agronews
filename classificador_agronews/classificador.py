# classificador.py
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from .models import ClassificacaoResultado, NoticiaInput

# Carrega as variáveis do .env assim que o módulo é importado
load_dotenv()

#servico de classificacao
class ClassificadorAgronews:

  def __init__(self, api_key: str = None):
    # Pega a chave do parâmetro ou busca no .env
    self.api_key = api_key or os.getenv("GEMINI_API_KEY")

    if not self.api_key:
        raise ValueError(
            "A chave GEMINI_API_KEY não foi encontrada no arquivo .env nem fornecida no __init__."
        )

    # Inicializa o cliente oficial do Gemini
    self.client = genai.Client(api_key=self.api_key)

  def classificar( self, noticia: NoticiaInput, categorias_validas: list[str] = None ) -> ClassificacaoResultado:
    prompt = f"Analise a seguinte notícia do agronegócio e classifique-a:\n\nTítulo: {noticia.titulo}\nConteúdo: {noticia.conteudo}"

    if categorias_validas:
        prompt += f"\n\nCategorias permitidas para escolha: {', '.join(categorias_validas)}"

    # Chamada estruturada ao Gemini
    response = self.client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ClassificacaoResultado,  # Força o schema Pydantic
            temperature=0.1,
        ),
    )

    # Valida o JSON de retorno e converte de volta para o objeto Pydantic
    return ClassificacaoResultado.model_validate_json(response.text)