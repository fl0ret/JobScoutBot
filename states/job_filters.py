from aiogram.fsm.state import State, StatesGroup

class JobFilter(StatesGroup):
    city = State()        # Выбор города
    salary = State()      # Указание минимальной зарплаты
    employment = State()  # Тип занятости
    specialty = State()   # Специальность пользователя
    experience = State()  # Опыт работы