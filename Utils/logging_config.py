import os
from typing import Optional
from loguru import logger

class LoggerConfig:
    """Simple configuration class for Loguru loggers across the project."""
    
    _initialized: bool = False
    _log_directory: Optional[str] = None
    
    @classmethod
    def initialize(cls, log_directory: Optional[str] = None, base_directory: Optional[str] = None):
        """Initialize logging system with Loguru."""
        # Store the log directory
        cls._log_directory = log_directory
        
        # Remove all existing handlers
        logger.remove()
        
        # Add console handler with colorful format
        logger.add(
            sink=lambda msg: print(msg, end=""),
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <cyan>{name}</cyan> | <level>{level: <8}</level> | <white>{message}</white>",
            level="INFO"
        )
        
        # Add file handler with clean format
        logger.add(
            sink=os.path.join(log_directory, "app_{time:YYYY-MM-DD}.log"),
            rotation="00:00",  # Create new file at midnight
            retention="30 days",
            format="{time:YYYY-MM-DD HH:mm:ss} | {name} | {level: <8} | {message}",
            level="DEBUG"
        )
        
        cls._initialized = True
    
    @classmethod
    def setup_logger(cls, log_directory: str):
        """
        Set up the logger to write to the specified directory.
        This is an alias for initialize() to maintain backward compatibility.
        
        Args:
            log_directory: Path where log files should be created
        """
        # Create log directory if it doesn't exist
        os.makedirs(log_directory, exist_ok=True)
        
        # Call initialize with the directory
        cls.initialize(log_directory=log_directory)
    
    @classmethod
    def get_log_directory(cls) -> str:
        """Return the current log directory."""
        return cls._log_directory

def get_logger(name: str):
    """Get a logger instance with the specified name."""
    return logger.bind(name=name)

def add_execution_separator(logger, env):
    """
    Adds a separator in logs to indicate a new execution.
    
    Args:
        logger: The logger instance to use
        env: Environment name
    """
    separator = "=" * 80
    logger.info(f"\n{separator}\n🚀 NEW TEST EXECUTION STARTING ON {env}\n{separator}\n")