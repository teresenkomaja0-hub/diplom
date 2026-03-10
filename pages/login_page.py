from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure

class VKAuthPage:
    """Класс для работы со страницей авторизации VK (Firefox)."""

    # Локаторы элементов авторизации
    BUTTON_OTHER_WAYS = (By.XPATH, "//span[contains(text(),'Войти другим способом')]/..")
    INPUT_PHONE = (By.XPATH, "//input[@type='tel' and @name='login']")
    BUTTON_LOGIN = (By.XPATH, "//span[contains(text(),'Войти')]/..")
    INPUT_CODE = (By.XPATH, "//input[@name='code' or @type='tel']")
    BUTTON_GET_SMS = (By.XPATH, "//span[contains(text(),'Получить SMS')]")
    ERROR_MESSAGE = (By.XPATH, "//div[contains(text(),'Неверный номер') or contains(text(),'ошибка')]")
    # Локатор кнопки Sign up
    BUTTON_SIGNUP = (By.CSS_SELECTOR, "button[data-testid='signup']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    @allure.step("Открыть страницу авторизации")
    def open(self):
        """Открыть страницу авторизации VK."""
        self.driver.get("https://vk.com")

    @allure.step("Начать процесс авторизации")
    def start_login(self):
        """Нажать кнопку 'Войти другим способом'."""
        try:
            button = self.wait.until(EC.element_to_be_clickable(self.BUTTON_OTHER_WAYS))
            button.click()
        except Exception:
            # Кнопка может быть уже скрыта или не нужна
            pass

    @allure.step("Ввести текст в поле")
    def input_text(self, locator, text):
        """Ввести текст в указанное поле."""
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    @allure.step("Клик по элементу")
    def click(self, locator):
        """Кликнуть по элементу."""
        element = self.find(locator)
        element.click()

    @allure.step("Найти элемент")
    def find(self, locator):
        """Найти элемент на странице."""
        return self.wait.until(EC.presence_of_element_located(locator))

    @allure.step("Авторизоваться с номером телефона")
    def login_with_phone(self, phone_number):
        """Полный процесс авторизации с номером телефона."""
        self.open()
        self.start_login()
        self.input_text(self.INPUT_PHONE, phone_number)
        self.click(self.BUTTON_LOGIN)

    @allure.step("Авторизоваться с некорректным номером")
    def login_with_invalid_phone(self, invalid_phone):
        """Попытка авторизации с некорректным номером."""
        self.open()
        self.start_login()
        self.input_text(self.INPUT_PHONE, invalid_phone)
        self.click(self.BUTTON_LOGIN)

    @allure.step("Проверить видимость кнопки 'Получить SMS'")
    def check_sms_button(self):
        """Проверить, видна ли кнопка 'Получить SMS'."""
        try:
            button = self.find(self.BUTTON_GET_SMS)
            return button.is_displayed()
        except Exception:
            return False

    @allure.step("Нажать кнопку Sign up и перейти на новую страницу")
    def click_signup_and_wait(self):
        """
        Нажать кнопку Sign up с ожиданием перехода на новую страницу.
        Использует явное ожидание для стабильности.
        """
        # Находим кнопку и кликаем
        button = self.find(self.BUTTON_SIGNUP)
        button.click()

        # Ждём перехода — проверяем изменение URL
        self.wait.until(
            lambda driver: driver.current_url != "https://vk.com"
        )
