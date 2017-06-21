#!/usr/bin/python

class Interval_Calculator:
	
	# takes in the start time of a segment, the end time of the same segment,
	# and the list of creak values (paired with their timestamps)
	# that fall within the segment's start and end times
	# 
	# returns an array containing the overall average creak value followed
	# by the 15 interval averages for the given segment
	def calculate_interval_values(startTime, endTime, creakList):
		output = []
		interval = (endTime - startTime)/15.0
		creaks = iter(creakList)
		prev = ''
		curr = creaks.next()
		for i in range(0,14):
			startInterval = startTime + i*interval
			endInterval = startTime = (i+1)*interval
			tempList = []
			while curr[0] < endInterval and curr[0] >= startInterval:
				tempList.append(curr[1])
				prev = curr
				curr = creaks.next()
			if not tempList:
				if not prev:
					tempList.append(curr[1])
				else:
					middle = startInterval + interval/2
					if abs(middle - prev[0]) < abs(curr[0] - middle):
						tempList.append(prev[1])
					else:
						tempList.append(curr[1])
			output.append(float(sum(tempList))/float(len(tempList)))

		return output

	def calculate_f0_interval_values(startTime, endTime, valuesList):
		output = []
		interval = (endTime - startTime)/15.0
		values = iter(valuesList)
		prev = ''
		curr = values.next()
		for i in range(0,14):
			startInterval = startTime + i*interval
			endInterval = startTime = (i+1)*interval
			tempList = []
			while curr[0] < endInterval and curr[0] >= startInterval:
				tempList.append(curr)
				prev = curr
				curr = creaks.next()
			if not tempList:
				if not prev:
					tempList.append(curr[1])
				else:
					middle = startInterval + interval/2
					if abs(middle - prev[0]) < abs(curr[0] - middle):
						tempList.append(prev[1])
					else:
						tempList.append(curr[1])
			output.append(float(sum(tempList))/float(len(tempList)))

		return output