import datetime
import re
import os

def parse_time(time_str):
    match = re.search(r'(\d+):(\d+)\s*([apAP][mM]*)', time_str)
    if match:
        hour = int(match.group(1))
        minute = int(match.group(2))
        period = match.group(3).lower()
        return hour, minute, period
    else:
        return None
    
def parse_day(day_str):
    days_mapping = {
        'today': 2,
        'tomorrow': 3,
        'sunday': 6,
        'monday': 0,
        'tuesday': 1,
        'wednesday': 2,
        'thursday': 3,
        'friday': 4,
        'saturday': 5
    }

    day_str_lower = day_str.lower()
    return days_mapping.get(day_str_lower, None)

def add_reminder():
    print("What would you like to be reminded of?")
    reminder_text = ''
    if reminder_text:
        print("When should I remind you?")
        time_str = ''
        if time_str:
            parsed_time = parse_time(time_str)
            if parsed_time:
                print("On which day?")
                day_str = ''
                if day_str:
                    current_time = datetime.datetime.now()
                    reminder_day = current_time.weekday()  # Default to today if not specified
                    period = parsed_time[2]
                    parsed_day = parse_day(day_str)
                    if parsed_day is not None:
                        reminder_day = parsed_day

                    reminder_time = datetime.datetime(current_time.year, current_time.month, current_time.day + (reminder_day - current_time.weekday()), parsed_time[0], parsed_time[1])
                    save_reminder(reminder_time, period, reminder_text)
                    print(f"Reminder set for {reminder_text} at {reminder_time.strftime('%H:%M')} {period} on {day_str}.")
                else:
                    print("Invalid day. Please try again.")
            else:
                print("Invalid time format. Please try again.")
        else:
            print("Invalid time. Please try again.")

def save_reminder(reminder_time, period, reminder_text):
    with open("reminders.txt", "a") as file:
        file.write(f"{reminder_time.strftime('%Y-%m-%d %H:%M:%S')}, {period}, {reminder_text}\n")

def load_reminders():
    reminders = []
    if os.path.exists("reminders.txt"):
        with open("reminders.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split(",")
                if len(parts) == 3:
                    reminder_time = datetime.datetime.strptime(parts[0], "%Y-%m-%d %H:%M:%S")
                    period = parts[1].strip()
                    reminder_text = parts[2].strip()
                    reminders.append((reminder_time, period, reminder_text))
    return reminders

def remove_expired_reminders(reminders):
    current_time = datetime.datetime.now()

    # Use a list comprehension to filter expired reminders
    updated_reminders = [(date, time, period) for date, time, period in reminders
                         if date > current_time and not expired(date, time, period, current_time)]

    return updated_reminders

def expired(date, time, period, current_time):
    formatted_date = date.strftime('%Y-%m-%d')
    formatted_time = time
    formatted_period = period.upper()

    current_date = current_time.strftime('%Y-%m-%d')
    current_time = current_time.strftime('%I:%M:%S')
    current_period = datetime.datetime.now().strftime('%p')

    return formatted_date < current_date or (formatted_date == current_date and formatted_time < current_time and formatted_period == current_period)

def auto_delete_expired_reminders():
    reminders = load_reminders()
    updated_reminders = remove_expired_reminders(reminders)
    
    # Write the updated reminders back to the file
    with open("reminders.txt", "w") as file:
        for reminder_time, period, reminder_text in updated_reminders:
            file.write(f"{reminder_time.strftime('%Y-%m-%d %H:%M:%S')}, {period}, {reminder_text}\n")

def print_today_reminders():
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    reminders = load_reminders()
    today_reminders = [(date, period, text) for date, period, text in reminders if date.strftime('%Y-%m-%d') == today]

    if today_reminders:
        print("Today's Reminders:")
        for reminder_time, period, reminder_text in today_reminders:
            print(f"{reminder_time.strftime('%H:%M')} {period}: {reminder_text}")
    else:
        print("No reminders for today.")

# Add this function call wherever you want to print today's reminders
print_today_reminders()