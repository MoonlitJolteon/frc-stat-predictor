import json
import os


class ConfigurationManager:
    """Manages configuration settings for the application"""

    def __init__(self, config_file="config.json"):
        self.__config_file = config_file
        self.__config = {}
        self.load_config()

    def load_config(self):
        """Load configuration from file"""
        if os.path.exists(self.__config_file):
            try:
                with open(self.__config_file, "r") as f:
                    self.__config = json.load(f)
            except Exception as e:
                print(f"Error loading configuration: {e}")

    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.__config_file, "w") as f:
                json.dump(self.__config, f, indent=4)
        except Exception as e:
            print(f"Error saving configuration: {e}")

    def get(self, key, default=None):
        """Get a configuration value"""
        return self.__config.get(key, default)

    def set(self, key, value):
        """Set a configuration value"""
        self.__config[key] = value
        self.save_config()
