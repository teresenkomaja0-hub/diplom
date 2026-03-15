# tests/test_vk_login.py
import time
import os
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

# Импортируем конфигурацию
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import settings, test_data

class TestVKLoginButton:
    """Класс для тестирования кнопок и ссылок на VK."""

    def setup_method(self):
        """Подготовка перед каждым тестом - открываем новый браузер."""
        options = Options()
        options.add_argument(f"--width={settings.BROWSER_WIDTH}")
        options.add_argument(f"--height={settings.BROWSER_HEIGHT}")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        
        self.driver = webdriver.Firefox(options=options)
        self.driver.implicitly_wait(settings.IMPLICIT_WAIT)
        self.wait = WebDriverWait(self.driver, settings.EXPLICIT_WAIT)
        
        # Создаем папку для скриншотов если её нет
        if not os.path.exists(settings.ERROR_SCREENSHOT_PATH):
            os.makedirs(settings.ERROR_SCREENSHOT_PATH)
            
        print(f"\n🚀 Запуск нового теста, браузер открыт")

    def teardown_method(self):
        """Очистка после каждого теста - полностью закрываем браузер."""
        if hasattr(self, 'driver'):
            try:
                self.driver.quit()
                print(f"✅ Тест завершен, браузер полностью закрыт")
            except Exception as e:
                print(f"⚠️ Ошибка при закрытии браузера: {e}")
                try:
                    self.driver.service.stop()
                except:
                    pass
            finally:
                self.driver = None

    def take_screenshot(self, name):
        """Вспомогательный метод для создания скриншотов"""
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name=name,
            attachment_type=allure.attachment_type.PNG
        )

    @allure.epic("UI тесты VK")
    @allure.feature("Авторизация")
    @allure.story("Кнопка входа")
    @allure.title("Проверка кнопки 'Войти другим способом'")
    @allure.description("Тест проверяет, что кнопка 'Войти другим способом' существует и нажимается")
    def test_other_login_button_click(self):
        self.driver.get(settings.VK_WITH_PARAM_URL)
        self.take_screenshot("vk_main_page")

        login_button = self.wait.until(
            EC.presence_of_element_located(test_data.LOCATORS['login_button'])
        )

        assert login_button.is_displayed(), "Кнопка не видна на странице"
        button_text = login_button.text
        
        allure.attach(
            button_text,
            name="button_text",
            attachment_type=allure.attachment_type.TEXT
        )

        text_matched = any(expected in button_text for expected in test_data.EXPECTED_TEXTS['login_button'])
        assert text_matched, f"Неожиданный текст кнопки: {button_text}"
        print(f"✅ Текст кнопки: '{button_text}'")

        login_button.click()
        self.take_screenshot("after_button_click")

        # Проверка появления QR или изменение URL
        try:
            qr_element = self.wait.until(
                EC.presence_of_element_located(test_data.LOCATORS['qr_element'])
            )
            assert qr_element.is_displayed(), "QR код не появился"
            allure.attach(
                "QR код появился после нажатия кнопки",
                name="qr_appeared",
                attachment_type=allure.attachment_type.TEXT
            )
            print("✅ QR код появился - кнопка работает!")
        except:
            current_url = self.driver.current_url
            allure.attach(
                f"URL после нажатия: {current_url}",
                name="current_url",
                attachment_type=allure.attachment_type.TEXT
            )
            assert current_url != settings.VK_WITH_PARAM_URL, "URL не изменился после нажатия"
            print(f"✅ URL изменился на: {current_url}")

    @allure.epic("UI тесты VK")
    @allure.feature("Авторизация")
    @allure.story("Ввод номера телефона")
    @allure.title("Автоматический ввод номера телефона после нажатия кнопки 'Войти другим способом'")
    @allure.description("Тест автоматически нажимает кнопку 'Войти другим способом' и вводит номер телефона")
    def test_auto_enter_phone_number(self):
        self.driver.get(settings.VK_WITH_PARAM_URL)
        self.take_screenshot("vk_main_page_start")

        login_button = self.wait.until(EC.element_to_be_clickable(test_data.LOCATORS['login_button']))
        assert login_button.is_displayed(), "Кнопка не видна на странице"
        print(f"✅ Нажата кнопка с текстом: '{login_button.text}'")
        login_button.click()

        self.take_screenshot("after_button_click")

        phone_input = self.wait.until(EC.presence_of_element_located(test_data.LOCATORS['phone_input']))
        assert phone_input.is_displayed(), "Поле для ввода номера не появилось"
        print("✅ Поле для ввода номера телефона появилось")
        self.take_screenshot("phone_input_appeared")

        phone_input.clear()
        phone_input.send_keys(test_data.TEST_USER['phone'])
        time.sleep(1)
        entered_value = phone_input.get_attribute("value")
        print(f"Введенный номер: {entered_value}")

    @allure.epic("UI тесты VK")
    @allure.feature("Ссылки")
    @allure.story("Пользовательское соглашение")
    @allure.title("Проверка перехода на страницу с условиями использования")
    @allure.description("Тест проверяет, что кнопка 'Условия использования' ведет на правильную страницу")
    def test_terms_link_click(self):
        """Тест проверяет переход по ссылке 'Условия использования'"""
        self.driver.get(settings.VK_WITH_PARAM_URL)
        original_window = self.driver.current_window_handle
        
        print(f"📌 Исходная вкладка: {original_window}")
        self.take_screenshot("vk_page_terms_test")

        terms_link = self.wait.until(EC.presence_of_element_located(test_data.LOCATORS['terms_link']))
        assert terms_link.is_displayed(), "Ссылка на условия использования не видна на странице"

        link_text = terms_link.text
        print(f"🔗 Текст ссылки: '{link_text}'")
        
        text_matched = any(expected in link_text for expected in test_data.EXPECTED_TEXTS['terms_link'])
        assert text_matched, f"Неожиданный текст ссылки: {link_text}"

        link_href = terms_link.get_attribute("href")
        print(f"📌 URL ссылки: {link_href}")
        assert settings.VK_TERMS_URL in link_href, f"Ссылка ведет на {link_href}, ожидалось {settings.VK_TERMS_URL}"

        terms_link.click()
        time.sleep(2)

        # Переключаемся на новую вкладку
        for window in self.driver.window_handles:
            if window != original_window:
                self.driver.switch_to.window(window)
                break

        time.sleep(2)
        self.take_screenshot("after_terms_click")

        current_url = self.driver.current_url
        print(f"📍 Текущий URL: {current_url}")
        assert settings.VK_TERMS_URL in current_url, f"Не удалось перейти на страницу условий"

        # Возвращаемся на исходную вкладку
        self.driver.switch_to.window(original_window)
        print("🔄 Возврат на исходную вкладку")

    @allure.epic("UI тесты VK")
    @allure.feature("Ссылки")
    @allure.story("VK Developers")
    @allure.title("Проверка перехода на страницу VK Developers")
    @allure.description("Тест проверяет, что ссылка на VK Developers ведет на правильную страницу")
    def test_vk_dev_link_click(self):
        """Тест проверяет переход по ссылке на VK Developers"""
        # Используем новый URL для 4 теста
        self.driver.get(settings.VK_SPECIAL_URL)
        original_window = self.driver.current_window_handle
        
        print(f"📌 Исходная вкладка: {original_window}")
        print(f"📌 Тестовый URL: {settings.VK_SPECIAL_URL}")
        self.take_screenshot("vk_page_with_special_url")

        dev_link = self.wait.until(EC.presence_of_element_located(test_data.LOCATORS['dev_link']))
        assert dev_link.is_displayed(), "Ссылка на VK Developers не видна на странице"

        link_text = dev_link.text
        print(f"🔗 Текст ссылки: '{link_text}'")
        
        text_matched = any(expected.lower() in link_text.lower() for expected in test_data.EXPECTED_TEXTS['dev_link'])
        assert text_matched, f"Неожиданный текст ссылки: {link_text}"

        link_href = dev_link.get_attribute("href")
        print(f"📌 URL ссылки: {link_href}")
        assert "dev.vk.com" in link_href, f"Ссылка ведет на {link_href}, ожидалось {settings.VK_DEV_URL}"

        dev_link.click()
        time.sleep(3)

        # Переключаемся на новую вкладку
        new_window = None
        for window in self.driver.window_handles:
            if window != original_window:
                new_window = window
                self.driver.switch_to.window(window)
                print(f"✅ Переключились на новую вкладку: {window}")
                break

        assert new_window is not None, "Новая вкладка не открылась"
        time.sleep(3)

        self.take_screenshot("after_dev_link_click")

        current_url = self.driver.current_url
        print(f"📍 Текущий URL: {current_url}")
        assert "dev.vk.com" in current_url, f"Не удалось перейти на страницу VK Developers"

        # Возвращаемся и закрываем дополнительную вкладку
        self.driver.switch_to.window(original_window)
        if new_window and new_window in self.driver.window_handles:
            self.driver.switch_to.window(new_window)
            self.driver.close()
            print("🗑️ Закрыта дополнительная вкладка с VK Developers")
            self.driver.switch_to.window(original_window)

    @allure.epic("UI тесты VK")
    @allure.feature("Языковые настройки")
    @allure.story("Выбор языка")
    @allure.title("Проверка выбора китайского языка на главной странице VK")
    @allure.description("Тест проверяет возможность смены языка на китайский через селектор языка")
    def test_vk_language_selection(self):
        """Пятый тест: выбор китайского языка на главной странице VK"""
        # Используем новый URL для 5 теста
        self.driver.get(settings.VK_SPECIAL_URL)
        original_window = self.driver.current_window_handle
        
        print(f"\n📌 Шаг 1: Открыта страница VK: {settings.VK_SPECIAL_URL}")
        self.take_screenshot("step1_vk_main_page")

        # Шаг 2: Находим и кликаем на селектор языка
        print("🔍 Шаг 2: Поиск селектора языка...")
        try:
            language_selector = self.wait.until(
                EC.element_to_be_clickable(test_data.LOCATORS['language_selector'])
            )
            assert language_selector.is_displayed(), "Селектор языка не найден"
            
            current_language = language_selector.text
            print(f"🌐 Текущий язык селектора: '{current_language}'")
            
            # Сохраняем информацию о текущем языке
            allure.attach(
                f"Текущий язык: {current_language}",
                name="current_language",
                attachment_type=allure.attachment_type.TEXT
            )
            
            # Кликаем на селектор языка
            language_selector.click()
            time.sleep(2)
            
            # Проверяем, что меню открылось
            language_menu = self.wait.until(
                EC.presence_of_element_located(test_data.LOCATORS['language_menu'])
            )
            assert language_menu.is_displayed(), "Меню выбора языка не открылось"
            
            self.take_screenshot("step2_language_menu_open")
            print("✅ Меню выбора языка открылось")
            
            # Шаг 3: Выбираем китайский язык
            print("🔍 Шаг 3: Выбор китайского языка...")
            
            # Используем локатор из test_data.py
            chinese_language = self.wait.until(
                EC.element_to_be_clickable(test_data.LOCATORS['chinese_language'])
            )
            
            chinese_text = chinese_language.text
            print(f"🇨🇳 Выбран язык: '{chinese_text}'")
            
            # Проверяем, что это китайский язык
            assert "汉语" in chinese_text or "中文" in chinese_text or "Chinese" in chinese_text, f"Выбран не китайский язык: {chinese_text}"
            
            # Сохраняем информацию о выбранном языке
            allure.attach(
                f"Выбранный язык: {chinese_text}",
                name="selected_language",
                attachment_type=allure.attachment_type.TEXT
            )
            
            # Кликаем на китайский язык
            chinese_language.click()
            time.sleep(3)
            
            # Проверяем, что язык изменился
            new_language_selector = self.wait.until(
                EC.presence_of_element_located(test_data.LOCATORS['language_selector'])
            )
            new_language = new_language_selector.text
            print(f"🌐 Новый язык селектора: '{new_language}'")
            
            # Сохраняем информацию о новом языке
            allure.attach(
                f"Новый язык: {new_language}",
                name="new_language",
                attachment_type=allure.attachment_type.TEXT
            )
            
            # Проверяем, что язык изменился на китайский
            assert new_language != current_language, "Язык не изменился"
            assert "汉" in new_language or "中文" in new_language, f"Язык не изменился на китайский: {new_language}"
            
            self.take_screenshot("step3_after_language_change")
            print("✅ Тест выбора китайского языка успешно завершен")
            
        except Exception as e:
            print(f"❌ Ошибка при смене языка: {e}")
            self.take_screenshot("step2_language_error")
            
            # Сохраняем информацию об ошибке
            allure.attach(
                f"Ошибка: {str(e)}",
                name="language_selection_error",
                attachment_type=allure.attachment_type.TEXT
            )
            raise e


if __name__ == "__main__":
    print("=" * 60)
    print("ТЕСТЫ КНОПОК И ССЫЛОК НА VK")
    print("=" * 60)

    import pytest
    pytest.main(["-v", "tests/"])