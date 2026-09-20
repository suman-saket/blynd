# Backend

## First time Command

```powershell
# 0)  Clone the repo, go inside the backend folder,
cd you_system_file_path\blynd\backend

# 1) creates a private Python environment in the .venv folder
python -m venv .venv

# 2) switches your terminal to use that environment's Python and packages instead of the system ones
.\.venv\Scripts\Activate.ps1

# 3) installs the Python libraries this backend needs into the active environment
pip install fastapi uvicorn beanie pymongo pydantic-settings

# 4) Run the Local Server   
python -m uvicorn src.main:app --reload
```

## Daily Ritual Command To Spin Up BackEnd Project

```powershell
# 1) Go to your system file path where proect is cloned
cd you_system_file_path\blynd\backend

# 2) switches your terminal to use that environment's Python and packages instead of the system ones
.\.venv\Scripts\Activate.ps1 
 
# 3) This command is optional only needed when you want to deactiavte your project virtual environemnt(Not needed unless you want to)

deactivate 

# 4) Run the Local Server   
python -m uvicorn src.main:app --reload
```

Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)