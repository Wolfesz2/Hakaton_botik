import array
import aiogram.types
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters import state
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, message
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from Config import TOKEN, HOST, PASSWORD, DB_NAME, USER
from Utils import States
import psycopg2

connect = psycopg2.connect(
    host=HOST,
    user=USER,
    password=PASSWORD,
    database=DB_NAME
)
L_msg = []
Q_msg = []
P_name = []
P_msg = []
W_Contacts = []
Workers_id = []



with connect:
    with connect.cursor() as cursor:
        for i in range(1, 31):
            cursor.execute(f"""select text_msg from "Message" where id_msg={i}""")
            text = ''.join(cursor.fetchone())
            L_msg.append(text)
    with connect.cursor() as cursor:
        for i in range(1, 7):
            cursor.execute(f"""select q_text from "Quest" where q_id={i}""")
            text = ''.join(cursor.fetchone())
            Q_msg.append(text)
    with connect.cursor() as cursor:
        for i in range(1, 5):
            cursor.execute(f"""select text_pr from "Projects" where id={i}""")
            text = ''.join(cursor.fetchone())
            P_msg.append(text)
    with connect.cursor() as cursor:
        for i in range(1, 5):
            cursor.execute(f"""select name_pr from "Projects" where id={i}""")
            text = ''.join(cursor.fetchone())
            P_name.append(text)
    with connect.cursor() as cursor:
        cursor.execute("""select * from "Employees" """)
        for i in cursor:
                Workers_id.append(i[0])


connect.close()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

# inline кнопка назад
Back_button = InlineKeyboardButton('Назад❌', callback_data='back')
Back_inlkey = InlineKeyboardMarkup().add(Back_button)

# Inline клавиатура для Онбординга
Quest_button = InlineKeyboardButton('Квест❗', callback_data='Quest')
Text_button = InlineKeyboardButton('Текстовым\nвариантом📕', callback_data='Text')
Ondoard_inlkey = InlineKeyboardMarkup().add(Quest_button, Text_button, Back_button)



# Inline клавиатура для начала квеста
GoForw_button = InlineKeyboardButton('Идти дальше🚶', callback_data='go0')
StartQuest_inlkey = InlineKeyboardMarkup().add(GoForw_button, Back_button)

Holl_inlkey = InlineKeyboardMarkup().add(InlineKeyboardButton('Пройти направо',callback_data='go2'))
Left_inlkey = InlineKeyboardMarkup().add(InlineKeyboardButton('Теперь налево до круговой стенки',callback_data='go3'))
Down_inlkey = InlineKeyboardMarkup().add(InlineKeyboardButton('Теперь повернем направо',callback_data='go4'))
RightDown_inlkey = InlineKeyboardMarkup().add(InlineKeyboardButton('Снова пройдите налево до полукруга',callback_data='go5'))
RightUp_inlkey = InlineKeyboardMarkup().add(InlineKeyboardButton('Обратно в главный зал',callback_data='go1'))


# Inline клавиатура для Текстового онбординга
OficeMap_button = InlineKeyboardButton('Карта офиса📜', callback_data='OficeMap')
Equip_button = InlineKeyboardButton('Оборудование💻', callback_data='Equip')
Contacts_button = InlineKeyboardButton('Контакты📞', callback_data='Contacts')
Goal_button = InlineKeyboardButton('Цели🎯', callback_data='Goal')
OnboardText_inlkey = InlineKeyboardMarkup().add(OficeMap_button, Equip_button, Contacts_button, Goal_button, Back_button)

# inline клавиатура для Главной страницы
About_button = InlineKeyboardButton('Сведения📝', callback_data='About')
Ondoard_button = InlineKeyboardButton('Онбординг🔎', callback_data='Onboarding')
Main_menu_inlkey = InlineKeyboardMarkup().add(About_button, Ondoard_button, Back_button)

# inline клавиатура для Сведений
Me_button = InlineKeyboardButton('Обо мне👨', callback_data='About_me')
Company_button = InlineKeyboardButton('Компания🏢', callback_data='About_сompany')
Help_button = InlineKeyboardButton('Помощь🤝', callback_data='About_help')
About_inlkey = InlineKeyboardMarkup().add(Me_button, Company_button, Help_button, Back_button)

