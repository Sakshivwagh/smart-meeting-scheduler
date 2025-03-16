# Application
import datetime

class Scheduler:
    def __init__(self, work_hours=(9, 17), holidays=None):
        self.work_hours = work_hours
        self.holidays = set(holidays) if holidays else set()
        self.bookings = {}
    
    def is_available_day(self, day):
        return day.weekday() < 5 and day.strftime('%Y-%m-%d') not in self.holidays
    
    def book_meeting(self, user, day, start, end):
        if not self.is_available_day(day):
            return "Cannot schedule on weekends or holidays."
        
        if start < self.work_hours[0] or end > self.work_hours[1]:
            return "Meeting must be within working hours."
        
        date_str = day.strftime('%Y-%m-%d')
        meeting_slot = (start, end)
        
        self.bookings.setdefault(user, {}).setdefault(date_str, [])
        
        for existing_start, existing_end in self.bookings[user][date_str]:
            if not (meeting_slot[1] <= existing_start or meeting_slot[0] >= existing_end):
                return "Meeting time conflicts with another."
        
        self.bookings[user][date_str].append(meeting_slot)
        self.bookings[user][date_str].sort()
        return "Meeting successfully scheduled."
    
    def available_slots(self, user, day):
        if not self.is_available_day(day):
            return "No slots available on weekends or holidays."
        
        date_str = day.strftime('%Y-%m-%d')
        booked_slots = self.bookings.get(user, {}).get(date_str, [])
        available_slots = []
        
        current_time = self.work_hours[0]
        while current_time < self.work_hours[1]:
            slot = (current_time, current_time + 1)
            if all(slot[1] <= start or slot[0] >= end for start, end in booked_slots):
                available_slots.append(f"{slot[0]}:00 - {slot[1]}:00")
            current_time += 1
        
        return available_slots if available_slots else "No open slots available."
    
    def show_meetings(self, user, day):
        date_str = day.strftime('%Y-%m-%d')
        meetings = self.bookings.get(user, {}).get(date_str, [])
        
        if not meetings:
            return "No scheduled meetings."
        
        details = f"Meetings on {date_str}:\n"
        for start, end in sorted(meetings):
            details += f"  {start}:00 - {end}:00\n"
        return details

scheduler = Scheduler(holidays={"2025-03-17"})
user_name = "Alice"
day = datetime.date(2025, 3, 18)

print(scheduler.book_meeting(user_name, day, 10, 11))  
print("Available slots:", scheduler.available_slots(user_name, day))
print(scheduler.show_meetings(user_name, day))
