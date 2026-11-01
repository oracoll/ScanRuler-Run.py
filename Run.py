#!/usr/bin/env python3
import os
import subprocess
import sys
import shutil

def check_command(cmd):
    """Check if a command-line tool is available in the system PATH."""
    return shutil.which(cmd) is not None

def install_nodejs():
    """Attempt to install Node.js automatically based on the operating system."""
    print("[*] Node.js is not found on your system. Attempting automatic installation...")
    
    if os.name == 'nt':  # Windows
        if check_command("winget"):
            print("[*] Found 'winget'. Installing Node.js LTS via Windows Package Manager...")
            try:
                subprocess.run(
                    ["winget", "install", "-e", "--id", "OpenJS.NodeJS.LTS", "--accept-source-agreements", "--accept-package-agreements"],
                    check=True, shell=True
                )
                print("[✓] Node.js installed successfully via winget.")
                return True
            except subprocess.CalledProcessError as e:
                print(f"[X] Automatic installation via winget failed: {e}")
        elif check_command("choco"):
            print("[*] Found 'choco'. Installing Node.js via Chocolatey...")
            try:
                subprocess.run(["choco", "install", "nodejs", "-y"], check=True, shell=True)
                print("[✓] Node.js installed successfully via Chocolatey.")
                return True
            except subprocess.CalledProcessError as e:
                print(f"[X] Automatic installation via Chocolatey failed: {e}")
        else:
            print("[X] Could not find a package manager (winget/choco) on Windows.")
            print("    Please install Node.js manually from https://nodejs.org/")
            
    elif sys.platform == 'darwin':  # macOS
        if check_command("brew"):
            print("[*] Found Homebrew. Installing Node.js via Homebrew...")
            try:
                subprocess.run(["brew", "install", "node"], check=True)
                print("[✓] Node.js installed successfully via Homebrew.")
                return True
            except subprocess.CalledProcessError as e:
                print(f"[X] Automatic installation via Homebrew failed: {e}")
        else:
            print("[X] Homebrew (brew) not found on macOS.")
            print("    Please install Homebrew or download Node.js from https://nodejs.org/")
            
    elif sys.platform.startswith('linux'):  # Linux
        if check_command("apt"):
            print("[*] Found 'apt'. Installing Node.js and npm via apt...")
            try:
                subprocess.run(["sudo", "apt", "update"], check=True)
                subprocess.run(["sudo", "apt", "install", "-y", "nodejs", "npm"], check=True)
                print("[✓] Node.js and npm installed successfully via apt.")
                return True
            except subprocess.CalledProcessError as e:
                print(f"[X] Automatic installation via apt failed: {e}")
        else:
            print("[X] Supported package manager ('apt') not found on Linux.")
            print("    Please install Node.js using your distribution's package manager or from https://nodejs.org/")
    
    return False

def main():
    print("========================================")
    print("       ScanRuler Automatic Runner       ")
    print("========================================\n")
    
    # 1. Verify we are in the root directory of the repository
    if not os.path.exists("package.json"):
        print("[X] Error: 'package.json' not found in this directory.")
        print("    Please make sure you place 'run.py' directly in the root folder")
        print("    of the ScanRuler repository.")
        sys.exit(1)
    
    # 2. Check if Node.js and npm are installed, install if missing
    if not check_command("node") or not check_command("npm"):
        success = install_nodejs()
        if not success:
            print("\n[X] Error: Node.js/npm is required to run ScanRuler.")
            print("    Please install Node.js manually from https://nodejs.org/ and re-run this script.")
            sys.exit(1)
        
        # Re-check availability after installation
        if not check_command("node") or not check_command("npm"):
            print("\n[!] Node.js was installed, but might not be available in your current terminal PATH.")
            print("    Please restart your terminal/command prompt and run 'python run.py' again.")
            sys.exit(1)
    else:
        print("[✓] Node.js and npm are installed.")

    # 3. Install project dependencies if node_modules doesn't exist
    if not os.path.exists("node_modules"):
        print("\n[*] Installing dependencies (running 'npm install')...")
        try:
            subprocess.run(["npm", "install"], check=True, shell=(os.name == 'nt'))
            print("[✓] Dependencies installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"[X] Error during 'npm install': {e}")
            sys.exit(1)
    else:
        print("[✓] Dependencies already installed ('node_modules' folder found).")

    # 4. Start the local development server
    print("\n[🚀] Starting the ScanRuler development server...")
    print("    -> Look for the local URL link below (usually http://localhost:5173)")
    print("    -> Press Ctrl+C in this terminal at any time to stop the server.\n")
    print("-" * 50)

    try:
        subprocess.run(["npm", "run", "dev"], check=True, shell=(os.name == 'nt'))
    except KeyboardInterrupt:
        print("\n\n[!] Server stopped by user. Goodbye!")
    except subprocess.CalledProcessError as e:
        print(f"\n[X] Error running the development server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()