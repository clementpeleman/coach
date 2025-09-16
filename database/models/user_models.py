from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    """
    Core user model storing basic profile information
    """
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Basic demographics
    age = Column(Integer)
    gender = Column(String)  # male, female, other
    height_cm = Column(Float)
    weight_kg = Column(Float)
    timezone = Column(String, default="UTC")

    # Fitness profile
    fitness_level = Column(String)  # beginner, intermediate, advanced
    activity_level = Column(String)  # sedentary, lightly_active, etc.
    years_training = Column(Integer)

    # Health information
    resting_heart_rate = Column(Integer)
    max_heart_rate = Column(Integer)
    vo2_max = Column(Float)
    health_conditions = Column(JSON)  # List of health conditions/limitations

    # Preferences
    preferred_units = Column(String, default="metric")  # metric, imperial
    notification_preferences = Column(JSON)
    privacy_settings = Column(JSON)

    # System
    is_active = Column(Boolean, default=True)
    garmin_connected = Column(Boolean, default=False)
    onboarding_completed = Column(Boolean, default=False)


class UserProfile(Base):
    """
    Extended user profile with detailed preferences and settings
    """
    __tablename__ = "user_profiles"

    user_id = Column(String, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Training preferences
    available_days = Column(JSON)  # Days available for training
    session_duration_preference = Column(Integer)  # Preferred minutes per session
    time_of_day_preference = Column(String)  # morning, afternoon, evening
    equipment_available = Column(JSON)  # List of available equipment
    location_preferences = Column(JSON)  # indoor, outdoor, gym, home

    # Goal information
    primary_goal = Column(String)  # weight_loss, performance, general_fitness
    secondary_goals = Column(JSON)  # Additional goals
    target_events = Column(JSON)  # Races or events training for
    motivation_factors = Column(JSON)  # What motivates the user

    # Limitations and considerations
    injuries_history = Column(JSON)  # Past injuries and current limitations
    medical_clearance = Column(Boolean, default=False)
    exercise_restrictions = Column(JSON)  # Specific exercise limitations

    # Nutrition preferences
    dietary_restrictions = Column(JSON)  # Allergies, vegetarian, etc.
    nutrition_goals = Column(JSON)  # Weight management, performance fuel
    meal_prep_preference = Column(String)  # none, minimal, full
    supplement_preferences = Column(JSON)

    # Communication preferences
    coaching_style_preference = Column(String)  # supportive, direct, technical
    feedback_frequency = Column(String)  # daily, weekly, as_needed
    reminder_preferences = Column(JSON)


class UserBaselines(Base):
    """
    Baseline measurements and metrics for tracking progress
    """
    __tablename__ = "user_baselines"

    user_id = Column(String, primary_key=True)
    established_date = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Cardiovascular baselines
    resting_hr_baseline = Column(Float)
    hrv_baseline = Column(Float)
    max_hr_tested = Column(Integer)
    lactate_threshold_hr = Column(Integer)

    # Performance baselines
    vo2_max_baseline = Column(Float)
    running_pace_baseline = Column(JSON)  # Paces for different distances
    cycling_power_baseline = Column(JSON)  # Power zones
    strength_baselines = Column(JSON)  # Lift maxes

    # Health baselines
    body_composition = Column(JSON)  # Body fat %, muscle mass
    sleep_quality_baseline = Column(Float)
    stress_level_baseline = Column(Float)
    energy_level_baseline = Column(Float)

    # Fitness tests results
    initial_fitness_tests = Column(JSON)  # Results from onboarding tests
    latest_fitness_tests = Column(JSON)  # Most recent test results

    # Metrics for comparison
    baseline_period_start = Column(DateTime)
    baseline_period_end = Column(DateTime)
    baseline_confidence = Column(String)  # high, medium, low


class UserSession(Base):
    """
    User session tracking for personalized experiences
    """
    __tablename__ = "user_sessions"

    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    session_start = Column(DateTime, default=datetime.utcnow)
    session_end = Column(DateTime)

    # Session context
    interaction_type = Column(String)  # chat, checkin, analysis, planning
    platform = Column(String)  # web, mobile, whatsapp
    session_data = Column(JSON)  # Session-specific data

    # Conversation tracking
    message_count = Column(Integer, default=0)
    topics_discussed = Column(JSON)  # List of topics covered
    agents_involved = Column(JSON)  # Which agents participated

    # Outcomes
    goals_set = Column(JSON)  # Any goals set during session
    actions_planned = Column(JSON)  # Planned actions/workouts
    satisfaction_rating = Column(Integer)  # User satisfaction (1-5)

    is_active = Column(Boolean, default=True)