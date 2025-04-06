# -*- coding: utf-8 -*-
#  wai-life-bot - Telegram bot
#  Copyright (c) 2025 waibui
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import os
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
        self.load_plugin()

    def load_plugin(self):
        """
        Loads all plugins from the specified plugin folder, registering any commands found in them.
        Plugins should contain async functions starting with 'cmd_' to be recognized as commands.
        """
        os.makedirs(self.plugin_folder, exist_ok=True)
        
        for file in filter(lambda f: f.endswith(".py") and f != "__init__.py", os.listdir(self.plugin_folder)):
            module_name = f"{self.plugin_folder}.{file[:-3]}"
            try:
                module = importlib.import_module(module_name)

                for name, func in inspect.getmembers(module, inspect.iscoroutinefunction):
                    if name.startswith("cmd_"):
                        command = name[4:]  
                        self.commands[command] = func
                        self.help_texts[command] = (func.__doc__ or "No description").strip()

                Logger.info(f"Loaded plugin: {module_name}")
            except Exception as e:
                Logger.error(f"Error loading plugin {module_name}: {e}")

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
        
        importlib.invalidate_caches()
        self.load_plugin()
        
        return len(self.commands)
