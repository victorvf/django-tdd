import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith ouviu falar de uma nova aplicação online interessante para lista
        # de tarefas. Ela decide verificar sua homepage.
        self.browser.get('http://localhost:8000')

        # Ela percebe que o título da página e o cabeçalho mencionam listas de
        # tarefas (to-do)
        self.assertIn('To-Do', self.browser.title)

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # Ela é convidada a inserir um item de tarefa imediatamente
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item',
        )

        # Ela digita "Buy peacock feathers em uma caixa de texto.
        inputbox.send_keys('Buy peacock feathers')

        # Quando ela tecla enter, a página é atualizada, e agora a página lista
        # 1: Buy peacock feathers - como um item em uma lista de tarefas
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Buy peacock feathers' for row in rows),
            "New to-do item did not appear in table",
        )

        # Ainda continua havendo uma caixa de texto convidando-a a
        # acrescentar outro item.
        # Ela insere 'Use peacock feathers to make a fly'
        self.fail('Finish the test!')

        # A página é atualizada novamente e agora mostra os dois itens em
        # sua lista

        # Edith fica na dúvida se o site lembrará de sua lista. Então ela
        # nota que o site gerou um URL único para ela -- há um pequeno
        # texto explicativo para isso.

        # Ela acessa essa URL - sua lista de tarefas continua lá.

        # Satisfeita, ela volta a dormir


if __name__ == '__main__':
    unittest.main(warnings='ignore')
