import os
import sys
import importlib
import inspect
from typing import Callable, Dict, List
from telegram.ext import CommandHandler

from utils.logger import Logger

class PluginManager:
    """
    Manages loading, reloading, and executing plugins for a Telegram bot.

    Attributes:
        plugin_folder (str): The folder where plugin files are stored.
        commands (Dict[str, Callable]): A dictionary mapping command names to their corresponding handler functions.
        help_texts (Dict[str, str]): A dictionary mapping command names to their help text descriptions.
        loaded_modules (List[str]): A list of module names that have been loaded.
    """

    def __init__(self, plugin_folder: str = "plugins"):
        """
        Initializes the PluginManager with the specified folder for plugins.
        
        Args:
            plugin_folder (str): The folder where plugin files are stored (default is "plugins").
        """
        self.plugin_folder = plugin_folder
        self.commands: Dict[str, Callable] = {}
        self.help_texts: Dict[str, str] = {}
        self.loaded_modules: List[str] = []
        self.load_plugin()

    def load_plugin(self):
        """
        Loads all plugins from the specified plugin folder, registering any commands found in them.
        Plugins should contain async functions starting with 'cmd_' to be recognized as commands.
        """
        os.makedirs(self.plugin_folder, exist_ok=True)
        
        load_count = 0
        error_count = 0
        
        for file in filter(lambda f: f.endswith(".py") and f != "__init__.py", os.listdir(self.plugin_folder)):
            module_name = f"{self.plugin_folder}.{file[:-3]}"
            try:
                module = importlib.import_module(module_name)
                
                if module_name not in self.loaded_modules:
                    self.loaded_modules.append(module_name)

                cmd_count = 0
                for name, func in inspect.getmembers(module, inspect.iscoroutinefunction):
                    if name.startswith("cmd_"):
                        command = name[4:]  
                        self.commands[command] = func
                        self.help_texts[command] = (func.__doc__ or "No description").strip()
                        cmd_count += 1
                
                if cmd_count > 0:
                    load_count += 1
            except Exception as e:
                error_count += 1
                Logger.error(f"Error loading plugin {module_name}: {e}")
        
        # Log summary instead of individual plugin loads
        if load_count > 0:
            Logger.info(f"Loaded {load_count} plugin(s) with {len(self.commands)} command(s)")
        if error_count > 0:
            Logger.info(f"Failed to load {error_count} plugin(s)")

    def get_handlers(self) -> List[CommandHandler]:
        """
        Returns a list of CommandHandler objects corresponding to the loaded commands.
        
        Returns:
            List[CommandHandler]: A list of CommandHandler objects for each command.
        """
        return [CommandHandler(cmd, func) for cmd, func in self.commands.items()]

    def get_help(self) -> str:
        """
        Generates and returns a formatted help message with a list of available commands.
        
        Returns:
            str: A help message listing all available commands and their descriptions.
        """
        help_text = ["# Available Command:"]
        help_text.append("/help - Show this message")
        help_text.append("/reload - Reload plugins")
        help_text.extend([f"/{cmd} - {desc.splitlines()[0]}" for cmd, desc in self.help_texts.items()])
        
        return "\n".join(help_text)

    def reload(self) -> int:
        """
        Reloads all plugins, clearing the current commands and reloading the plugin folder.
        
        Returns:
            int: The number of commands loaded after reloading the plugins.
        """
        self.commands = {}
        self.help_texts = {}
        
        reload_count = 0
        error_count = 0
        
        for module_name in self.loaded_modules:
            try:
                if module_name in sys.modules:
                    importlib.reload(sys.modules[module_name])
                    reload_count += 1
            except Exception as e:
                error_count += 1
                Logger.error(f"Error reloading module {module_name}: {e}")
        
        if reload_count > 0:
            Logger.info(f"Reloaded {reload_count} module(s)")
        
        self.loaded_modules = []
        
        importlib.invalidate_caches()
        
        self.load_plugin()
        
        return len(self.commands)