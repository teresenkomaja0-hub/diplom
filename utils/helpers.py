"""Вспомогательные функции."""

import random
import string
import allure


@allure.step("Генерация случайного random_id")
def generate_random_id():
    """Генерация случайного ID для сообщений."""
    return random.randint(1, 1000000)


@allure.step("Генерация тестового сообщения")
def generate_test_message(prefix="Test", length=50):
    """Генерация тестового сообщения заданной длины."""
    letters = string.ascii_letters + string.digits + " "
    return prefix + " " + ''.join(random.choice(letters) for _ in range(length))


def attach_screenshot(driver, name="screenshot"):
    """Прикрепление скриншота к отчету Allure."""
    allure.attach(
        driver.get_screenshot_as_png(),
        name=name,
        attachment_type=allure.attachment_type.PNG
    )