# =========================================================
# File: dynamic_ambulance_priority_ai.py
# Project: AI-based Dynamic Ambulance Priority System
# Description:
#   Simulates real-time ambulance patient vitals and
#   dynamically recalculates priority (0–10) for green corridor
#   decision making without using real sensors.
# =========================================================

import random
import time


# ---------------------------------------------------------
# 1. Base Medical Priority (Static Context)
# ---------------------------------------------------------
def base_medical_priority(emergency_type):
    priority_map = {
        "cardiac_arrest": 5,
        "stroke": 4,
        "severe_accident": 4,
        "trauma": 3,
        "minor_injury": 1
    }
    return priority_map.get(emergency_type, 2)


# ---------------------------------------------------------
# 2. Vital Risk Analysis (Dynamic Intelligence)
# ---------------------------------------------------------
def spo2_risk(spo2):
    if spo2 < 85:
        return 3
    elif spo2 < 90:
        return 2
    elif spo2 < 94:
        return 1
    else:
        return 0


def heart_rate_risk(hr):
    if hr < 40 or hr > 130:
        return 2
    elif hr > 110:
        return 1
    else:
        return 0


def deterioration_risk(prev_spo2, curr_spo2):
    drop = prev_spo2 - curr_spo2
    if drop >= 5:
        return 2
    elif drop >= 2:
        return 1
    else:
        return 0


def vital_risk_score(hr, spo2, prev_spo2):
    risk = (
        spo2_risk(spo2)
        + heart_rate_risk(hr)
        + deterioration_risk(prev_spo2, spo2)
    )
    return min(risk, 5)


# ---------------------------------------------------------
# 3. Time-to-Hospital Risk
# ---------------------------------------------------------
def time_to_hospital_risk(eta_minutes):
    if eta_minutes > 15:
        return 2
    elif eta_minutes > 8:
        return 1
    else:
        return 0


# ---------------------------------------------------------
# 4. Final AI Priority Calculation (0–10)
# ---------------------------------------------------------
def calculate_priority(emergency_type, hr, spo2, prev_spo2, eta):
    priority_score = (
        base_medical_priority(emergency_type)
        + vital_risk_score(hr, spo2, prev_spo2)
        + time_to_hospital_risk(eta)
    )
    return min(priority_score, 10)


# ---------------------------------------------------------
# 5. Priority Category Mapping
# ---------------------------------------------------------
def priority_category(score):
    if score >= 9:
        return "CRITICAL"
    elif score >= 7:
        return "VERY HIGH"
    elif score >= 5:
        return "HIGH"
    elif score >= 3:
        return "MEDIUM"
    else:
        return "LOW"


# ---------------------------------------------------------
# 6. Traffic Signal Decision Logic
# ---------------------------------------------------------
def traffic_decision(priority_level):
    decisions = {
        "CRITICAL": "Immediate green corridor (override all signals)",
        "VERY HIGH": "Green corridor with maximum preference",
        "HIGH": "Green at next signal cycle",
        "MEDIUM": "Partial priority at intersections",
        "LOW": "Normal traffic flow"
    }
    return decisions[priority_level]


# ---------------------------------------------------------
# 7. Fake Sensor Data Generator (Simulated IoT)
# ---------------------------------------------------------
def generate_fake_vitals(prev_spo2):
    heart_rate = random.randint(80, 150)
    spo2 = max(80, min(98, prev_spo2 + random.randint(-4, 2)))
    return heart_rate, spo2


# ---------------------------------------------------------
# 8. Simulation Engine (Main Loop)
# ---------------------------------------------------------
def run_simulation():
    emergency_type = "stroke"   # Change this to test other cases
    eta = 15                    # Initial ETA to hospital (minutes)
    prev_spo2 = 96              # Initial SpO₂ level

    print("\n🚑 AI-Based Dynamic Ambulance Priority Simulation\n")

    for minute in range(1, 9):
        hr, spo2 = generate_fake_vitals(prev_spo2)
        priority = calculate_priority(
            emergency_type, hr, spo2, prev_spo2, eta
        )

        category = priority_category(priority)
        action = traffic_decision(category)

        print(f"Minute {minute}")
        print(f"  Heart Rate        : {hr} bpm")
        print(f"  Oxygen Level (SpO₂): {spo2}%")
        print(f"  ETA to Hospital   : {eta} minutes")
        print(f"  Priority Score    : {priority}/10")
        print(f"  Priority Level    : {category}")
        print(f"  Traffic Action    : {action}")
        print("-" * 55)

        prev_spo2 = spo2
        eta -= 1
        time.sleep(1)   # Simulate real-time delay


# ---------------------------------------------------------
# 9. Program Entry Point
# ---------------------------------------------------------
if __name__ == "__main__":
    run_simulation()
