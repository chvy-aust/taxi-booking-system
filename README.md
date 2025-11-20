# DEPENDENCIES:
    1. Installing: pip install -r requirements.txt
    2. Adding requirements: pip freeze > requirements.txt

# Roadmap [!!]
login
2. Use .execute() with a SELECT ... WHERE statement to check for a user with the email 
3. fetch user and return user
4. if user is null, end the login process (display UI feedback indicating there is no user with said email??? not sure how)
5. if it has a user -> compare the password value in step 1 with the selected password
6. if passwords match, login else end the login process (display UI feedback indicating incorrect credentials)
dashboards
- have to figure out how to carry the user object returned in step 3 from login -> dashboard (whether customer, admin, driver)
- if the _switch_scene() method in scenemanager is called with the optional user instance (like, _switch_scene('dashboard', user')) then it needs to
assign that user to the scenes user attribute (self.user)
- maybe a separate method to check the returned user's role attribute (self.role), so if role == customer, switch to customer dash (also not sure how to structure that code)
