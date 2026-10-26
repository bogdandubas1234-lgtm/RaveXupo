"""Android Rave automation through Appium; selectors must match the installed app."""
import os
import threading
import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

PACKAGE = os.getenv("RAVE_APP_PACKAGE", "com.wemesh.android")
APPIUM_URL = os.getenv("APPIUM_URL", "http://127.0.0.1:4723")
DEVICE_NAME = os.getenv("ANDROID_DEVICE", "Android Emulator")
CHAT_MESSAGES_XPATH = os.getenv("RAVE_CHAT_MESSAGES_XPATH", "")
CHAT_INPUT_ID = os.getenv("RAVE_CHAT_INPUT_ID", "")
CHAT_SEND_ID = os.getenv("RAVE_CHAT_SEND_ID", "")

class RaveAndroid:
    def __init__(self):
        options = UiAutomator2Options()
        options.platform_name = "Android"
        options.automation_name = "UiAutomator2"
        options.device_name = DEVICE_NAME
        options.new_command_timeout = 300
        self.driver = webdriver.Remote(command_executor=APPIUM_URL, options=options)
        self.driver.activate_app(PACKAGE)
        self._lock = threading.RLock()

    def join(self, url: str):
        if not url.startswith(("https://rave.link/", "https://rave.com/", "https://rave.watch/")):
            raise ValueError("Нужна ссылка комнаты Rave (rave.link / rave.com / rave.watch).")
        with self._lock:
            self.driver.execute_script("mobile: deepLink", {"url": url, "package": PACKAGE})
            time.sleep(5)
            self.driver.activate_app(PACKAGE)

    def send(self, text: str):
        if not CHAT_INPUT_ID or not CHAT_SEND_ID:
            raise RuntimeError("Не настроены RAVE_CHAT_INPUT_ID и RAVE_CHAT_SEND_ID. Отправьте /dumpui и укажите реальные элементы интерфейса в .env.")
        with self._lock:
            field = self.driver.find_element(AppiumBy.ID, CHAT_INPUT_ID)
            field.click()
            field.send_keys(text)
            self.driver.find_element(AppiumBy.ID, CHAT_SEND_ID).click()

    def messages(self):
        if not CHAT_MESSAGES_XPATH:
            return []
        with self._lock:
            return [e.text.strip() for e in self.driver.find_elements(AppiumBy.XPATH, CHAT_MESSAGES_XPATH) if e.text and e.text.strip()]

    def screenshot(self) -> bytes:
        with self._lock:
            return self.driver.get_screenshot_as_png()

    def dump_ui(self) -> str:
        with self._lock:
            return self.driver.page_source

    def leave(self):
        with self._lock:
            self.driver.activate_app(PACKAGE)

    def close(self):
        with self._lock:
            self.driver.quit()
