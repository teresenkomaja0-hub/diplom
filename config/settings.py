# config/settings.py
"""Настройки окружения для тестов"""
import os

# Базовые URL
BASE_URL = "https://vk.com"
VK_DEV_URL = "https://dev.vk.com/ru"
VK_TERMS_URL = "https://vk.com/terms"
VK_MINI_APPS_URL = "https://dev.vk.com/ru/mini-apps/overview"

# URL с параметрами
VK_WITH_PARAM_URL = "https://vk.com/?to=YXVkaW8-"
VK_SPECIAL_URL = "https://vk.com/?ysclid=mmrc2zy0od537749998"  # Новый URL для 4 и 5 тестов

# Настройки браузера
BROWSER_WIDTH = 1920
BROWSER_HEIGHT = 1080
IMPLICIT_WAIT = 10
EXPLICIT_WAIT = 15

# Пути для сохранения скриншотов при ошибках
ERROR_SCREENSHOT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "error_screenshots")