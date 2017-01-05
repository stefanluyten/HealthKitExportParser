# HealthKitExportParser

Notes from Stefan Luyten:
"export.xml" is the result of an export of your data in the iOS Health app.
This file needs to be present in the same folder as your python script.

heartparser.py focuses on two specific sets of data:
- Heart Rate in bpm
- Blood Pressure

The user chooses a start date and an end date to narrow the time range and can creates graphs with the modules, such as shown below. The parse module inside of heartparser.py has been updated to match the spacing found in the export xml file produced with iOS 10. 

Required dependencies: numpy, matplotlib, pandas, seaborn

Tip: to export your Apple Health data, open your Health app, click on the profile icon at the top right, and then select "Export Health Data."

![heartrate_2016-12-11to2017-01-05](https://cloud.githubusercontent.com/assets/20876870/21701273/54e5a572-d36a-11e6-9589-062fef8605eb.jpg)
