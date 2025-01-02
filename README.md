# IAtitus: Inteligência Artificial para Uso Acadêmico

IAtitus é uma aplicação voltada para o uso acadêmico, permitindo que professores cadastrem materiais didáticos e alunos interajam com a IA para realizar perguntas e gerar podcasts educacionais com base no conteúdo disponibilizado.

---

## Funcionalidades Principais

### Chatbot
- Alunos podem realizar perguntas à IA, que responde com base nos materiais cadastrados pelos professores.

### Geração de Podcasts
- Professores selecionam materiais e configuram um podcast educacional, que é gerado automaticamente e pode ser reproduzido no sistema.

### Cadastro de Materiais
- Professores podem fazer upload de documentos PDF, que são armazenados no banco de dados e utilizados para responder perguntas ou gerar podcasts.

---

## Estrutura do Projeto

### Diretórios e Arquivos

- **blueprints/**: Contém os módulos organizados por funcionalidade, cada um com seus templates HTML:
  - **chat/**: Controle de interações gerais.
  - **chatbot/**: Módulo do chatbot para perguntas e respostas.
  - **home/**: Página inicial.
  - **login/**: Módulo de autenticação.
  - **newdocument/**: Controle para upload de novos documentos.
  - **podcast/**: Geração e reprodução de podcasts.

- **data/**:
  - **audio/**: Diretório para arquivos de áudio gerados.
  - **transcripts/**: Diretório para transcrições e outros arquivos auxiliares.

- **DataBase/**:
  - **DBBuilder.py**: Script para criação e configuração do banco de dados.

- **static/**:
  - **staticTempFiles/**: Diretório temporário para armazenamento de arquivos estáticos.

- **config.py**:
  - Contém configurações globais, como chaves de API e funções utilitárias para manipulação de PDFs e chamadas de IA.

- **app.py**:
  - Arquivo principal que inicializa o servidor Flask e registra os Blueprints.

---

## Requisitos de Instalação

### 1. Dependências

Certifique-se de ter o **Python 3.8+** instalado.  
Instale as bibliotecas necessárias com o comando:

```bash
pip install flask python-dotenv PyPDF2 sqlite3 shutil podcastfy-client
```

### 2. Configuração do Ambiente

#### Configurar as Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```makefile
GPT_API_KEY=<sua-chave-gpt>
GEMINI_API_KEY=<sua-chave-gemini>
ELEVENLABS_API_KEY=<sua-chave-elevenlabs>
```

#### Baixar e Configurar o FFMPEG

Faça o download do **FFMPEG** (no site: https://www.ffmpeg.org/download.html) e adicione o executável ao PATH do sistema.

### 3. Inicialização do Banco de Dados

Execute o script `DBBuilder.py` para criar e popular o banco de dados inicial:

```bash
python DataBase/DBBuilder.py
```

---

## Como Usar

### Iniciar o Servidor

Execute o arquivo principal para iniciar a aplicação:

```bash
python app.py
```

### Funcionalidades Disponíveis

1. **Login**: Faça login para acessar os recursos.  
2. **Cadastro de Materiais**: Adicione documentos PDF para consulta.  
3. **Chatbot**: Pergunte à IA com base nos materiais cadastrados.  
4. **Podcasts**: Selecione materiais e configure a geração de podcasts.

---

## Estrutura de Banco de Dados

Tabelas principais:
- **TBCadeira**: Cadeiras/disciplinas cadastradas.
- **TBArquivo**: Materiais associados a cada cadeira.
- **TBAluno** e **TBCadAlu**: Controle de usuários e seus relacionamentos com as disciplinas.

---

## Agradecimentos

Este projeto foi possível graças ao uso de APIs de inteligência artificial, como **GPT**, **GEMINI** e **Eleven Labs**, além de ferramentas de código aberto.
