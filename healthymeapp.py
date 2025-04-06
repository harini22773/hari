import tkinter as tk
from tkinter import ttk
import json
from datetime import datetime
import os

class HealthyMeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HealthyMeapp - Daily Health Tracker")
        self.root.geometry("400x500")
        self.root.configure(bg="#E8F5E9")  # Light green background 
        # Data file path
        self.data_file = "health_data.json"
        
        # Initialize checkbox variables
        self.water_var = tk.BooleanVar()
        self.exercise_var = tk.BooleanVar()
        self.sleep_var = tk.BooleanVar()

        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Title
        title_label = tk.Label(
            self.root,
            text="HealthyMeapp",
            font=("Helvetica", 24, "bold"),
            bg="#E8F5E9",
            fg="#2E7D32"
        )
        title_label.pack(pady=20)

        # Frame for checkboxes
        checkbox_frame = tk.Frame(self.root, bg="#E8F5E9")
        checkbox_frame.pack(pady=10, padx=20, fill="x")

        # Style for checkboxes
        style = ttk.Style()
        style.configure(
            "Custom.TCheckbutton",
            background="#E8F5E9",
            font=("Helvetica", 12)
        )

        # Checkboxes
        self.water_check = ttk.Checkbutton(
            checkbox_frame,
            text="Did you drink enough water today? 💧",
            variable=self.water_var,
            style="Custom.TCheckbutton",
            command=self.update_message
        )
        self.water_check.pack(pady=5, anchor="w")

        self.exercise_check = ttk.Checkbutton(
            checkbox_frame,
            text="Did you exercise today? 🏃",
            variable=self.exercise_var,
            style="Custom.TCheckbutton",
            command=self.update_message
        )
        self.exercise_check.pack(pady=5, anchor="w")

        self.sleep_check = ttk.Checkbutton(
            checkbox_frame,
            text="Did you sleep well last night? 😴",
            variable=self.sleep_var,
            style="Custom.TCheckbutton",
            command=self.update_message
        )
        self.sleep_check.pack(pady=5, anchor="w")

        # Motivational message
        self.message_label = tk.Label(
            self.root,
            text="",
            font=("Helvetica", 12, "bold"),
            wraplength=350,
            bg="#E8F5E9",
            fg="#1565C0"
        )
        self.message_label.pack(pady=20)

        # Save button
        save_button = tk.Button(
            self.root,
            text="Save Progress",
            command=self.save_data,
            bg="#4CAF50",
            fg="white",
            font=("Helvetica", 10, "bold"),
            relief="raised",
            padx=20,
            pady=5
        )
        save_button.pack(pady=10)

    def update_message(self):
        all_checked = all([
            self.water_var.get(),
            self.exercise_var.get(),
            self.sleep_var.get()
        ])
        
        if all_checked:
            message = "🎉 Great job staying healthy today!"
        else:
            message = "💡 Try to complete your health goals!"
        
        self.message_label.config(text=message)

    def load_data(self):
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as file:
                    data = json.load(file)
                    
                    # Check if data is from today
                    saved_date = data.get('date', '')
                    current_date = datetime.now().strftime('%Y-%m-%d')
                    
                    if saved_date == current_date:
                        self.water_var.set(data.get('water', False))
                        self.exercise_var.set(data.get('exercise', False))
                        self.sleep_var.set(data.get('sleep', False))
                    else:
                        # Reset for new day
                        self.reset_checkboxes()
            
            self.update_message()
        
        except Exception as e:
            print(f"Error loading data: {e}")
            self.reset_checkboxes()

    def save_data(self):
        data = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'water': self.water_var.get(),
            'exercise': self.exercise_var.get(),
            'sleep': self.sleep_var.get()
        }
        
        try:
            with open(self.data_file, 'w') as file:
                json.dump(data, file)
            
            # Show temporary save confirmation
            original_text = self.message_label.cget("text")
            self.message_label.config(text="✅ Progress saved!")
            self.root.after(1500, lambda: self.message_label.config(text=original_text))
        
        except Exception as e:
            print(f"Error saving data: {e}")

    def reset_checkboxes(self):
        self.water_var.set(False)
        self.exercise_var.set(False)
        self.sleep_var.set(False)
    def show_statistics(self):
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Health Progress Statistics")
        stats_window.geometry("300x400")
        stats_window.configure(bg="#E8F5E9")

        # Calculate daily progress
        try:
            with open(self.data_file, 'r') as file:
                data = json.load(file)
                completed_tasks = sum([
                    data.get('water', False),
                    data.get('exercise', False),
                    data.get('sleep', False)
                ])
                completion_rate = (completed_tasks / 3) * 100

            stats_text = f"""
            Today's Health Summary:
            
            Tasks Completed: {completed_tasks}/3
            Success Rate: {completion_rate:.1f}%
            
            Daily Checklist:
            Water: {'✅' if data.get('water') else '❌'}
            Exercise: {'✅' if data.get('exercise') else '❌'}
            Sleep: {'✅' if data.get('sleep') else '❌'}
            
            Keep up the good work! 
            Every healthy choice counts! 🌟
            """
        except:
            stats_text = "Start your health journey today! 🌱"

        stats_label = tk.Label(
            stats_window,
            text=stats_text,
            bg="#E8F5E9",
            font=("Helvetica", 12),
            justify="left",
            padx=20,
            pady=20
        )
        stats_label.pack()

    def add_mood_tracker(self):
        mood_window = tk.Toplevel(self.root)
        mood_window.title("Mood Tracker")
        mood_window.geometry("300x200")
        mood_window.configure(bg="#E8F5E9")

        mood_label = tk.Label(
            mood_window,
            text="How are you feeling today?",
            bg="#E8F5E9",
            font=("Helvetica", 12, "bold")
        )
        mood_label.pack(pady=10)

        def save_mood(mood):
            try:
                with open(self.data_file, 'r') as file:
                    data = json.load(file)
                data['mood'] = mood
                with open(self.data_file, 'w') as file:
                    json.dump(data, file)
                self.show_notification(f"Mood saved: {mood}")
                mood_window.destroy()
            except Exception as e:
                self.show_notification("Error saving mood")

        moods = ["😊 Great", "🙂 Good", "😐 Okay", "😔 Not Great", "😢 Bad"]
        
        for mood in moods:
            tk.Button(
                mood_window,
                text=mood,
                command=lambda m=mood: save_mood(m),
                bg="#2196F3",
                fg="white",
                width=20
            ).pack(pady=2)

    def add_notes(self):
        notes_window = tk.Toplevel(self.root)
        notes_window.title("Health Notes")
        notes_window.geometry("400x300")
        notes_window.configure(bg="#E8F5E9")
        
        # Load existing notes
        try:
            with open(self.data_file, 'r') as file:
                data = json.load(file)
                existing_notes = data.get('notes', '')
        except:
            existing_notes = ''
        
        notes_text = tk.Text(
            notes_window,
            height=10,
            width=40,
            font=("Helvetica", 10)
        )
        notes_text.insert('1.0', existing_notes)
        notes_text.pack(pady=10, padx=10)
        
        def save_notes():
            notes = notes_text.get("1.0", tk.END)
            try:
                with open(self.data_file, 'r') as file:
                    data = json.load(file)
                data['notes'] = notes.strip()
                with open(self.data_file, 'w') as file:
                    json.dump(data, file)
                self.show_notification("Notes saved successfully!")
            except Exception as e:
                self.show_notification("Error saving notes")
        
        save_btn = tk.Button(
            notes_window,
            text="Save Notes",
            command=save_notes,
            bg="#4CAF50",
            fg="white",
            font=("Helvetica", 10, "bold")
        )
        save_btn.pack(pady=5)

    def show_notification(self, message):
        notification = tk.Toplevel(self.root)
        notification.geometry("300x100")
        notification.title("Notification")
        notification.configure(bg="#E8F5E9")
        
        label = tk.Label(
            notification,
            text=message,
            font=("Helvetica", 10),
            pady=20,
            bg="#E8F5E9"
        )
        label.pack()
        
        notification.after(2000, notification.destroy)

    def add_extra_buttons(self):
        button_frame = tk.Frame(self.root, bg="#E8F5E9")
        button_frame.pack(pady=10)
        
        stats_btn = tk.Button(
            button_frame,
            text="📊 Statistics",
            command=self.show_statistics,
            bg="#2196F3",
            fg="white",
            font=("Helvetica", 10)
        )
        stats_btn.pack(side=tk.LEFT, padx=5)
        
        mood_btn = tk.Button(
            button_frame,
            text="😊 Mood",
            command=self.add_mood_tracker,
            bg="#2196F3",
            fg="white",
            font=("Helvetica", 10)
        )
        mood_btn.pack(side=tk.LEFT, padx=5)
        
        notes_btn = tk.Button(
            button_frame,
            text="📝 Notes",
            command=self.add_notes,
            bg="#2196F3",
            fg="white",
            font=("Helvetica", 10)
        )
        notes_btn.pack(side=tk.LEFT, padx=5)
    

def main():
    root = tk.Tk()
    app = HealthyMeApp(root)
    
    # Center window on screen
    window_width = 400
    window_height = 500
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()
