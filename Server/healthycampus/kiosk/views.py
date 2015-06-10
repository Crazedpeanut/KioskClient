from django.shortcuts import render
from django.utils import timezone
from kiosk.models import Kiosk, CheckIn, User, KioskDistance, Heartbeat, UserKiosksToCheckIn
from django.db.models import Count
from datetime import datetime
from django.http import HttpResponse
import json
import gzip
import random

#this method is built so that if kiosk_amount > kiosks.length it only returns up to the maximum amount of kiosks, without doubling up on any kiosks
def _difficulty_generator(user, kiosk, kiosk_amount):
    uktci = user.userkioskstocheckin_set.all() #remove all current entries
    for i in uktci:
        i.delete()
    kiosks = Kiosk.objects.all().exclude(address=kiosk).order_by("?") #gets all the objects, but randomises their order, this could be terrible if amount of kiosks gets really big
    chosen = []
    
    if kiosk_amount > len(kiosks):
        kiosk_amount = len(kiosks)
    
    for i in range(0, kiosk_amount):
        choice = kiosks[i]
        uktci = UserKiosksToCheckIn(user=user, kiosk=choice)
        uktci.save()
        chosen.append(choice)
        
    return chosen

def _user_checkin_handle_return_data(kiosks):
    
    color = "22FF22"
    added = False
    if kiosks is None:
        return 'No locations available' #should possibly generate more here?
    #may want to make kiosk a different colour than k so that it shows current location?
    s = '{ "commands": [ { "command": "loadsequence", "sequence_num": "1", "fps": "1", "loop": "5", "frames": [ { "leds": [' #start
    #s += str(len(kiosks)) + ","
    for k in kiosks:
        if k.x > -1 and k.y > -1:
            added = True
            s += ' { "x": "' + str(k.x) + '", "y": "' + str(k.y) + '", "color": "' + color + '" } ,' #{ "x": "a", "y": "b", "color": "000000" }\
            #s += "|"+ str(k)+ "|" + ","
    if added:
        s = s[:-1] #cut off last comma, but only if something was added, to keep the json valid
    s += '] } ] }, { "command": "play_sequence", "sequence_num": "1" } ] }' #end
    
    return s
        

def _kiosk_in_UserKiosksToCheckIn(kiosk, user): #kiosk in UserKiosksToCheckIn
    try:
        kiosks_to_checkin = user.userkioskstocheckin_set.all()
        
        kiosks = []
        for k in kiosks_to_checkin:
            kiosks.append(k.kiosk)
            
        for k in kiosks:
            if k == kiosk:
                kiosks_to_checkin.get(kiosk=k).delete() #remove k from u.userKiosksToCheckin_set #THIS IS DELETING THE ENTIRE KIOSK
                kiosks.remove(k)#remove kiosk from the list
			#if kiosks == [] could generate a sequence to indicate no more left
                return kiosks, k #return the new list AND the kiosk that has been removed
        return kiosks, None
    except: #no kiosks found so default points
        pass
        
    return None, None
        
def _user_calculate_points(kiosk, user, user_seconds_since_last_checkin):
    #Currently just gives 200 points, should be changed to give
    #points based on what kiosk was checked into, how fast, etc
    if kiosk is not None:
        user.points += 200
    else:
        user.points += 100
            
    user.save()
    

def _user_checkin_anticheat_throwaway(kiosk, user_seconds_since_last_checkin, distance_travelled):

    '''if distance_travelled is None:
        distance_m = 0
    else:
        distance_m = distance_travelled.distance_m

    if distance_m is 0 and user_seconds_since_last_checkin > 1:
        return True
    elif distance_m is 0:
        return False
    
    user_speed = distance_m / user_seconds_since_last_checkin
    world_record_speed = 100 / 9.5 #approx
    
    if user_speed > world_record_speed:
        return True
    else:
        return False'''
    return False
    
def _user_checkin_user(request):

    try: 
        u = User.objects.get(barcode=request.POST['barcode'].rstrip())
        return u
    except: #error if user doesnt exist
        if 'barcode' in request.POST:
            u = User(barcode=request.POST['barcode'].rstrip()) #make new user
            u.save()
            return u
        else:
            return None
        