# Inline клавиатура для Обо мне
Role_schedule_button = InlineKeyboardButton('Распорядок📆', callback_data='Role_schedule')
Role_guide_button = InlineKeyboardButton('Должностная инструкция📃', callback_data='Role_guide')
Role_Place_button = InlineKeyboardButton('Где рабочее место?📟', callback_data='Role_place')
Role_inlkey = InlineKeyboardMarkup().add(Role_schedule_button, Role_guide_button, Role_Place_button, Back_button)

# Inline клавиатура для Должностных инструкций
Work_process_button = InlineKeyboardButton('Организация рабочего процесса🤝', callback_data='Work_process')
Work_calls_button = InlineKeyboardButton('Рабочие созвоны☎️', callback_data='Work_calls')
Work_inlkey = InlineKeyboardMarkup().add(Work_calls_button, Work_process_button, Back_button)

# Inline клавиатура для Рабочих созвонов
Call_schedule_button = InlineKeyboardButton('Расписание звонков📆', callback_data='Call_schedule')
Call_records_button = InlineKeyboardButton('Записи созвонов💾', callback_data='Call_records')
Call_inlkey = InlineKeyboardMarkup().add(Call_schedule_button, Call_records_button, Back_button)

# Inline клавиатура для Компания
Dept_workers_button = InlineKeyboardButton('Отделы и работкники👔', callback_data='Dept_workers')
Company_history_button = InlineKeyboardButton('История компании📜', callback_data='Company_history')
Company_projects_button = InlineKeyboardButton('Проекты компании📚', callback_data='Company_projects')
About_company_inlkey = InlineKeyboardMarkup().add(Dept_workers_button, Company_history_button, Company_projects_button,
                                                  Back_button)

# Inline клавиатура для проектов компании
NextProject_button = InlineKeyboardButton('➡️', callback_data='Next')
PreviousProject_button = InlineKeyboardButton('⬅️', callback_data='Previous')
Project_inlkey = InlineKeyboardMarkup().add(PreviousProject_button, Back_button ,NextProject_button)

# Inline клавиатура для Отделы
Programmer_button = InlineKeyboardButton('Разработчики🖥', callback_data='Programmer')
Accountant_button = InlineKeyboardButton('Бухгалтерский отдел💰', callback_data='Accountant')
HR_button = InlineKeyboardButton('Отдел кадров🖌', callback_data='HR')
Cyber_Security_button = InlineKeyboardButton('Отдел Кибер-безопасности🔐', callback_data='Cyber')
Busyness_button = InlineKeyboardButton('Отдел бизнес аналитиков🔎', callback_data='Busyness')
Dept_inlkey = InlineKeyboardMarkup().add(Programmer_button, Accountant_button, HR_button, Cyber_Security_button,
                                         Busyness_button, Back_button)

# Inline клавиатура для Помощь
Support_button = InlineKeyboardButton('Поддержка📞', callback_data='Support')
Help_info_button = InlineKeyboardButton('Ссылки на чаты отделов📱', callback_data='Inf')
Help_food_button = InlineKeyboardButton('Еда🍩', callback_data='Help_food')
Help_map_button = InlineKeyboardButton('Карта офиса📜', callback_data='Help_map')
Help_inlkey = InlineKeyboardMarkup().add(Support_button, Help_info_button, Help_food_button, Help_map_button,
                                         Back_button)

# ReplyKeyboard
MainMenu_button = types.KeyboardButton('Главное меню🚪', callback_data='Mainmenu')
Rkb = ReplyKeyboardMarkup(resize_keyboard=True).add(MainMenu_button)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await state.State.set(States.Auth)
    await message.reply('Чтобы продолжить, введите код сотрудника:')


@dp.message_handler(state=States.Auth or States.MainMenu)  # код сотрудника
async def main_menu(message: types.Message):
    if Workers_id.count(int(message.text))>0:
        await state.State.set(States.MainMenu)
        await message.reply(text='код успешно введен', reply_markup=Rkb)
        await bot.send_message(chat_id=message.chat.id, text=L_msg[24],
                               reply_markup=Main_menu_inlkey)
    else:
        await  bot.send_message(chat_id=message.chat.id, text='Код не верный, введите повторно свой код')


