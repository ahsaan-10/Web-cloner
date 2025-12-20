# VS Code Setup Guide

Complete guide to set up and use this project in Visual Studio Code.

## Prerequisites Installed ✅

- [x] Python 3.11.14
- [x] Virtual environment created (`venv/`)
- [x] All dependencies installed
- [x] VS Code configurations created

## Quick Start in VS Code

### 1. Open the Project

```bash
code /home/user/Web-cloner
```

Or in VS Code:
- `File` → `Open Folder` → Select `Web-cloner`

### 2. Select Python Interpreter

1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
2. Type: `Python: Select Interpreter`
3. Choose: `./venv/bin/python` (Python 3.11.14)

This will activate your virtual environment automatically!

### 3. Run the Application

**Method 1: Using Tasks (Recommended)**
1. Press `Ctrl+Shift+B` (Build task)
2. Select: `Run Streamlit App`
3. The app will open in your browser at `http://localhost:8501`

**Method 2: Using Terminal**
1. Open terminal: `Ctrl+` ` (backtick)
2. The venv should activate automatically
3. Run: `streamlit run src/app.py`

**Method 3: Using Debug**
1. Go to Run & Debug (`Ctrl+Shift+D`)
2. Select: `Streamlit: Run with Browser`
3. Press `F5` or click the green play button

## VS Code Features Configured

### 1. Python Settings (`.vscode/settings.json`)

- **Virtual Environment**: Automatically uses `./venv/bin/python`
- **Auto-activation**: Terminal auto-activates venv
- **Editor**: Tab size 4, rulers at 88/120 characters
- **File exclusions**: Hides `__pycache__`, `.pyc` files
- **Streamlit optimized**: File watcher configured

### 2. Launch Configurations (`.vscode/launch.json`)

Three debug configurations available:

1. **Streamlit: Run App** - Run in headless mode
2. **Streamlit: Run with Browser** - Open browser automatically
3. **Python: Current File** - Debug any Python file

Access via: `Run & Debug` panel (`Ctrl+Shift+D`)

### 3. Tasks (`.vscode/tasks.json`)

Quick tasks accessible via `Ctrl+Shift+P` → `Tasks: Run Task`:

- **Run Streamlit App** - Start the application
- **Install Dependencies** - Run pip install
- **Check Python Version** - Verify Python version
- **List Installed Packages** - View all packages

Default build task: `Ctrl+Shift+B` runs the app!

## Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Run App (Build Task) | `Ctrl+Shift+B` |
| Open Terminal | `Ctrl+` ` |
| Command Palette | `Ctrl+Shift+P` |
| Select Interpreter | `Ctrl+Shift+P` → Python: Select Interpreter |
| Run & Debug | `Ctrl+Shift+D` |
| Start Debugging | `F5` |
| Toggle Sidebar | `Ctrl+B` |
| Search Files | `Ctrl+P` |
| Global Search | `Ctrl+Shift+F` |

## Project Structure in Explorer

```
Web-cloner/
├── .vscode/                    # VS Code configurations
│   ├── settings.json          # Python & editor settings
│   ├── launch.json            # Debug configurations
│   └── tasks.json             # Quick tasks
├── venv/                      # Virtual environment (hidden in explorer)
├── src/                       # Source code
│   └── app.py                # Main Streamlit app
├── data/                      # Database files
├── archive/                   # Old versions
├── docs/                      # Documentation
└── requirements.txt           # Dependencies
```

## Using the Debugger

### Debug the Streamlit App

1. Open `src/app.py`
2. Click in the gutter to set breakpoints (red dots)
3. Press `F5` or go to Run & Debug
4. Select: `Streamlit: Run with Browser`
5. Use the app - it will pause at breakpoints
6. Use debug controls:
   - `F5`: Continue
   - `F10`: Step Over
   - `F11`: Step Into
   - `Shift+F11`: Step Out
   - `Shift+F5`: Stop

### Debug Variables

- **Variables pane**: See all variables in current scope
- **Watch pane**: Add expressions to watch
- **Call Stack**: See function call hierarchy
- **Debug Console**: Execute Python code while paused

## Terminal Usage

### The terminal auto-activates your virtual environment!

