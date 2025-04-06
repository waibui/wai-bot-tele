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

import sys
import subprocess
import pkg_resources

# from config.settings import Setting
# from model.exception import DependencyError, RequirementsFileNotFoundError

def install_dependencies():
    """
    Installs missing dependencies listed in the requirements file.

    This function first checks for any missing dependencies and then attempts 
    to install them using `pip`. If an installation fails, it raises an exception.

    Raises:
        DependencyError: If installation of any package fails.
    """
    missing_packages = check_dependencies()
    
    if missing_packages:
        print(f"Installing missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.check_output(
                [sys.executable, "-m", "pip", "install", *missing_packages],
                stderr=subprocess.STDOUT
            )
        except subprocess.CalledProcessError as e:
            # raise DependencyError(f"Failed to install dependencies: {e.output.decode()}") from e
            pass

def get_dependencies():
    """
    Reads and returns the list of dependencies from the requirements.txt file.

    Returns:
        list[str]: A list of required package names.

    Raises:
        RequirementsFileNotFoundError: If the requirements.txt file is not found.
        IOError: If there is an error reading the file.
    """
    try: 
        with open('requirements.txt', 'r', encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    except FileNotFoundError as e:    
        # raise RequirementsFileNotFoundError(f"Requirements file not found: {Setting.REQUIREMENTS}") from e
        pass
    except IOError as e:
        # raise IOError(f"Error reading the requirements file: {Setting.REQUIREMENTS}") from e
        pass

def check_dependencies():
    """
    Checks if all required dependencies are installed.

    This function reads the dependencies from the `requirements.txt` file and 
    verifies if they are installed. It returns a list of missing dependencies.

    Returns:
        list[str]: A list of missing package names.
    """
    dependencies = get_dependencies()
    missing_packages = []
    
    for package in dependencies:
        try:
            pkg_resources.require(package)
        except pkg_resources.DistributionNotFound:
            missing_packages.append(package)
        except pkg_resources.VersionConflict as e:
            print(f"Version conflict detected for {package}: {e}")
            missing_packages.append(package)
            
    return missing_packages