Patch export for manual application

Files included:
- core/services/llm_service.py
- pkg_resources.py

How to apply:
1. Stop your dev server if running.
2. Backup files:
   - copy core/services/llm_service.py to core/services/llm_service.py.bak
   - copy pkg_resources.py to pkg_resources.py.bak (if exists)
3. Copy files from patch_export into the repository root, preserving paths.
   Example (PowerShell):

   Copy-Item -Path .\patch_export\core\services\llm_service.py -Destination .\core\services\llm_service.py -Force
   Copy-Item -Path .\patch_export\pkg_resources.py -Destination .\pkg_resources.py -Force

4. Run Django checks and migrations:

   & ".\.venv\Scripts\python.exe" manage.py check
   & ".\.venv\Scripts\python.exe" manage.py makemigrations
   & ".\.venv\Scripts\python.exe" manage.py migrate --noinput

5. Start server:

   & ".\.venv\Scripts\python.exe" manage.py runserver

Notes:
- If you use Git locally, commit the changes after verifying them.
- If you want a standard git patch, tell me and I will attempt to generate a unified diff file instead.
