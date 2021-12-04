import math

weekdays = [
  "Monday", 
  "Tuesday",
  "Wednesday",
  "Thursday",
  "Friday",
  "Saturday",
  "Sunday"]

def add_time(start, duration, startDay=""):
  new_time = ""

  #
  # Get current hour & minute
  #
  idx = start.find(":")
  currentHour = int(start[:idx])
  temp = start[idx+1:]
  idx2 = temp.find(" ")
  currentMinute = int(temp[:idx2])
  currentZone = temp[idx2+1:]
  if (currentZone == "PM"):
    currentHour = currentHour + 12

  #
  # Get duration by minutes
  #
  idx = duration.find(":")
  hour = int(duration[:idx])
  minute = int(duration[idx+1:])
  totalMinute = hour * 60 + minute

  #
  # Calculate final time
  #
  finalTotalMinute = currentMinute + totalMinute
  finalTotalHour = currentHour + math.floor(finalTotalMinute/60)

  finalMinute = finalTotalMinute % 60
  finalHour = finalTotalHour % 24
  finalDay = math.floor(finalTotalMinute / (24 * 60))

  new_time = ":" + str(finalMinute).zfill(2)
  if (finalHour == 12):
    finalZone = "PM"
    new_time = str(finalHour) + new_time + " " + finalZone
  elif (finalHour == 0):
    finalZone = "AM"
    new_time = "12" + new_time + " " + finalZone
  elif (finalHour >= 12):
    finalZone = "PM"
    new_time = str(finalHour-12) + new_time + " " + finalZone
  else:
    finalZone = "AM"
    new_time = str(finalHour) + new_time + " " + finalZone

  nextDay = False
  if currentZone == "PM" and finalZone == "AM" and totalMinute <= 60 * 24:
    nextDay = True
  if currentZone == finalZone and totalMinute <= 60 * 24 and totalMinute > 60 * 12:
    nextDay = True

  #
  # Format day
  #
  dayFormatted = False
  finalDayStr = startDay
  finalDayIdx = -1
  if finalDayStr != "":
    finalDayStr = finalDayStr.lower().capitalize();
    finalDayIdx = weekdays.index(finalDayStr)

  if finalDay >= 1 and not nextDay:
    dayFormatted = True
    if finalDayIdx == -1:
      new_time = new_time + f" ({finalDay + 1} days later)"
    else:
      finalDayStr = findDay(finalDayIdx, finalDay + 1)
      new_time = new_time + f", {finalDayStr} ({finalDay + 1} days later)"
      
  if finalDay <= 1 and nextDay:
    dayFormatted = True
    if finalDayIdx == -1:
      new_time = new_time + f" (next day)"
    else:
      finalDayStr = findDay(finalDayIdx, 1)
      new_time = new_time + f", {finalDayStr} (next day)"

  if not dayFormatted and finalDayIdx != -1:
    finalDayStr = findDay(finalDayIdx, finalDay)
    new_time = new_time + f", {finalDayStr}"

  return new_time

def findDay(startIdx, days):
  finalIdx = startIdx + days
  return weekdays[finalIdx % 7]
