import random
import time
from datetime import datetime

# מחלקה זו מגדירה סוג מזון והיכן הוא מאוחסן
class FoodType:
    def __init__(self, name: str, storage_location: str):
        self.name = name
        self.storage_location = storage_location # היכן נמצא האוכל (על הקרקע, בשקיות וכו')
# מחלקה זו מגדירה את תוכנית ההאכלה לפרות, על סמך העונה או החג
class NutritionPlan:
    def __init__(self, season: str, holiday: str = None):
        self.season = season
        self.holiday = holiday
        self.plans = {}  # מחזיק את תוכנית המזון לכל רפת וסוג פרה

    # קבעו תוכנית האכלה עבור סככה וסוג פרה ספציפיים
    def set_plan(self, shed_id: str, cow_type: str, food_mix: dict):
        if shed_id not in self.plans:
            self.plans[shed_id] = {}
        self.plans[shed_id][cow_type] = food_mix

    # קבלו את תערובת המזון לסוג רפת ופרה
    def get_food_mix(self, shed_id: str, cow_type: str):
        return self.plans.get(shed_id, {}).get(cow_type, {})

# מחלקה זו מגדירה סככה (בה מחזיקים פרות), ואיזה סוג של פרות יש
class Shed:
    def __init__(self, shed_id: str, cow_type: str, cow_count: int):
        self.shed_id = shed_id
        self.cow_type = cow_type
        self.cow_count = cow_count

# זוהי המערכת המרכזית המנהלת את פעולות ההאכלה בחווה
class MooMoverSystem:
    def __init__(self):
        self.food_types = {} # רשימת סוגי מזון
        self.nutrition_plan = None  # תוכנית התזונה הנוכחית
        self.sheds = [] # רשימת כל הסככות
        self.food_storage = {}  # כמה מכל מזון יש במלאי
        self.water_tank_liters = 200  # כמות מים זמינה לערבוב
        self.distributions_per_day = 4  # מספר הפעמים שהאוכל מוגש ביום
        self.food_pushes_per_day = 6 # מספר הפעמים שאוכל נדחק לאחור

    # הוסף מזון חדש למערכת
    def add_food_type(self, food_type: FoodType):
        self.food_types[food_type.name] = food_type
        self.food_storage[food_type.name] = 1000  # התחל עם 1000 ק"ג מכל מזון

    # הגדר את תוכנית ההאכלה ליום
    def set_nutrition_plan(self, plan: NutritionPlan):
        self.nutrition_plan = plan

    # הוסף סככה חדשה (והפרות שלה) למערכת
    def add_shed(self, shed: Shed):
        self.sheds.append(shed)

    # אסוף את הכמות הנכונה של מזון עבור סככה ספציפית
    def collect_food(self, shed: Shed):
        print(f"\n📦 Collecting food for Shed {shed.shed_id} ({shed.cow_type})...")
        food_mix = self.nutrition_plan.get_food_mix(shed.shed_id, shed.cow_type)
        total_mix = {}
        for food_name, kg_per_cow in food_mix.items():
            total_kg = kg_per_cow * shed.cow_count  # סך מזון = כמות פרה × מספר פרות
            if self.food_storage[food_name] < total_kg:
                raise ValueError(f"❌ Not enough {food_name} in stock!")
            self.food_storage[food_name] -= total_kg # צמצם מלאי
            total_mix[food_name] = total_kg
            print(f"✅ Collected {total_kg:.2f} kg of {food_name} from {self.food_types[food_name].storage_location}")
        return total_mix

    # מערבבים את כל מרכיבי המזון יחד באופן שווה
    def mix_food(self, total_mix: dict):
        print("🔄 Mixing food for uniform distribution...")
        time.sleep(1)
        print("✅ Mix completed.")
        return total_mix
    # פונקציה הבודקת הרם המעבר פנוי
    def check_clear_path(self, shed: Shed):
        print(f"🛤️ Checking clear path to Shed {shed.shed_id}...")
        for attempt in range(3):
            path_clear = random.choice([True, False, True])  # More likely to be clear
            if path_clear:
                print("✅ Path is clear.")
                return True
            else:
                print("⚠️ Path is blocked. Attempting to clear...")
                time.sleep(0.5)
        print(f"❌ Failed to clear path to Shed {shed.shed_id}. Skipping distribution.")
        return False

    # הוסף מים למזון כדי להקל על הפרות
    def add_water(self, mix: dict):
        print("💧 Adding water to soften the mix...")
        liters_added = min(self.water_tank_liters, 30) # הוסף עד 30 ליטר בכל פעם
        self.water_tank_liters -= liters_added
        print(f"✅ {liters_added} liters of water added.")
        return mix

    # העבירו את האוכל המוכן לפרות בדיר
    def distribute_food(self, shed: Shed, mix: dict):
        print(f"🚜 Distributing food in Shed {shed.shed_id}...")
        portion = sum(mix.values()) / shed.cow_count  # חלקו את סך האוכל באופן שווה
        for cow_id in range(1, shed.cow_count + 1):
            eaten = portion * random.uniform(0.75, 1.0)  # כל פרה אוכלת בין 75% ל-100%
            print(f"Cow {cow_id}: Given {portion:.2f} kg, ate {eaten:.2f} kg")

    # דחוף לאחור מזון שנשפך או לא נאכל
    def push_food_back(self, shed: Shed):
        print(f"🧹 Pushing back spilled food in Shed {shed.shed_id}...")
        time.sleep(0.5)
        print("✅ Food pushed back.")

    # הפעל את כל תהליך ההאכלה במשך היום
   
    def run_daily_cycle(self):
        print(f"\n===== 🚀 Starting Daily Feeding Cycle: {datetime.now().strftime('%Y-%m-%d')} =====")
        for i in range(self.distributions_per_day):
            print(f"\n🔁 Feeding Round {i+1}/{self.distributions_per_day}")
            for shed in self.sheds:
                mix = self.collect_food(shed)
                mixed = self.mix_food(mix)
                softened = self.add_water(mixed)
                self.distribute_food(shed, softened)

        for i in range(self.food_pushes_per_day):
            print(f"\n🔁 Food Push Round {i+1}/{self.food_pushes_per_day}")
            for shed in self.sheds:
                self.push_food_back(shed)

        print("\n✅ Daily cycle completed.\n=====================================================\n")


# === שימוש לדוגמה ===
if __name__ == "__main__":
    moo = MooMoverSystem()

    # הוסף סוגים שונים של מזון למערכת
    moo.add_food_type(FoodType("Hay", "Ground Zone A"))
    moo.add_food_type(FoodType("Corn", "Bag Area B"))
    moo.add_food_type(FoodType("Minerals", "Bag Area C"))
    moo.add_food_type(FoodType("Silage", "Ground Zone D"))

    # צור תוכנית האכלה לעונת האביב ולחג הפסח
    plan = NutritionPlan(season="Spring", holiday="Passover")
    plan.set_plan("Shed1", "Milking Cows", {"Hay": 4, "Corn": 3, "Minerals": 0.5})
    plan.set_plan("Shed2", "Calves", {"Hay": 2, "Silage": 3})
    moo.set_nutrition_plan(plan)

    # הוסף שתי סככות עם סוגים שונים של פרות
    moo.add_shed(Shed("Shed1", "Milking Cows", 5))
    moo.add_shed(Shed("Shed2", "Calves", 4))

    # הפעל את תהליך ההאכלה והמזון המלא להיום
    moo.run_daily_cycle()
