from app import notifications

def add_notification(id, message):
    if id not in notifications:
        notifications[id] = []
    notifications[id].append({"message": message})

def create_message_to_waiter(table_name):
    return f"Đã xong {table_name}"