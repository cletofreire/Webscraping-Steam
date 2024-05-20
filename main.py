from pandas_gbq import to_gbq
from google.oauth2 import service_account
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import pandas as pd
import logging
from dotenv import load_dotenv
import os

load_dotenv()

# Configurando logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Carregando credenciais do BigQuery
credencial = service_account.Credentials.from_service_account_file(
    os.getenv('GOOGLE_APPLICATION_CREDENTIALS'),
    scopes=["https://www.googleapis.com/auth/bigquery"]
)

# Inicializando o navegador (Firefox)
driver = webdriver.Firefox()

try:
    driver.get("https://steamdb.info/sales/")

    # Espera para garantir que a tabela esteja presente
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "DataTables_Table_0")))

    # Função para rolar a página lentamente até que todas as linhas estejam visíveis
    def scroll_down_page(speed=10):
        current_scroll_position, new_height = 0, 1
        while current_scroll_position <= new_height:
            current_scroll_position += speed
            driver.execute_script(
                "window.scrollTo(0, {});".format(current_scroll_position))
            new_height = driver.execute_script(
                "return document.body.scrollHeight")

    # Lista vazia para armazenar os dados dos jogos
    games = []

    # Função para extrair dados de uma página da tabela
    def extract_data_from_page(soup):
        table = soup.find(id="DataTables_Table_0")
        rows = table.find_all("tr", class_="app")

        for row in rows:
            data_cells = row.find_all("td")

            game_data = {
                "Name": data_cells[2].find("a").text.strip(),
                "Discount_percentage": data_cells[3].text.strip(),
                "Price": data_cells[4].text.strip(),
                "Rating": data_cells[5].text.strip(),
                "Release": data_cells[6].text.strip(),
                "Ends": data_cells[7].text.strip(),
                "Started": data_cells[8].text.strip()
            }

            logging.info(game_data)
            games.append(game_data)

    # Extraindo dados de todas as páginas
    while True:
        scroll_down_page()  # Rolando lentamente até que todas as linhas estejam visíveis
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        extract_data_from_page(soup)

        try:
            next_button = driver.find_element(
                By.CSS_SELECTOR, 'button.dt-paging-button.next')
            if next_button.get_attribute('aria-disabled') == 'true':
                break
            next_button.click()
            WebDriverWait(driver, 10).until(EC.staleness_of(next_button))
        except Exception as e:
            logging.error(f"Erro ao navegar: {e}")
            break
finally:
    driver.quit()

# Criando DataFrame
df = pd.DataFrame(games)

logging.info("DataFrame criado com sucesso")

# Exporta os dados para o BigQuery
try:
    df.to_gbq(destination_table=os.getenv('BIGQUERY_TABLE'),
              project_id=os.getenv('BIGQUERY_PROJECT_ID'),
              if_exists='replace',
              credentials=credencial)
    logging.info("Dados carregados com sucesso no BigQuery")
except Exception as e:
    logging.error(f"Erro ao carregar dados no BigQuery: {e}")
