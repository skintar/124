from dataclasses import dataclass, field
from typing import List, Dict, Callable
from datetime import datetime, timedelta
import json

@dataclass
class Quest:
    id: str
    name: str
    description: str
    objective: str
    reward: Dict[str, int]
    is_completed: bool = False
    is_active: bool = False
    progress: int = 0
    max_progress: int = 1
    prerequisites: List[str] = field(default_factory=list)
    time_limit: timedelta = None
    start_time: datetime = None
    repeatable: bool = False

class QuestManager:
    def __init__(self):
        self.quests: Dict[str, Quest] = {}
        self.active_quests: List[Quest] = []

    def add_quest(self, quest: Quest):
        self.quests[quest.id] = quest

    def start_quest(self, quest_id: str):
        if quest_id in self.quests and not self.quests[quest_id].is_active:
            quest = self.quests[quest_id]
            if all(self.quests[prereq].is_completed for prereq in quest.prerequisites):
                quest.is_active = True
                quest.start_time = datetime.now()
                self.active_quests.append(quest)
                print(f"Начат новый квест: {quest.name}")
                print(f"Описание: {quest.description}")
            else:
                print("Не выполнены предварительные условия для этого квеста.")
        else:
            print("Квест не найден или уже активен.")

    def complete_quest(self, quest_id: str):
        if quest_id in self.quests and self.quests[quest_id].is_active:
            quest = self.quests[quest_id]
            quest.is_completed = True
            quest.is_active = False
            self.active_quests.remove(quest)
            print(f"Квест '{quest.name}' выполнен!")
            print(f"Награда: {quest.reward}")
            if quest.repeatable:
                quest.is_completed = False
                quest.progress = 0
            return quest.reward
        else:
            print("Квест не найден или не активен.")
            return None

    def update_quest_progress(self, quest_id: str, progress: int):
        if quest_id in self.quests and self.quests[quest_id].is_active:
            quest = self.quests[quest_id]
            quest.progress += progress
            if quest.progress >= quest.max_progress:
                return self.complete_quest(quest_id)
            print(f"Прогресс квеста '{quest.name}': {quest.progress}/{quest.max_progress}")
        return None

    def check_quests(self, condition: Callable[[], bool], quest_id: str):
        if condition():
            return self.complete_quest(quest_id)
        return None

    def get_active_quests(self) -> List[Quest]:
        return self.active_quests

    def get_all_quests(self) -> List[Quest]:
        return list(self.quests.values())

    def get_quest_status(self, quest_id: str) -> str:
        if quest_id in self.quests:
            quest = self.quests[quest_id]
            if quest.is_completed:
                return "Выполнен"
            elif quest.is_active:
                if quest.time_limit:
                    time_left = quest.start_time + quest.time_limit - datetime.now()
                    if time_left.total_seconds() > 0:
                        return f"Активен (осталось времени: {time_left})"
                    else:
                        self.fail_quest(quest_id)
                        return "Провален (время истекло)"
                return f"Активен (прогресс: {quest.progress}/{quest.max_progress})"
            else:
                if all(self.quests[prereq].is_completed for prereq in quest.prerequisites):
                    return "Доступен"
                else:
                    return "Недоступен (не выполнены предварительные условия)"
        else:
            return "Квест не найден"

    def fail_quest(self, quest_id: str):
        if quest_id in self.quests and self.quests[quest_id].is_active:
            quest = self.quests[quest_id]
            quest.is_active = False
            self.active_quests.remove(quest)
            print(f"Квест '{quest.name}' провален.")
            if quest.repeatable:
                quest.progress = 0

    def save_quests(self, filename: str):
        quest_data = {quest_id: {
            'is_completed': quest.is_completed,
            'is_active': quest.is_active,
            'progress': quest.progress,
            'start_time': quest.start_time.isoformat() if quest.start_time else None
        } for quest_id, quest in self.quests.items()}
        
        with open(filename, 'w') as f:
            json.dump(quest_data, f)

    def load_quests(self, filename: str):
        with open(filename, 'r') as f:
            quest_data = json.load(f)
        
        for quest_id, data in quest_data.items():
            if quest_id in self.quests:
                quest = self.quests[quest_id]
                quest.is_completed = data['is_completed']
                quest.is_active = data['is_active']
                quest.progress = data['progress']
                quest.start_time = datetime.fromisoformat(data['start_time']) if data['start_time'] else None
                
                if quest.is_active and quest not in self.active_quests:
                    self.active_quests.append(quest)
                elif not quest.is_active and quest in self.active_quests:
                    self.active_quests.remove(quest)

# Пример использования
quest_manager = QuestManager()

# Создание квестов
quest1 = Quest(
    id="q1",
    name="Спасение деревни",
    description="Защитите деревню от нападения монстров",
    objective="Победите 5 монстров возле деревни",
    reward={"опыт": 100, "золото": 50},
    max_progress=5
)

quest2 = Quest(
    id="q2",
    name="Поиск артефакта",
    description="Найдите древний артефакт в заброшенном храме",
    objective="Исследуйте храм и найдите артефакт",
    reward={"опыт": 200, "артефакт": 1},
    prerequisites=["q1"],
    time_limit=timedelta(hours=2)
)

quest3 = Quest(
    id="q3",
    name="Ежедневная тренировка",
    description="Выполните ежедневные упражнения",
    objective="Победите 3 тренировочных манекена",
    reward={"опыт": 50, "золото": 10},
    max_progress=3,
    repeatable=True
)

# Добавление квестов в менеджер
quest_manager.add_quest(quest1)
quest_manager.add_quest(quest2)
quest_manager.add_quest(quest3)

# Пример игрового цикла
def game_loop():
    quest_manager.start_quest("q1")
    
    # Симуляция прогресса квеста
    for i in range(5):
        print(f"Сражение с монстром {i+1}")
        reward = quest_manager.update_quest_progress("q1", 1)
        if reward:
            print(f"Получена награда: {reward}")
    
    # Попытка начать квест с предварительными условиями
    quest_manager.start_quest("q2")
    
    # Начало повторяемого квеста
    quest_manager.start_quest("q3")
    quest_manager.update_quest_progress("q3", 3)
    

    # Вывод статуса всех квестов
    print("\nСтатус квестов:")
    for quest in quest_manager.get_all_quests():
        print(f"{quest.name}: {quest_manager.get_quest_status(quest.id)}")

    # Сохранение состояния квестов
    quest_manager.save_quests("quests_save.json")

    # Симуляция перезапуска игры
    new_quest_manager = QuestManager()
    new_quest_manager.add_quest(quest1)
    new_quest_manager.add_quest(quest2)
    new_quest_manager.add_quest(quest3)
    new_quest_manager.load_quests("quests_save.json")

    print("\nСостояние квестов после загрузки:")
    for quest in new_quest_manager.get_all_quests():
        print(f"{quest.name}: {new_quest_manager.get_quest_status(quest.id)}")

    # Попытка повторного выполнения ежедневного квеста
    new_quest_manager.start_quest("q3")
    new_quest_manager.update_quest_progress("q3", 3)

    print("\nФинальное состояние квестов:")
    for quest in new_quest_manager.get_all_quests():
        print(f"{quest.name}: {new_quest_manager.get_quest_status(quest.id)}")

# Запуск игрового цикла
game_loop()