# обработчики Назад
@dp.callback_query_handler(state='*', text='back')
async def process_back_command(query: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state == 'States:About':
        await state.set_state(States.MainMenu)
        await query.message.edit_text(text=L_msg[24], reply_markup=Main_menu_inlkey)
    elif current_state == 'States:MainMenu':
        await state.set_state(States.Auth)
        await query.message.edit_text(text='Сессия завершена, введите код сотрудника снова:')
    elif current_state == 'States:AboutMe':
        await state.set_state(States.About)
        await query.message.edit_text(text=L_msg[22], reply_markup=About_inlkey)
    elif current_state == 'States:AboutMeSchedule':
        await state.set_state(States.AboutMe)
        await query.message.edit_text(text=L_msg[0], reply_markup=Role_inlkey)
    elif current_state == 'States:AboutMeGuide':
        await state.set_state(States.AboutMe)
        await query.message.edit_text(text=L_msg[0], reply_markup=Role_inlkey)
    elif current_state == 'States:AboutMeGuideWork':
        await state.set_state(States.AboutMeGuide)
        await query.message.edit_text(text=L_msg[2], reply_markup=Work_inlkey)
    elif current_state == 'States:AboutMeGuideCalls':
        await state.set_state(States.AboutMeGuide)
        await query.message.edit_text(text=L_msg[2], reply_markup=Work_inlkey)
    elif current_state == 'States:AboutCompany':
        await state.set_state(States.About)
        await query.message.edit_text(text=L_msg[22], reply_markup=About_inlkey)
    elif current_state == 'States:AboutCompanyDep':
        await state.set_state(States.AboutCompany)
        await query.message.edit_text(text=L_msg[9], reply_markup=About_company_inlkey)
    elif current_state == 'States:AboutCompanyHistory':
        await state.set_state(States.AboutCompany)
        await query.message.edit_text(text=L_msg[9], reply_markup=About_company_inlkey)
    elif current_state == 'States:AboutCompanyProject' or 'States:AboutCompanyProject1' or 'States:AboutCompanyProject2' or 'States:AboutCompanyProject3':
        await state.set_state(States.AboutCompany)
        await query.message.edit_text(text=L_msg[9], reply_markup=About_company_inlkey)
    elif current_state == 'States:AboutCompanyDepAcc':
        await state.set_state(States.AboutCompanyDep)
        await query.message.edit_text(text=L_msg[11], reply_markup=Dept_inlkey)
    elif current_state == 'States:AboutCompanyDepCad':
        await state.set_state(States.AboutCompanyDep)
        await query.message.edit_text(text=L_msg[11], reply_markup=Dept_inlkey)
    elif current_state == 'States:AboutCompanyDepDev':
        await state.set_state(States.AboutCompanyDep)
        await query.message.edit_text(text=L_msg[11], reply_markup=Dept_inlkey)
    elif current_state == 'States:AboutCompanyDepCyb':
        await state.set_state(States.AboutCompanyDep)
        await query.message.edit_text(text=L_msg[11], reply_markup=Dept_inlkey)
    elif current_state == 'States:AboutCompanyDepAn':
        await state.set_state(States.AboutCompanyDep)
        await query.message.edit_text(text=L_msg[11], reply_markup=Dept_inlkey)
    elif current_state == 'States:AboutHelp':
        await state.set_state(States.About)
        await query.message.edit_text(text=L_msg[22], reply_markup=About_inlkey)
    elif current_state == 'States:AboutHelpChat':
        await state.set_state(States.AboutHelp)
        await query.message.edit_text(text=L_msg[15], reply_markup=Help_inlkey)
    elif current_state == 'States:AboutHelpMap':
        await state.set_state(States.AboutHelp)
        await query.message.edit_text(text=L_msg[15], reply_markup=Help_inlkey)
    elif current_state == 'States:AboutHelpFood':
        await state.set_state(States.AboutHelp)
        await query.message.edit_text(text=L_msg[15], reply_markup=Help_inlkey)
    elif current_state == 'States:AboutHelpInf':
        await state.set_state(States.AboutHelp)
        await query.message.edit_text(text=L_msg[15], reply_markup=Help_inlkey)
    elif current_state == 'States:Onboard':
        await state.set_state(States.MainMenu)
        await query.message.edit_text(text=L_msg[24], reply_markup=Main_menu_inlkey)
    elif current_state == 'States:OnboardText':
        await state.set_state(States.Onboard)
        await query.message.edit_text(text=L_msg[21], reply_markup=Ondoard_inlkey)
    elif current_state == 'States:OnboardTextMap':
        await state.set_state(States.OnboardText)
        await query.message.edit_text(text=L_msg[20], reply_markup=OnboardText_inlkey)
    elif current_state == 'States:OnboardTextEquip':
        await state.set_state(States.OnboardText)
        await query.message.edit_text(text=L_msg[20], reply_markup=OnboardText_inlkey)
    elif current_state == 'States:OnboardTextGoal':
        await state.set_state(States.OnboardText)
        await query.message.edit_text(text=L_msg[20], reply_markup=OnboardText_inlkey)
    elif current_state == 'States:OnboardQuest':
        await state.set_state(States.Onboard)
        await query.message.edit_text(text=L_msg[20], reply_markup=Ondoard_inlkey)
    elif current_state == 'States:OnboardQuestForward':
        await state.set_state(States.Quest)
        await query.message.edit_text(text='BD', reply_markup=StartQuest_inlkey)
    elif current_state == 'States:OnboardQuestRight':
        await state.set_state(States.Quest)
        await query.message.edit_text(text='BD', reply_markup=StartQuest_inlkey)
    elif current_state == 'States:AboutMeGuideProcess':
        await state.set_state(States.AboutMeGuide)
        await query.message.edit_text(text=L_msg[2], reply_markup=Work_inlkey)
    elif current_state == 'States:AboutMeGuideCallsSchedule':
        await state.set_state(States.AboutMeGuideCalls)
        await query.message.edit_text(text=L_msg[8], reply_markup=Call_inlkey)
    elif current_state == 'States:OnboardTextCont':
        await state.set_state(States.OnboardText)
        await query.message.edit_text(text=L_msg[20], reply_markup=OnboardText_inlkey)
    elif current_state == 'States:AboutMeGuideCallsRec':
        await state.set_state(States.AboutMeGuideCalls)
        await query.message.edit_text(text=L_msg[8], reply_markup=Call_inlkey)


@dp.message_handler(state='*', text='Главное меню🚪')
async def main_menu_process(message: types.message):
    await bot.send_message(chat_id=message.chat.id,text=L_msg[24], reply_markup=Main_menu_inlkey)



# Обработчики inline кнопок
@dp.callback_query_handler(state=States.MainMenu, text='About')  # сведения
async def about_menu(query: types.CallbackQuery):
    await state.State.set(States.About)
    await query.message.edit_text(text=L_msg[22], reply_markup=About_inlkey)


# обработчики ветки о компании
@dp.callback_query_handler(state=States.About, text='About_сompany')
async def about_company(query: types.CallbackQuery):
    await state.State.set(States.AboutCompany)
    await query.message.edit_text(text=L_msg[9], reply_markup=About_company_inlkey)


@dp.callback_query_handler(state=States.AboutCompany, text='Dept_workers')
async def dept_workers(query: types.CallbackQuery):
    await state.State.set(States.AboutCompanyDep)
    await query.message.edit_text(text=L_msg[11], reply_markup=Dept_inlkey)


@dp.callback_query_handler(state=States.AboutCompany, text='Company_history')
async def company_history(query: types.CallbackQuery):
    await state.State.set(States.AboutCompanyHistory)
    await query.message.edit_text(text=L_msg[10], reply_markup=Back_inlkey)


@dp.callback_query_handler(state=States.AboutCompany, text='Company_projects')
async def company_projects(query: types.CallbackQuery):
    await state.State.set(States.AboutCompanyProject)
    await query.message.edit_text(text=P_name[0]+'\n'+P_msg[0], reply_markup=Project_inlkey)


@dp.callback_query_handler(state=States.AboutCompanyProject, text='Next')
async def next(query: types.CallbackQuery):
    await state.State.set(States.AboutCompanyProject1)
    await query.message.edit_text(text=P_name[0]+'\n'+P_msg[0], reply_markup=Project_inlkey)


@dp.callback_query_handler(state=States.AboutCompanyProject, text='Previous')
async def previous(query: types.CallbackQuery):
    await state.State.set(States.AboutCompanyProject3)
    await query.message.edit_text(text=P_name[0]+'\n'+P_msg[0], reply_markup=Project_inlkey)


@dp.callback_query_handler(state=States.AboutCompanyProject1, text='Next')
async def next(query: types.CallbackQuery):
    await state.State.set(States.AboutCompanyProject2)
    await query.message.edit_text(text=P_name[1]+'\n'+P_msg[1], reply_markup=Project_inlkey)


@dp.callback_query_handler(state=States.AboutCompanyProject1, text='Previous')
async def previous(query: types.CallbackQuery):
    await state.State.set(States.AboutCompanyProject)
    await query.message.edit_text(text=P_name[1]+'\n'+P_msg[1], reply_markup=Project_inlkey)


@dp.callback_query_handler(state=States.AboutCompanyProject2, text='Next')
async def next(query: types.CallbackQuery):
    await state.State.set(States.AboutCompanyProject3)
    await query.message.edit_text(text=P_name[2]+'\n'+P_msg[2], reply_markup=Project_inlkey)


@dp.callback_query_handler(state=States.AboutCompanyProject2, text='Previous')
async def previous(query: types.CallbackQuery):
    await state.State.set(States.AboutCompanyProject1)
    await query.message.edit_text(text=P_name[2]+'\n'+P_msg[2], reply_markup=Project_inlkey)


@dp.callback_query_handler(state=States.AboutCompanyProject3, text='Next')
async def next(query: types.CallbackQuery):
    await state.State.set(States.AboutCompanyProject)
    await query.message.edit_text(text=P_name[3]+'\n'+P_msg[3], reply_markup=Project_inlkey)


@dp.callback_query_handler(state=States.AboutCompanyProject3, text='Previous')
async def previous(query: types.CallbackQuery):
    await state.State.set(States.AboutCompanyProject2)
    await query.message.edit_text(text=P_name[3]+'\n'+P_msg[3], reply_markup=Project_inlkey)


@dp.callback_query_handler(state=States.AboutCompanyDep, text='Programmer')
async def programmer(query: types.CallbackQuery):
    await state.State.set(States.AboutCompanyDepDev)
    await query.message.edit_text(text=L_msg[12], reply_markup=Back_inlkey)


@dp.callback_query_handler(state=States.AboutCompanyDep, text='Accountant')
async def accountant(query: types.CallbackQuery):
    await state.State.set(States.AboutCompanyDepAcc)
    await query.message.edit_text(text=L_msg[17], reply_markup=Back_inlkey)


@dp.callback_query_handler(state=States.AboutCompanyDep, text='HR')
async def hr(query: types.CallbackQuery):
    await state.State.set(States.AboutCompanyDepCad)
    await query.message.edit_text(text=L_msg[18], reply_markup=Back_inlkey)


@dp.callback_query_handler(state=States.AboutCompanyDep, text='Cyber')
async def cyber(query: types.CallbackQuery):
    await state.State.set(States.AboutCompanyDepCyb)
    await query.message.edit_text(text=L_msg[13], reply_markup=Back_inlkey)


@dp.callback_query_handler(state=States.AboutCompanyDep, text='Busyness')
async def busyness(query: types.CallbackQuery):
    await state.State.set(States.AboutCompanyDepAn)
    await query.message.edit_text(text=L_msg[14], reply_markup=Back_inlkey)


# обработчики ветки обо мне
@dp.callback_query_handler(state=States.About, text='About_me')
async def about_me(query: types.CallbackQuery):
    await state.State.set(States.AboutMe)
    await query.message.edit_text(text=L_msg[0], reply_markup=Role_inlkey)


@dp.callback_query_handler(state=States.AboutMe, text='Role_schedule')
async def role_schedule(query: types.CallbackQuery):
    await state.State.set(States.AboutMeSchedule)
    await query.message.edit_text(text=L_msg[1], reply_markup=Back_inlkey)


@dp.callback_query_handler(state=States.AboutMe, text='Role_guide')
async def role_guide(query: types.CallbackQuery):
    await state.State.set(States.AboutMeGuide)
    await query.message.edit_text(text=L_msg[2], reply_markup=Work_inlkey)


@dp.callback_query_handler(state=States.AboutMeGuide, text='Work_process')
async def work_process(query: types.CallbackQuery):
    await state.State.set(States.AboutMeGuideProcess)
    await query.message.edit_text(text='САМ СДЕЛАЕШЬ', reply_markup=Back_inlkey)


@dp.callback_query_handler(state=States.AboutMeGuide, text='Work_calls')
async def work_calls(query: types.CallbackQuery):
    await state.State.set(States.AboutMeGuideCalls)
    await query.message.edit_text(text=L_msg[8], reply_markup=Call_inlkey)


@dp.callback_query_handler(state=States.AboutMeGuideCalls, text='Call_records')
async def call_records(query: types.CallbackQuery):
    await state.State.set(States.AboutMeGuideCallsRec)
    await query.message.edit_text(text='САМ', reply_markup=Back_inlkey)


@dp.callback_query_handler(state=States.AboutMeGuideCalls, text='Call_schedule')
async def call_schedule(query: types.CallbackQuery):
    await state.State.set(States.AboutMeGuideCallsSchedule)
    await query.message.edit_text(text='САМ', reply_markup=Back_inlkey)


# обработчики ветки помощь
@dp.callback_query_handler(state=States.About, text='About_help')
async def about_help(query: types.CallbackQuery):
    await state.State.set(States.AboutHelp)
    await query.message.edit_text(text=L_msg[15], reply_markup=Help_inlkey)


@dp.callback_query_handler(state=States.AboutHelp, text='Support')
async def about_help(query: types.CallbackQuery):
    await state.State.set(States.AboutHelpChat)
    await query.message.edit_text(text=L_msg[19], reply_markup=Back_inlkey)


@dp.callback_query_handler(state=States.AboutHelp, text='Inf')
async def about_help(query: types.CallbackQuery):
    await state.State.set(States.AboutHelpInf)
    await query.message.edit_text(text=L_msg[28], reply_markup=Back_inlkey)


@dp.callback_query_handler(state=States.AboutHelp, text='Help_food')
async def about_help(query: types.CallbackQuery):
    await state.State.set(States.AboutHelpFood)
    await query.message.edit_text(text=L_msg[16], reply_markup=Back_inlkey)


@dp.callback_query_handler(state=States.AboutHelp, text='Help_map')
async def about_help(query: types.CallbackQuery):
    await state.State.set(States.AboutHelpMap)
    await query.message.edit_text(text=L_msg[27], reply_markup=Back_inlkey)


@dp.callback_query_handler(state=States.MainMenu, text='Onboarding')
async def onboarding(query: types.CallbackQuery):
    await state.State.set(States.Onboard)
    await query.message.edit_text(text=L_msg[21], reply_markup=Ondoard_inlkey)


@dp.callback_query_handler(state=States.Onboard, text='Quest')
async def quest(query: types.CallbackQuery):
    await state.State.set(States.Quest)
    await query.message.edit_text(text=Q_msg[0], reply_markup=StartQuest_inlkey)

@dp.callback_query_handler(state=States.Quest, text='go0')
async def quest(query: types.CallbackQuery):
    await state.State.set(States.Go0)
    await query.message.edit_text(text=Q_msg[1], reply_markup=Holl_inlkey)

@dp.callback_query_handler(state=States.Go0, text='go1')
async def quest(query: types.CallbackQuery):
    await state.State.set(States.Go1)
    await query.message.edit_text(text=Q_msg[2], reply_markup=Left_inlkey)

@dp.callback_query_handler(state=States.Go1, text='go2')
async def quest(query: types.CallbackQuery):
    await state.State.set(States.Go2)
    await query.message.edit_text(text=Q_msg[3], reply_markup=Down_inlkey)

@dp.callback_query_handler(state=States.Go2, text='go3')
async def quest(query: types.CallbackQuery):
    await state.State.set(States.Go3)
    await query.message.edit_text(text=Q_msg[5], reply_markup=RightDown_inlkey)

@dp.callback_query_handler(state=States.Go3, text='go4')
async def quest(query: types.CallbackQuery):
        await state.State.set(States.Go4)
        await query.message.edit_text(text=Q_msg[4], reply_markup=RightUp_inlkey)

@dp.callback_query_handler(state=States.Go4, text='go4')
async def quest(query: types.CallbackQuery):
        await state.State.set(States.Go0)
        await query.message.edit_text(text=Q_msg[1], reply_markup=Holl_inlkey)

@dp.callback_query_handler(state=States.Onboard, text='Text')
async def text(query: types.CallbackQuery):
    await state.State.set(States.OnboardText)
    await query.message.edit_text(text=L_msg[20], reply_markup=OnboardText_inlkey)


@dp.callback_query_handler(state=States.OnboardText, text='OficeMap')
async def oficemap(query: types.CallbackQuery):
    await state.State.set(States.OnboardTextMap)
    await query.message.edit_text(text=L_msg[27], reply_markup=Back_inlkey)


@dp.callback_query_handler(state=States.OnboardText, text='Contacts')
async def contacts(query: types.CallbackQuery):
    await state.State.set(States.OnboardTextCont)
    await query.message.edit_text(text='САМ', reply_markup=Back_inlkey)


@dp.callback_query_handler(state=States.OnboardText, text='Equip')
async def equip(query: types.CallbackQuery):
    await state.State.set(States.OnboardTextEquip)
    await query.message.edit_text(text=L_msg[26], reply_markup=Back_inlkey)


@dp.callback_query_handler(state=States.OnboardText, text='Goal')
async def goal(query: types.CallbackQuery):
    await state.State.set(States.OnboardTextGoal)
    await query.message.edit_text(text=L_msg[25], reply_markup=Back_inlkey)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
