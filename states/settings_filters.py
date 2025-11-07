from aiogram.fsm.state import StatesGroup, State

class SettingsFilter(StatesGroup):
    city = State()
    salary = State()
    employment = State()
    experience = State()
    vacancies_per_page = State()
    only_with_salary = State()
