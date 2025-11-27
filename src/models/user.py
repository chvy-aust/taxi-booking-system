class User:
    def __init__(self, row_object):
        self.id = row_object['id']
        self.role = row_object['role']
        self.firstname = row_object['firstname']
        self.lastname = row_object['lastname']
        self.dob = row_object['dob']
        self.phonenum = row_object['phonenum']
        self.email = row_object['email']
        self.address = row_object['address']
        self.password = row_object['password']