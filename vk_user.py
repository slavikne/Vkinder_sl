import requests


class VkUser:
    # Класс для работы с Вконтакте
    def __init__(self, token):
        self.token = token

    def get_info_user(self, user):
        """Метод получает информацию о пользователе  Вконтакте """
        params = {
            'user_ids': user,
            'fields': 'city,sex,relation,bdate',
            'access_token': self.token,
            'v': '5.131'
        }
        URL = 'https://api.vk.com/method/users.get'
        list_params = []
        res_vk = requests.get(URL, params=params)
        # print(res_vk.json())
        info_user = res_vk.json()['response']
        print()

        if info_user[0].get('city') is None:
            get_city = None
        else:
            get_city = info_user[0]['city']['id']
        if info_user[0].get('bdate') is None:
            bdate = None
        else:
            bdate = info_user[0].get('bdate')
        list_params.append(info_user[0].get('id'))
        list_params.append(info_user[0].get('first_name'))
        list_params.append(info_user[0].get('last_name'))
        list_params.append(get_city)
        list_params.append(info_user[0].get('sex'))
        list_params.append(bdate)
        return list_params

    def user_search(self, search_param):
        """Метод создает список найденных пользователей"""
        params_search = {
            'count': 1000,
            'sex': search_param[4],
            'birth_year': search_param[5],
            'city': search_param[3],
            'status': 1,
            'fields': 'city,sex,relation,bdate',
            'access_token': self.token,
            'v': '5.131'
        }
        URL = 'https://api.vk.com/method/users.search'
        found_users = []
        res_vk = requests.get(URL, params=params_search)
        info_users = res_vk.json()
        if len(res_vk.json()['response']['items']) > 1:
            for user in info_users['response']['items']:
                if user.get('city') is not None:
                    if user['city']['id'] == search_param[3]:
                        if user['is_closed'] == False:
                            found_users.append([user['id'], user['first_name'], user['last_name']])
        else:
            found_users = None
        return found_users

    def get_id_city(self, city):
        """Метод возвращает id города"""
        params_city = {
            'country_id': 1,
            'count': 1,
            'q': city,
            'access_token': self.token,
            'v': '5.131'
        }
        res_vk = requests.get('https://api.vk.com/method/database.getCities', params=params_city)
        if len(res_vk.json()['response']['items']) < 1:
            id_city = None
        else:
            id_city = res_vk.json()['response']['items'][0]['id']
        return id_city

    def get_photo_found_users(self, id_found_user):
        """Метод возвращает список фотографий найденных пользователей"""
        params_photo = {
            'owner_id': id_found_user,
            'extended': 1,
            'album_id': 'profile',
            'access_token': self.token,
            'v': '5.131'
        }
        URL = 'https://api.vk.com/method/photos.get'
        list_url_on_img = []
        res_vk = requests.get(URL, params=params_photo)
        info_photos = res_vk.json()['response']['items']
        for photo in info_photos:
            count_likes = photo['likes']['count']
            id_photo = photo['id']
            owner_id = photo['owner_id']
            list_url_on_img.append({'id_photo': id_photo, 'owner_id': owner_id, 'count_likes': count_likes})
            list_url_on_img.sort(key=lambda d: d['count_likes'], reverse=True)   # сортируем фото по количеству лайков
        return list_url_on_img[:3]



