class UserModel():
    users = []

    def __init_(self):
        users = []

    def username_password_match(self, _username, _pwd):
        for i in users:
            if i[_username] == _pwd:
                return True
            return False
    
    def add_user(self, _username, _pwd):
        users.append({_username:_pwd})

