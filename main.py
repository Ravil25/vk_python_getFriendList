import webbrowser
import requests

from settings import CLIENT_URL
from domain.vk_api.friends import FriendsManager

if __name__ == "__main__":
    default_filename_csv = 'report.csv'
    default_filename_json = 'report.json'
    default_filename_tsv = 'report.tsv'

    response = requests.get(CLIENT_URL)
    webbrowser.open(response.url)
    friends_manager = FriendsManager()

    access_token = input("Введите скопированный access token\n")
    user_id = int(input("Введите id пользователя\n"))

    friends_list_ids = friends_manager.get_friends_list(user_id, access_token)
    friends_info = friends_manager.get_user_info(friends_list_ids, access_token)

    preferred_format = input("В каком формате вывести отчет?(csv - 1, tsv - 2, json - 3)\n")

    if preferred_format == "1":
        file_path = input("Укажите путь к файлу. Пример: C:\\Users\\user\\Desktop\\report.csv\n")
        if file_path == "":
            friends_manager.save_friends_to_csv(default_filename_csv)
            print(f'Отчет сохранен в файл: {default_filename_csv}')
        else:
            friends_manager.save_friends_to_csv(file_path)
            print(f'Отчет сохранен в файл: {file_path}')
    elif preferred_format == "2":
        file_path = input("Укажите путь к файлу. Пример: C:\\Users\\user\\Desktop\\report.tsv\n")
        if file_path == "":
            friends_manager.save_friends_to_tsv(default_filename_tsv)
            print(f'Отчет сохранен в файл: {default_filename_tsv}')
        else:
            friends_manager.save_friends_to_tsv(file_path)
            print(f'Отчет сохранен в файл: {file_path}')
    elif preferred_format == "3":
        file_path = input("Укажите путь к файлу. Пример: C:\\Users\\user\\Desktop\\report.json\n")
        if file_path == "":
            friends_manager.save_friends_list_json(default_filename_json)
            print(f'Отчет сохранен в файл: {default_filename_json}')
        else:
            friends_manager.save_friends_list_json(file_path)
            print(f'Отчет сохранен в файл: {file_path}')
    else:
        file_path = input("Укажите путь к файлу. Пример: C:\\Users\\user\\Desktop\\report.csv\n")
        if file_path == "":
            friends_manager.save_friends_to_csv(default_filename_csv)
            print(f'Отчет сохранен в файл: {default_filename_csv}')
        else:
            friends_manager.save_friends_to_csv(file_path)
            print(f'Отчет сохранен в файл: {file_path}')



