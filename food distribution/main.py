import random
import time
from datetime import datetime

# This class defines a type of food and where it's stored
class FoodType:
    def __init__(self, name: str, storage_location: str):
        self.name = name
        self.storage_location = storage_location  # Where the food is located (on the ground, in bags, etc.)

# This class defines the feeding plan for cows, based on the season or holiday
class NutritionPlan:
    def __init__(self, season: str, holiday: str = None):
        self.season = season
        self.holiday = holiday
        self.plans = {}  # Holds the food plan for each shed and cow type

    # Set a feeding plan for a specific shed and cow type
    def set_plan(self, shed_id: str, cow_type: str, food_mix: dict):
        if shed_id not in self.plans:
            self.plans[shed_id] = {}
        self.plans[shed_id][cow_type] = food_mix

    # Get the food mix for a shed and cow type
    def get_food_mix(self, shed_id: str, cow_type: str):
        return self.plans.get(shed_id, {}).get(cow_type, {})

# This class defines a shed (where cows are kept), and what type of cows are there
class Shed:
    def __init__(self, shed_id: str, cow_type: str, cow_count: int):
        self.shed_id = shed_id
        self.cow_type = cow_type
        self.cow_count = cow_count

# This is the main system that manages feeding operations on the farm
class MooMoverSystem:
    def __init__(self):
        self.food_types = {}  # List of food types
        self.nutrition_plan = None  # The current nutrition plan
        self.sheds = []  # List of all sheds
        self.food_storage = {}  # How much of each food is in stock
        self.water_tank_liters = 200  # Amount of water available for mixing
        self.distributions_per_day = 4  # Number of times food is served per day
        self.food_pushes_per_day = 6  # Number of times food is pushed back

    # Add a new food to the system
    def add_food_type(self, food_type: FoodType):
        self.food_types[food_type.name] = food_type
        self.food_storage[food_type.name] = 1000  # Start with 1000 kg of each food

    # Set the feeding plan for the day
    def set_nutrition_plan(self, plan: NutritionPlan):
        self.nutrition_plan = plan

    # Add a new shed (and its cows) to the system
    def add_shed(self, shed: Shed):
        self.sheds.append(shed)

    # Collect the correct amount of food for a specific shed
    def collect_food(self, shed: Shed):
        print(f"\n📦 Collecting food for Shed {shed.shed_id} ({shed.cow_type})...")
        food_mix = self.nutrition_plan.get_food_mix(shed.shed_id, shed.cow_type)
        total_mix = {}
        for food_name, kg_per_cow in food_mix.items():
            total_kg = kg_per_cow * shed.cow_count  # Total food = amount per cow × number of cows
            if self.food_storage[food_name] < total_kg:
                raise ValueError(f"❌ Not enough {food_name} in stock!")
            self.food_storage[food_name] -= total_kg  # Reduce stock
            total_mix[food_name] = total_kg
            print(f"✅ Collected {total_kg:.2f} kg of {food_name} from {self.food_types[food_name].storage_location}")
        return total_mix

    # Mix all food ingredients together evenly
    def mix_food(self, total_mix: dict):
        print("🔄 Mixing food for uniform distribution...")
        time.sleep(1)
        print("✅ Mix completed.")
        return total_mix

    # Add water to the food to make it easier for cows to eat
    def add_water(self, mix: dict):
        print("💧 Adding water to soften the mix...")
        liters_added = min(self.water_tank_liters, 30)  # Add up to 30 liters at a time
        self.water_tank_liters -= liters_added
        print(f"✅ {liters_added} liters of water added.")
        return mix

    # Deliver the prepared food to the cows in a shed
    def distribute_food(self, shed: Shed, mix: dict):
        print(f"🚜 Distributing food in Shed {shed.shed_id}...")
        portion = sum(mix.values()) / shed.cow_count  # Divide total food evenly
        for cow_id in range(1, shed.cow_count + 1):
            eaten = portion * random.uniform(0.75, 1.0)  # Each cow eats between 75% to 100%
            print(f"Cow {cow_id}: Given {portion:.2f} kg, ate {eaten:.2f} kg")

    # Push back food that spilled or was not eaten
    def push_food_back(self, shed: Shed):
        print(f"🧹 Pushing back spilled food in Shed {shed.shed_id}...")
        time.sleep(0.5)
        print("✅ Food pushed back.")

    # Run the entire feeding process for the day
    def run_daily_cycle(self):
        print(f"\n===== 🚀 Starting Daily Feeding Cycle: {datetime.now().strftime('%Y-%m-%d')} =====")
        # Repeat the feeding process several times during the day
        for i in range(self.distributions_per_day):
            print(f"\n🔁 Feeding Round {i+1}/{self.distributions_per_day}")
            for shed in self.sheds:
                mix = self.collect_food(shed)
                mixed = self.mix_food(mix)
                softened = self.add_water(mixed)
                self.distribute_food(shed, softened)

        # Push back food several times a day
        for i in range(self.food_pushes_per_day):
            print(f"\n🔁 Food Push Round {i+1}/{self.food_pushes_per_day}")
            for shed in self.sheds:
                self.push_food_back(shed)

        print("\n✅ Daily cycle completed.\n=====================================================\n")


# === Example Usage ===
if __name__ == "__main__":
    moo = MooMoverSystem()

    # Add different types of food to the system
    moo.add_food_type(FoodType("Hay", "Ground Zone A"))
    moo.add_food_type(FoodType("Corn", "Bag Area B"))
    moo.add_food_type(FoodType("Minerals", "Bag Area C"))
    moo.add_food_type(FoodType("Silage", "Ground Zone D"))

    # Create a feeding plan for the spring season and Passover holiday
    plan = NutritionPlan(season="Spring", holiday="Passover")
    plan.set_plan("Shed1", "Milking Cows", {"Hay": 4, "Corn": 3, "Minerals": 0.5})
    plan.set_plan("Shed2", "Calves", {"Hay": 2, "Silage": 3})
    moo.set_nutrition_plan(plan)

    # Add two sheds with different types of cows
    moo.add_shed(Shed("Shed1", "Milking Cows", 5))
    moo.add_shed(Shed("Shed2", "Calves", 4))

    # Run the full feeding and food management process for today
    moo.run_daily_cycle()
