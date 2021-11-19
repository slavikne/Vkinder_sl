import psycopg2
import sqlalchemy


class DB:

    def __init__(self):
        engine = sqlalchemy.create_engine('postgresql+psycopg2://postgres:123456@localhost:5432/db_vkinder')
        self.connection = engine.connect()

    def added_user(self, id_user):
        res = self.connection.execute(f"""select id from users_vk
                where id = {id_user};""").fetchall()
        if len(res) < 1:
            self.connection.execute(f"""insert into users_vk values({id_user});""")

    def added_found_user(self, id_found_user, id_user):
        res = self.connection.execute(f"""select fu_vk_id, u_vk_id from found_users
                                        where fu_vk_id = {id_found_user} and 
                                        u_vk_id = {id_user};""").fetchall()

        if len(res) < 1:
            self.connection.execute(f"""insert into found_users values({id_found_user},{id_user});""")

    def added_photo_found_user(self, id_photo, id_found_user):
        res = self.connection.execute(f"""select id_photo, u_vk_id from photos
                                        where id_photo = {id_photo} ;""").fetchall()

        if len(res) < 1:
            self.connection.execute(f"""insert into photos values({id_photo},{id_found_user});""")

    def select_db(self, id_found_user, id_user):
        res = self.connection.execute(f"""select fu_vk_id, u_vk_id from found_users
                                                where fu_vk_id = {id_found_user} and 
                                                u_vk_id = {id_user};""").fetchall()
        if len(res) < 1:
            return True
        else:
            return False

    def select_bl(self, id_found_user, id_user):
        res = self.connection.execute(f"""select fu_bl_id, u_vk_id from black_list
                                                where fu_bl_id = {id_found_user} and 
                                                u_vk_id = {id_user};""").fetchall()
        if len(res) < 1:
            return True
        else:
            return False

    def added_black_list(self, id_found_user, id_user):
        try:
            res = self.connection.execute(f"""select fu_bl_id, u_vk_id from black_list
                                                    where fu_bl_id = {id_found_user} and 
                                                    u_vk_id = {id_user};""").fetchall()

            if len(res) < 1:
                self.connection.execute(f"""insert into black_list values({id_found_user},{id_user});""")
            return True
        except:
            return False

    def added_favorites(self, id_found_user, id_user):
        try:
            res = self.connection.execute(f"""select fu_fv_id, u_vk_id from favorites
                                                    where fu_fv_id = {id_found_user} and 
                                                    u_vk_id = {id_user};""").fetchall()
            if len(res) < 1:
                self.connection.execute(f"""insert into favorites values({id_found_user},{id_user});""")
            return True
        except:
            return False

    def show_select_favorites(self, id_user):
        res = self.connection.execute(f"""select fu_fv_id, u_vk_id from favorites
                                        where u_vk_id = {id_user};""").fetchall()

        return res

    def show_select_photo(self, id_user):
        res = self.connection.execute(f"""select id_photo, u_vk_id from photos
                                                where u_vk_id = {id_user}
                                                limit 1;""").fetchall()
        return res

    # def cleaning_DB(self):