def _user_checkin_kiosk(request):
    try:
        return Kiosk.objects.get(address=request.POST['address'].rstrip())
    except: #error if kiosk address doesnt exist
        if 'address' in request.POST:
            k = Kiosk(address=request.POST['address'].rstrip()) #make new kiosk
            k.save()
            return k
        else:
            return None
        
def _user_checkin_distance(user, kiosk):
    kiosk_distance = None

    #get the last (most recent) kiosk the user signed into before this new check in
    try:
        last_kiosk = user.checkin_set.last().kiosk
    except: #user has no previous kiosk sign ins
        return None
    
    try:
        kiosk_distance = KioskDistance.objects.get(kiosk_one=kiosk, kiosk_two=last_kiosk)
        distance = kiosk_distance.distance_m
    except: #if kiosk_one to kiosk_two distance doesnt exist this is called
        try:
            kiosk_distance = KioskDistance.objects.get(kiosk_two=kiosk, kiosk_one=last_kiosk)
            distance = kiosk_distance.distance_m
        except: #if previous try fails and then kiosk_two to kiosk_one distance doesnt exist this is called
            distance = 0
    
    user.distance_travelled_m += distance
    user.save()   
        
    return kiosk_distance

def _user_checkin_time_since(user, date_checkin):
    try:
        date_previous = user.checkin_set.all().last().date
        timedelta = date_checkin - date_previous
        return timedelta.total_seconds()
    except:
        return 0

def user_checkin(request):
    if request.method == 'POST':
        u = _user_checkin_user(request) #handle users barcode
        if u is None:
            # Redisplay the question voting form.
            return render(request, 'kiosk/user_checkin.html', {
                'error_message': 'No barcode was provided',
            })  

        k = _user_checkin_kiosk(request) #handle the kiosk the user signed into
        if k is None:
            # Redisplay the question voting form.
            return render(request, 'kiosk/user_checkin.html', {
                'error_message': 'No kiosk address was provided',
            })

        kiosk_distance = _user_checkin_distance(u, k) #calculate distance between previous kiosk and checked in one 

        kiosks, kiosk_in_kiosk_checkins = _kiosk_in_UserKiosksToCheckIn(k, u) #note that this method will remove kiosk_in_kiosk_checkins from kiosks list
        
        try: #lazy way to tell if a number was provided, if difficulty doesnt exist, or isnt an int, it will just move past this
            if int(request.POST['difficulty']) > 0:
                kiosks = _difficulty_generator(u, k, int(request.POST['difficulty']))
        except:
            pass
            
        json_data =_user_checkin_handle_return_data(kiosks) #get data for returning 
        
        if "timestamp" in request.POST:
            d = datetime.strptime(request.POST['timestamp'], "%Y-%m-%d %H:%M:%S.%f")
        else:#if timestamp wasnt provided
            d = timezone.now()
            
        usslc = _user_checkin_time_since(u, d)
        if _user_checkin_anticheat_throwaway(k, usslc, kiosk_distance):
            return HttpResponse('Suspected of cheating')
                                
        _user_calculate_points(kiosk_in_kiosk_checkins, u, usslc)
        
        if kiosk_distance is None:
            c = CheckIn(kiosk=k, date=d, user=u, user_seconds_since_last_checkin=usslc)
        else:
            c = CheckIn(kiosk=k, date=d, user=u, distance=kiosk_distance, user_seconds_since_last_checkin=usslc)
        
        c.save()

        return HttpResponse(json_data, content_type="application/json") #return whatever data was needed
    
    else:
        return render(request, 'kiosk/user_checkin.html', {
            'error_message': "No POST data found",
        })

