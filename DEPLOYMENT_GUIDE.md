# 🚀 Restaurant Voice Agent - Deployment Guide

## 🔍 Issue Identified

The agent works on your machine but hangs on others due to **dependency version conflicts**. Your global Python has working versions, but the virtual environment installs newer, incompatible versions.

## 📊 Version Comparison

| Package | Working (Global) | Problematic (VEnv) | Issue |
|---------|------------------|---------------------|-------|
| openai | 1.101.0 | 2.13.0 | ⚠️ **MAJOR VERSION BREAK** |
| livekit-protocol | 1.0.5 | 1.1.1 | 🚨 **CRITICAL - CAUSES HANGING** |
| livekit-agents | 1.2.8 | 1.3.8 | ⚠️ Compatibility issues |
| livekit | 1.0.12 | 1.0.20 | ⚠️ API changes |
| livekit-plugins-openai | 1.2.8 | 1.3.8 | ⚠️ Must match agents version |

## 🛠️ Solution

### For New Users (Cloning from GitHub):

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd <repo-name>
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate  # Windows
   # or
   source .venv/bin/activate  # Linux/Mac
   ```

3. **Install EXACT working versions**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify installation**:
   ```bash
   python check_dependencies.py
   ```

5. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

### For Existing Users (Fixing Current VEnv):

1. **Activate your virtual environment**:
   ```bash
   .\.venv\Scripts\activate
   ```

2. **Run the fix script**:
   ```bash
   python fix_venv.py
   ```

3. **Verify the fix**:
   ```bash
   python check_dependencies.py
   ```

## 🔧 Key Files Created

1. **`requirements.txt`** - Exact working versions
2. **`check_dependencies.py`** - Diagnose dependency issues
3. **`fix_venv.py`** - Fix existing virtual environments
4. **`.env.example`** - Template for environment variables

## ⚠️ Critical Dependencies

**DO NOT UPGRADE** these packages without testing:

- `openai==1.101.0` (v2.x breaks compatibility)
- `livekit-protocol==1.0.5` 🚨 **CRITICAL - v1.1.1 causes hanging**
- `livekit-agents==1.2.8` (newer versions have issues)
- `livekit-plugins-openai==1.2.8` (must match agents version)

## 🧪 Testing

After setup, test with:

```bash
# Check dependencies
python check_dependencies.py

# Basic functionality test
python test_agent_basic.py

# Test agent loading
python -c "from agent import RestaurantAgent; print('Agent loads successfully')"

# Run the agent
python agent.py dev
```

## 🚨 Troubleshooting

### Agent hangs after greeting:
1. Check OpenAI SDK version: `pip show openai`
2. If version is 2.x, downgrade: `pip install openai==1.101.0`
3. Restart the agent

### Import errors:
1. Run: `python check_dependencies.py`
2. Install missing packages from requirements.txt
3. Use exact versions specified

### Environment variables missing:
1. Copy `.env.example` to `.env`
2. Fill in your actual API keys
3. Ensure all required variables are set

## 📋 Required API Keys

- `OPENAI_API_KEY` - OpenAI API key
- `PINECONE_API_KEY` - Pinecone vector database
- `MONGO_URI` - MongoDB connection string
- `LIVEKIT_*` - LiveKit configuration
- Others as specified in `.env.example`

## 🎯 Success Indicators

✅ All dependencies show "SUCCESS" in check_dependencies.py
✅ Agent loads without errors
✅ Agent responds after greeting (not just greets and hangs)
✅ Menu search works for food queries

## 📞 Support

If issues persist:
1. Run `python check_dependencies.py` and share output
2. Check console logs for specific error messages
3. Verify all API keys are valid and have credits
4. Ensure network connectivity to external APIs