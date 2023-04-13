from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.helper import Helper, HelperMode, ListItem


class States(StatesGroup):
    mode = HelperMode.snake_case

    Auth = State()
    MainMenu = State()
    About = State() # сведения
    # обо мне и все что выходит из него
    AboutMe = State()
    AboutMeSchedule = State()
    AboutMeGuide = State()
    AboutMeGuideProcess = State()
    AboutMeGuideWork = State()
    AboutMeGuideCalls = State()
    AboutMeGuideCallsSchedule = State()
    AboutMeGuideCallsRec = State()
    # компания и все что выходит из нее
    AboutCompany = State()
    AboutCompanyDep = State()
    AboutCompanyHistory = State()
    AboutCompanyProject = State()
    AboutCompanyProject1 = State()
    AboutCompanyProject2 = State()
    AboutCompanyProject3 = State()
    AboutCompanyDepAcc = State()
    AboutCompanyDepCad = State()
    AboutCompanyDepDev = State()
    AboutCompanyDepCyb = State()
    AboutCompanyDepAn = State()
    # помощь и все что в ней
    AboutHelp = State()
    AboutHelpChat = State()
    AboutHelpMap = State()
    AboutHelpFood = State()
    AboutHelpInf = State()
    Onboard = State()  # Онбординг
    # Текст и все что в нем
    OnboardText = State()
    OnboardTextMap = State()
    OnboardTextCont = State()
    OnboardTextEquip = State()
    OnboardTextGoal = State()
    # Квест и все что в нем
    Quest = State()
    Go0=State()
    Go1=State()
    Go2=State()
    Go3=State()
    Go4=State()
    Go5=State()