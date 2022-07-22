from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from States_music_bot import States
import json

bot = Bot(token="5214806664:AAGPEY-Vkq6qmnV04P3AJjwEwetT59M4YWM", parse_mode='html')
dp = Dispatcher(bot, storage=MemoryStorage())

"""defs"""

info = {"users": []}


# with open("users.json", "w") as file:
#     json.dump(info, file, indent=3)

# inf = {"nickname": "",
#        "user_id": "",
#        "number_of_posts":"",
#        "subscribers": []}


def reader():
    with open("users.json", "r") as file:
        inf = json.load(file)
    return inf


def adder(inf):
    with open("users.json", "w") as file:
        json.dump(inf, file, indent=3)


def change_nickname(user_id: int, new_nick: str):
    inf = reader()
    for i in inf["users"]:
        if i["user_id"] == user_id:
            i["nickname"] = new_nick
            break
    adder(inf)


def unsubscribe(first_user_id, second_user_id):
    inf = reader()
    for i in range(len(inf["users"])):
        if inf["users"][i]["user_id"] == first_user_id:
            for j in inf["users"][i]["subscribed"]:
                if j == second_user_id:
                    inf["users"][i]["subscribed"].remove(second_user_id)
                    break
    for i in range(len(inf["users"])):
        if inf["users"][i]["user_id"] == second_user_id:
            for j in inf["users"][i]["subscribers"]:
                if j == first_user_id:
                    inf["users"][i]["subscribers"].remove(first_user_id)
                    break
    adder(inf)


def get_info_about_user(user_id):
    inf = reader()["users"]
    for i in inf:
        if i["user_id"] == user_id:
            return i


def get_info_about_user_by_name(nickname):
    inf = reader()["users"]
    for i in inf:
        if i["nickname"] == nickname:
            return i


def subscribed(nickname: str, user_id: int):
    inf = reader()
    a = 0
    for i in inf["users"]:
        if i["nickname"] == nickname:
            a = i["user_id"]
            break
    for i in range(len(inf["users"])):
        if inf["users"][i]["user_id"] == user_id:
            inf["users"][i]["subscribed"].append(a)
            break
    adder(inf)


def subscribe(nickname: str, user_id: int):
    inf = reader()
    for i in inf["users"]:
        if i["nickname"] == nickname:
            i["subscribers"].append(user_id)
    adder(inf)


def num_of_posts(user_id: int):
    inf = reader()
    for i in inf["users"]:
        if i["user_id"] == user_id:
            i["number_of_posts"] += 1
    adder(inf)


def popular():
    inf = reader()["users"]
    sort = {}
    list_of = []
    for i in range(len(inf)):
        list_of.append(len(inf[i]["subscribers"]))
        sort["{}".format(len(inf[i]["subscribers"]))] = i

    list_of = max(list_of)
    user_names = inf[int(sort[str(list_of)])]["nickname"]
    user_id = inf[int(sort[str(list_of)])]["user_id"]
    return user_names, user_id


def rewrite_file(text):
    with open("usernames.txt", "w") as file:
        file.writelines(text)
    return 1


def write_in_file(nickname: str):
    with open("usernames.txt", "a") as file:
        file.write(nickname + "\n")
    return 1


def read_file():
    with open("usernames.txt", "r") as file:
        text = file.read()
    return text


def check_registration(user_id):
    inf = reader()["users"]
    for i in inf:
        if user_id == i["user_id"]:
            return True


def add_id_to_file(user_id):
    with open("user_ids.txt", "a") as file:
        file.write(str(user_id) + "\n")


"""keyboards"""
registration_inline_keyboard = types.InlineKeyboardMarkup()
button_registration = types.InlineKeyboardButton(text="Зареєструватись", callback_data="registration")
registration_inline_keyboard.add(button_registration)

user_ac_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
button1_ac = types.KeyboardButton(text="Поділитись 🎵музикою🎵")
button2_ac = types.KeyboardButton(text="Пошук друзів")
button3_ac = types.KeyboardButton(text="👤Мій профіль👤")
user_ac_keyboard.add(button3_ac).add(button1_ac).add(button2_ac)

user_settings_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
button1_s = types.KeyboardButton(text="Змінити ім'я 👤профілю👤")
button3_s = types.KeyboardButton(text="Мої підписки")
# button4_s = types.KeyboardButton(text="Допомога ЗСУ")
back_button = types.KeyboardButton(text="🔙Назад🔙")
user_settings_keyboard.add(button1_s).add(button3_s).add(back_button)

