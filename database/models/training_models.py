from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class TrainingPlan(Base):
    """
    Training plan structure and metadata
    """
    __tablename__ = "training_plans"

    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Plan metadata
    name = Column(String, nullable=False)
    description = Column(Text)
    plan_type = Column(String)  # base_building, race_prep, general_fitness
    duration_weeks = Column(Integer)
    difficulty_level = Column(String)  # beginner, intermediate, advanced

    # Plan structure
    phases = Column(JSON)  # Training phases and periodization
    weekly_structure = Column(JSON)  # Days per week, session types
    progression_strategy = Column(JSON)  # How plan progresses over time

    # Goals and targets
    primary_goal = Column(String)
    target_events = Column(JSON)  # Races or events this plan targets
    performance_targets = Column(JSON)  # Specific performance goals

    # Plan status
    status = Column(String, default="active")  # active, paused, completed, archived
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    completion_percentage = Column(Float, default=0.0)

    # Adaptations and modifications
    original_plan_id = Column(String)  # If adapted from another plan
    adaptations_made = Column(JSON)  # Record of plan modifications
    adherence_rate = Column(Float)  # Percentage of workouts completed


class Workout(Base):
    """
    Individual workout sessions within a training plan
    """
    __tablename__ = "workouts"

    id = Column(String, primary_key=True)
    training_plan_id = Column(String, ForeignKey("training_plans.id"))
    user_id = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Workout planning
    planned_date = Column(DateTime)
    workout_type = Column(String)  # easy_run, intervals, strength, recovery
    sport = Column(String)  # running, cycling, swimming, strength
    category = Column(String)  # endurance, speed, strength, recovery

    # Workout structure
    name = Column(String, nullable=False)
    description = Column(Text)
    instructions = Column(Text)
    workout_structure = Column(JSON)  # Detailed workout steps/intervals
    estimated_duration = Column(Integer)  # Minutes
    estimated_tss = Column(Float)  # Training Stress Score

    # Execution tracking
    status = Column(String, default="planned")  # planned, in_progress, completed, skipped
    actual_date = Column(DateTime)
    actual_duration = Column(Integer)
    completion_notes = Column(Text)

    # Performance data (populated after completion)
    garmin_activity_id = Column(String)
    performance_data = Column(JSON)  # Detailed performance metrics
    perceived_exertion = Column(Integer)  # RPE 1-10
    workout_quality = Column(String)  # excellent, good, average, poor

    # Analysis results
    actual_tss = Column(Float)
    training_zones_distribution = Column(JSON)  # Time in each zone
    performance_analysis = Column(JSON)  # Analysis from TrainingAnalyzer


class WorkoutTemplate(Base):
    """
    Reusable workout templates for consistent training
    """
    __tablename__ = "workout_templates"

    id = Column(String, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Template metadata
    name = Column(String, nullable=False)
    description = Column(Text)
    sport = Column(String)
    workout_type = Column(String)
    difficulty_level = Column(String)
    estimated_duration = Column(Integer)

    # Template structure
    workout_structure = Column(JSON)  # Workout intervals and structure
    instructions = Column(Text)
    coaching_tips = Column(Text)
    equipment_needed = Column(JSON)

    # Usage and effectiveness
    usage_count = Column(Integer, default=0)
    average_rating = Column(Float)
    tags = Column(JSON)  # Searchable tags

    # Customization options
    is_customizable = Column(Boolean, default=True)
    variable_parameters = Column(JSON)  # Parameters that can be adjusted
    adaptation_rules = Column(JSON)  # How template adapts to user level


class TrainingLoad(Base):
    """
    Training load tracking and management
    """
    __tablename__ = "training_load"

    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Training stress scores
    daily_tss = Column(Float, default=0.0)
    acute_load = Column(Float)  # 7-day rolling average
    chronic_load = Column(Float)  # 42-day rolling average
    training_stress_balance = Column(Float)  # Chronic - Acute

    # Load distribution
    endurance_load = Column(Float, default=0.0)
    intensity_load = Column(Float, default=0.0)
    strength_load = Column(Float, default=0.0)
    total_volume = Column(Float)  # Total training minutes

    # Training status assessment
    training_status = Column(String)  # productive, maintaining, overreaching
    recommended_focus = Column(String)  # recovery, base, intensity
    load_trend = Column(String)  # increasing, stable, decreasing

    # Recovery metrics
    recovery_time_needed = Column(Integer)  # Hours until next hard session
    adaptation_state = Column(String)  # adapting, adapted, maladapted


class PerformanceMetric(Base):
    """
    Key performance indicators and benchmarks
    """
    __tablename__ = "performance_metrics"

    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    workout_id = Column(String, ForeignKey("workouts.id"))
    metric_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Metric identification
    metric_type = Column(String)  # vo2_max, threshold_pace, max_power
    sport = Column(String)
    test_type = Column(String)  # field_test, lab_test, workout_derived

    # Metric values
    value = Column(Float, nullable=False)
    units = Column(String, nullable=False)
    confidence_level = Column(String)  # high, medium, low
    test_conditions = Column(JSON)  # Weather, equipment, course details

    # Context and analysis
    improvement_from_baseline = Column(Float)  # Percentage improvement
    percentile_ranking = Column(Float)  # Age/gender percentile
    trend_direction = Column(String)  # improving, stable, declining
    next_test_recommended = Column(DateTime)

    # Related data
    contributing_factors = Column(JSON)  # Training, recovery, etc.
    external_factors = Column(JSON)  # Stress, sleep, nutrition