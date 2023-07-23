import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager


class HomePageTest(LiveServerTestCase):
    def setUp(self):
        options = Options()
        options.add_argument('-headless')
        manager = GeckoDriverManager().install()
        driver = webdriver.Firefox(options=options, service=FirefoxService(manager))
        self.driver = driver

    def tearDown(self):
        self.driver.quit()

    def test_can_check_home_items(self):
        #Usuario vai ate a homepage
        self.driver.get(self.live_server_url)
    
        #Aguarda a pagina carregar
        WebDriverWait(self.driver,60).until(EC.visibility_of(self.driver.find_element(By.XPATH,"//input[@type='radio'][@value='EUR']")))

        #Usuario checa o titulo da pagina
        self.assertIn('BRMed',self.driver.title)
        
        #Ele verifica se ha um formulario na pagina
        form_element = self.driver.find_element(By.XPATH,'//form')
        self.assertIsNotNone(form_element)

        #Insere as datas do formulario
        self.driver.find_element(By.ID,'start_date').send_keys('10/01/2000')
        self.driver.find_element(By.ID,'end_date').send_keys('15/01/2000')

        #Resolve escolher a conversao de usd x eur e clica no elemento
        self.driver.find_element(By.XPATH,"//input[@type='radio'][@value='EUR']").click()

        #Realiza o post
        button = self.driver.find_element(By.XPATH,"//button[@type='submit']")
        self.driver.execute_script("arguments[0].click();", button)

        #Usuario aguarda a pagina do grafico carregar para checar as informacoes
        time.sleep(8)

        self.driver.find_element(By.XPATH,'//button[contains(text(),"Voltar")]').click()
        
        #Apos ver os dados ele fecha o navegador
        self.tearDown()