import requests
import csv
import json

from datetime import datetime


class FriendsManager:
    def __init__(self):
        self.friend_list = []

    def save_friends_list_json(self, file_name="report.json"):
        self.friend_list.sort(key=lambda x: x['first_name'])
        json_object = json.dumps(self.friend_list)
        with open(file_name, "w") as outfile:
            outfile.write(json_object)

    def get_friends_list(self, user_id, access_token):
        # URL для выполнения запроса к VK API для получения списка друзей
        url = f"https://api.vk.com/method/friends.get?user_id={user_id}&access_token={access_token}&v=5.131"

        # Выполняем запрос к VK API
        response = requests.get(url)

        # Проверяем, что запрос успешен (статусный код 200)
        if response.status_code == 200:
            # Получаем данные из ответа в формате JSON
            data = response.json()
            # Проверяем, что запрос выполнен успешно без ошибок
            if 'error' in data:
                print("Ошибка при выполнении запроса:", data['error']['error_msg'])
                return []
            else:
                # Извлекаем id наших друзей из данных
                friends_list = data['response']['items']
                return friends_list
        else:
            print("Ошибка при выполнении запроса:", response.status_code)
            return []

    def get_user_info(self, user_ids, access_token):
        # Преобразуем список ID друзей в строку  для запроса VK API
        user_ids_str = ','.join(str(id) for id in user_ids)

        # URL для выполнения запроса к VK API для получения информации о пользователях
        url = f"https://api.vk.com/method/users.get?user_ids={user_ids_str}&fields=first_name,last_name,country,city," \
              f"bdate,sex&access_token={access_token}&v=5.131 "

        # Выполняем запрос к VK API
        response = requests.get(url)

        # Проверяем, что запрос успешен (статусный код 200)
        if response.status_code == 200:
            # Получаем данные из ответа в формате JSON
            data = response.json()

            # Проверяем, что запрос выполнен успешно без ошибок
            if 'error' in data:
                print("Ошибка при выполнении запроса:", data['error']['error_msg'])
                return []
            else:
                for i in data['response']:
                    self.friend_list.append(i)
                # Возвращаем список данных о пользователях
                return data['response']

        else:
            print("Ошибка при выполнении запроса:", response.status_code)
            return []

    def save_friends_to_csv(self, filename="report.csv"):
        # Открываем CSV файл для записи
        with open(filename, mode='w', encoding='utf-8-sig', newline='') as file:
            # Создаем объект для записи данных в CSV файл
            writer = csv.writer(file, delimiter=";")

            # Записываем заголовки столбцов
            writer.writerow(['Имя', 'Фамилия', 'Страна', 'Город', 'Дата рождения', 'Пол'])
            self.friend_list.sort(key=lambda x: x['first_name'])
            # Записываем данные о друзьях

            for friend in self.friend_list:
                # Проверяем наличие данных о стране и городе, так как они могут быть не указаны
                country = friend.get('country', {}).get('title', '')
                city = friend.get('city', {}).get('title', '')
                gender = {2: "мужской", 1: "женский", 0: "неизвестно"}
                # Записываем информацию о друзьях в CSV файл
                date_obj = None
                try:
                    # Пробуем преобразовать введенную строку в объект даты с ожидаемым форматом
                    date_obj = datetime.strptime(friend.get('bdate', ''), '%d.%m.%Y').strftime("%Y.%m.%d")
                except ValueError:
                    print("Ошибка! Дата не соответствует формату ДД.ММ.ГГГГ")
                finally:
                    writer.writerow([friend['first_name'] if friend['first_name'] else 'неизвестно',
                                     friend['last_name'] if friend['last_name'] else 'неизвестно',
                                     country if country else 'неизвестно',
                                     city if city else 'неизвестно',
                                     date_obj if date_obj else "неизвестно",
                                     gender[friend.get('sex', '')]])

    def save_friends_to_tsv(self, tsv_filename, filename="report.csv"):

        with open(filename, 'r', encoding='utf-8-sig') as csv_file, open(tsv_filename, 'w',
                                                                         encoding='utf-8-sig') as tsv_file:
            # Читаем каждую строку из CSV файла
            for line in csv_file:
                # Заменяем запятые на табуляции и записываем в TSV файл
                tsv_line = line.replace(';', '\t')
                tsv_file.write(tsv_line)
