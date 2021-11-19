from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_user import VkUser
from vk_bot import VkBot
from db_vkinder import DB

with open('token_vk_group.txt', 'r') as file_object:
    token_vk_group = file_object.read().strip()
with open('token_vk_user.txt', 'r') as file_object:
    token_vk_user = file_object.read().strip()

vk = vk_api.VkApi(token=token_vk_group)
longpoll = VkLongPoll(vk)

vkuser = VkUser(token_vk_user)
vkbot = VkBot()
db = DB()


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7), })


def photo_msg(user_id, found_user_id, id_photo):
    vk.method('messages.send',
              {'user_id': user_id, 'attachment': f'photo{found_user_id}_{id_photo}', 'random_id': randrange(10 ** 7)})


def get_param_city(user_id):
    """Функция получает id города для поиска """
    write_msg(user_id, f"Ой, для поиска не хватает данных")
    write_msg(user_id, f"Введите город поиска")
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                city_user = event.text
                if vkuser.get_id_city(city_user) is None:
                    write_msg(user_id, f"Город не найден, попробуй еще раз")
                else:
                    return vkuser.get_id_city(city_user)


def get_param_year(user_id):
    """Функция получает год рождения для поиска """
    write_msg(user_id, f"Ой, для поиска не хватает данных")
    write_msg(user_id, f"Введите год своего рождения")
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                year = event.text
                if (year.isdigit() == False) or (len(year) < 4) or (int(year) < 1900):
                    write_msg(user_id, f"Год задан неверно, попробуй еще раз ")
                else:
                    return year


def processing_parameters(user_id):
    """Функция подготавливает параметры  для поиска"""

    params_search = vkuser.get_info_user(user_id)
    if params_search[3] is None:
        params_search[3] = get_param_city(user_id)

    # Проверка года рождения пользователя
    if params_search[5] is None or len(params_search[5].split('.')) < 3:
        year_user = get_param_year(user_id)
    else:
        year_user = params_search[5].split('.')[2]
    params_search[5] = year_user

    # Преобразование параметра пол пользователя на противоположное значение
    if params_search[4] == 1:
        params_search[4] = 2
    elif params_search[4] == 2:
        params_search[4] = 1

    return params_search


def show_result_search(result_found, user_id):
    """Функция выводит результаты поиска"""

    sample = 0
    for search_user in result_found:
        
        # Проверка на наличие пользователя в базе  и в черном списке
        query_select = db.select_db(search_user[0], user_id)
        query_select_in_bl = db.select_bl(search_user[0], user_id)
        if query_select == True and query_select_in_bl == True:
            sample += 1
            db.added_user(search_user[0])

            # Добавление результата поиска в БД
            db.added_found_user(search_user[0], user_id)
            # Отправка пользователю сообщения с результатами поиска
            write_msg(user_id, f'{search_user[1]} {search_user[2]}\nhttps://vk.com/id{search_user[0]}')

            photo_param = vkuser.get_photo_found_users(search_user[0])
            i = 0
            while i < len(photo_param):
                photo_msg(user_id, photo_param[i]['owner_id'], photo_param[i]['id_photo'])
                db.added_photo_found_user(photo_param[i]['id_photo'], photo_param[i]['owner_id'])
                i += 1

        # Выход из цикла после вывода 5 результатов поиска
        if sample >= 5:
            sample = 0
            break


def black_list(user_id, message):
    """Функция добавляет пользователя в черный список"""

    write_msg(user_id, f"Ну и кто вам не угодил?\nУкажите id пользователя.")

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                id_in_black_list = event.text
                result = db.added_black_list(id_in_black_list, event.user_id)
                if result:
                    write_msg(user_id, f" {vkbot.bot(message)[0]}")
                    write_msg(event.user_id, f"Готово")
                    break
                else:
                    write_msg(event.user_id, f"Что-то пошло не так, попробуй еще раз.")
                    break


def favorites(user_id, message):
    """Функция добавляет пользователя в избранное"""

    write_msg(user_id, f"Ну и кто вам приглянулся?\nУкажите id пользователя.")
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                id_in_favorites = event.text
                result = db.added_favorites(id_in_favorites, event.user_id)
                if result:
                    write_msg(user_id, f" {vkbot.bot(message)[0]}")
                    write_msg(event.user_id, f"Готово")
                    break
                else:
                    write_msg(event.user_id, f"Что-то пошло не так, попробуй еще раз.")
                    break


def show_favorites(user_id, message):
    """Функция выводит тех кто находится в избранном"""

    write_msg(user_id, f" {vkbot.bot(message)[0]}")
    query_select_in_favorites = db.show_select_favorites(user_id)
    if len(query_select_in_favorites) < 1:
        write_msg(user_id, f"К сожалению список избраных пуст. Сначала добавь туда кого-нибудь.")
    else:
        for favor in query_select_in_favorites:
            write_msg(user_id, f'https://vk.com/id{favor[0]}')
            q_sel_in_ph = db.show_select_photo(favor[0])
            if len(q_sel_in_ph) > 0:
                photo_msg(user_id, q_sel_in_ph[0][1], q_sel_in_ph[0][0])


def main():
    for event in longpoll.listen():

        if event.type == VkEventType.MESSAGE_NEW:

            if event.to_me:
                if vkbot.bot(event.text)[1] == 'hello':
                    write_msg(event.user_id, f" {vkbot.bot(event.text)[0]} {vkuser.get_info_user(event.user_id)[1]}")
                elif vkbot.bot(event.text)[1] == 'familiarity':

                    # Добавление пользователя в БД
                    db.added_user(event.user_id)
                    write_msg(event.user_id, f" {vkbot.bot(event.text)[0]}")

                    # Проверка на наличие данных в результате поиска
                    p_s = processing_parameters(event.user_id)
                    if vkuser.user_search(p_s) is not None:
                        res_found = vkuser.user_search(p_s)

                        # Вывод результатов поиска
                        show_result_search(res_found, event.user_id)

                    else:
                        write_msg(event.user_id, f'К сожалению я никого не нашел,\n'
                                                 f'попробуй еще раз и измени параметры поиска')
                # Добавление в черный список
                elif vkbot.bot(event.text)[1] == 'black_list':
                    black_list(event.user_id, event.text)

                elif vkbot.bot(event.text)[1] == 'show_favorites':
                    show_favorites(event.user_id, event.text)

                # Добавление в избранное
                elif vkbot.bot(event.text)[1] == 'favorites':
                    favorites(event.user_id, event.text)

                else:
                    write_msg(event.user_id, f" {vkbot.bot(event.text)[0]}")


if __name__ == '__main__':
    main()
