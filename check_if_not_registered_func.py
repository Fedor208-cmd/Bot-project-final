import json

def check_if_not_registered(update, context):
    usr = str(update.message.from_user.id) #Узнаём ID пользователя
    file = open("database_users.json", "r", encoding="utf-8") #Открываем базу данных и преобразуем в словарь
    ctrl = json.load(file)
    file.close()
    return bool(usr not in ctrl.keys()) #Возвращает True если пользователь не зарегистрирован





