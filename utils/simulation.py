import random


def generate_sensor_data():

    voltage = random.randint(220, 240)

    current = round(random.uniform(3, 15), 2)

    frequency = round(random.uniform(49.8, 50.2), 2)

    temperature = random.randint(25, 55)

    return {
        "Voltage": voltage,
        "Current": current,
        "Frequency": frequency,
        "Temperature": temperature
    }


if __name__ == "__main__":

    data = generate_sensor_data()

    print(data)