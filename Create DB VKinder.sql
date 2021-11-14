create table Users_Vk(
id serial primary key
);


create table Found_Users(
FU_VK_id integer  references Users_Vk(id),
U_VK_id integer  references Users_Vk(id),
constraint PK_FU primary key (FU_VK_id, U_VK_id)
);

create table Black_list(
FU_BL_id integer references Users_Vk(id),
U_VK_id integer  references Users_Vk(id),
constraint PK_BL primary key (FU_BL_id, U_VK_id)
);

create table Favorites(
FU_FV_id integer references Users_Vk(id),
U_VK_id integer  references Users_Vk(id),
constraint PK_FV primary key (FU_FV_id, U_VK_id)
);

create table Photos(
id_photo integer primary key,
U_VK_id integer  references Users_Vk(id)
);

