#!/usr/bin/env python3
"""
Fix virtual environment with exact working versions
This script will downgrade packages to the known working versions
"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a command and show progress"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False

def check_venv():
    """Check if we're in a virtual environment"""
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    if not in_venv:
        print("❌ Not in a virtual environment!")
        print("📋 Please activate your virtual environment first:")
        print("   .\.venv\Scripts\activate")
        return False
    
    print(f"✅ Virtual environment detected: {os.environ.get('VIRTUAL_ENV', 'Unknown')}")
    return True

def main():
    """Main function to fix the virtual environment"""
    print("🔧 FIXING VIRTUAL ENVIRONMENT WITH WORKING VERSIONS")
    print("=" * 60)
    
    if not check_venv():
        return
    
    # Critical packages that need to be downgraded to working versions
    critical_downgrades = [
        # OpenAI - CRITICAL: v2.x breaks compatibility
        "openai==1.101.0",
        
        # LiveKit packages - must be compatible versions
        "livekit==1.0.12",
        "livekit-agents==1.2.8", 
        "livekit-api==1.0.5",
        "livekit-protocol==1.0.5",  # CRITICAL: v1.1.1 causes hanging
        "livekit-plugins-openai==1.2.8",
        
        # Other packages
        "pymongo==4.14.1",
        "python-dotenv==1.1.1",
        "aiohttp==3.12.15",
        "twilio==9.8.2",
        "silero-vad==6.0.0"
    ]
    
    print("📋 The following packages will be downgraded to working versions:")
    for package in critical_downgrades:
        print(f"   - {package}")
    print()
    
    # Uninstall problematic packages first
    print("🗑️ Uninstalling current versions...")
    packages_to_uninstall = [pkg.split('==')[0] for pkg in critical_downgrades]
    uninstall_cmd = f"{sys.executable} -m pip uninstall -y {' '.join(packages_to_uninstall)}"
    
    if not run_command(uninstall_cmd, "Uninstalling current versions"):
        print("⚠️ Some packages may not have been installed, continuing...")
    
    # Install working versions
    print("\n📦 Installing working versions...")
    for package in critical_downgrades:
        if not run_command(f"{sys.executable} -m pip install {package}", f"Installing {package}"):
            print(f"❌ Failed to install {package}")
            return
    
    # Install remaining dependencies
    print("\n📦 Installing remaining dependencies...")
    remaining_packages = [
        "pinecone==8.0.0",
        "livekit-plugins-noise-cancellation==0.2.5",
        "livekit-plugins-silero==1.2.8", 
        "livekit-plugins-deepgram==1.2.8",
        "livekit-plugins-bey==1.2.8",
        "livekit-plugins-cartesia==1.2.8",
        "livekit-plugins-google==1.2.8",
        "livekit-plugins-tavus==1.2.8",
        "tzdata==2025.2"
    ]
    
    for package in remaining_packages:
        run_command(f"{sys.executable} -m pip install {package}", f"Installing {package}")
    
    print("\n🔍 Verifying installation...")
    
    # Test critical imports
    test_imports = [
        'livekit',
        'livekit.agents', 
        'livekit.plugins.openai',
        'livekit.plugins.openai.realtime',
        'openai',
        'pinecone'
    ]
    
    all_good = True
    for module in test_imports:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            all_good = False
    
    print("\n" + "=" * 60)
    if all_good:
        print("🎉 Virtual environment fixed successfully!")
        print("📋 You can now run: python agent.py dev")
        print("\n💡 Key fixes applied:")
        print("   - Downgraded OpenAI SDK from v2.x to v1.101.0")
        print("   - Downgraded LiveKit packages to compatible versions")
        print("   - All packages now match the working global environment")
    else:
        print("❌ Some issues remain. Check the errors above.")
        print("📋 You may need to:")
        print("   - Delete .venv folder and recreate it")
        print("   - Check your Python version compatibility")

if __name__ == "__main__":
    main()