"""API тесты для VK."""

import pytest
import requests
import allure
from configs.env import API_BASE_URL, API_VERSION
from configs.test_data import API_TOKEN, TEST_MESSAGES, TEST_USER


@allure.epic("API тесты VK")
@allure.feature("Сообщения")
class TestMessagesAPI:
    """Тестирование методов работы с сообщениями."""

    def setup_method(self):
        """Подготовка перед каждым тестом."""
        self.base_params = {
            "v": API_VERSION,
            "access_token": API_TOKEN,
            "peer_id": TEST_USER["peer_id"]
        }

    @allure.story("Отправка сообщений")
    @allure.title("Отправка сообщения на кириллице")
    @pytest.mark.api
    @pytest.mark.smoke
    def test_send_cyrillic_message(self):
        """Тест отправки сообщения на кириллице."""
        with allure.step("Подготовка параметров запроса"):
            params = {
                **self.base_params,
                "message": TEST_MESSAGES["cyrillic"],
                "random_id": 123456
            }

        with allure.step("Отправка POST запроса"):
            response = requests.post(
                f"{API_BASE_URL}/messages.send",
                params=params,
                timeout=10
            )

        with allure.step("Проверка ответа"):
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            assert "response" in response.json(), "Response should contain 'response' field"
            
            allure.attach(
                str(response.json()),
                name="response_body",
                attachment_type=allure.attachment_type.JSON
            )

    @allure.story("Отправка сообщений")
    @allure.title("Отправка сообщения с цифрами")
    @pytest.mark.api
    def test_send_numbers_message(self):
        """Тест отправки сообщения с цифрами."""
        with allure.step("Подготовка параметров запроса"):
            params = {
                **self.base_params,
                "message": TEST_MESSAGES["numbers"],
                "random_id": 123457
            }

        with allure.step("Отправка запроса"):
            response = requests.post(
                f"{API_BASE_URL}/messages.send",
                params=params,
                timeout=10
            )

        with allure.step("Проверка ответа"):
            assert response.status_code == 200
            assert "response" in response.json()

    @allure.story("Отправка сообщений")
    @allure.title("Отправка пустого сообщения (негативный)")
    @pytest.mark.api
    @pytest.mark.negative
    def test_send_empty_message(self):
        """Тест отправки пустого сообщения (ожидаем ошибку)."""
        with allure.step("Подготовка параметров запроса"):
            params = {
                **self.base_params,
                "message": TEST_MESSAGES["empty"],
                "random_id": 123458
            }

        with allure.step("Отправка запроса"):
            response = requests.post(
                f"{API_BASE_URL}/messages.send",
                params=params,
                timeout=10
            )

        with allure.step("Проверка ошибки"):
            assert response.status_code == 200
            response_json = response.json()
            assert "error" in response_json
            assert response_json["error"]["error_code"] == 100
            assert "empty" in response_json["error"]["error_msg"].lower()

    @allure.story("Отправка сообщений")
    @allure.title("Отправка сообщения без токена (негативный)")
    @pytest.mark.api
    @pytest.mark.negative
    def test_send_without_token(self):
        """Тест отправки сообщения без токена авторизации."""
        with allure.step("Подготовка параметров запроса"):
            params = {
                "v": API_VERSION,
                "peer_id": TEST_USER["peer_id"],
                "message": TEST_MESSAGES["cyrillic"],
                "random_id": 123459
            }

        with allure.step("Отправка запроса"):
            response = requests.post(
                f"{API_BASE_URL}/messages.send",
                params=params,
                timeout=10
            )

        with allure.step("Проверка ошибки авторизации"):
            assert response.status_code == 200
            response_json = response.json()
            assert "error" in response_json
            assert response_json["error"]["error_code"] == 5

    @allure.story("Получение сообщений")
    @allure.title("Получение истории сообщений")
    @pytest.mark.api
    def test_get_messages_history(self):
        """Тест получения истории сообщений с пользователем."""
        with allure.step("Подготовка параметров запроса"):
            params = {
                "v": API_VERSION,
                "access_token": API_TOKEN,
                "peer_id": TEST_USER["peer_id"],
                "count": 20
            }

        with allure.step("Отправка запроса"):
            response = requests.get(
                f"{API_BASE_URL}/messages.getHistory",
                params=params,
                timeout=10
            )

        with allure.step("Проверка ответа"):
            assert response.status_code == 200
            response_json = response.json()
            assert "response" in response_json
            assert "items" in response_json["response"]
            assert isinstance(response_json["response"]["items"], list)