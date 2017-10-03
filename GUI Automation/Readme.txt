=============================================================================================
COMPA FRAMEWORK WATCHDOG
=============================================================================================
                            OBJECT SPECIFICATION
=============================================================================================
ProjectName: BMW ACSM5 
Source: Application.py
Revision: 1.1 
Author: David Szurovecz 
Date: 2017/08/24 08:24:32CEST 

Purpose : Program should sense that the test has been stopped and realize the actual
progress has been made before the collision and restart it from the correct point.



HISTORY:
Revision 0.8:
- Added Configurator Class.
- Removing TESTLIST MAPPER Dictionary.
- Added Exception Handling for more functions.

Revision 0.9 :
-Added more System Messages
-Added Logger Functions
-Removed TestConfig Attribute getter from the Parser because it was redundant

Revision 1.0:
- Added new property to configurator Class
- Instrument Init now works with parameters not /w template mathcing
- Hard coded String Removed. Now Configurator Class parse and XML

Revision 1.1:
- Added new property for Moushandler Class Failsafe and delay time
- Redundance improvements
- More better GUI
- Now Installer Is Available
- Timestamp now appear after every action on the console window
- Added Exceptions
- Console String Messages has been moved to Logger as Class variables
- All Threads are Daemon now (If main application quit all thread die)
- TimeStamp bug fixed
- New Exception Handled: object Reference not set to an instance of an object