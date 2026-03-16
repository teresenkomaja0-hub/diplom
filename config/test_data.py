"""Тестовые данные для автотестов"""
from selenium.webdriver.common.by import By

# Данные для авторизации (используйте тестовый аккаунт!)
TEST_USER = {
    "login": "логин",  # замените на свой
    "password": "пароль",  

    "phone": "+7 123 456 78 90",  # Теперь с пробелами, как форматирует VK
    "phone_raw": "+71234567890",
    "peer_id": 209793519,      # ВАЖНО: число, а не строка!
    "name": "Test User"
}

# Невалидные данные
INVALID_USER = {
    "login": "invalid@test.com",
    "password": "wrong_password"
}

# Токен для API (получите отдельный для тестов)
API_TOKEN = "vk1.a.F10Fr3VaFOU6Caxp3bpixvIR0lu9ua5Xn8ilGOoX4U5SCuAMqhIcdnCksQh5Tr0cfaJ6lPGtVoTdw5SoN76bu-LcWcjRSJrpauIqVitS4cMBVp48F5xgPJKBPl10Cs8x0sgZdsZp903tpqSOaGvey1_kiEk1nJRgCh88BL_ryWNHtmXcG9VHDT9arcS6bVLS1GodbRaJUHOCa8oJNeeN2A"

# Тестовые сообщения
TEST_MESSAGES = {
    "cyrillic": "QA спрашивает у QA: какова твоя профессия?",
    "latin": "Hello, World!",
    "numbers": "9999999999999999999",
    "empty": "",
    "long": "A" * 1000
}

# Ожидаемые тексты для кнопок и ссылок
EXPECTED_TEXTS = {
    'login_button': [
        "Войти другим способом", 
        "Other sign-in options", 
        "Другим способом", 
        "Sign in with another way"
    ],
    'terms_link': [
        "Условия использования", 
        "Terms of Use", 
        "Условия", 
        "Terms"
    ],
    'dev_link': [
        "VK Developers", 
        "Разработчикам", 
        "Developers", 
        "Для разработчиков", 
        "VK API"
    ],
    'mini_apps_title': [
        "Мини-приложения", 
        "Обзор", 
        "Mini Apps", 
        "Overview"
    ],
    'language_selector': [
        "Русский", 
        "English", 
        "Language",
        "汉语"
    ]
}

# Локаторы элементов (вынесены для удобства поддержки)
LOCATORS = {
    'login_button': (By.XPATH, "//*[@id='START_QR_PAGE']/div/div[2]/div/button[1]"),
    'phone_input': (By.XPATH, "//*[@id='ENTER_LOGIN_PAGE']/div/form/div[1]/div[3]/span/div/div[2]/input"),
    'qr_element': (By.XPATH, "//*[contains(@class, 'qr') or contains(@src, 'qrcode') or contains(@alt, 'QR')]"),
    'terms_link': (By.XPATH, "/html/body/div[15]/div/div/div/div[4]/div/div/div[1]/div/div[3]/a"),
    'dev_link': (By.XPATH, "/html/body/div[15]/div/div/div/div[4]/div/div/div[2]/div/div[2]/a"),
    
    # Локаторы для выбора языка
    'language_selector': (By.XPATH, "/html/body/div[15]/div/div/div/div[4]/div/div/div[3]/div/div/a/span"),
    'chinese_language': (By.XPATH, "//*[@id='all_languages_list']/div[4]/div[16]/a/span"),  # Китайский язык (汉语)
    'language_menu': (By.XPATH, "//*[@id='all_languages_list']"),
    
    # Альтернативные локаторы для китайского языка
    'chinese_language_by_text': (By.XPATH, "//*[@id='all_languages_list']//a/span[contains(text(), '汉语') or contains(text(), '中文') or contains(text(), 'Chinese')]"),
    
    # Локаторы для мини-приложений
    'overview_link_1': (By.XPATH, "//a[contains(@href, '/ru/mini-apps/overview') or contains(text(), 'Обзор')]"),
    'overview_link_2': (By.XPATH, "//*[@id='panel']/div/div[2]/main/div/section[2]/div[2]/div/div[5]/div/footer/a[2]"),
    'h1_overview': (By.XPATH, "//h1[contains(text(), 'Обзор') or contains(text(), 'Overview')]"),
    'dev_logo': (By.XPATH, "//*[contains(@class, 'logo') or contains(@class, 'header') or contains(text(), 'VK Developers')]"),
    'nav_menu': (By.XPATH, "//nav | //*[contains(@class, 'nav') or contains(@class, 'menu')]"),
    
    # Дополнительные локаторы для мини-приложений
    'mini_apps_link': (By.XPATH, "//a[contains(@href, 'mini-apps') or contains(text(), 'Мини-приложения') or contains(text(), 'Mini Apps')]"),
    'docs_link': (By.XPATH, "//a[contains(@href, 'docs') or contains(text(), 'Документация') or contains(text(), 'Documentation')]"),
}