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
    3. Add try_except operation to add user to database (see -> user todo.)
    4. Add success popup.
    5. Add system delay between success popup -> redirection to splash
    6. OPTIONAL: Add shortcut to redirect to login.
    7. OPTIONAL: Add password hashing.
    8. OPTIONAL: Capture phonenum match groups and reformat to one pattern.

### --- src/app/application.py
    1. Add database initialization script.

### --- src/models/user.py
    1.  Construct user.
    2. Add user-related db operations.
