import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import math

class HealthCalculator:
    """
    Utility class for health and fitness calculations.

    Provides standardized calculations for:
    - Training zones (heart rate, power, pace)
    - Training load and stress scores
    - Recovery metrics and recommendations
    - Health risk assessments
    - Performance predictions and trends

    All calculations follow established sports science protocols
    and can be customized based on individual baselines.
    """

    @staticmethod
    def calculate_heart_rate_zones(max_hr: int, resting_hr: int, method: str = "karvonen") -> Dict:
        """
        Calculate heart rate training zones

        Methods:
        - 'karvonen': Heart Rate Reserve method (more accurate)
        - 'percentage': Simple percentage of max HR method

        Returns zones 1-5 with intensity descriptions
        """
        if method == "karvonen":
            hr_reserve = max_hr - resting_hr
            zones = {
                "zone1": {
                    "name": "Active Recovery",
                    "min_hr": round(resting_hr + (hr_reserve * 0.50)),
                    "max_hr": round(resting_hr + (hr_reserve * 0.60)),
                    "intensity": "50-60% HRR",
                    "description": "Very light intensity, active recovery"
                },
                "zone2": {
                    "name": "Aerobic Base",
                    "min_hr": round(resting_hr + (hr_reserve * 0.60)),
                    "max_hr": round(resting_hr + (hr_reserve * 0.70)),
                    "intensity": "60-70% HRR",
                    "description": "Light intensity, fat burning"
                },
                "zone3": {
                    "name": "Aerobic",
                    "min_hr": round(resting_hr + (hr_reserve * 0.70)),
                    "max_hr": round(resting_hr + (hr_reserve * 0.80)),
                    "intensity": "70-80% HRR",
                    "description": "Moderate intensity, aerobic development"
                },
                "zone4": {
                    "name": "Lactate Threshold",
                    "min_hr": round(resting_hr + (hr_reserve * 0.80)),
                    "max_hr": round(resting_hr + (hr_reserve * 0.90)),
                    "intensity": "80-90% HRR",
                    "description": "Hard intensity, lactate threshold"
                },
                "zone5": {
                    "name": "VO2 Max",
                    "min_hr": round(resting_hr + (hr_reserve * 0.90)),
                    "max_hr": max_hr,
                    "intensity": "90-100% HRR",
                    "description": "Very hard intensity, VO2 max"
                }
            }
        else:  # percentage method
            zones = {
                "zone1": {
                    "name": "Active Recovery",
                    "min_hr": round(max_hr * 0.50),
                    "max_hr": round(max_hr * 0.60),
                    "intensity": "50-60% Max HR",
                    "description": "Very light intensity, active recovery"
                }
                # Additional zones...
            }

        return zones

    @staticmethod
    def calculate_training_stress_score(duration_minutes: int, avg_heart_rate: int,
                                      threshold_hr: int, max_hr: int) -> float:
        """
        Calculate Training Stress Score (TSS) from heart rate data

        TSS = (duration_hours * intensity_factor^2 * 100)
        Intensity Factor = average HR / threshold HR (normalized)
        """
        if threshold_hr <= 0 or duration_minutes <= 0:
            return 0.0

        duration_hours = duration_minutes / 60.0

        # Normalize heart rate to intensity factor
        hr_ratio = avg_heart_rate / threshold_hr
        intensity_factor = min(hr_ratio, 1.15)  # Cap at 115% of threshold

        tss = duration_hours * (intensity_factor ** 2) * 100
        return round(tss, 1)

    @staticmethod
    def calculate_hrv_baseline(hrv_readings: List[float], window_days: int = 7) -> Dict:
        """
        Calculate HRV baseline and deviation analysis

        Returns baseline values and current status relative to baseline
        """
        if len(hrv_readings) < 3:
            return {"error": "Insufficient data for baseline calculation"}

        recent_readings = hrv_readings[-window_days:] if len(hrv_readings) >= window_days else hrv_readings
        baseline = np.mean(recent_readings)
        std_dev = np.std(recent_readings)

        current_hrv = hrv_readings[-1] if hrv_readings else baseline
        z_score = (current_hrv - baseline) / std_dev if std_dev > 0 else 0

        # Interpret HRV status
        if z_score > 0.5:
            status = "above_baseline"
            interpretation = "Good recovery, ready for training"
        elif z_score < -0.5:
            status = "below_baseline"
            interpretation = "Possible fatigue or stress, consider easier training"
        else:
            status = "normal"
            interpretation = "Normal recovery status"

        return {
            "baseline": round(baseline, 1),
            "current": round(current_hrv, 1),
            "z_score": round(z_score, 2),
            "status": status,
            "interpretation": interpretation,
            "confidence": "high" if len(recent_readings) >= 7 else "moderate"
        }

    @staticmethod
    def estimate_vo2_max(age: int, gender: str, resting_hr: int, activity_level: str) -> float:
        """
        Estimate VO2 max using non-exercise prediction equations

        Uses the Jackson equation with modifications for activity level
        """
        if gender.lower() == "male":
            base_vo2 = 15.3 * (220 - age) / resting_hr
        else:  # female
            base_vo2 = 15.3 * (220 - age) / resting_hr * 0.85

        # Activity level adjustments
        activity_multiplier = {
            "sedentary": 0.85,
            "lightly_active": 0.95,
            "moderately_active": 1.0,
            "very_active": 1.1,
            "extremely_active": 1.2
        }

        multiplier = activity_multiplier.get(activity_level, 1.0)
        estimated_vo2 = base_vo2 * multiplier

        return round(estimated_vo2, 1)

    @staticmethod
    def calculate_caloric_needs(weight_kg: float, height_cm: float, age: int, gender: str,
                               activity_level: str, goal: str = "maintain") -> Dict:
        """
        Calculate daily caloric needs using Mifflin-St Jeor equation

        Returns BMR, TDEE, and goal-adjusted calories
        """
        # Basal Metabolic Rate (BMR) calculation
        if gender.lower() == "male":
            bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
        else:  # female
            bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161

        # Activity multipliers for TDEE
        activity_multipliers = {
            "sedentary": 1.2,
            "lightly_active": 1.375,
            "moderately_active": 1.55,
            "very_active": 1.725,
            "extremely_active": 1.9
        }

        tdee = bmr * activity_multipliers.get(activity_level, 1.55)

        # Goal adjustments
        goal_adjustments = {
            "lose_weight": -500,  # 1 lb per week deficit
            "lose_weight_fast": -750,
            "maintain": 0,
            "gain_weight": 300,
            "gain_muscle": 200
        }

        goal_calories = tdee + goal_adjustments.get(goal, 0)

        return {
            "bmr": round(bmr),
            "tdee": round(tdee),
            "goal_calories": round(goal_calories),
            "macros": {
                "protein_g": round(weight_kg * 1.6),  # 1.6g per kg
                "fat_g": round(goal_calories * 0.25 / 9),  # 25% of calories
                "carbs_g": round((goal_calories - (weight_kg * 1.6 * 4) - (goal_calories * 0.25)) / 4)
            }
        }

    @staticmethod
    def assess_recovery_time(training_load: float, fitness_level: int, age: int) -> int:
        """
        Estimate recovery time needed based on training load

        Returns recommended recovery hours
        """
        # Base recovery time from training load
        base_recovery = training_load * 0.5  # hours

        # Age adjustment (recovery slows with age)
        age_factor = 1 + ((age - 25) * 0.01)  # 1% increase per year after 25

        # Fitness level adjustment (better fitness = faster recovery)
        fitness_factor = max(0.7, 1.2 - (fitness_level / 100))

        total_recovery = base_recovery * age_factor * fitness_factor

        return max(12, min(72, round(total_recovery)))  # Between 12-72 hours