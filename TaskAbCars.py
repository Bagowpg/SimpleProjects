from pymongo import *

client = MongoClient('mongodb://localhost:27017/')

print("Enter the name of database")
db = client[input(str())]
print("Enter the name of collection")
mycollection = db[input(str())]

def Manufacture(mark):
    i = 0
    for car in mycollection.find():
        key_exists = "manufacture" in car
        if key_exists and car["manufacture"] == mark:
            print (" id: ", car["_id"])
            i+=1
    print("Amount of cars: ", i)

def LaterThen(year):
    for car in mycollection.find():
        key_exists = "year" in car
        if key_exists:
            now = int(year)
            if car["year"] >= now:
                print (" id: ", car["_id"])

def Options(__id):
    for car in mycollection.find():
        key_exists = "car_options" in car
        if key_exists and str(car["_id"]) == __id:
            print("Car option list:")
            for i in range(len(car["car_options"])):
                print(car["car_options"][i])
        elif not key_exists and str(car["_id"]) == __id:
            print("Car options are not found")

def Manager(command):
    parts = command.split()
    if parts[0] == 'help':
        print (
            'manufacture <manufacture> - Amount and list cars of that mark\n' 
            'later_then <year> - All cars manufactured not earlier than the specified year\n'
            'options <id> - Car option list\n'
            'quit - Stop programm')
        Manager(input())
    elif parts[0] == 'manufacture':
        Manufacture(parts[1])
        Manager(input())
    elif parts[0] == 'later_then':
        LaterThen(parts[1])
        Manager(input())
    elif parts[0] == 'options':
        Options(parts[1])
        Manager(input())
    elif parts[0] == 'quit':
        exit()
    else:
         print ('Wrong command')
                
Manager(input())