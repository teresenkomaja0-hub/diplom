# tests/test_ui.py
import time
import os
import allure
import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

# Импортируем конфигурацию
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import settings, test_data
from pages.buttons_links_page import VKButtonsLinksPage  # Импортируем новый класс


@allure.epic("UI тесты VK")
@allure.feature("Кнопки и ссылки")
class TestVKButtonsAndLinks:
    """Класс для тестирования кнопок и ссылок на VK."""

    def setup_method(self):
        """Подготовка перед каждым тестом."""
        options = Options()
        options.add_argument(f"--width={settings.BROWSER_WIDTH}")
        options.add_argument(f"--height={settings.BROWSER_HEIGHT}")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        
        self.driver = webdriver.Firefox(options=options)
        self.driver.implicitly_wait(settings.IMPLICIT_WAIT)
        
        # Создаем экземпляр страницы с кнопками и ссылками
        self.page = VKButtonsLinksPage(self.driver)
        
        print(f"\n🚀 Запуск нового теста, браузер открыт")

    def teardown_method(self):
        """Очистка после каждого теста."""
        if hasattr(self, 'driver'):
            try:
                self.driver.quit()
                print(f"✅ Тест завершен, браузер полностью закрыт")
            except Exception as e:
                print(f"⚠️ Ошибка при закрытии браузера: {e}")
            finally:
                self.driver = None
                self.page = None

    @allure.title("Проверка кнопки 'Войти другим способом'")
    def test_other_login_button_click(self):
        """Тест проверяет, что кнопка 'Войти другим способом' существует и нажимается."""
        self.page.open_vk_page(settings.VK_WITH_PARAM_URL)
        self.page.take_screenshot("vk_main_page")

        self.page.click_login_button()
        self.page.take_screenshot("after_button_click")

        # Проверка появления QR или изменение URL
        if not self.page.check_qr_code_appears():
            assert self.page.check_url_changed(settings.VK_WITH_PARAM_URL)

    @allure.title("Автоматический ввод номера телефона")
    def test_auto_enter_phone_number(self):
        """Тест автоматического ввода номера телефона."""
        self.page.open_vk_page(settings.VK_WITH_PARAM_URL)
        self.page.take_screenshot("vk_main_page_start")

        self.page.click_login_button()
        self.page.take_screenshot("after_button_click")

        entered_value = self.page.enter_phone_number(test_data.TEST_USER['phone'])
        assert entered_value == test_data.TEST_USER['phone'], "Номер введен некорректно"

    @allure.title("Проверка перехода на страницу с условиями использования")
    def test_terms_link_click(self):
        """Тест проверяет переход по ссылке 'Условия использования'."""
        original_window = self.driver.current_window_handle
        
        self.page.open_vk_page(settings.VK_WITH_PARAM_URL)
        self.page.take_screenshot("vk_page_terms_test")

        terms_link = self.page.get_terms_link()
        self.page.check_link_url(terms_link, "vk.com/terms")

        terms_link.click()
        time.sleep(2)

        new_window = self.page.switch_to_new_window(original_window)
        assert new_window is not None, "Новая вкладка не открылась"
        
        self.page.take_screenshot("after_terms_click")
        
        # Проверяем URL новой вкладки
        current_url = self.driver.current_url
        assert "vk.com/terms" in current_url, f"Не удалось перейти на страницу условий"
        
        # Возвращаемся на исходную вкладку
        self.driver.switch_to.window(original_window)

    @allure.title("Проверка перехода на страницу VK Developers")
    def test_vk_dev_link_click(self):
        """Тест проверяет переход по ссылке на VK Developers."""
        self.page.open_vk_page(settings.VK_SPECIAL_URL)
        original_window = self.driver.current_window_handle
        
        print(f"📌 Тестовый URL: {settings.VK_SPECIAL_URL}")
        self.page.take_screenshot("vk_page_with_special_url")

        dev_link = self.page.get_dev_link()
        self.page.check_link_url(dev_link, "dev.vk.com")

        dev_link.click()
        time.sleep(3)

        new_window = self.page.switch_to_new_window(original_window)
        assert new_window is not None, "Новая вкладка не открылась"

        self.page.take_screenshot("after_dev_link_click")

        # Проверяем URL новой вкладки
        current_url = self.driver.current_url
        assert "dev.vk.com" in current_url, f"Не удалось перейти на страницу VK Developers"

        # Возвращаемся и закрываем дополнительную вкладку
        self.page.close_additional_window(new_window, original_window)

    @allure.title("Проверка выбора китайского языка")
    def test_vk_language_selection(self):
        """Тест проверяет возможность смены языка на китайский."""
        self.page.open_vk_page(settings.VK_SPECIAL_URL)
        self.page.take_screenshot("step1_vk_main_page")

        # Получаем текущий язык
        old_language = self.page.get_language_selector().text
        
        # Открываем меню выбора языка
        self.page.open_language_menu()
        self.page.take_screenshot("step2_language_menu_open")
        
        # Выбираем китайский язык
        self.page.select_chinese_language()
        
        # Проверяем, что язык изменился
        new_language = self.page.verify_language_changed(old_language)
        self.page.take_screenshot("step3_after_language_change")
        
        print(f"✅ Язык успешно изменен с '{old_language}' на '{new_language}'")