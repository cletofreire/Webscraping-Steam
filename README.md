
# SteamDB Data Extraction and Automation

Este projeto tem como objetivo extrair o máximo possível de dados do site [SteamDB Sales](https://steamdb.info/sales/) e automatizar a exportação desses dados para uma tabela no Google BigQuery.





## Stack utilizada

**Linguagem:** Python.

**Bibliotecas:** pandas-gbq, google-auth, beautifulsoup4, selenium, pandas, python-dotenv, logging, os. 

**Ferramentas:** Google Cloud Platform, Google BigQuery.




## Funcionalidades

- Extração de Dados: Coleta de dados de vendas do site SteamDB usando beautifulsoup4 e selenium.

- Transformação de Dados: Processamento e limpeza dos dados usando pandas.

- Carregamento de Dados: Automação da exportação dos dados para o Google BigQuery usando pandas-gbq.

## Variáveis de Ambiente

Para rodar esse projeto, você vai precisar adicionar as seguintes variáveis de ambiente no seu .env. **Importante configurar as credenciais no Google BigQuery.**

`GOOGLE_APPLICATION_CREDENTIALS`=path/to/your-service-account-file.json

`BIGQUERY_PROJECT_ID`=your-bigquery-project-id

`BIGQUERY_TABLE`=your-bigquery-table


## Rodando localmente

Este projeto utiliza ambientel virtual [(VENV)](https://docs.python.org/3/library/venv.html)

Clone o projeto

```bash
git clone https://github.com/cletofreire/Desafio-BeAnalytic.git
```

Entre no diretório do projeto

```bash
cd Desafio-BeAnalytic
```

Abra o terminal e instale as dependências

```bash
pip install -r requirements.txt
```

Rode o script

```bash
python main.py
```


## Autores

- [@ocletofreire](https://github.com/cletofreire)

