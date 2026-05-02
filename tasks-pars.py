import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://future-step.ru" #вынеси в окружение

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def get_soup(url: str) -> BeautifulSoup:
    response = requests.get(url, headers=HEADERS, timeout=20)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def clean_text(text: str) -> str:
    text = text.replace("\xa0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_task_text(soup: BeautifulSoup) -> str:
    condition = soup.select_one(".task-condition")

    if not condition:
        return ""

    block = BeautifulSoup(str(condition), "html.parser")

    # Удаляем блок "Скачать файл", чтобы он не попадал в условие
    for a in block.find_all("a", href=True):
        href = a["href"]

        if "download.php" in href:
            parent = a.find_parent("p")
            if parent:
                parent.decompose()
            else:
                a.decompose()

    # Картинки убираем из текста, но отдельно соберём их в images
    for img in block.find_all("img"):
        img.decompose()

    text = block.get_text("\n", strip=True)

    return clean_text(text)


def extract_images(soup: BeautifulSoup) -> list[str]:
    condition = soup.select_one(".task-condition")

    if not condition:
        return []

    images = []
    #тут получаем изображения в блоке task-condition
    for img in condition.find_all("img"):

        src = img.get("src") or img.get("data-src") or img.get("data-lazy-src")

        if not src:
            continue

        full_url = urljoin(BASE_URL, src)

        if "/wp-content/uploads/" in full_url:
            images.append(full_url)

    return list(dict.fromkeys(images))


def extract_files(soup: BeautifulSoup) -> list[str]:
    condition = soup.select_one(".task-condition")

    if not condition:
        return []

    files = []

    for a in condition.find_all("a", href=True):
        href = a["href"]

        if "download.php" in href or "/uploads/" in href:
            files.append(urljoin(BASE_URL, href))

    return list(dict.fromkeys(files))


def extract_answer(soup: BeautifulSoup) -> str | None:
    answer_block = soup.select_one(".answer pre")

    if answer_block:
        return clean_text(answer_block.get_text(" ", strip=True))

    answer_block = soup.select_one(".answer")

    if answer_block:
        return clean_text(answer_block.get_text(" ", strip=True))

    return None


def parse_task_page(url: str) -> dict:
    soup = get_soup(url)
    #находим заголовки
    title_tag = soup.find(["h1", "h2"])
    title = title_tag.get_text(" ", strip=True) if title_tag else ""

    number_match = re.search(r"№\s*(\d+)", title)
    number = int(number_match.group(1)) if number_match else None

    return {
        "number": number,
        "title": title,
        "task_text": extract_task_text(soup),
        "images": extract_images(soup),
        "files": extract_files(soup),
        "answer": extract_answer(soup)
    }

#поиск задачи по номеру
def find_task_by_number(number: int) -> dict:
    url = f"{BASE_URL}/task/{number}/"
    return parse_task_page(url)

#поиск задачи по типу ну например от 1 до 27
def get_links_by_type(task_type: int) -> list[str]:
    links = set()
    page = 1

    while True:
        if page == 1:
            url = f"{BASE_URL}/task/?task_type%5B%5D=task-{task_type}"
        else:
            url = f"{BASE_URL}/task/page/{page}/?task_type%5B%5D=task-{task_type}"

        soup = get_soup(url)

        found = False

        for a in soup.find_all("a", href=True):
            href = urljoin(BASE_URL, a["href"])

            if re.match(rf"{BASE_URL}/task/\d+/?$", href):
                links.add(href)
                found = True

        if not found:
            break

        page += 1

    return list(links)


def find_tasks_by_type(task_type: int) -> list[dict]:
    links = get_links_by_type(task_type)
    return [parse_task_page(link) for link in links]

#это для тебя просто можно выбрать по типу задачу спарсим или просто по номеру
def manager_ege(mode: str, value: int):
    if mode == "number":
        return find_task_by_number(value)

    if mode == "type":
        return find_tasks_by_type(value)
