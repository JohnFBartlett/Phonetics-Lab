class IntervalCalculator:
    # takes in the start time of a segment, the end time of the same segment,
    # and the list of creak values (paired with their timestamps)
    # that fall within the segment's start and end times
    #
    # returns an array containing the overall average creak value followed
    # by the 15 interval averages for the given segment
    @staticmethod
    def calculate_interval_values(startTime, endTime, creakList):
        output = []
        print(creakList)
        # first get average
        just_vals = [elem[1] for elem in creakList]
        avg_val = sum(just_vals) / float(len(just_vals))
        output.append(avg_val)

        interval = (endTime - startTime) / 15.0
        creaks = iter(creakList)
        prev = ''
        curr = next(creaks)
        print('Curr: ' + str(curr))
        for i in range(0, 15):
            startInterval = startTime + i * interval
            endInterval = startTime + (i + 1) * interval
            tempList = []
            while curr[0] < endInterval and curr[0] >= startInterval:
                tempList.append(curr[1])
                prev = curr
                try:
                    curr = next(creaks)
                except StopIteration:
                    break
            if not tempList:
                if not prev:
                    tempList.append(curr[1])
                else:
                    middle = startInterval + interval / 2
                    if abs(middle - prev[0]) < abs(curr[0] - middle):
                        tempList.append(prev[1])
                    else:
                        tempList.append(curr[1])
            print("List of values for interval " + str(i) + ": " + str(tempList))
            interval_entry = float(sum(tempList)) / float(len(tempList))
            print("Interval entry = " + str(interval_entry))
            output.append(interval_entry)
        print("Printing output")
        print(output)
        return output

    @staticmethod
    def calculate_f0_interval_values(startTime, endTime, valuesList):
        output = []
        print(valuesList)
        print('Getting f0 averages.')
        # first get average
        f0_vals = [elem[1] for elem in valuesList]
        avg_f0_val = sum(f0_vals) / float(len(f0_vals))
        output.append(avg_f0_val)

        interval = (endTime - startTime) / 15.0
        values = iter(valuesList)
        prev = ''
        curr = next(values)
        # print('Curr: ' + str(curr))
        for i in range(0, 15):
            startInterval = startTime + i * interval
            endInterval = startTime + (i + 1) * interval
            tempList = []
            while endInterval > curr[0] >= startInterval:
                tempList.append(curr[1])
                prev = curr
                try:
                    curr = next(values)
                except StopIteration:
                    break
            if not tempList:
                if not prev:
                    tempList.append(curr[1])
                else:
                    middle = startInterval + interval / 2
                    if abs(middle - prev[0]) < abs(curr[0] - middle):
                        tempList.append(prev[1])
                    else:
                        tempList.append(curr[1])
            print("List of values for interval " + str(i) + ": " + str(tempList))
            interval_entry = float(sum(tempList)) / float(len(tempList))
            print("Interval entry = " + str(interval_entry))
            output.append(interval_entry)

        print('Getting pitchmark averages.')
        try:
            pm_vals = [elem[2] for elem in valuesList]
            avg_pm_val = sum(pm_vals) / float(len(pm_vals))
            output.append(avg_pm_val)
        except:
            print("Input doesn't have pm column!")
            return None

        interval = (endTime - startTime) / 15.0
        values = iter(valuesList)
        prev = ''
        curr = next(values)
        for i in range(0, 15):
            startInterval = startTime + i * interval
            endInterval = startTime + (i + 1) * interval
            tempList = []
            while endInterval > curr[0] >= startInterval:
                tempList.append(curr[2])
                prev = curr
                try:
                    curr = next(values)
                except StopIteration:
                    break
            if not tempList:
                if not prev:
                    tempList.append(curr[2])
                else:
                    middle = startInterval + interval / 2
                    if abs(middle - prev[0]) < abs(curr[0] - middle):
                        tempList.append(prev[2])
                    else:
                        tempList.append(curr[2])
            print("List of values for interval " + str(i) + ": " + str(tempList))
            interval_entry = float(sum(tempList)) / float(len(tempList))
            print("Interval entry = " + str(interval_entry))
            output.append(interval_entry)
        print("Printing output")
        print(output)
        return output