"""
GridGuard AI - Virtual LT Circuit Simulator

Simulates a simplified LT feeder:
Source -> LT Cable -> Load

The calculated electrical values are passed to
the existing GridGuard AI fault-detection system.
"""

import math


# Resistivity in ohm-mm²/m
WIRE_RESISTIVITY = {
    "Copper": 0.0175,
    "Aluminium": 0.0282,
}


def calculate_line_resistance(material, length_m, area_mm2):
    """Calculate LT cable resistance."""

    if material not in WIRE_RESISTIVITY:
        raise ValueError("Unsupported wire material")

    if length_m <= 0:
        raise ValueError("Line length must be greater than 0")

    if area_mm2 <= 0:
        raise ValueError("Wire area must be greater than 0")

    resistivity = WIRE_RESISTIVITY[material]

    # R = rho * L / A
    return resistivity * length_m / area_mm2


def simulate_circuit(
    source_voltage=230.0,
    frequency=50.0,
    material="Copper",
    length_m=100.0,
    area_mm2=16.0,
    load_power_w=1150.0,
    fault="Normal",
    temperature=30.0,
):
    """
    Simulate a simplified single-phase LT feeder.

    Returns:
        voltage, current, frequency, temperature,
        line_resistance, power
    """

    # Calculate cable resistance
    line_resistance = calculate_line_resistance(
        material,
        length_m,
        area_mm2,
    )

    voltage = float(source_voltage)

    # -------------------------------------------------
    # NORMAL / LOAD CONDITION
    # -------------------------------------------------

    if fault == "Normal":
        # Approximate load current
        current = load_power_w / max(voltage, 1.0)

        # Voltage drop through LT line
        voltage_drop = current * line_resistance

        voltage = max(
            source_voltage - voltage_drop,
            0.0,
        )

    # -------------------------------------------------
    # OVERLOAD
    # -------------------------------------------------

    elif fault == "Overload":
        # Increase load demand
        overload_power = load_power_w * 3.0

        current = overload_power / max(source_voltage, 1.0)

        voltage_drop = current * line_resistance

        voltage = max(
            source_voltage - voltage_drop,
            0.0,
        )

        temperature += min(current * 0.8, 20.0)

    # -------------------------------------------------
    # UNDER-VOLTAGE
    # -------------------------------------------------

    elif fault == "Undervoltage":
        # Simulate reduced supply voltage
        voltage = source_voltage * 0.85

        current = load_power_w / max(voltage, 1.0)

    # -------------------------------------------------
    # OVER-VOLTAGE
    # -------------------------------------------------

    elif fault == "Overvoltage":
        # Simulate increased supply voltage
        voltage = source_voltage * 1.20

        current = load_power_w / max(voltage, 1.0)

    # -------------------------------------------------
    # LINE BREAK
    # -------------------------------------------------

    elif fault == "Line Break":
        # Open circuit -> practically no current
        voltage = 0.0
        current = 0.0

    else:
        raise ValueError(
            f"Unknown fault condition: {fault}"
        )

    return {
        "Voltage": round(voltage, 2),
        "Current": round(current, 2),
        "Frequency": round(frequency, 2),
        "Temperature": round(temperature, 2),
        "Line Resistance": round(line_resistance, 4),
        "Load Power": round(load_power_w, 2),
        "Wire Material": material,
        "Line Length": round(length_m, 2),
        "Wire Area": round(area_mm2, 2),
        "Fault Condition": fault,
    }


def get_circuit_status(simulation):
    """Return a simple status for the virtual feeder."""

    voltage = simulation["Voltage"]
    current = simulation["Current"]

    if simulation["Fault Condition"] == "Line Break":
        return "🔴 LINE BROKEN"

    if simulation["Fault Condition"] == "Overload":
        return "🟠 OVERLOADED"

    if simulation["Fault Condition"] == "Undervoltage":
        return "🟡 LOW VOLTAGE"

    if simulation["Fault Condition"] == "Overvoltage":
        return "🟣 HIGH VOLTAGE"

    if voltage == 0 and current == 0:
        return "🔴 NO SUPPLY"

    return "🟢 LINE NORMAL"