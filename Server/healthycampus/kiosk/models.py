from django.db import models

class User(models.Model): #one of these should be unique, probably username
    username = models.CharField(max_length=200, default='')
    password = models.CharField(max_length=200, default='')
    barcode = models.CharField(max_length=200, default='')
    distance_travelled_m = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    
    def __str__(self):
        return self.barcode

class Kiosk(models.Model):
    address = models.CharField(max_length=200, default='')
    name = models.CharField(max_length=200, default='No Name')
    longitude = models.CharField(max_length=10, default='')
    latitude = models.CharField(max_length=10, default='')
    ip = models.CharField(max_length=15, default='') #IPv4 with dots ie 123.456.789.101
    x = models.IntegerField(default=-1)
    y = models.IntegerField(default=-1)

    def __str__(self):             
        return self.address

class Heartbeat(models.Model):
    kiosk = models.ForeignKey(Kiosk)
    ip = models.CharField(max_length=15, default='') #IPv4 with dots ie 123.456.789.101
    date_server = models.DateTimeField('date checked in on server', blank=True)
    date_kiosk = models.DateTimeField('date checked in on kiosk', blank=True)

    def __str__(self):
        return self.kiosk.address + " - " + str(self.date_server)
    
class UserKiosksToCheckIn(models.Model):
    kiosk = models.ForeignKey(Kiosk, null=True)
    user = models.ForeignKey(User)
    
    def __str__(self):
        return self.user.barcode + ' - ' + self.kiosk.address
        
class KioskDistance(models.Model):
    kiosk_one = models.ForeignKey(Kiosk, related_name="kiosk_one")
    kiosk_two = models.ForeignKey(Kiosk, related_name="kiosk_two")
    distance_m = models.IntegerField(default=0)
    
    def __str__(self):
        return self.kiosk_one.address + " - " + self.kiosk_two.address + " - " + str(self.distance_m) + " meters"
    #1 to 2, and 2 to 1 should be the same. how? code now exists in a view, should be a function here?
    
class CheckIn(models.Model):
    kiosk = models.ForeignKey(Kiosk, null=True)
    date = models.DateTimeField('date checked in', blank=True)
    user = models.ForeignKey(User, null=True)
    distance = models.ForeignKey(KioskDistance, null=True)
    user_seconds_since_last_checkin = models.FloatField(default=0)
    user_points_earned = models.IntegerField(default=0)

    def __str__(self):   
        return self.kiosk.address + " - " + str(self.date)
    
    class Meta:
        ordering = ['-date'] #this magic makes it by ordered in database by time (newest first)
    
'''         
class Path(models.Model):
    kiosk = models.ForeignKey(Kiosk, null=True)
    difficulty = models.CharField(max_length=200, default='')
    user = models.ForeignKey(User, null=True)

    def __str__(self):
        return self.kiosk.address + " - " + self.difficulty 
   
class PathNode(models.Model):
    path = models.ForeignKey(Path)
    kiosk = models.ForeignKey(Kiosk)
    sequence_number = models.IntegerField()
    
    def __str__(self):
        return self.path.difficulty + " - " + str(self.sequence_number)
'''  