from telegram.ext import ConversationHandler
import json
from check_if_not_registered_func import check_if_not_registered

async def delete(update, context):
    if check_if_not_registered(update, context):
        await update.message.reply_text("Вы не зарегистрированы!")
        return ConversationHandler.END #Сообщаем, если пользователь не зарегистрирован и завершаем диалог
    file = open("database_users.json", "r", encoding="utf-8")
    all_questions = json.load(file)
    questions = all_questions[str(update.message.from_user.id)]
    file.close()
    line = ""
    name = all_questions[str(update.message.from_user.id)]["name"] #Имя пользователя
    for i in range (1, len(questions) - 1): #Красивый список вопросов
        if i != "age" and i != "name":
            line += f"{i}: {questions[str(i)]}\n"
    await update.message.reply_text(f"{name}, какой вопрос Вы бы хотели убрать? Введите номер вопроса.\n"
                                    f"{line}")
    return 2

async def delete_complete(update, context):
    key = update.message.text #Номер удаляемого вопроса
    file = open("database_users.json", "r", encoding="utf-8")
    all_questions = json.load(file)
    questions = all_questions[str(update.message.from_user.id)] #имеющиеся вопросы
    file.close()
    if key not in questions.keys(): #Ошибка в случае неправильного номера
        await update.message.reply_text("Вопрос с таким номером не существует. Повторите попытку.")
        return 2
    del questions[key] #Удаление вопроса
    new_questions = dict()
    new_key = 1
    for ind, question in questions.items(): #Сдвигаем нумерацию
        if ind != "age" and ind != "name":
            new_questions[new_key] = question
            new_key += 1
    new_questions["name"] = questions["name"] #Сохраняем имя и возраст
    new_questions["age"] = questions["age"]
    all_questions[str(update.message.from_user.id)] = new_questions #Обновляем базу данных
    file = open("database_users.json", "w", encoding="utf-8")
    json.dump(all_questions, file,  indent=4, ensure_ascii=False)
    file.close()
    await update.message.reply_text("Вопрос удалён.")
    return ConversationHandler.END