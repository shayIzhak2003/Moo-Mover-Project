import random
import time
from datetime import datetime

class FoodType:
    def __init__(self, name, weight_per_cow):
        self.name = name
        self.weight_per_cow = weight_per_cow  # kg per cow

class MooFeedingSystem:
    def __init__(self, cow_count):
        self.cow_count = cow_count
        self.food_types = []
        self.food_storage = {}
        self.leftovers = {}
        self.appetite_history = {}  # track how much cows eat on average
        self.battery_level = 100  # simulate battery percentage
        self.log = []

    # ---------------- SYSTEM SETUP ----------------

    def add_food_type(self, food_type: FoodType):
        self.food_types.append(food_type)
        self.food_storage[food_type.name] = 0
        self.leftovers[food_type.name] = 0
        self.appetite_history[food_type.name] = []

    def system_diagnostics(self):
        print("\n🔧 Running system diagnostics...")
        time.sleep(1)
        print("✅ All systems operational")
        print(f"🔋 Battery Level: {self.battery_level}%\n")

    def battery_monitor(self):
        self.battery_level -= random.uniform(1, 3)
        if self.battery_level < 20:
            print("⚠️ Low battery warning! Please recharge soon.")
        elif self.battery_level < 5:
            print("❌ Battery critically low. Aborting operation.")
            exit()

    # ---------------- LOADING & MIXING ----------------

    def smart_load_and_mix(self):
        print("🔄 Smart loading and mixing...")
        for food in self.food_types:
            adjustment_factor = self._calculate_adaptive_weight(food.name)
            total_needed = food.weight_per_cow * self.cow_count * adjustment_factor
            self.food_storage[food.name] = total_needed
            print(f"✅ Loaded {total_needed:.2f} kg of {food.name}")

    def _calculate_adaptive_weight(self, food_name):
        history = self.appetite_history[food_name]
        if not history:
            return 1  # default multiplier
        average_consumption = sum(history) / len(history)
        standard = self._get_food_by_name(food_name).weight_per_cow
        if average_consumption < standard * 0.8:
            return 0.9
        elif average_consumption > standard * 1.1:
            return 1.1
        return 1

    def _get_food_by_name(self, name):
        for food in self.food_types:
            if food.name == name:
                return food
        return None

    # ---------------- DISTRIBUTION ----------------

    def detect_obstacle(self):
        camera_obstacle = random.choice([False, False, True])  # less frequent
        radar_obstacle = random.choice([False, False, True])
        return camera_obstacle or radar_obstacle

    def distribute_food(self):
        print("🚜 Distributing food along the trough...")
        for food in self.food_types:
            portion = self.food_storage[food.name] / self.cow_count
            total_eaten = 0
            for cow_id in range(1, self.cow_count + 1):
                if self.detect_obstacle():
                    print(f"🛑 Obstacle detected near cow {cow_id}. Waiting...")
                    time.sleep(2)
                    continue
                eaten = portion * random.uniform(0.7, 1.0)
                leftover = portion - eaten
                total_eaten += eaten
                self.leftovers[food.name] += leftover
                self._log(f"Cow {cow_id} received {portion:.2f} kg of {food.name}, ate {eaten:.2f} kg")
            self.appetite_history[food.name].append(total_eaten / self.cow_count)

    # ---------------- MONITORING ----------------

    def dynamic_refill_check(self):
        print("\n🔁 Checking for food consumption analytics...")
        for food in self.food_types:
            leftover = self.leftovers[food.name]
            standard_total = food.weight_per_cow * self.cow_count
            if leftover > 0.25 * standard_total:
                print(f"⚠️ High leftover for {food.name} ({leftover:.2f} kg). Consider adjusting.")
            else:
                print(f"✅ {food.name} consumption within normal range.")

    def clean_feeder(self):
        print("\n🧽 Cleaning trough after feeding...")
        time.sleep(1)
        print("✨ Trough cleaned successfully.\n")

    def _log(self, message):
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_entry = f"[{timestamp}] {message}"
        print(log_entry)
        self.log.append(log_entry)

    def print_log(self):
        print("\n📊 Feeding Cycle Log:")
        for entry in self.log:
            print(entry)

    # ---------------- MAIN ROUTINE ----------------

    def run_cycle(self):
        print("\n=========== 🐮 MOO Feeding Cycle Started ===========")
        self.system_diagnostics()
        self.battery_monitor()
        self.smart_load_and_mix()
        self.distribute_food()
        self.dynamic_refill_check()
        self.clean_feeder()
        self.battery_monitor()
        self.print_log()
        print("=========== ✅ Cycle Complete ===========\n")
        
        
if __name__ == "__main__":
    moo_system = MooFeedingSystem(cow_count=6)

    moo_system.add_food_type(FoodType("Hay", 4.5))
    moo_system.add_food_type(FoodType("Corn", 2.8))
    moo_system.add_food_type(FoodType("Minerals", 0.6))

    # Run multiple feeding cycles
    for day in range(1, 4):
        print(f"🌄 Day {day}")
        moo_system.run_cycle()
        time.sleep(2)
 