back_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
back_button1 = types.KeyboardButton(text="🔙Назад🔙")
back_keyboard.add(back_button1)

unsub_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
back_button2 = types.KeyboardButton(text="🔙Назад🔙")
unsub_button = types.KeyboardButton(text="Скасувати підписку на автора")
unsub_keyboard.add(unsub_button).add(back_button2)

"""admin keyboard"""
admin_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_admin1 = types.KeyboardButton(text="Повідомлення всім користувачам")
button_admin2 = types.KeyboardButton(text="Кількість користувачів бота")
admin_keyboard.add(button_admin1).add(button_admin2)

"""command handlers"""


@dp.message_handler(commands="start")
async def start_command(message: types.Message):
    _id = message.from_user.id
    # print(message.from_user.id)
    if check_registration(_id):
        await message.answer("Ви вже зареєстровані", reply_markup=user_ac_keyboard)
    else:
        add_id_to_file(_id)
        await message.answer("Привіт 👋🏻,\n"
                             "я бот створений 🇺🇦українською🇺🇦\n"
                             "командою розробників,\n"
                             "щоб допомогти тобі в обміні улюбленою 🎵музикою🎵,\n"
                             "та 📝дописами📝 до неї.\n",
                             reply_markup=registration_inline_keyboard)


@dp.message_handler(commands="admin")
async def admin_command(message: types.Message):
    _id = message.from_user.id
    if str(_id) == "789402487":
        await message.answer("Вітаємо Розробник", reply_markup=admin_keyboard)
    else:
        await message.answer("Вибачте та ви не адміністратор", reply_markup=user_ac_keyboard)


@dp.message_handler(commands="help")
async def help_command(message: types.Message):
    await message.answer("Цей бот створений щоб приносити вам радіть 🙃\n"
                         "та ділитися 🎵музикою🎵 одразу з великою кількістю людей.\n"
                         "Меню інтуїтивно зрозуміле та просте,\n"
                         "щоб ним змогли користуватись абсолютно всі.\n"
                         "ком'юніті: @Vo1doni та @me_gusta_itto\n"
                         "Ми вважаємо що рекламі в нашому продукті поки не місце,\n"
                         "а якщо плануватимемо її вмикати то всіх про це повідомимо!\n")


"""registration"""


@dp.callback_query_handler(text="registration")
async def user_registration(call: types.CallbackQuery):
    await call.message.answer("Введіть ваше ім'я профілю для цієї мережі😅")
    await States.registration.set()


@dp.message_handler(state=States.registration)
async def ok_or_not(message: types.Message, state: FSMContext):
    _id = message.from_user.id
    await state.finish()
    if message.text not in " /.,<>?@#$%^&*()!№;:₴~'" and len(message.text) < 24:
        if message.text + "\n" in read_file():
            await message.answer("Вибачте та це ім'я профілю вже зайнято!🙃\n"
                                 "Виберіть та введіть інше ім'я профілю!")
            await States.registration.set()
        else:
            write_in_file(message.text)
            inf = reader()
            inf["users"].append({"nickname": message.text,
                                 "user_id": _id,
                                 "number_of_posts": 0,
                                 "subscribed": [],
                                 "subscribers": []})
            adder(inf)
            await message.answer("Вітаємо!🎉✨\n"
                                 "Реєстрацію пройдено успішно!\n"
                                 "Підписуйтесь на друзів,\n"
                                 "діліться 🎵музикою🎵 яка цікава саме вам,\n"
                                 "та головне - кайфуйте!😄\n", reply_markup=user_ac_keyboard)
    else:
        await message.answer("Вибачте та ваш нікнейм не може бути цим символом😔\n"
                             "Виберіть та введіть інше ім'я профілю!")
        await States.registration.set()


"""work with audio"""


@dp.message_handler(content_types="audio")
async def music(message: types.Message):
    _id = message.from_user.id
    inf = get_info_about_user(_id)
    num_of_posts(_id)
    for i in inf["subscribers"]:
        await bot.send_message(chat_id=i, text="Пісня від  <code>{}</code>".format(inf["nickname"]), parse_mode="html")
        await message.forward(i)
    await message.answer("🎵Пісня🎵 розіслана!")


