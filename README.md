# Classificador — Agronews

Módulo stateless em Python projetado para classificar notícias do agronegócio e gerar resumos curtos utilizando a API do **Google Gemini** e validação de schemas com **Pydantic**.

Desenvolvido para atuar como um microserviço/pacote independente, permitindo integração direta com outros projetos (como pipelines de scrapers ou aplicações Django).

---

## Tecnologias Utilizadas

- **Python 3.10+**
- **Google GenAI SDK** (`google-genai`)
- **Pydantic v2** (Validação e garantia da estrutura de saída)
- **python-dotenv** (Gerenciamento de variáveis de ambiente)


## Pré-requisitos

1. Python 3.10 ou superior instalado.
2. Uma chave de API do **Google Gemini** (gratuita via [Google AI Studio](https://aistudio.google.com/)).

## Configuração do Ambiente Local

### 1. Clonar o repositório e acessar a pasta

```bash
git clone [https://github.com/Lur4n/classificador-agronews.git](https://github.com/Lur4n/classificador-agronews)

cd classificador-agronews
```

### 2. Criar o Ambiente  Virtual (Windows)
```bash
python -m venv venv
```
#### Ativar o Ambiente  Virtual (Windows)
```
.\venv\Scripts\Activate.ps1
```

### 3. Instalar as Dependências e o Pacote Local
```
python.exe -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

### 4. Configurar as Variáveis de Ambiente
Copie o  arquivo de exemplo:
```bash
cp .env.example .env
```
Edite o arquivo .env e adicione sua chave da API:
```bash
GEMINI_API_KEY="ADICIONE SUA CHAVE DA API DO GEMINI AQUI"
```

### 5. Testando Localmente
Para validar o funcionamento sem depender de banco de dados ou outras aplicações:
```bash
python tests/test_classificador.py
```

## Estrutura do Projeto
```bash
classificador-agronews/
├── models.py                 # Schemas Pydantic (NoticiaInput, ClassificacaoResultado)
├── classificador.py          # Cliente do Gemini e lógica de classificação
├── pyproject.toml            # Configuração de empacotamento da biblioteca
├── requirements.txt          # Lista de dependências do ambiente
├── .env.example              # Modelo de configuração das variáveis
├── .gitignore                # Arquivos ignorados pelo Git
└── tests/
    └── test_classificador.py # Script de teste de integração
```
## Empacotamento com pyproject.toml
O arquivo **pyproject.toml** na raiz transforma este repositório em um pacote Python válido. Ele define o nome da biblioteca (`classificador-agronews`), a versão e as dependências necessárias para distribuição e instalação via pip.

## Como Testar a Biblioteca no Seu Projeto Django (`web-agronews`)
*Por ser stateless (sem banco de dados próprio), este módulo pode ser instalado diretamente no ambiente virtual de outros projetos, como o **web-agronews**.*

### 1. Instalação no web-agronews
Para testar a integração da biblioteca em um ambiente Django real sem afetar o banco de dados, você pode criar um **Management Command** personalizado.

No terminal do seu projeto Django `web-agronews`, com o ambiente virtual ativado, instale o pacote em modo editável  (-e):

Com o ambiente virtual do web-agronews ativado, instale o pacote localmente em modo editável (-e):
```bash
pip install -e /caminho/para/classificador-agronews
```


### 2. Criar Estrutura de Pastas
Dentro da app onde ficará a lógica (ex: noticias), crie a pasta management/commands com os arquivos `__init__.py`:
```
New-Item -ItemType Directory -Path "noticias\management\commands" -Force
New-Item -ItemType File -Path "noticias\management\__init__.py" -Force
New-Item -ItemType File -Path "noticias\management\commands\__init__.py" -Force
```
### 3. Adicionar a API Key no .env do web-agronews
No arquivo .env do web-agronews, declare a chave da API do Gemini:
```
GEMINI_API_KEY="sua_chave_do_google_ai_studio_aqui"
```

### 4. Criar o Script de Teste
Crie o arquivo test_classificacao.py no caminho noticias/management/commands/test_classificacao.py e adicione o seguinte conteúdo:
```
from django.core.management.base import BaseCommand
from classificador_agronews.classificador import ClassificadorAgronews
from classificador_agronews.models import NoticiaInput


class Command(BaseCommand):
  help = "Executa um teste local do classificador Agronews com dados estáticos."

  def handle(self, *args, **options):
    self.stdout.write(self.style.SUCCESS("Iniciando o teste local do classificador Agronews...\n"))

    # Instancia o classificador (requer GEMINI_API_KEY no arquivo .env)
    classificador = ClassificadorAgronews()

    # Dados de notícia estáticos para teste
    noticia_teste = NoticiaInput(
        id=1,
        titulo="Preço do milho recua no Sul após avanço da colheita",
        conteudo=(
            "O mercado interno de milho registrou ligeira queda nos preços nesta semana "
            "no Paraná e em Santa Catarina. A maior oferta gerada pela colheita de safra "
            "pressionou as cotações, enquanto os compradores trabalham abastecidos."
        )
    )

    categorias_esperadas = ["Milho", "Soja", "Café", "Bovino"]

    self.stdout.write(f"Enviando a notícia para análise:\n - Manchete: {noticia_teste.titulo}\n")

    # Processamento via Gemini API
    resultado = classificador.classificar(
        noticia=noticia_teste,
        categorias_validas=categorias_esperadas
    )

    # Exibição do resultado no terminal
    self.stdout.write("=" * 40)
    self.stdout.write("RESULTADO DA CLASSIFICAÇÃO")
    self.stdout.write("=" * 40)
    self.stdout.write(f"Categoria Principal identificada: {resultado.categoria_principal}")

    if resultado.resumo_curto:
        self.stdout.write(f"Resumo: {resultado.resumo_curto}")

    self.stdout.write("\nDistribuição de Probabilidade:")
    for i in resultado.distribuicao:
        self.stdout.write(f" - {i.nome}: {i.percentual:.1f}%")
```


### 5. Executar o comando
Garantindo que a variável GEMINI_API_KEY esteja definida no seu arquivo .env, rode no terminal:
```
python manage.py test_classificador
```

## Autores

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/ciniro">
        <img
          src="https://github.com/ciniro.png"
          width="100px"
          alt="Foto de perfil de Ciniro Nametala"
        /><br>
        <sub><b>Dr. Ciniro Nametala</b></sub>
      </a>
      <br>
      <sub>Professor responsável</sub>
    </td>
    <td align="center">
        <a href="https://github.com/Lur4n">
            <img src="https://github.com/Lur4n.png" width="100px"/>
            <br>
            <sub><b>Luan Carlos dos Santos</b></sub>
        </a>
        <br>
        <sub>Pesquisador / Desenvolvedor</sub>
    </td>
  </tr>
</table>
