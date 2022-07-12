"""
В нашей школе мы не можем разглашать персональные данные пользователей, но
чтобы преподаватель и ученик смогли объяснить нашей поддержке, кого они имеют в
виду (у преподавателей, например, часто учится несколько Саш), мы генерируем
пользователям уникальные и легко произносимые имена. Имя у нас состоит из
прилагательного, имени животного и двузначной цифры. В итоге получается,
например, "Перламутровый лосось 77". Для генерации таких имен мы и решали
следующую задачу:
Получить с русской википедии список всех животных и вывести количество животных
на каждую букву алфавита. Результат должен получиться в следующем виде:
А: 642
Б: 412
В:....


Для получения списка животных использовался API Википедии. Эту задачу можно
решить другим путём, если дополнительно использовать BeautifulSoup и парсить
полученные страницы.

При конечном выводе сначала идут буквы A-Z, а потом кириллица. При этом буква Ё
стоит до А.
"""

import requests

URL = "https://ru.wikipedia.org/w/api.php"
PARAMS = {
    "action": "query",
    "list": "categorymembers",
    "cmlimit": "max",
    "format": "json",
    "cmtype": "page",
    "cmtitle": "Категория:Животные по алфавиту"
}


def get_pages(session: requests.Session, cmcontinue: str = None):
    params = PARAMS
    if cmcontinue:
        params["cmcontinue"] = cmcontinue

    response = session.get(url=URL, params=params)
    data = response.json()

    if "continue" in data:
        continue_token = data["continue"]["cmcontinue"]
    else:
        continue_token = None
    titles = (t["title"] for t in data["query"]["categorymembers"])

    return continue_token, titles


def get_titles():
    session = requests.session()
    titles = []
    cmcontinue = None

    while True:
        cmcontinue, new_titles = get_pages(session, cmcontinue)

        titles.extend(new_titles)
        if not cmcontinue:
            break

    return titles


def count_titles(titles):
    counts = {}

    for t in titles:
        key = t[0]

        if key in counts:
            counts[key] += 1
        else:
            counts[key] = 1

    return counts


def print_counts(counts: dict):
    for key, val in sorted(counts.items()):
        print(f"{key}: {val}")


def main():
    titles = get_titles()
    counts = count_titles(titles)

    print_counts(counts)


if __name__ == "__main__":
    main()