"""admin handlers"""


@dp.message_handler(text="Повідомлення всім користувачам")
async def message_for_all(message: types.Message):
    _id = message.from_user.id
    if str(_id) == "789402487":
        await message.answer("Введіть повідомлення яке хочете розіслати всім")
        await States.msg_for_all.set()
    else:
        await message.answer("Вибачте та ви не адміністратор", reply_markup=user_ac_keyboard)


@dp.message_handler(state=States.msg_for_all)
async def send_msg_all(message: types.Message, state: FSMContext):
    await state.finish()
    _id = message.from_user.id
    if str(_id) == "789402487":
        with open("user_ids.txt", "r") as file:
            text = file.readlines()
            for i in range(len(text)):
                text[i] = text[i].replace("/n", "")
                await bot.send_message(chat_id=text[i], text=f"{message.text}", parse_mode="html")
            await message.answer("Повідомлення розіслано!", reply_markup=admin_keyboard)
    else:
        await message.answer("Вибачте та ви не адміністратор", reply_markup=user_ac_keyboard)


@dp.message_handler(text="Кількість користувачів бота")
async def message_for_all(message: types.Message):
    _id = message.from_user.id
    if str(_id) == "789402487":
        with open("usernames.txt", "r") as file:
            text = file.readlines()
            len_of_text = len(text)
        await message.answer(f"На данний момент у боті зареєстровано {len_of_text} користувачів")
    else:
        await message.answer("Вибачте та ви не адміністратор", reply_markup=user_ac_keyboard)


"""user handlers"""


@dp.message_handler(text="👤Мій профіль👤")
async def my_profile(message: types.Message):
    _id = message.from_user.id
    inf = get_info_about_user(_id)
    mention = inf["nickname"]
    number_of_subscribers = len(inf["subscribers"])
    number_of_subscribed = len(inf["subscribed"])
    number_of_posts = inf["number_of_posts"]
    await message.answer(f"Ваш нікнейм: <code>{mention}</code>\n"
                         f"Кількість підписників: {number_of_subscribers}\n"
                         f"Кількість підписок: {number_of_subscribed}\n"
                         f"Кількість музичних постів: {number_of_posts}\n", parse_mode="html",
                         reply_markup=user_settings_keyboard)


@dp.message_handler(text="Пошук друзів")
async def find_friends(message: types.Message):
    nickname, _ids = popular()
    inf1 = len(get_info_about_user(_ids)["subscribers"])
    posts = get_info_about_user(_ids)["number_of_posts"]
    await message.answer(f"Найпопулярніший автор: <code>{nickname}</code>\n"
                         f"Кількість підписників: {inf1}\n"
                         f"Кількість музичних постів: {posts}\n", parse_mode="html")

    await message.answer("Надішліть будь ласка ім'я акаунта вашого друга\n"
                         "Чи того акаунту на який хочете підписатись\n", reply_markup=back_keyboard)
    await States.subscribe.set()


@dp.message_handler(state=States.subscribe)
async def sub(message: types.Message, state: FSMContext):
    await state.finish()
    nickname = message.text
    inf = reader()
    nicknames = []
    for i in inf["users"]:
        nicknames.append(i["nickname"])
    nicks = " ".join(nicknames)
    if message.text == "🔙Назад🔙":
        await message.answer("Ви повернулись до головного меню", reply_markup=user_ac_keyboard)
    else:
        if nickname in nicks:
            a = 0
            srt = ""
            for i in inf["users"]:
                if i["nickname"] == nickname:
                    a = i["user_id"]
                    srt = "".join(str(i["subscribers"]))
                    break

            if a != message.from_user.id and str(message.from_user.id) not in srt:
                subscribe(nickname, message.from_user.id)
                subscribed(nickname, message.from_user.id)
                await message.answer("Підписку оформлено!", reply_markup=user_ac_keyboard)
            else:
                await message.answer("Вибачте та ви не можете підписатись на самого себе,\n"
                                     "aбо на автора підписка на якого була оформлена вами раніше!\n"
                                     "Введіть ім'я автора на якого хочете підписатись\n", reply_markup=back_keyboard)
                await States.subscribe.set()
        else:
            await message.answer("Такого користувача не існує!", reply_markup=user_ac_keyboard)


