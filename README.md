# club_shade
Simulation of proposed shade covering for ice rink

Shade.py produces a map of what portion of the rink (y axis) is covered at various times (x axis). It does not represent the area of the rink covered, since the x axis is time, not distance. The blue is what is covered by the proposed shade covering, the green is a pessimistic approximation of what the trees already cover.

Heat.py produces a heatmap of minutes of shade provided by the cover, it does not facor in the trees.

In both shade.y and heat.py, the date range 10/15 - 3/15 has been hardcoded in main but can be changed. The range of time 9am to 4pm has also been hardcoded, as that is when the sun's intensity is the most significant. Future work for heat.py could use the actual sunrise and sunset times, then weight minutes of coverage by intensity of solar radiation, all data avaliable in the pysolar library. Shade.py could also theoretically account for sunrise and sunset, but an irregular time range would make plotting such a graph difficult.

The rink is assumed to be 200 ft long by 80 ft wide tilted 3.8 degrees NW. These estimates, as well as the latitude and longitude of center ice  were determined with Google Earth.

This simulation does not account for light reflected off the ice onto the bottom of the cover, then back onto the ice, but a low-emissivity material should be a consideration for the cover to prevent this.

Questions on calcuations and documentation can be sent to matt.lewton9@gmail.com, or mlewton@purdue.edu.
