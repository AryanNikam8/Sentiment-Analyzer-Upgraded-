import tkinter as tk
from tkinter import messagebox, ttk
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import time

nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    sentiment_scores = sia.polarity_scores(text)
    if sentiment_scores['compound'] > 0.05:
        sentiment = "Positive"
    elif sentiment_scores['compound'] < -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    return sentiment, sentiment_scores

def update_progress():
    for i in range(101):
        progress_var.set(i)
        progress_label.config(text=f"Progress: {i}%")
        progress_bar.update_idletasks()
        time.sleep(0.01)  # Faster progress for a smoother experience

    # Display the button once progress reaches 100%
    progress_label.config(text="\u2714 Ready", fg="green")  # Checkmark and green text
    open_app_button.pack(pady=20)  # Show the button

def open_sentiment_analyzer():
    root.destroy()  # Close the progress bar window
    main()          # Open the sentiment analyzer

def display_tips(sentiment):
    if sentiment == "Negative":
        tips = [
            "Take a short walk outside.",
            "Listen to uplifting music.",
            "Talk to a trusted friend.",
            "Try mindfulness exercises.",
            "Treat yourself to something you love."
        ]
    elif sentiment == "Positive":
        tips = [
            "Share your happiness!",
            "Reflect on your blessings.",
            "Explore a new hobby.",
            "Spread kindness to others.",
            "Celebrate your achievements."
        ]
    else:
        tips = [
            "Try something new!",
            "Connect with a friend.",
            "Plan a fun activity.",
            "Watch an inspiring video.",
            "Appreciate the little things around you."
        ]

    # Configure the tips tag with a darker gray color
    output_text.tag_configure("tips", foreground="#404040", font=("Calibri", 15, "italic"))  # Dark gray

    for tip in tips:
        output_text.insert(tk.END, f"- {tip}\n", "tips")


def get_sentiment():
    user_input = user_input_entry.get().strip()

    if user_input.lower() == 'exit':
        sentiment_root.quit()  # Exit the program when 'exit' is typed
        return

    if not user_input:
        messagebox.showwarning("Input Error", "Please enter some text to analyze.")
        return

    try:
        sentiment, sentiment_scores = analyze_sentiment(user_input)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        return

    user_input_entry.delete(0, tk.END)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, f"\u2b50 Sentiment: {sentiment} \u2b50\n", "sentiment")
    output_text.insert(tk.END, f"Scores: {sentiment_scores}\n\n", "sentiment")
    display_tips(sentiment)

def clear_output():
    user_input_entry.delete(0, tk.END)
    output_text.delete(1.0, tk.END)

def exit_application():
    # Confirmation dialog before exiting
    confirm_exit = messagebox.askyesno(
        "Exit Confirmation", "Are you sure you want to exit?"
    )
    if confirm_exit:
        messagebox.showinfo("Goodbye", "Goodbye! Thank you for using the Sentiment Analyzer.")
        sentiment_root.quit()   # Stops the Tkinter event loop
        sentiment_root.destroy()  # Immediately destroys the window


def create_progress_bar_gui():
    global root, progress_var, progress_label, progress_bar, open_app_button

    root = tk.Tk()
    root.title("Creative Progress Bar")
    
    # Set window size and center it
    window_width = 400
    window_height = 250
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    root.configure(bg="#282c34")  # Dark background

    progress_var = tk.IntVar()

    progress_label = tk.Label(
        root, text="Progress: 0%", font=("Arial", 16, "bold"), bg="#282c34", fg="#61dafb"
    )  # Light blue text
    progress_label.pack(pady=20)

    style = ttk.Style()
    style.theme_use("default")
    style.configure(
        "TProgressbar",
        thickness=20,
        troughcolor="#444",
        background="#61dafb",
        bordercolor="#282c34"
    )

    progress_bar = ttk.Progressbar(
        root, orient="horizontal", length=300, mode="determinate", variable=progress_var, style="TProgressbar"
    )
    progress_bar.pack(pady=20)

    # Button to open the sentiment analyzer (initially hidden)
    open_app_button = tk.Button(
        root, text="Open Sentiment Analyzer", command=open_sentiment_analyzer,
        font=("Arial", 12, "bold"), bg="#61dafb", fg="#282c34", activebackground="#4a9fda"
    )

    # Credits
    credits_label = tk.Label(
        root,
        text="Developed by Aryan Nikam",
        font=("Arial", 10),
        bg="#282c34",
        fg="#61dafb"
    )
    credits_label.pack(side=tk.BOTTOM, pady=10)

    # Start the progress automatically
    root.after(100, update_progress)

    root.mainloop()