When you open a terminal in VS Code:
```bash
# You'll see (venv) in the prompt:
(venv) user@host:~/Web-cloner$

# You can run Python commands directly:
python --version
pip list
streamlit run src/app.py
```

### Manual Activation (if needed)

```bash
# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

## Installed Extensions Recommendations

Install these VS Code extensions for the best experience:

1. **Python** (ms-python.python) - Essential
2. **Pylance** (ms-python.vscode-pylance) - IntelliSense
3. **Python Debugger** (ms-python.debugpy) - Debugging
4. **SQLite Viewer** (qwtel.sqlite-viewer) - View databases
5. **Markdown All in One** (yzhang.markdown-all-in-one) - Docs
6. **GitLens** (eamodio.gitlens) - Git enhanced

Install via: `Ctrl+Shift+X` (Extensions panel)

## Common Tasks

### Run the Application
```bash
# Press Ctrl+Shift+B
# Or in terminal:
streamlit run src/app.py
```

### Install New Package
```bash
pip install package-name
pip freeze > requirements.txt  # Update requirements
```

### View Database
- Install SQLite Viewer extension
- Right-click `data/cloned_sites.db`
- Select "Open with SQLite Viewer"

### Format Code
```bash
# Install black (optional)
pip install black

# Format a file
black src/app.py
```

### Git Operations
```bash
git status
git add .
git commit -m "Your message"
git push
```

## Troubleshooting

### Virtual Environment Not Activating

1. `Ctrl+Shift+P` → `Python: Select Interpreter`
2. Choose `./venv/bin/python`
3. Close and reopen terminal

### "Module not found" Errors

```bash
# Ensure venv is activated, then:
pip install -r requirements.txt
```

### Streamlit Won't Start

```bash
# Check if streamlit is installed:
pip list | grep streamlit

# Reinstall if needed:
pip install streamlit
```

### Port Already in Use

```bash
# Kill process on port 8501:
lsof -ti:8501 | xargs kill -9

# Or use a different port:
streamlit run src/app.py --server.port 8502
```

## Streamlit Configuration

### Create `.streamlit/config.toml` (Optional)

```toml
[server]
port = 8501
headless = true
enableCORS = false

[browser]
gatherUsageStats = false
serverAddress = "localhost"

[theme]
base = "dark"
primaryColor = "#00d4ff"
backgroundColor = "#0a0a0f"
```

## Testing Your Setup

### 1. Check Python Version
```bash
python --version
# Should show: Python 3.11.14
```

### 2. Check Dependencies
```bash
pip list
# Should show: streamlit, requests, beautifulsoup4, etc.
```

### 3. Run the App
```bash
streamlit run src/app.py
```

### 4. Test in Browser
- Go to: `http://localhost:8501`
- Try cloning a website (e.g., `https://example.com`)
- Check if it works!

## File Watching

VS Code is configured to:
- Auto-reload when you save Python files
- Ignore venv directory for better performance
- Watch for changes in src/ directory

## IntelliSense & Autocomplete

With Pylance installed, you get:
- **Auto-imports**: Automatic import suggestions
- **Type hints**: Hover for type information
- **Parameter hints**: Function parameter info
- **Quick fixes**: Automatic error corrections
- **Refactoring**: Rename symbols across files

## Git Integration

VS Code shows:
- **Modified files**: Yellow in explorer
- **Untracked files**: Green in explorer
- **Git status**: In status bar
- **Changes**: In Source Control panel (`Ctrl+Shift+G`)

Quick git commands:
- `Ctrl+Shift+G`: Open Source Control
- Click `+` to stage files
- Type commit message
- Click `✓` to commit

## Next Steps

1. ✅ Open project in VS Code
2. ✅ Select Python interpreter
3. ✅ Run the app (`Ctrl+Shift+B`)
4. ✅ Try cloning a website
5. ✅ Explore the code with IntelliSense
6. ✅ Set breakpoints and debug
7. ✅ Make changes and see live reload

## Additional Resources

- [Streamlit Docs](https://docs.streamlit.io)
- [VS Code Python Docs](https://code.visualstudio.com/docs/python/python-tutorial)
- [Project README](README.md)
- [Quick Start Guide](QUICKSTART.md)

---

**You're all set!** Press `Ctrl+Shift+B` to run the app and start cloning websites! 🚀
