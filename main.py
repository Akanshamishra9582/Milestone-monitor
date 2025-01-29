import tkinter as tk
import datetime

# Path to the icon image
icon_path = "images/cgev.ico"

# Create the main window
root = tk.Tk()
root.title("Milestone Monitor")
root.configure(bg="#d8f3dc")
root.iconbitmap(icon_path)
root.geometry("1600x300")

# Get today's date
today = datetime.date.today()
# Get the ordinal day of the year
day_of_year = today.timetuple().tm_yday

# Progress stages colors
progress_stages = ["#b7efc5", "#6ede8a", "#25a244", "#1a7431", "#04471c"]
# Month names
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
# List to hold buttons
buttons = []


# Function to create a row of buttons for a week
def create_row(week):
    # Display month labels
    for i in range(0, 12):
        month = tk.Label(root, text=months[i], font=("Helvetica", 10), bg="#d8f3dc")
        month.grid(row=0, column=(1+i)*4, padx=2, pady=2)

    # Create buttons for each day in the week
    for i in range(1, 8):
        color_button = tk.Button(root, background="#ffffff", width=1, height=0)
        color_button.bind("<Button-1>", change_button_color)
        color_button.grid(row=i, column=week, padx=6, pady=2)
        buttons.append(color_button)


# Function to change the color of a button
def change_button_color(event):
    """Change button background color based on progress stages"""

    # Get button widget and current background color
    button = event.widget
    bg_color = button.cget("background")

    # Iterate through the progress stages
    for index, item in enumerate(progress_stages):
        # Change color if current color matches and index is within range
        if bg_color == item and index < 4:
            button.configure(bg=progress_stages[index+1])
            break
        # Set color to first stage if not found in progress stages
        if bg_color not in progress_stages:
            button.configure(bg=progress_stages[0])


def save_buttons():
    with open("buttons_data.txt", "w") as file:
        for button in buttons:
            bg_color = button.cget("background")
            file.write(bg_color + "\n")
    root.destroy()


# Function to load button colors from a file
def load_buttons():
    colors = []
    try:
        with open("buttons_data.txt", "r") as file:
            for line in file:
                bg_color = line.strip()
                colors.append(bg_color)
            return colors
    except FileNotFoundError:
        pass  # Do nothing if the file is not found
    return colors


# Variable to track edit mode
edit = False


# Function to toggle edit mode
def button_edit_on_off():
    global edit
    button_index = 0
    if not edit:
        # Enable edit mode
        for b in buttons:
            if button_index == day_of_year:
                button_index += 1
                bg_color = b.cget("background")
                if bg_color in progress_stages:
                    pass
                else:
                    b.configure(bg="#252422")
            else:
                b.configure(state="disabled")
                b.unbind("<Button-1>")
                button_index += 1
        edit = True  # Update edit mode
    else:
        # Disable edit mode
        for b in buttons:
            b.configure(state="normal")
            b.bind("<Button-1>", change_button_color)
        edit = False


# Create rows of buttons for each week
for i in range(1, 52):
    create_row(i)

# Load existing button colors from file
existing_colors = load_buttons()
# Apply existing colors to buttons
for button, color in zip(buttons, existing_colors):
    button.configure(bg=color)

# Toggle edit mode
button_edit_on_off()

# Display labels for progress stages
label_less = tk.Label(root, text="Less", font=("Helvetica", 12), bg="#d8f3dc")
label_less.grid(row=10, column=0, padx=2, pady=2)

for index, stage_color in enumerate(progress_stages):
    example_color = tk.Button(root, state="disabled", background=stage_color, width=1, height=0)
    example_color.grid(row=10, column=index+1, padx=2, pady=2)

# Button to exit and save
exit_button = tk.Button(root, command=save_buttons, text="Exit and save", background="#f07167")
exit_button.grid(row=9, column=54, padx=6, pady=2)


# Button to toggle edit mode
edit_button = tk.Button(root, command=button_edit_on_off, text="Edit", background="#f07167")
edit_button.grid(row=9, column=53, padx=6, pady=2)

# run the application
root.mainloop()