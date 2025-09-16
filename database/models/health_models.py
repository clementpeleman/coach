from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class HealthMetric(Base):
    """
    Daily health and wellness metrics from wearable devices
    """
    __tablename__ = "health_metrics"

    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Heart rate metrics
    resting_heart_rate = Column(Integer)
    heart_rate_variability = Column(Float)  # RMSSD in milliseconds
    max_heart_rate_today = Column(Integer)
    avg_heart_rate_today = Column(Integer)

    # Sleep metrics
    sleep_duration_minutes = Column(Integer)
    sleep_efficiency_percentage = Column(Float)
    deep_sleep_minutes = Column(Integer)
    light_sleep_minutes = Column(Integer)
    rem_sleep_minutes = Column(Integer)
    awake_minutes = Column(Integer)
    sleep_score = Column(Float)  # Overall sleep quality score

    # Stress and recovery
    stress_level_avg = Column(Float)  # Average stress (0-100)
    stress_level_max = Column(Float)  # Peak stress
    body_battery_start = Column(Integer)  # Energy at day start
    body_battery_end = Column(Integer)  # Energy at day end
    body_battery_charged = Column(Integer)  # Energy gained during rest
    body_battery_drained = Column(Integer)  # Energy consumed during activity

    # Activity summary
    steps = Column(Integer)
    floors_climbed = Column(Integer)
    calories_burned = Column(Integer)
    active_calories = Column(Integer)
    distance_meters = Column(Float)
    active_minutes = Column(Integer)
    sedentary_minutes = Column(Integer)

    # Additional wellness
    respiration_rate = Column(Float)  # Breaths per minute
    pulse_ox = Column(Float)  # Blood oxygen saturation
    hydration_level = Column(String)  # well_hydrated, adequate, dehydrated

    # Data quality indicators
    data_completeness = Column(Float)  # Percentage of complete data
    device_wear_time = Column(Integer)  # Minutes device was worn
    sync_timestamp = Column(DateTime)


class SleepSession(Base):
    """
    Detailed sleep session data with stages and events
    """
    __tablename__ = "sleep_sessions"

    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    sleep_date = Column(DateTime, nullable=False)  # Date of sleep (evening start)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Sleep timing
    bedtime = Column(DateTime)
    sleep_onset = Column(DateTime)  # When sleep actually started
    wake_time = Column(DateTime)
    get_up_time = Column(DateTime)  # When got out of bed

    # Sleep quality metrics
    total_sleep_time = Column(Integer)  # Minutes of actual sleep
    sleep_efficiency = Column(Float)  # TST / Time in bed
    sleep_onset_latency = Column(Integer)  # Minutes to fall asleep
    wake_after_sleep_onset = Column(Integer)  # Minutes awake during night
    number_of_awakenings = Column(Integer)

    # Sleep stages (minutes)
    light_sleep = Column(Integer)
    deep_sleep = Column(Integer)
    rem_sleep = Column(Integer)
    awake_time = Column(Integer)

    # Sleep stage percentages
    light_sleep_percentage = Column(Float)
    deep_sleep_percentage = Column(Float)
    rem_sleep_percentage = Column(Float)

    # Sleep scoring and analysis
    sleep_score = Column(Float)  # Overall quality score (0-100)
    restfulness = Column(Float)  # How restful the sleep was
    timing_score = Column(Float)  # Consistency with sleep schedule
    duration_score = Column(Float)  # Adequacy of sleep duration

    # Environmental factors
    bedroom_temperature = Column(Float)
    environmental_data = Column(JSON)  # Noise, light, etc.

    # Subjective measures
    subjective_quality = Column(Integer)  # User-rated quality (1-5)
    morning_energy = Column(Integer)  # Energy level on waking (1-5)
    sleep_notes = Column(Text)  # User notes about sleep


class StressEvent(Base):
    """
    Stress monitoring and stress events throughout the day
    """
    __tablename__ = "stress_events"

    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Stress measurements
    stress_level = Column(Float)  # Stress level (0-100)
    stress_category = Column(String)  # rest, low, medium, high
    duration_minutes = Column(Integer)  # How long stress lasted

    # Context information
    event_type = Column(String)  # work, exercise, personal, unknown
    activity_context = Column(String)  # What user was doing
    location_context = Column(String)  # Where user was

    # Physiological markers
    heart_rate_during = Column(Integer)
    hrv_during = Column(Float)
    respiration_rate = Column(Float)

    # Recovery information
    recovery_time = Column(Integer)  # Minutes to return to baseline
    recovery_complete = Column(Boolean, default=False)

    # User input
    stress_trigger = Column(String)  # User-identified cause
    coping_strategy = Column(String)  # How user handled stress
    effectiveness_rating = Column(Integer)  # How well strategy worked (1-5)


class WellnessAssessment(Base):
    """
    Comprehensive wellness assessments and trends
    """
    __tablename__ = "wellness_assessments"

    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    assessment_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Assessment period
    assessment_type = Column(String)  # daily, weekly, monthly
    period_start = Column(DateTime)
    period_end = Column(DateTime)

    # Composite scores
    overall_wellness_score = Column(Float)  # Composite wellness (0-100)
    readiness_score = Column(Float)  # Training readiness (0-100)
    recovery_score = Column(Float)  # Recovery status (0-100)
    energy_score = Column(Float)  # Energy levels (0-100)

    # Individual domain scores
    sleep_score = Column(Float)
    stress_score = Column(Float)
    activity_score = Column(Float)
    hrv_score = Column(Float)
    nutrition_score = Column(Float)

    # Trend analysis
    trend_direction = Column(String)  # improving, stable, declining
    trend_strength = Column(String)  # strong, moderate, weak
    trend_confidence = Column(Float)  # Statistical confidence

    # Recommendations
    primary_recommendation = Column(String)
    secondary_recommendations = Column(JSON)
    focus_areas = Column(JSON)  # Areas needing attention

    # Risk assessment
    health_risk_level = Column(String)  # low, moderate, high
    overtraining_risk = Column(Float)  # Risk percentage
    illness_risk = Column(Float)  # Risk percentage
    injury_risk = Column(Float)  # Risk percentage

    # Comparative analysis
    percentile_vs_baseline = Column(Float)
    percentile_vs_peers = Column(Float)


class HealthAlert(Base):
    """
    Health alerts and notifications for concerning patterns
    """
    __tablename__ = "health_alerts"

    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    alert_timestamp = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Alert classification
    alert_type = Column(String)  # hrv_deviation, poor_sleep, high_stress
    severity_level = Column(String)  # info, warning, urgent
    category = Column(String)  # recovery, performance, health

    # Alert content
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    detailed_analysis = Column(JSON)

    # Data that triggered alert
    trigger_metric = Column(String)
    trigger_value = Column(Float)
    threshold_value = Column(Float)
    deviation_magnitude = Column(Float)

    # Recommendations
    immediate_actions = Column(JSON)
    lifestyle_adjustments = Column(JSON)
    medical_consultation = Column(Boolean, default=False)

    # Status tracking
    status = Column(String, default="active")  # active, acknowledged, resolved
    acknowledged_at = Column(DateTime)
    resolved_at = Column(DateTime)
    user_response = Column(Text)

    # Follow-up
    requires_follow_up = Column(Boolean, default=False)
    follow_up_date = Column(DateTime)
    resolution_notes = Column(Text)