# pages/buttons_links_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
import time


class VKButtonsLinksPage:
    """
    Класс для работы с кнопками и ссылками на главной странице VK.
    
    Содержит методы для:
    - Работы с кнопкой "Other sign-in options"
    - Проверки появления QR-кода
    - Работы с полем ввода телефона
    - Перехода по ссылкам (Terms, Developers)
    - Смены языка
    """

    def __init__(self, driver):
        """
        Инициализация страницы с кнопками и ссылками.
        
        Args:
            driver: WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    # Локаторы для кнопок и ссылок
    LOGIN_BUTTON = (By.XPATH, "//*[@id='START_QR_PAGE']/div/div[2]/div/button[1]")
    QR_ELEMENT = (By.XPATH, "//*[contains(@class, 'qr') or contains(@src, 'qrcode') or contains(@alt, 'QR')]")
    PHONE_INPUT = (By.XPATH, "//*[@id='ENTER_LOGIN_PAGE']/div/form/div[1]/div[3]/span/div/div[2]/input")
    TERMS_LINK = (By.XPATH, "/html/body/div[15]/div/div/div/div[4]/div/div/div[1]/div/div[3]/a")
    DEV_LINK = (By.XPATH, "/html/body/div[15]/div/div/div/div[4]/div/div/div[2]/div/div[2]/a")
    
    # Локаторы для выбора языка
    LANGUAGE_SELECTOR = (By.XPATH, "/html/body/div[15]/div/div/div/div[4]/div/div/div[3]/div/div/a/span")
    LANGUAGE_MENU = (By.XPATH, "//*[@id='all_languages_list']")
    CHINESE_LANGUAGE = (By.XPATH, "//*[@id='all_languages_list']/div[4]/div[16]/a/span")

    # Ожидаемые тексты для проверок
    EXPECTED_BUTTON_TEXTS = [
        "Войти другим способом",
        "Other sign-in options",
        "Другим способом",
        "Sign in with another way"
    ]
    
    EXPECTED_TERMS_TEXTS = [
        "Условия использования",
        "Terms of Use",
        "Условия",
        "Terms"
    ]
    
    EXPECTED_DEV_TEXTS = [
        "VK Developers",
        "Разработчикам",
        "Developers",
        "Для разработчиков"
    ]

    @allure.step("Открыть страницу VK")
    def open_vk_page(self, url):
        """
        Открыть страницу VK по указанному URL.
        
        Args:
            url (str): URL страницы для открытия
        """
        self.driver.get(url)
        allure.attach(
            f"Открыта страница: {url}",
            name="page_url",
            attachment_type=allure.attachment_type.TEXT
        )

    @allure.step("Найти и проверить кнопку входа")
    def get_login_button(self):
        """
        Найти кнопку 'Other sign-in options' и проверить её текст.
        
        Returns:
            WebElement: Найденная кнопка
        """
        button = self.wait.until(
            EC.presence_of_element_located(self.LOGIN_BUTTON)
        )
        assert button.is_displayed(), "Кнопка не видна на странице"
        
        button_text = button.text
        text_matched = any(expected in button_text for expected in self.EXPECTED_BUTTON_TEXTS)
        assert text_matched, f"Неожиданный текст кнопки: {button_text}"
        
        allure.attach(
            button_text,
            name="button_text",
            attachment_type=allure.attachment_type.TEXT
        )
        
        print(f"✅ Текст кнопки: '{button_text}'")
        return button

    @allure.step("Нажать кнопку входа")
    def click_login_button(self):
        """Нажать на кнопку 'Other sign-in options'."""
        button = self.get_login_button()
        button.click()
        time.sleep(1)

    @allure.step("Проверить появление QR-кода")
    def check_qr_code_appears(self):
        """
        Проверить, что после нажатия кнопки появляется QR-код.
        
        Returns:
            bool: True если QR-код появился
        """
        try:
            qr_element = self.wait.until(
                EC.presence_of_element_located(self.QR_ELEMENT)
            )
            assert qr_element.is_displayed(), "QR код не появился"
            allure.attach(
                "QR код появился после нажатия кнопки",
                name="qr_appeared",
                attachment_type=allure.attachment_type.TEXT
            )
            print("✅ QR код появился - кнопка работает!")
            return True
        except:
            return False

    @allure.step("Проверить изменение URL")
    def check_url_changed(self, original_url):
        """
        Проверить, что URL изменился после нажатия.
        
        Args:
            original_url (str): Исходный URL
            
        Returns:
            bool: True если URL изменился
        """
        current_url = self.driver.current_url
        allure.attach(
            f"URL после нажатия: {current_url}",
            name="current_url",
            attachment_type=allure.attachment_type.TEXT
        )
        
        if current_url != original_url:
            print(f"✅ URL изменился на: {current_url}")
            return True
        return False

    @allure.step("Ввести номер телефона")
    def enter_phone_number(self, phone_number):
        """
        Ввести номер телефона в соответствующее поле.
        
        Args:
            phone_number (str): Номер телефона для ввода
            
        Returns:
            str: Введенное значение
        """
        phone_input = self.wait.until(
            EC.presence_of_element_located(self.PHONE_INPUT)
        )
        assert phone_input.is_displayed(), "Поле для ввода номера не появилось"
        print("✅ Поле для ввода номера телефона появилось")
        
        phone_input.clear()
        phone_input.send_keys(phone_number)
        time.sleep(1)
        
        entered_value = phone_input.get_attribute("value")
        print(f"Введенный номер: {entered_value}")
        
        allure.attach(
            f"Введен номер: {entered_value}",
            name="entered_phone",
            attachment_type=allure.attachment_type.TEXT
        )
        
        return entered_value

    @allure.step("Найти ссылку Terms/Условия использования")
    def get_terms_link(self):
        """
        Найти ссылку на условия использования.
        
        Returns:
            WebElement: Найденная ссылка
        """
        link = self.wait.until(
            EC.presence_of_element_located(self.TERMS_LINK)
        )
        assert link.is_displayed(), "Ссылка на условия использования не видна"
        
        link_text = link.text
        text_matched = any(expected in link_text for expected in self.EXPECTED_TERMS_TEXTS)
        assert text_matched, f"Неожиданный текст ссылки: {link_text}"
        
        print(f"🔗 Текст ссылки: '{link_text}'")
        
        allure.attach(
            link_text,
            name="terms_link_text",
            attachment_type=allure.attachment_type.TEXT
        )
        
        return link

    @allure.step("Найти ссылку Developers/Разработчикам")
    def get_dev_link(self):
        """
        Найти ссылку на VK Developers.
        
        Returns:
            WebElement: Найденная ссылка
        """
        link = self.wait.until(
            EC.presence_of_element_located(self.DEV_LINK)
        )
        assert link.is_displayed(), "Ссылка на VK Developers не видна"
        
        link_text = link.text
        text_matched = any(expected.lower() in link_text.lower() 
                          for expected in self.EXPECTED_DEV_TEXTS)
        assert text_matched, f"Неожиданный текст ссылки: {link_text}"
        
        print(f"🔗 Текст ссылки: '{link_text}'")
        
        allure.attach(
            link_text,
            name="dev_link_text",
            attachment_type=allure.attachment_type.TEXT
        )
        
        return link

    @allure.step("Проверить URL ссылки")
    def check_link_url(self, link_element, expected_url_part):
        """
        Проверить, что URL ссылки содержит ожидаемую часть.
        
        Args:
            link_element: WebElement ссылки
            expected_url_part (str): Ожидаемая часть URL
            
        Returns:
            str: Полный URL ссылки
        """
        link_href = link_element.get_attribute("href")
        print(f"📌 URL ссылки: {link_href}")
        
        assert expected_url_part in link_href, \
            f"Ссылка ведет на {link_href}, ожидалось {expected_url_part}"
        
        allure.attach(
            link_href,
            name="link_url",
            attachment_type=allure.attachment_type.TEXT
        )
        
        return link_href

    @allure.step("Переключиться на новую вкладку")
    def switch_to_new_window(self, original_window):
        """
        Переключиться на новую открытую вкладку.
        
        Args:
            original_window: Идентификатор исходной вкладки
            
        Returns:
            str: Идентификатор новой вкладки или None
        """
        new_window = None
        for window in self.driver.window_handles:
            if window != original_window:
                new_window = window
                self.driver.switch_to.window(window)
                print(f"✅ Переключились на новую вкладку: {window}")
                break
        
        if new_window:
            allure.attach(
                f"Переключились на новую вкладку: {new_window}",
                name="window_switch",
                attachment_type=allure.attachment_type.TEXT
            )
        
        return new_window

    @allure.step("Закрыть дополнительную вкладку")
    def close_additional_window(self, window_to_close, return_to_window):
        """
        Закрыть дополнительную вкладку и вернуться на исходную.
        
        Args:
            window_to_close: Идентификатор вкладки для закрытия
            return_to_window: Идентификатор вкладки для возврата
        """
        if window_to_close and window_to_close in self.driver.window_handles:
            self.driver.switch_to.window(window_to_close)
            self.driver.close()
            print("🗑️ Закрыта дополнительная вкладка")
            self.driver.switch_to.window(return_to_window)

    @allure.step("Найти селектор языка")
    def get_language_selector(self):
        """
        Найти селектор выбора языка.
        
        Returns:
            WebElement: Найденный селектор языка
        """
        selector = self.wait.until(
            EC.element_to_be_clickable(self.LANGUAGE_SELECTOR)
        )
        assert selector.is_displayed(), "Селектор языка не найден"
        
        current_language = selector.text
        print(f"🌐 Текущий язык селектора: '{current_language}'")
        
        allure.attach(
            f"Текущий язык: {current_language}",
            name="current_language",
            attachment_type=allure.attachment_type.TEXT
        )
        
        return selector

    @allure.step("Открыть меню выбора языка")
    def open_language_menu(self):
        """Кликнуть по селектору языка и открыть меню."""
        selector = self.get_language_selector()
        selector.click()
        time.sleep(2)
        
        menu = self.wait.until(
            EC.presence_of_element_located(self.LANGUAGE_MENU)
        )
        assert menu.is_displayed(), "Меню выбора языка не открылось"
        print("✅ Меню выбора языка открылось")

    @allure.step("Выбрать китайский язык")
    def select_chinese_language(self):
        """
        Выбрать китайский язык в меню.
        
        Returns:
            str: Текст выбранного языка
        """
        chinese = self.wait.until(
            EC.element_to_be_clickable(self.CHINESE_LANGUAGE)
        )
        
        chinese_text = chinese.text
        print(f"🇨🇳 Выбран язык: '{chinese_text}'")
        
        # Проверяем, что это китайский язык
        assert "汉语" in chinese_text or "中文" in chinese_text or "Chinese" in chinese_text, \
            f"Выбран не китайский язык: {chinese_text}"
        
        allure.attach(
            f"Выбранный язык: {chinese_text}",
            name="selected_language",
            attachment_type=allure.attachment_type.TEXT
        )
        
        chinese.click()
        time.sleep(3)
        
        return chinese_text

    @allure.step("Проверить изменение языка")
    def verify_language_changed(self, old_language):
        """
        Проверить, что язык интерфейса изменился.
        
        Args:
            old_language (str): Предыдущий язык
            
        Returns:
            str: Новый язык
        """
        new_selector = self.wait.until(
            EC.presence_of_element_located(self.LANGUAGE_SELECTOR)
        )
        new_language = new_selector.text
        print(f"🌐 Новый язык селектора: '{new_language}'")
        
        allure.attach(
            f"Новый язык: {new_language}",
            name="new_language",
            attachment_type=allure.attachment_type.TEXT
        )
        
        assert new_language != old_language, "Язык не изменился"
        assert "汉" in new_language or "中文" in new_language, \
            f"Язык не изменился на китайский: {new_language}"
        
        return new_language

    @allure.step("Сделать скриншот")
    def take_screenshot(self, name):
        """
        Сделать скриншот и прикрепить к Allure отчету.
        
        Args:
            name (str): Название скриншота
        """
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name=name,
            attachment_type=allure.attachment_type.PNG
        )