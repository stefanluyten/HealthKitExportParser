from xml.dom import minidom

xmldoc = minidom.parse('export.xml')
recordlist = xmldoc.getElementsByTagName('Record')
for s in recordlist:
	if s.attributes['type'].value == "HKQuantityTypeIdentifierHeartRate":
		year = s.attributes['startDate'].value[:4]
		month = s.attributes['startDate'].value[4:6]
		date = s.attributes['startDate'].value[6:8]
		hour = s.attributes['startDate'].value[8:10]	
		minute = s.attributes['startDate'].value[10:12]	
		try:
			#try to parse the consolidated values
			print "%s,%s,%s,%s,%s,%d,%d,%d,%d" % (year, month, date, hour, minute,   float(s.attributes['min'].value)*60, float(s.attributes['max'].value)*60, float(s.attributes['average'].value)*60, float(s.attributes['recordCount'].value))
    		except:
    			#try to parse the non-consolidated ones
    			print "%s,%s,%s,%s,%s,%d,%d,%d,%d,+" % (year, month, date, hour, minute, float(s.attributes['value'].value)*60, float(s.attributes['value'].value)*60, float(s.attributes['value'].value)*60, 1)