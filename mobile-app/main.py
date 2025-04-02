
import requests
import random
import time

URL = "http://127.0.0.1:5000/devices"

devices = [
    "Samsung Galaxy A54",
    "iPhone 14 Pro",
    "Google Pixel 7",
    "OnePlus 11",
    "Xiaomi Mi 12"
]

def generate_device_data():
    device_name = random.choice(devices)
    data = {
        device_name: {
            "battery": f"{random.randint(10, 100)}%",
            "signal_strength": f"{random.randint(1, 5)} bars",
            "GPS": random.choice(["Yoqilgan", "O'chirilgan"]),
            "WiFi_status": random.choice(["Ulangan", "Uzilgan"]),
            "last_seen": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    }
    return data

while True:
    device_data = generate_device_data()
    response = requests.post(URL, json=device_data)

    if response.status_code == 200:
        print(f"✅ Yangi ma'lumot yuborildi: {device_data}")
    else:
        print(f"❌ Xatolik: {response.status_code}, {response.text}")

    time.sleep(20)  # Har 20 soniyada yangi ma’lumot yuborish
