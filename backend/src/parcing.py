from datetime import datetime

import requests
from bs4 import BeautifulSoup
import os
import time


#Функция, которая сохраняет текст
def save_content(text: str, file_name: str):

    file_name = datetime.now().strftime('%y.%m.%d.%f_') + file_name + '.txt'

    if not os.path.exists("files/"):
        os.makedirs("files/")

    with open(f'files/{file_name}', 'w', encoding='utf-8') as file:
        file.write(text)


def link_parsing(url: str):
    try:
        response = requests.get(url)
        assert response.status_code == 200
    except:
        raise Exception("Failed to load page")

    soup = BeautifulSoup(response.content, 'html.parser')

    paragraphs = soup.find_all('p')
    article_text = '\n'.join([para.get_text() for para in paragraphs])

    save_content(article_text, 'article')


def main():
    BASE_URL = "https://www.cancer.gov"
    START_URL = f"{BASE_URL}/types"
    CSV_FILE = "pdq_index_requests.csv"
    TEXT_FOLDER = "pdq_texts_requests"

    os.makedirs(TEXT_FOLDER, exist_ok=True)

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    # Получаем главную страницу /types
    resp = requests.get(START_URL, headers=headers)
    soup = BeautifulSoup(resp.content, "html.parser")

    # Получаем все уникальные ссылки на типы рака
    option_tags = soup.select("option[data-link^='/types/']")
    unique_links = []
    seen = set()

    for opt in option_tags:
        link = opt.get("data-link")
        if link and link not in seen:
            seen.add(link)
            unique_links.append(BASE_URL + link)

    for type_url in unique_links:
        print(f"\n🔍 Обработка: {type_url}")
        type_name = type_url.rstrip("/").split("/")[-1]

        try:
            # Получаем страницу типа рака
            resp = requests.get(type_url, headers=headers)
            soup = BeautifulSoup(resp.content, "html.parser")

            # Ищем ссылку на HP-версию
            hp_links = soup.select("a[href*='/hp']")
            hp_url = None
            for a in hp_links:
                href = a.get("href", "")
                if "/types/" in href and "/hp" in href:
                    hp_url = href if href.startswith("http") else BASE_URL + href
                    break

            if not hp_url:
                print("❌ HP-версия не найдена")
                continue

            print(f"🩺 Найдена HP-версия: {hp_url}")
            time.sleep(0.5)

            link_parsing(hp_url)


        except Exception as e:
            print(f"❌ Ошибка на {type_url}: {e}")


if __name__ == '__main__':
    main()