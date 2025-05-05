
import sqlite3
from getpass import getpass

DB_NAME = 'app_reviews.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    with open('database.sql', 'r') as f:
        cursor.executescript(f.read())
    conn.commit()
    conn.close()

def register():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    username = input("Enter new username: ")
    password = getpass("Enter new password: ")
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print("Registration successful.")
    except sqlite3.IntegrityError:
        print("Username already exists.")
    conn.close()

def login():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    username = input("Username: ")
    password = getpass("Password: ")
    cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def submit_review(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    app_name = input("App Name: ")
    review = input("Your Review: ")
    cursor.execute("INSERT INTO reviews (user_id, app_name, review) VALUES (?, ?, ?)", (user_id, app_name, review))
    conn.commit()
    print("Review submitted.")
    conn.close()

def view_reviews():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT u.username, r.app_name, r.review FROM reviews r JOIN users u ON r.user_id = u.id")
    for row in cursor.fetchall():
        print(f"User: {row[0]}, App: {row[1]}, Review: {row[2]}")
    conn.close()

def update_review(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, app_name, review FROM reviews WHERE user_id = ?", (user_id,))
    for r in cursor.fetchall():
        print(f"Review ID: {r[0]} | App: {r[1]} | Review: {r[2]}")
    review_id = input("Enter Review ID to update: ")
    new_review = input("New Review: ")
    cursor.execute("UPDATE reviews SET review = ? WHERE id = ? AND user_id = ?", (new_review, review_id, user_id))
    conn.commit()
    print("Review updated.")
    conn.close()

def delete_review(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, app_name, review FROM reviews WHERE user_id = ?", (user_id,))
    for r in cursor.fetchall():
        print(f"Review ID: {r[0]} | App: {r[1]} | Review: {r[2]}")
    review_id = input("Enter Review ID to delete: ")
    cursor.execute("DELETE FROM reviews WHERE id = ? AND user_id = ?", (review_id, user_id))
    conn.commit()
    print("Review deleted.")
    conn.close()

def main():
    init_db()
    while True:
        print("\n=== App Review System ===")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            register()
        elif choice == '2':
            user_id = login()
            if user_id:
                while True:
                    print("\n1. Submit Review")
                    print("2. View All Reviews")
                    print("3. Update My Review")
                    print("4. Delete My Review")
                    print("5. Logout")
                    action = input("Choose: ")

                    if action == '1':
                        submit_review(user_id)
                    elif action == '2':
                        view_reviews()
                    elif action == '3':
                        update_review(user_id)
                    elif action == '4':
                        delete_review(user_id)
                    elif action == '5':
                        break
            else:
                print("Invalid credentials.")
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