def user_checkin_file(request):
    if request.method == 'POST':
        #add a file form here
        
        try:
            unzipped = gzip.open(request.FILES['file'])#unzip file 
            contents = unzipped.read().decode("utf-8")
            contents = contents.replace('\'', '\"') #convert all 's to "s
            data = json.loads(contents)

            for checkin in data['checkins']:
                if 'barcode' in checkin:
                    try:
                        u = User.objects.get(barcode=checkin['barcode'])
                    except: #error if user doesnt exist
                        u = User(barcode=checkin['barcode']) #make new user
                        u.save()
                else:
                    continue #skip to next checkin
                    
                if 'address' in checkin:
                    try:
                        k = Kiosk.objects.get(address=checkin['address'])
                    except: #error if kiosk address doesnt exist
                        k = Kiosk(checkin['address']) #make new kiosk
                        k.save() 
                else:
                    continue  #skip to next checkin
                          
                kiosk_distance = _user_checkin_distance(u, k)   
                       
                if 'timestamp' in checkin:
                    d = datetime.strptime(checkin['timestamp'], "%Y-%m-%d %H:%M:%S.%f")
                else:#if timestamp wasnt provided
                    d = timezone.now()
                   
                usslc = _user_checkin_time_since(u, d)
                if _user_checkin_anticheat_throwaway(k, usslc, kiosk_distance):
                    continue #suspected of cheating so skip to next checkin
                
                _user_calculate_points(k, u, usslc)
                
                if kiosk_distance is None:
                    c = CheckIn(kiosk=k, date=d, user=u, user_seconds_since_last_checkin=usslc)
                else:
                    c = CheckIn(kiosk=k, date=d, user=u, distance=kiosk_distance, user_seconds_since_last_checkin=usslc)
                c.save()
                
            return HttpResponse('')  
        except Exception as e:
            return HttpResponse(repr(e))          

def heartbeat_checkin(request):
    
    ip = None
    timestamp = None
    
    if request.method == 'POST':
        if 'host' in request.POST:
            try:
                k = Kiosk.objects.get(address=request.POST['host'])
            except:
                k = Kiosk(address=request.POST['host']) #make new kiosk
                k.save()
        else:
            return render(request, 'kiosk/heartbeat_checkin.html', {
                'error_message': "No host name found",
            })
            
        if 'timestamp'in request.POST:
            timestamp = datetime.strptime(request.POST['timestamp'], "%Y-%m-%d %H:%M:%S.%f")
        
        if 'ip' in request.POST:
            ip = request.POST['ip']
            k.ip = ip
            k.save()
            
        date = timezone.now()
            
        hb = Heartbeat(kiosk=k, ip=ip, date_server=date, date_kiosk=timestamp)
        hb.save()
        
        #Anything that should be sent to kiosks at the end of a heartbeat such as updating
        #a map or something should go here, although prototype game has nothing to return
        #so this just remains blank
        
        return HttpResponse('')
    else:
        return render(request, 'kiosk/heartbeat_checkin.html', {
            'error_message': "No POST data found",
        })
    
       
def global_leaderboards(request):
    users = User.objects.all()
    most_users = users.annotate(amount=Count('checkin')).order_by('-amount') #most checkins by user
    most_distance_users = users.order_by('-distance_travelled_m') #most distance travelled by users
    recent = CheckIn.objects.all().order_by('-date')[:10] #show the last 10 checkins by most recent
    most_kiosks = Kiosk.objects.all().annotate(amount=Count('checkin')).order_by('-amount') #most checkins by kiosk
    most_points= users.order_by('points') #TODO: this isnt working
    
    return render(request, 'kiosk/global_leaderboards.html', {
        'most_points_list': most_points,
    	'recent_checkin_list': recent,
    	'most_checkin_list': most_users,
    	'kiosk_checkin_list': most_kiosks,
        'most_distance_list': most_distance_users,
    })

def user_detail(request, user_id): 
    try:
        user = User.objects.get(barcode=user_id)
        #user = user.order_by('checkin__date')
        
        return render(request, 'kiosk/user_details.html', {
            'user': user,
        })
    except Exception as e:
        return render(request, 'kiosk/user_details.html', {
            'error_message': "Failed to find details for " + str(user_id),
        })
        
def user_detail_search(request):
    return render(request, 'kiosk/user_details_search.html', {})
    
def kiosk(request):
    return render(request, 'kiosk/kiosk.html', {})

def test(request):
    return render(request, 'kiosk/test_form.html')