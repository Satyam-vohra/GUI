import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk  # For images
import pyttsx3
import speech_recognition as sr
import threading
import time  
import wikipedia
import os
import webbrowser  # To open links
from googlesearch import search  # Google Search Module

# Function to make the assistant speak
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Adjust speaking speed
    engine.setProperty('volume', 1)  # Adjust volume
    engine.say(text)
    engine.runAndWait()

# Function to listen for voice commands
def listen():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)  # Reduce background noise
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        process_command(command)
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        speak("Sorry, I did not understand that.")
    except sr.RequestError:
        print("Sorry, I could not request results.")
        speak("Sorry, I could not request results.")

# Function to process commands
def process_command(command):
    command = command.lower()

    if 'hello' in command:
        response = "Hello, how can I assist you today?"
    elif 'time' in command:
        current_time = time.strftime("%H:%M:%S")
        response = f"The current time is {current_time}"
    elif 'name' in command:
        response = "I am Erik, your assistant."
    elif 'goodbye' in command or 'exit' in command:
        response = "Goodbye, have a great day!"
        speak(response)
        window.quit()  # Close the GUI
        return
    elif 'wikipedia' in command:
        topic = command.replace("wikipedia", "").strip()
        if topic:
            response = fetch_wikipedia_summary(topic)
        else:
            response = "Please specify a topic to search on Wikipedia."
    elif 'search google for' in command:
        query = command.replace("search google for", "").strip()
        if query:
            response = fetch_google_search(query)
        else:
            response = "Please specify what to search for on Google."
    else:
        response = "Sorry, I did not understand that command."

    speak(response)
    update_gui(response)

# Fetch summary from Wikipedia
def fetch_wikipedia_summary(topic):
    try:
        summary = wikipedia.summary(topic, sentences=2)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"That topic is ambiguous. Here are some options: {', '.join(e.options)}"
    except wikipedia.exceptions.PageError:
        return "Sorry, I could not find that topic on Wikipedia."
    except Exception as e:
        return "An error occurred while fetching the information."

# Fetch top Google search results
def fetch_google_search(query):
    try:
        search_results = list(search(query, num=5, stop=5, pause=2))  # Get top 5 results
        result_text = "Here are the top Google search results:\n"
        
        # Display each search result
        for idx, url in enumerate(search_results, start=1):
            result_text += f"{idx}. {url}\n"
            create_link_button(url)  # Create clickable button
        
        return result_text
    except Exception as e:
        return "Sorry, I couldn't perform a Google search."

# Create clickable link button
def create_link_button(url):
    def open_link():
        webbrowser.open(url)  # Open the URL in a browser

    link_button = tk.Button(results_frame, text=url, fg="blue", cursor="hand2", font=("Arial", 12), command=open_link)
    link_button.pack(anchor="w", padx=20)

# Update GUI with assistant's response
def update_gui(text):
    def insert_text():
        text_box.config(state=tk.NORMAL)
        text_box.insert(tk.END, "Erik: " + text + '\n')
        text_box.config(state=tk.DISABLED)
        text_box.yview(tk.END)

    window.after(0, insert_text)

# Function to process typed command
def process_typed_command():
    command = command_entry.get().strip()  # Get text from input field
    command_entry.delete(0, tk.END)  # Clear input field
    if command:
        text_box.config(state=tk.NORMAL)
        text_box.insert(tk.END, "You: " + command + '\n')
        text_box.config(state=tk.DISABLED)
        process_command(command)  # Process the typed command

# Function to open predefined websites
def open_website(url):
    webbrowser.open(url)

# Function to exit the application
def exit_application():
    window.quit()

# GUI Setup
window = tk.Tk()
window.title("Erik Assistant")
window.state("zoomed")  # Make the window full screen
window.configure(bg='black')

# Load and display an image (Full Screen)
image_path = "C:\\Users\\shiva\\Downloads\\2.webp"# Corrected Path
#image_path = "C:\\Users\\shiva\\Downloads\\erik.jpg"
if os.path.exists(image_path):
    img = Image.open(image_path)
    img = img.resize((window.winfo_screenwidth(), window.winfo_screenheight()))  # Resize to full screen
    photo = ImageTk.PhotoImage(img)
    image_label = tk.Label(window, image=photo, bg='white')
    image_label.place(x=0, y=0, relwidth=1, relheight=1)  # Cover entire window
else:
    print("Error: Image not found. Check the file path.")

# Text box to display conversation
text_box = tk.Text(window, height=10, width=80, wrap=tk.WORD, state=tk.DISABLED, bg='oldlace', fg='black', font=("Arial", 16))
text_box.pack(pady=20)

# Input frame for typing commands
input_frame = tk.Frame(window, bg="blue")
input_frame.pack(pady=10)

# Entry box for typed command
command_entry = tk.Entry(input_frame, width=50, font=("Arial", 14))
command_entry.grid(row=0, column=0, padx=10)

# Submit button for typed command
submit_button = tk.Button(input_frame, text="Submit", command=process_typed_command, width=10, height=1, bg='royalblue', fg='white', font=("Arial", 14))
submit_button.grid(row=0, column=1, padx=10)

# Frame for displaying Google search results
results_frame = tk.Frame(window, bg="white")
results_frame.pack(pady=10)

# Buttons Frame
button_frame = tk.Frame(window, bg="black")
button_frame.pack(pady=20)

# Quick Access Buttons
web_buttons = [
    ("Google", "https://www.google.com"),
    ("YouTube", "https://www.youtube.com"),
    ("LinkedIn", "https://www.linkedin.com"),
    ("ChatGPT", "https://chat.openai.com"),
    ("Wikipedia", "https://www.wikipedia.org")
]

for name, url in web_buttons:
    tk.Button(button_frame, text=name, command=lambda u=url: open_website(u), width=15, height=2, bg='green', fg='white', font=("Arial", 14)).pack(side=tk.LEFT, padx=10)

# Button to manually activate voice recognition
listen_button = tk.Button(button_frame, text="Listen", command=lambda: threading.Thread(target=listen).start(),
                          width=15, height=2, bg='gray', fg='white', font=("Arial", 14))
listen_button.pack(side=tk.LEFT, padx=10)

# Exit button
exit_button = tk.Button(button_frame, text="Exit", command=exit_application, width=15, height=2, bg='red', fg='white', font=("Arial", 14))
exit_button.pack(side=tk.LEFT, padx=10)

# Start Tkinter event loop
window.mainloop()
