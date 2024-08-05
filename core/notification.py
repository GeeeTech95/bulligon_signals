from Users.models import Notification as NotModel



class Notification() :
    model = NotModel

    @classmethod
    def notify(cls,user,msg) :
        cls.model.objects.create(user=user,message=msg)
