import pytest
import allure
from selenium.webdriver.remote.webdriver import WebDriver

# Импорты из ваших конфигурационных файлов
from configs.env import BASE_URL, DEFAULT_TIMEOUT
from configs.test_data import TEST_USER, INVALID_USER

# Импорты страниц
from pages.login_page import VKAuthPage
from pages.main_page import MainPage

@allure.epic("UI тесты VK")
@allure.feature("Авторизация и навигация")
class TestVKAuthAndNavigation:
    """Комплексное тестирование UI авторизации и навигации во ВКонтакте."""

    @pytest.fixture(autouse=True)
    def setup(self, driver: WebDriver):
        """Фикстура для подготовки перед каждым тестом."""
        self.driver = driver
        self.auth_page = VKAuthPage(driver)
        self.main_page = MainPage(driver)

    @allure.story("Авторизация по номеру телефона")
    @allure.title("Успешная авторизация с корректным номером")
    def test_successful_login_with_phone(self):
        """Тест успешной авторизации с корректным номером телефона."""
        with allure.step("Открыть страницу авторизации"):
            self.auth_page.open()

        with allure.step("Начать процесс авторизации"):
            self.auth_page.start_login()

        with allure.step(f"Ввести корректный номер {TEST_USER['phone']}"):
            self.auth_page.input_text(
                self.auth_page.INPUT_PHONE,
                TEST_USER["phone"]
            )

        with allure.step("Нажать кнопку 'Войти'"):
            self.auth_page.click(self.auth_page.BUTTON_LOGIN)

        with allure.step("Ввести тестовый код подтверждения"):
            try:
                code_input = self.auth_page.find(self.auth_page.INPUT_CODE)
                code_input.send_keys("12345")
                code_input.send_keys("\n")
            except Exception:
                pytest.fail("Поле ввода кода не появилось в отведённое время")

        with allure.step("Проверить, что пользователь авторизован"):
            assert self.main_page.is_user_logged_in(), \
                "Пользователь не авторизован после ввода корректных данных"

    @allure.story("Обработка ошибок авторизации")
    @allure.title("Отображение ошибки при вводе некорректного номера")
    def test_login_with_invalid_phone_shows_error(self):
        """Тест отображения ошибки при вводе некорректного номера."""
        with allure.step("Открыть страницу авторизации"):
            self.auth_page.open()

        with allure.step(f"Ввести некорректный номер {INVALID_USER['login']}"):
            self.auth_page.login_with_invalid_phone(INVALID_USER["login"])

        with allure.step("Проверить отображение сообщения об ошибке"):
            error_message = self.auth_page.find(self.auth_page.ERROR_MESSAGE)
            assert error_message.is_displayed(), \
                "Сообщение об ошибке не отображается при вводе некорректного номера"
            allure.attach(
                error_message.text,
                name="error_message_text",
                attachment_type=allure.attachment_type.TEXT
            )

    @allure.story("Элементы интерфейса авторизации")
    @allure.title("Проверка видимости кнопки 'Получить SMS'")
    def test_sms_button_visibility(self):
        """Тест видимости кнопки 'Получить SMS'."""
        with allure.step("Открыть страницу авторизации"):
            self.auth_page.open()

        with allure.step("Начать процесс авторизации"):
            self.auth_page.start_login()

        with allure.step("Проверить видимость кнопки 'Получить SMS'"):
            visible = self.auth_page.check_sms_button()
            assert visible, "Кнопка 'Получить SMS' не видна"

    @allure.story("Сессия пользователя")
    @allure.title("Выход из системы после успешной авторизации")
    def test_logout_after_login(self):
        """Тест выхода из системы после авторизации."""
        with allure.step("Авторизоваться с корректным номером"):
            self.auth_page.login_with_phone(TEST_USER["phone"])

        with allure.step("Выполнить выход из системы"):
            logout_success = self.main_page.logout()
            assert logout_success, "Не удалось выполнить выход из системы"

        with allure.step("Проверить статус авторизации после выхода"):
            assert not self.main_page.is_user_logged_in(), \
                "Пользователь всё ещё авторизован после выхода"

    @allure.story("Навигация после авторизации")
    @allure.title("Проверка отображения ленты новостей после входа")
    def test_newsfeed_display_after_login(self):
        """Тест отображения ленты новостей после успешной авторизации."""
        with allure.step("Авторизоваться с корректным номером"):
            self.auth_page.login_with_phone(TEST_USER["phone"])


        with allure.step("Проверить отображение ленты новостей"):
            newsfeed = self.main_page.wait.until(
                EC.presence_of_element_located(self.main_page.NEWS_FEED)
            )
            assert newsfeed.is_displayed(), "Лента новостей не отображается после авторизации"

        with allure.step("Сделать скриншот главной страницы"):
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="main_page_after_login",
                attachment_type=allure.attachment_type.PNG
            )


    @allure.story("Навигация по интерфейсу")
    @allure.title("Автоматический переход при нажатии кнопки Sign up")
    def test_signup_button_navigation(self):
        """Тест автоматического перехода при нажатии кнопки Sign up."""
        with allure.step("Открыть страницу авторизации"):
            self.auth_page.open()

        with allure.step("Нажать кнопку Sign up и дождаться перехода"):
            # Используем новый метод для клика и ожидания
            self.auth_page.click_signup_and_wait()

        with allure.step("Проверить, что произошёл переход на новую страницу"):
            current_url = self.driver.current_url
            allure.attach(
                current_url,
                name="Current URL after signup click",
                attachment_type=allure.attachment_type.TEXT
            )

            # Проверяем, что URL изменился (не равен исходной странице)
            assert current_url != "https://vk.com", \
                f"Переход не произошёл, текущий URL: {current_url}"

        with allure.step("Сделать скриншот новой страницы"):
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="Page after signup button click",
                attachment_type=allure.attachment_type.PNG
            )



