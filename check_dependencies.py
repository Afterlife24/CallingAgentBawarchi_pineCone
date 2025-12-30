#!/usr/bin/env python3
"""
Dependency checker script to identify exact versions working vs not working
"""

import subprocess
import sys
import os
from pathlib import Path

def get_pip_list():
    """Get list of installed packages with versions"""
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "list"], 
                              capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error getting pip list: {e}")
        return None

def get_critical_packages():
    """Get versions of critical packages for the agent"""
    critical_packages = [
        'livekit',
        'livekit-agents', 
        'livekit-api',
        'livekit-plugins-openai',
        'livekit-plugins-noise-cancellation',
        'openai',
        'pinecone',
        'pymongo',
        'python-dotenv',
        'aiohttp',
        'twilio',
        'silero-vad',
        'tzdata'
    ]
    
    versions = {}
    for package in critical_packages:
        try:
            result = subprocess.run([sys.executable, "-m", "pip", "show", package], 
                                  capture_output=True, text=True, check=True)
            lines = result.stdout.split('\n')
            for line in lines:
                if line.startswith('Version:'):
                    versions[package] = line.split(':', 1)[1].strip()
                    break
        except subprocess.CalledProcessError:
            versions[package] = "NOT INSTALLED"
    
    return versions

def test_imports():
    """Test if critical imports work"""
    imports_to_test = [
        ('livekit', 'LiveKit core'),
        ('livekit.agents', 'LiveKit Agents'),
        ('livekit.plugins.openai', 'LiveKit OpenAI plugin'),
        ('livekit.plugins.openai.realtime', 'LiveKit OpenAI Realtime'),
        ('openai', 'OpenAI SDK'),
        ('pinecone', 'Pinecone SDK'),
        ('pymongo', 'MongoDB driver'),
        ('dotenv', 'Python dotenv'),
        ('aiohttp', 'Async HTTP client'),
        ('twilio', 'Twilio SDK')
    ]
    
    results = {}
    for module, description in imports_to_test:
        try:
            __import__(module)
            results[module] = "✅ SUCCESS"
        except ImportError as e:
            results[module] = f"❌ FAILED: {e}"
        except Exception as e:
            results[module] = f"⚠️ ERROR: {e}"
    
    return results

def test_agent_components():
    """Test if agent-specific components load"""
    components = {}
    
    # Test prompts
    try:
        from prompts import AGENT_INSTRUCTION, SESSION_INSTRUCTION
        if len(AGENT_INSTRUCTION) > 100:
            components['prompts'] = "✅ SUCCESS"
        else:
            components['prompts'] = "❌ FAILED: Instructions too short"
    except Exception as e:
        components['prompts'] = f"❌ FAILED: {e}"
    
    # Test search_menu
    try:
        from search_menu import search_menu
        components['search_menu'] = "✅ SUCCESS"
    except Exception as e:
        components['search_menu'] = f"❌ FAILED: {e}"
    
    # Test agent class
    try:
        from agent import RestaurantAgent
        components['agent_class'] = "✅ SUCCESS"
    except Exception as e:
        components['agent_class'] = f"❌ FAILED: {e}"
    
    return components

def main():
    """Main function to run all checks"""
    print("🔍 DEPENDENCY ANALYSIS")
    print("=" * 60)
    
    # Check if we're in venv
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    venv_path = os.environ.get('VIRTUAL_ENV', 'Not detected')
    
    print(f"Python executable: {sys.executable}")
    print(f"Python version: {sys.version}")
    print(f"Virtual environment: {'YES' if in_venv else 'NO'}")
    print(f"VIRTUAL_ENV path: {venv_path}")
    print()
    
    # Get critical package versions
    print("📦 CRITICAL PACKAGE VERSIONS:")
    print("-" * 40)
    versions = get_critical_packages()
    for package, version in versions.items():
        status = "✅" if version != "NOT INSTALLED" else "❌"
        print(f"{status} {package:<35} {version}")
    print()
    
    # Test imports
    print("🔍 IMPORT TESTS:")
    print("-" * 40)
    import_results = test_imports()
    for module, result in import_results.items():
        print(f"{module:<35} {result}")
    print()
    
    # Test agent components
    print("🤖 AGENT COMPONENT TESTS:")
    print("-" * 40)
    component_results = test_agent_components()
    for component, result in component_results.items():
        print(f"{component:<35} {result}")
    print()
    
    # Summary
    failed_packages = [pkg for pkg, ver in versions.items() if ver == "NOT INSTALLED"]
    failed_imports = [mod for mod, res in import_results.items() if "FAILED" in res]
    failed_components = [comp for comp, res in component_results.items() if "FAILED" in res]
    
    print("📊 SUMMARY:")
    print("-" * 40)
    print(f"Environment: {'Virtual Environment' if in_venv else 'Global Python'}")
    print(f"Missing packages: {len(failed_packages)}")
    print(f"Failed imports: {len(failed_imports)}")
    print(f"Failed components: {len(failed_components)}")
    
    if failed_packages:
        print(f"\n❌ Missing packages: {', '.join(failed_packages)}")
    if failed_imports:
        print(f"\n❌ Failed imports: {', '.join(failed_imports)}")
    if failed_components:
        print(f"\n❌ Failed components: {', '.join(failed_components)}")
    
    if not failed_packages and not failed_imports and not failed_components:
        print("\n🎉 All dependencies look good!")
        print("📋 Try running: python agent.py dev")
    else:
        print("\n⚠️ Issues detected. This might explain why the agent hangs.")
    
    # Save detailed pip list to file
    pip_list = get_pip_list()
    if pip_list:
        env_type = "venv" if in_venv else "global"
        filename = f"pip_list_{env_type}.txt"
        with open(filename, 'w') as f:
            f.write(f"Environment: {env_type}\n")
            f.write(f"Python: {sys.executable}\n")
            f.write(f"Virtual ENV: {venv_path}\n\n")
            f.write(pip_list)
        print(f"\n💾 Detailed package list saved to: {filename}")

if __name__ == "__main__":
    main()