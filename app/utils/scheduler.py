# app/utils/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

def check_meal_reminders(db):
    """
    This function checks pending meal reminders and triggers notifications if the reminder time has arrived.
    """
    print("Checking meal reminders...")
    current_time = datetime.now()

    # Fetch all 'pending' reminders and send notifications if it's time
    reminders = db.meal_reminders.find({"status": "pending"})
    for reminder in reminders:
        if reminder['reminder_time'] <= current_time:
            print(f"Sending reminder for {reminder['meal']}: {reminder['reminder_message']}")
            # Trigger notification (e.g., push notification or email)
            db.meal_reminders.update_one(
                {"_id": reminder['_id']},
                {"$set": {"status": "notified"}}
            )

def start_scheduler(app, db):
    """
    Starts the background scheduler to check meal reminders every minute.
    """
    scheduler = BackgroundScheduler()

    # Add the job to check meal reminders and pass the db instance
    scheduler.add_job(func=lambda: check_meal_reminders(db), trigger="interval", minutes=1)
    scheduler.start()

    # Shut down the scheduler when the app exits (note the 'exc' parameter)
    app.teardown_appcontext(lambda exc: scheduler.shutdown())
