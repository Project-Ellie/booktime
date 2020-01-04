from django.db.models import Manager


class ActiveManager(Manager):
    def active(self):
        return self.filter(active=True)
