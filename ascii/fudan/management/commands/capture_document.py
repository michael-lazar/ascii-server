import os
from time import sleep

from django.conf import settings
from django.core.management.base import BaseCommand
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class Command(BaseCommand):
    help = "Captures screenshots of a specified webpage"

    def add_arguments(self, parser):
        parser.add_argument(
            "url",
            type=str,
            help="The URL of the webpage to capture",
        )
        parser.add_argument(
            "--font-size",
            type=int,
            default=24,
            help="Font size in pixels",
        )
        parser.add_argument(
            "--output-dir",
            type=str,
            default=os.path.join(settings.DATA_ROOT, "screenshots"),
            help="Directory to save the screenshots",
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting the screenshot capture process"))

        output_dir = options["output_dir"]
        os.makedirs(output_dir, exist_ok=True)

        width = options["font_size"] * 41
        height = options["font_size"] * 22

        driver = self.setup_driver(options["url"])
        sleep(1)  # Allow page to load

        # Adjust window size to ensure the viewport size is correct
        inner_height = driver.execute_script("return window.innerHeight")
        outer_height = driver.execute_script("return window.outerHeight")

        chrome_height = outer_height - inner_height

        # Set the window size to account for the chrome
        driver.set_window_size(width, height + chrome_height)

        scroll_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("return document.body.style.overflow = 'hidden';")

        current_scroll_position = 0
        screenshot_count = 0

        while current_scroll_position < scroll_height:
            driver.execute_script(f"window.scrollTo(0, {current_scroll_position})")
            sleep(0.1)  # Allow scroll to finish
            file_path = os.path.join(output_dir, f"screenshot_{screenshot_count}.png")
            driver.save_screenshot(file_path)
            self.stdout.write(self.style.SUCCESS(f"Saved {file_path}"))

            current_scroll_position += height
            screenshot_count += 1

        driver.quit()

    def setup_driver(self, url):
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)
        return driver
