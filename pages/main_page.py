from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
import time

class MainPage:
    """Класс для работы с главной страницей."""

    # Локаторы для главной страницы
    USER_AVATAR = (By.CSS_SELECTOR, ".TopNavAvatar__image")
    USER_MENU = (By.CSS_SELECTOR, ".TopNavMenu__profile")
    LOGOUT_BUTTON = (By.XPATH, "//a[contains(text(), 'Выйти')]")
    NEWS_FEED = (By.CSS_SELECTOR, ".feed_row")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    @allure.step("Проверить успешный вход")
    def is_user_logged_in(self):
        """Проверка, что пользователь авторизован."""
        try:
            avatar = self.driver.find_element(*self.USER_AVATAR)
            return avatar.is_displayed()
        except:
            return False

    @allure.step("Выполнить выход из системы")
    def logout(self):
        """Выход из аккаунта."""
        try:
            # Клик по меню пользователя
            menu = self.wait.until(EC.element_to_be_clickable(self.USER_MENU))
            menu.click()
            time.sleep(1)

            # Клик по кнопке выхода
            logout = self.wait.until(EC.element_to_be_clickable(self.LOGOUT_BUTTON))
            logout.click()
            return True
        except Exception:
            return False
