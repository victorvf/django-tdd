"""
    1. Quando não conseguimos ver o erro na mensagem retornada, muitas vezes
usar o time.sleep(valor considerável) já irá resolver o problema.
"""
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

from django.test import LiveServerTestCase

MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id("id_list_table")
                rows = table.find_elements_by_tag_name("tr")
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith ouviu falar de uma nova aplicação online interessante para lista
        # de tarefas. Ela decide verificar sua homepage.
        self.browser.get(self.live_server_url)

        # Ela percebe que o título da página e o cabeçalho mencionam listas de
        # tarefas (to-do)
        self.assertIn("To-Do", self.browser.title)

        header_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn("To-Do", header_text)

        # Ela é convidada a inserir um item de tarefa imediatamente
        inputbox = self.browser.find_element_by_id("id_new_item")
        self.assertEqual(
            inputbox.get_attribute("placeholder"),
            "Enter a to-do item",
        )

        # Ela digita "Buy peacock feathers" em uma caixa de texto.
        inputbox.send_keys("Buy peacock feathers")

        # Quando ela tecla enter, a página é atualizada, e agora a página lista
        # 1: Buy peacock feathers - como um item em uma lista de tarefas
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy peacock feathers")

        # Ainda continua havendo uma caixa de texto convidando-a a
        # acrescentar outro item.
        # Ela insere 'Use peacock feathers to make a fly'
        inputbox = self.browser.find_element_by_id("id_new_item")
        inputbox.send_keys("Use peacock feathers to make a fly")
        inputbox.send_keys(Keys.ENTER)

        # A página é atualizada novamente e agora mostra os dois itens em
        # sua lista
        self.wait_for_row_in_list_table("1: Buy peacock feathers")
        self.wait_for_row_in_list_table("2: Use peacock feathers to make a fly")

        # Edith fica na dúvida se o site lembrará de sua lista. Então ela
        # nota que o site gerou um URL único para ela -- há um pequeno
        # texto explicativo para isso.
        self.fail("Finish the test!")

        # Ela acessa essa URL - sua lista de tarefas continua lá.

        # Satisfeita, ela volta a dormir