def main():
    global sentiment_root, user_input_entry, output_text

    sentiment_root = tk.Tk()
    sentiment_root.title("Sentiment Analysis Chatbot")

    # Set window size and center it
    window_width = 500
    window_height = 600
    screen_width = sentiment_root.winfo_screenwidth()
    screen_height = sentiment_root.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    sentiment_root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
    
    sentiment_root.config(bg="#000000")

    # Main frame
    frame = tk.Frame(sentiment_root, bg="#000000")
    frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

    # Welcome label
    welcome_label = tk.Label(
        frame, text="\ud83d\ude80 Sentiment Analysis Chatbot \ud83d\ude80", 
        font=("Freestyle Script", 24, 'bold'), bg="#000000", fg="#61dafb"
    )
    welcome_label.pack(pady=10)

    # User input label and entry
    user_input_label = tk.Label(
        frame, text="How's Your Day Today? :", font=("Comic Sans MS", 12), bg="#000000", fg="white"
    )
    user_input_label.pack(pady=5)

    user_input_entry = tk.Entry(frame, width=40, font=("MV Boli", 12), relief=tk.SUNKEN, bg="#444444", fg="#ffffff")
    user_input_entry.pack(pady=5)

    # Buttons
    button_frame = tk.Frame(frame, bg="#000000")
    button_frame.pack(pady=15)

    analyze_button = tk.Button(
        button_frame, text="Analyze Sentiment", command=get_sentiment, 
        font=("Comic Sans MS", 12), bg="#c80afc", fg="white", activebackground="#e080fc"
    )
    analyze_button.grid(row=0, column=0, padx=5)

    clear_button = tk.Button(
        button_frame, text="Clear Output", command=clear_output, 
        font=("Comic Sans MS", 12), bg="#c80afc", fg="white", activebackground="#e080fc"
    )
    clear_button.grid(row=0, column=1, padx=5)

    exit_button = tk.Button(
        button_frame, text="Exit", command=exit_application, 
        font=("Comic Sans MS", 12), bg="#ff4d4d", fg="white", activebackground="#e080fc"
    )
    exit_button.grid(row=0, column=2, padx=5)

    # Output label and text box
    output_label = tk.Label(
        frame, text="\ud83d\udd0d Sentiment Analysis Output:", font=("Comic Sans MS", 12), bg="#000000", fg="white"
    )
    output_label.pack(pady=5)

    output_text = tk.Text(
        frame, height=10, width=40, font=("MV Boli", 12), wrap=tk.WORD, 
        bg="#f0f8ff", bd=2, fg="#000080"
    )
    output_text.tag_configure("sentiment", foreground="green", font=("MV Boli", 14, "bold"))
    output_text.tag_configure("tips", foreground="orange", font=("MV Boli", 12, "italic"))
    output_text.pack(pady=10)

    # Credits label
    credits_label = tk.Label(
        sentiment_root,
        text="Developed by Aryan Nikam",
        font=("Arial", 10),
        bg="#000000",
        fg="#61dafb"
    )
    credits_label.pack(side=tk.BOTTOM, pady=10)

    # Bind Enter key to analyze sentiment
    sentiment_root.bind('<Return>', lambda event: get_sentiment())

    sentiment_root.mainloop()

if __name__ == "__main__":
    create_progress_bar_gui()
