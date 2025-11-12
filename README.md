# DEPENDENCIES:
    1. Installing: pip install -r requirements.txt
    2. Adding requirements: pip freeze > requirements.txt

# TODOS

## Important stuff:
    1. Make database schema
    2. Construct models
    3. Complete register (see -> register.py todo)
    4. Start login

## PACKAGE SPECIFIC:
### --- database/dc.py
    1. Refactor main() into a db initialization script.
    2. Optimize db.py

### --- src/app/scenes/base.py
    1. Handle refreshing scenes.

### --- src/app/scenes/register.py
    1. Add field validation.
    2. Add text validation hints (see -> input_edit todo)
    3. Add try_except operation to add user to database (see -> user todo.)
    4. Add success popup.
    5. Add system delay between success popup -> redirection to splash
    6. OPTIONAL: Add shortcut to redirect to login.
    7. OPTIONAL: Add password hashing.

### --- src/app/widgets/input_edit.py
    1. Add error hint text indicators.
    2. Inherit DateEdit from InputEdit. 
    3. Add year(), month(), day(), age() properties to DateEdit.

### --- src/app/application.py
    1. Add database initialization script.

### --- src/app/scene_manager.py
    1. Handle passing data between screens.

### --- src/models/user.py
    1.  Construct user.
    2. Add user-related db operations.

### --- src/utils/validation.py
    1. Add age requirement check.
    2. Add email regex check.
    3. Add password regex check.
    4. Add phone number regex check.
    5. Optimize validation.