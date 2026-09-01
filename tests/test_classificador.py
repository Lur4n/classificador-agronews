import sys
from pathlib import Path

# Adiciona a pasta pai (raiz do projeto) ao caminho de buscas do Python
sys.path.append(str(Path(__file__).resolve().parent.parent))

from classificador_agronews.classificador import ClassificadorAgronews
from classificador_agronews.models import NoticiaInput

def main():
  print("Iniciando o teste local do classificador Agronews...\n")
  
  # Instanciando o classificador(ele já pega a chave da api no env automaticamente)
  classificador = ClassificadorAgronews()
  
  # Criando dados de noticia de exemplo usando o schema NoticiaInput
  noticia_teste = NoticiaInput(
    id = 1,
    titulo = "Preço do milho recua no Sul após avanço da colheita",
    conteudo=(
      "O mercado interno de milho resgitrou ligeira queda nos preços nesta semana "
      "no Paraná e em Santa Catarina. A maior oferta gerada pela colheita de safra "
      "pressionou as cotações, equanto os compradores trabalham abastecidos."
    ) 
  )
  
  # Lista de categorias esperadas na classificação
  categorias_esperadas = ["Milho", "Soja", "Café", "Bovino"]
  
  print(f"Enviando a noticia para análise:\n - Manchete: {noticia_teste.titulo}\n")

  # Classificando a noticia_teste
  
  resultado = classificador.classificar(
    noticia=noticia_teste,
    categorias_validas=categorias_esperadas
  )
  
  # Imprimindo resultados validados
  print(40*"=")
  print("RESULTADO DA CLASSIFICAÇÃO")
  print(40*"=")
  print(f"Categoria Principal identificada: {resultado.categoria_principal}")
  
  if resultado.resumo_curto:
    print(f"Resumo: {resultado.resumo_curto}")
  
  print("\n Distribuição de Probabilidade")
  for i in resultado.distribuicao:
    print(f" - {i.nome}: {i.percentual:.1f}%")

if __name__ == "__main__":
  main()
  