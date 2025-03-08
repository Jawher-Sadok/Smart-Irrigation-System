from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz
import subprocess
import time

def is_time_between_6_and_630(local_time_str):
    # Define the time range in HH:MM format
    start_time = "06:00"
    end_time = "06:30"

    # Convert the time strings into datetime objects
    time_format = '%H:%M'
    local_time = datetime.strptime(local_time_str, time_format)
    start_time_dt = datetime.strptime(start_time, time_format)
    end_time_dt = datetime.strptime(end_time, time_format)

    # Check if the local_time is between start_time and end_time
    return start_time_dt <= local_time <= end_time_dt
def get_local_time(latitude, longitude):
    # Initialize TimezoneFinder object
    tf = TimezoneFinder()

    # Find the timezone of the given coordinates
    timezone_str = tf.timezone_at(lat=latitude, lng=longitude)

    if timezone_str:
        # Get the timezone object
        timezone = pytz.timezone(timezone_str)

        # Get the current time in that timezone
        local_time = datetime.now(timezone)

        # Return the time in HH:MM format
        return local_time.strftime('%H:%M')
    else:
        return "Timezone not found"

# Example usage
latitude = 36.892359973193614
longitude = 10.187902646026297
 

while True :
  # usage:
  local_time_str = get_local_time(latitude, longitude)
  result = is_time_between_6_and_630(local_time_str)
  if result :
    subprocess.run(["python", "solution.py"])
    time.sleep(1800)  # Pause for 30 minutes before the next iteration 
