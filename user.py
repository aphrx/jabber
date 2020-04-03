from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id_, name, email, profile_pic):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic

    @staticmethod
    def get(user_id, mongo):
        user = mongo.db.users.find_one({"id": user_id})
        if not user:
            return None
        return User(id_=user["id"],
                    name=user["name"],
                    email=user["email"],
                    profile_pic=user["profile_pic"])  # User object

    @staticmethod
    def create(id, name, email, profile_pic, mongo):
        user = {
            "id": id,
            "name": name,
            "email": email,
            "profile_pic": profile_pic,
            "linkedIn": {
                "email": "",
                "pwd": ""
            },
            "cv": "",
            "resume": "",
            "cron":{
                "cron_job": "",
                "cron_loc": "",
            }
        }
        mongo.db.users.insert(user)
