import os
from typing import Dict, Any, Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

class DatabaseConfig:
    """
    Database configuration and connection management for the health coaching system.

    Supports multiple database backends:
    - SQLite for development and testing
    - PostgreSQL for production
    - Memory database for unit tests

    Features:
    - Connection pooling for performance
    - Environment-based configuration
    - Secure credential management
    - Migration support
    - Backup and recovery settings
    """

    def __init__(self):
        self.environment = os.getenv("ENVIRONMENT", "development")
        self.database_configs = self._load_database_configs()
        self.engine = None
        self.session_factory = None

    def _load_database_configs(self) -> Dict[str, Dict[str, Any]]:
        """
        Load database configurations for different environments
        """
        return {
            "development": {
                "database_url": os.getenv("DEV_DATABASE_URL", "sqlite:///./coach_dev.db"),
                "pool_size": 5,
                "max_overflow": 10,
                "pool_timeout": 30,
                "pool_recycle": 3600,
                "echo": True,  # SQL logging for development
                "backup_enabled": False
            },

            "testing": {
                "database_url": "sqlite:///:memory:",
                "pool_size": 1,
                "max_overflow": 0,
                "pool_timeout": 30,
                "pool_recycle": -1,
                "echo": False,
                "backup_enabled": False
            },

            "staging": {
                "database_url": os.getenv("STAGING_DATABASE_URL"),
                "pool_size": 10,
                "max_overflow": 20,
                "pool_timeout": 30,
                "pool_recycle": 3600,
                "echo": False,
                "backup_enabled": True,
                "backup_schedule": "daily"
            },

            "production": {
                "database_url": os.getenv("PROD_DATABASE_URL"),
                "pool_size": 20,
                "max_overflow": 40,
                "pool_timeout": 30,
                "pool_recycle": 3600,
                "echo": False,
                "backup_enabled": True,
                "backup_schedule": "hourly",
                "ssl_required": True,
                "connection_encryption": True
            }
        }

    def get_database_url(self) -> str:
        """
        Get database URL for current environment
        """
        config = self.database_configs.get(self.environment, self.database_configs["development"])
        return config["database_url"]

    def create_engine(self, database_url: Optional[str] = None):
        """
        Create SQLAlchemy engine with appropriate configuration
        """
        if database_url is None:
            database_url = self.get_database_url()

        config = self.database_configs.get(self.environment, self.database_configs["development"])

        # Engine configuration based on database type
        if database_url.startswith("sqlite"):
            # SQLite-specific configuration
            engine_kwargs = {
                "echo": config.get("echo", False),
                "connect_args": {
                    "check_same_thread": False,
                    "timeout": 30
                }
            }
        else:
            # PostgreSQL and other database configuration
            engine_kwargs = {
                "echo": config.get("echo", False),
                "poolclass": QueuePool,
                "pool_size": config.get("pool_size", 10),
                "max_overflow": config.get("max_overflow", 20),
                "pool_timeout": config.get("pool_timeout", 30),
                "pool_recycle": config.get("pool_recycle", 3600),
                "pool_pre_ping": True  # Verify connections before use
            }

            # Add SSL configuration for production
            if config.get("ssl_required", False):
                engine_kwargs["connect_args"] = {
                    "sslmode": "require",
                    "sslcert": os.getenv("DB_SSL_CERT"),
                    "sslkey": os.getenv("DB_SSL_KEY"),
                    "sslrootcert": os.getenv("DB_SSL_ROOT_CERT")
                }

        self.engine = create_engine(database_url, **engine_kwargs)
        self.session_factory = sessionmaker(bind=self.engine)

        return self.engine

    def get_session(self):
        """
        Get database session for transactions
        """
        if self.session_factory is None:
            self.create_engine()
        return self.session_factory()

    def initialize_database(self):
        """
        Initialize database schema and create tables
        """
        from database.models.user_models import Base as UserBase
        from database.models.training_models import Base as TrainingBase
        from database.models.health_models import Base as HealthBase

        if self.engine is None:
            self.create_engine()

        # Create all tables
        UserBase.metadata.create_all(self.engine)
        TrainingBase.metadata.create_all(self.engine)
        HealthBase.metadata.create_all(self.engine)

    def get_backup_configuration(self) -> Dict[str, Any]:
        """
        Get backup configuration for current environment
        """
        config = self.database_configs.get(self.environment, {})

        if not config.get("backup_enabled", False):
            return {"enabled": False}

        return {
            "enabled": True,
            "schedule": config.get("backup_schedule", "daily"),
            "retention_days": config.get("backup_retention_days", 30),
            "backup_location": os.getenv("BACKUP_LOCATION", "./backups"),
            "compression": config.get("backup_compression", True),
            "encryption": config.get("backup_encryption", False)
        }

    def get_migration_configuration(self) -> Dict[str, Any]:
        """
        Get database migration configuration
        """
        return {
            "migration_directory": "./migrations",
            "auto_migration": self.environment != "production",
            "backup_before_migration": self.environment == "production",
            "rollback_enabled": True,
            "migration_timeout": 300  # 5 minutes
        }

    def health_check(self) -> Dict[str, Any]:
        """
        Perform database health check
        """
        try:
            if self.engine is None:
                self.create_engine()

            # Test connection
            with self.engine.connect() as connection:
                result = connection.execute("SELECT 1")
                result.fetchone()

            # Get connection pool status
            pool = self.engine.pool

            return {
                "status": "healthy",
                "database_url": self.get_database_url().split("@")[-1] if "@" in self.get_database_url() else self.get_database_url(),
                "environment": self.environment,
                "pool_size": getattr(pool, "size", None),
                "checked_in": getattr(pool, "checkedin", None),
                "checked_out": getattr(pool, "checkedout", None),
                "overflow": getattr(pool, "overflow", None)
            }

        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "environment": self.environment
            }

# Global database instance
db_config = DatabaseConfig()