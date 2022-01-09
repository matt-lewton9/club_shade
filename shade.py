import datetime
from pysolar.solar import get_altitude, get_azimuth
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.image as mpimg
import math

#init datasets and constants
HEIGHT = 30
BOTTOM = 75
WIDTH = 50
R_WIDTH = 80 #width of rink (E-W)
R_LENGTH = 200 #length of rink
LATITUDE = 38.974173 #Rink latitude
LONGITUDE = -77.078337 #Rink longitude
TILT = 3.8 #degrees, tilt of rink from N-S

def main(): #main function for direct usage
    
    day_delta = datetime.timedelta(days=1) #set t step to 1 day
    start_date = datetime.date(2021, 10, 15) # hardcode start date
    end_date = datetime.date(2022, 3, 15) #hardcode end date

    for i in range((end_date - start_date).days): #get day, month, year as datetime objects, then get plot and create a graph
        Day = (start_date + i*day_delta).day
        Month = (start_date + i*day_delta).month
        Year = (start_date + i*day_delta).year
        mins, wall, scrl, scrr = calcShade(Day, Month, Year)
        makeGraph(mins, wall, scrl, scrr, Day, Month, Year)

def getInputs():#get date info from user for single use cases
    Year = 2021 #int(input("Year: "))
    Month = int(input("Month: "))
    Day = int(input("Day: "))
    return Day, Month, Year

def calcShade(Day, Month, Year):

    #Init empty arrays
    mins = [] #minutes of day
    wall = [] #shade provided by wall
    scrl = [] #shade covering left bound
    scrr = [] #shade convering right bound

    #iterate through times for each minute
    for h in range(7):
        for m in range(60):

            #Get raw values
            time = datetime.datetime(Year, Month, Day, 10+4+h, m, 0, tzinfo=datetime.timezone.utc) #get current time in datetime format
            mins.append(h*60 + m) #append minute to minutes
            alt = get_altitude(LATITUDE, LONGITUDE, time) #get the sun's altitude
            az = get_azimuth(LATITUDE, LONGITUDE, time) #get the sun's azimuth

            #Calculate useful data
            d = HEIGHT/math.tan(alt*math.pi/180) #calculate shade distance
            theta = math.radians(270 - az - TILT) #calculate shade angle 
            left =  d*math.sin(theta) + BOTTOM #calculate left shade bound
            right  = d*math.sin(theta) + BOTTOM + WIDTH #calculate right shade bound

            #Update datasets
            wall.append(HEIGHT/math.tan(alt*math.pi/180)) #update wall shade array
            scrl.append(left) #update left shade array
            scrr.append(right) #update right shade array

    return mins, wall, scrl, scrr 

def makeGraph(mins, wall, scrl, scrr, Day, Month, Year):

    plt.clf() #clear graph in between iterations

    #Plot axis
    plt.axis([0, 420, 0, 200])
    plt.xticks([0, 60, 120, 180, 240, 300, 360, 420], ['9:00 am', '10:00 am', '11:00 am', '12:00 pm', '1:00pm', '2:00pm', '3:00pm', '4:00pm'])
    plt.xticks(rotation = 45, ha="right", rotation_mode="anchor")

    #Plot Image
    img = mpimg.imread('rink4.jpg')
    plt.imshow(img, extent=[0, 420, 0, 200], aspect=4)

    #Add Labels
    plt.title("Shade Range on "+str(Month)+"/"+str(Day)+"/"+str(Year))
    plt.ylabel('Baseline 0 ft at trees, Winter Center at 200 ft')
    plt.xlabel('Time (North Side/Trees)')

    #Plot lines
    plt.plot(mins, wall, color='green') #plot shade by trees
    plt.plot(mins, scrl, color='blue') #plot shade by cover bottom line
    plt.plot(mins, scrr, color='blue') #plot shade by cover top line
    plt.fill_between(mins, wall, color='green', alpha = .2) #fill green area
    plt.fill_between(mins, scrr, scrl, color='blue', alpha = .2) #fill blue area
    plt.savefig("10-15_3-15_Shade/" +str(Month)+"-"+str(Day)+"-"+ str(Year) + "_Shade.png", format = 'png', bbox_inches = 'tight') #save image as png

    #plt.show()

main() #call main