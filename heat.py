import matplotlib
import matplotlib.pyplot as plt
from pysolar.solar import get_altitude, get_azimuth
import datetime
import math
import matplotlib.image as mpimg

#INIT constants and globals
HEIGHT = 15 #height of cover above ice (ft)
BOTTOM = 75 #Bottom edge of cover, distance from North edge of rink (ft)
C_WIDTH = 125 #width of cover (N-S) (ft)
R_WIDTH = 80 #width of rink (E-W) (ft)
R_LENGTH = 200 #length of rink (ft)
LATITUDE = 38.974173 #Rink latitude
LONGITUDE = -77.078337 #Rink longitude
TILT = 3.8 #degrees, tilt of rink from N-S

#main function for direct usage
def main():
    
    
    # Single day use
    Day, Month, Year = getInputs()
    shade = simShade(Day, Month, Year) #sim shade
    graphData(shade, Day, Month, Year) #make graph
    
    """
    #For Hardcoded date range
    # The size of each step in days
    day_delta = datetime.timedelta(days=1) #set t step to one day
    start_date = datetime.date(2021, 10, 15) #set start date to Oct 15
    end_date = datetime.date(2022, 3, 15) #set end date to march 15
    for i in range((end_date - start_date).days): #get day, month, year as datetime objects, then simulate shade and create a graph
        Day = (start_date + i*day_delta).day
        Month = (start_date + i*day_delta).month
        Year = (start_date + i*day_delta).year
        shade = simShade(Day, Month, Year) #sim shade
        graphData(shade, Day, Month, Year) #make graph
    """

def getInputs(): #get date from user
    #get date info
    Year = 2021 #int(input("Year: "))
    Month = int(input("Month: "))
    Day = int(input("Day: "))
    return Day, Month, Year

def simShade(Day, Month, Year):
    shade  = [] #create empty array for all shade
    
    #Init main dataset as blank, 200x84 array for rink dimensions
    for y in range(R_LENGTH):
        shade.append([])
        for x in range(R_WIDTH):
            shade[y].append(0)

    #iterate through times for each minute
    for h in range(7): #iterate from 9am to 4pm
        for m in range(60): #for each minute 0-59

            #Get raw values
            time = datetime.datetime(Year, Month, Day, 10+4+h, m, 0, tzinfo=datetime.timezone.utc) #hardcode 9am start
            alt = get_altitude(LATITUDE, LONGITUDE, time) #get sun altitude
            az = get_azimuth(LATITUDE, LONGITUDE, time) #get sun azimuth

            #Calculate useful values
            d = HEIGHT/math.tan(alt*math.pi/180) #shadow distance
            theta = math.radians(270 - az - TILT) #convert azimuth to shadow theta, where east is 0, and flip negative for shadow
            bott_lft = (d*math.cos(theta), d*math.sin(theta) + BOTTOM) #tuple, x, y coordinates on rink for bottom left corner of shadow

            #update heatmap tables
            for y in range(0, 199): #iterate over every y step on rink
                for x in range(R_WIDTH): #iterate over every x step on rink
                    if x >= bott_lft[0] and x <= bott_lft[0] + R_WIDTH and y >= bott_lft[1] and y <= bott_lft[1] + C_WIDTH: #if within projected shadow range, using bottom left corner as refrence
                        shade[y][x]+=1 #add 1 minute of shade
    return shade #return output

def graphData(shade, Day, Month, Year):
    
    plt.clf() #clear graph in between iterations

    #Plot Axis
    plt.axis([0, R_WIDTH - 1, 0, R_LENGTH - 1])
    plt.xticks([], [])

    #Map rink image and heatmap
    img = mpimg.imread('rink4.jpg') #read image
    plt.imshow(img, extent=[0, R_WIDTH, 0, R_LENGTH]) #add image to graph
    plt.imshow(shade, cmap="magma_r", alpha = .5, aspect='equal') #create heatmap

    #Colorbar
    plt.colorbar(label="Minutes of Shade") #create colorbar

    #Add Titles/Labels
    plt.title("Shade Map on "+str(Month)+"/"+str(Day)+"/"+str(Year)) #title
    plt.ylabel('Baseline 0 ft at trees, Winter Center at 200 ft') #y axis label
    plt.xlabel("North Side/Trees") #x axis label
    
    #plt.savefig("10-15_3-15_Heatmaps/" +str(Month)+"-"+str(Day)+"-"+ str(Year) + "_heatmap.png", format = 'png', bbox_inches = 'tight') #save image as png

    plt.show() #show image

main()