@dp.message_handler(text="Поділитись 🎵музикою🎵")
async def change_music(message: types.Message):
    await message.answer("Надішліть мені будь ласка 🎵пісню🎵\n"
                         "або ж декілька, якими хочете поділитись з друзями\n"
                         "🎵Музику🎵 можна надсилати з 📝дописом📝 під нею...", reply_markup=back_keyboard)


@dp.message_handler(text="🔙Назад🔙", state=None)
async def back(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Ви повернулись до головного меню", reply_markup=user_ac_keyboard)


@dp.message_handler(text="Змінити ім'я 👤профілю👤")
async def my_nickname(message: types.Message):
    await message.answer("Введіть нове ім'я профілю!", reply_markup=back_keyboard)
    await States.change_name.set()


@dp.message_handler(state=States.change_name)
async def change_name(message: types.Message, state: FSMContext):
    await state.finish()
    new_nickname = message.text
    _id = message.from_user.id
    if new_nickname == "🔙Назад🔙":
        await message.answer("Ви повернулись до головного меню", reply_markup=user_ac_keyboard)
    else:
        if message.text not in " /.,<>?@#$%^&*()!№;:₴~'" and len(message.text) < 24:
            if message.text + "\n" in read_file():
                await message.answer("Вибачте та це ім'я профілю вже зайнято!😔\n"
                                     "Виберіть та введіть інше ім'я профілю!", reply_markup=back_keyboard)
                await States.change_name.set()
            else:
                text = read_file()
                text = text.replace(get_info_about_user(_id)["nickname"] + "\n", new_nickname + "\n")
                rewrite_file(text)
                change_nickname(_id, new_nickname)
                await message.answer("Вітаємо!🎉✨\n"
                                     "Ім'я 👤профілю👤 змінено успішно!\n"
                                     "Підписуйтесь на друзів,\n"
                                     "діліться 🎵музикою🎵 яка цікава саме вам,\n"
                                     "та головне - кайфуйте!\n", reply_markup=user_ac_keyboard)
        else:
            await message.answer("Вибачте та ваш нікнейм не може бути цим символом😔\n"
                                 "Виберіть та введіть інше ім'я профілю!", reply_markup=back_keyboard)
            await States.change_name.set()


@dp.message_handler(text="Мої підписки")
async def my_subscribed(message: types.Message):
    _id = message.from_user.id
    subscrib = get_info_about_user(_id)["subscribed"]
    if len(subscrib) == 0:
        await message.answer("Ви не підписані на жодного 👤автора🗣!", reply_markup=user_settings_keyboard)
    else:
        await message.answer("Ви підписані на таких 👤авторів🗣 : \n", reply_markup=unsub_keyboard)
        for i in subscrib:
            name = get_info_about_user(i)["nickname"]
            await message.answer(f"<code>{name}</code>\n")


@dp.message_handler(text="Скасувати підписку на автора")
async def un_subscribe(message: types.Message):
    await message.answer("Введіть нікнейм 👤автора👤 від якого хочете відписатись")
    await States.unsubscribe.set()


@dp.message_handler(state=States.unsubscribe)
async def unsubscribed(message: types.Message, state: FSMContext):
    await state.finish()
    _id = message.from_user.id
    text = read_file()
    if message.text == "🔙Назад🔙":
        await message.answer("Ви повернулись до меню вашого 👤акаунту👤", reply_markup=user_settings_keyboard)
    else:
        if message.text + "\n" in text:
            unsub_id = get_info_about_user_by_name(message.text)["user_id"]
            unsubscribe(_id, unsub_id)
            await message.answer(f"Вітаємо ви успішно відписались від <code>{message.text}</code>",
                                 reply_markup=user_settings_keyboard)
        else:
            await message.answer("Вибачте та такого 👤автора🗣 не існує!\n"
                                 "Введіть коректний нікнейм 👤автора🗣!", reply_markup=unsub_keyboard)


@dp.message_handler(text="Допомога ЗСУ")
async def help_for_zsu(message: types.Message):
    await message.answer("З огляду на ситуацію в країні\n"
                         "ми вирішили зробити це віконце для пожертв.\n"
                         "Всі кошти що надійдуть на карту у цьому вікні\n"
                         "будуть надіслані на допомогу ЗСУ.\n"
                         "Чеки будемо відправляти раз у тиждень!\n")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
