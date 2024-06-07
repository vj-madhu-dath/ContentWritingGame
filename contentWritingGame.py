# code to open a file for a specific time chosen by the user and then close it.
# during this time the user must be able to edit the contents
# of the file

# %%
import os
import tkinter as tk
os.system('cls')
print("#")
import pandas as pd
os.system('cls')
print("#####")
import datetime
os.system('cls')
print("##########")
import matplotlib.pyplot as plt
os.system('cls')
print("##################")
import seaborn as sns
os.system('cls')
print("#################################")
os.system('cls')
import pyautogui

input("Shall we begin the game? (Press Enter)")
pyautogui.hotkey('alt','enter')


def writingGame():
    duration = input("How many minutes do you want to write? ")
    topic = input("What is the topic ")
    time = int(float(duration)*60*1000)
    print(time)

    def save_and_close():
        
        now = datetime.datetime.now()
        dateAndTime = ':'.join(str(now).split(':')[:2])
        content = text_area.get("1.0", "end-1c")
        length = len(content.split())
        content = f"# {topic}\n###### {dateAndTime}\n" + content
        #topic=length=duration=10
        
        try: 
            df = pd.read_csv("WordPerHour.csv",index_col=False)
        except:
            df = pd.DataFrame(columns=["Topic","Word_Count","Minutes","WPH","DateTime"])
        newRow = [topic,length,duration,length*60/float(duration),dateAndTime]

        temp_df = pd.DataFrame(columns=["Topic","Word_Count","Minutes","WPH","DateTime"])
        temp_df.loc[0] = [topic,length,duration,length*60/float(duration),dateAndTime]
        print(temp_df)

        df.loc[len(df.index)] = newRow
        df.to_csv("WordPerHour.csv",index=False)
        df.to_json("WordsPerHour.json", indent=4,index=False,orient='records')

        with open("Draft.md", "a") as file:
            file.write("\n"+content)
        root.destroy()  # Close the Tkinter windowpp
        input("Please press enter to show the plot")

        df.set_index(df["DateTime"])

        # Plotting with Seaborn
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=df['WPH'], marker='o', linestyle='-')
        plt.title('WPH')
        plt.xlabel('DateTime')
        plt.ylabel('Words Per Hour')
        plt.subplots_adjust(bottom=0.307,top=0.921,left=0.048,right=0.97)
        plt.grid(True)
        plt.xticks(ticks=range(len(df)), labels=df["DateTime"].values, rotation = 70)
        

        for index, value, minutes in zip(df.index, df['WPH'],df['Minutes']):
            plt.text(index,value, f"({minutes})", ha='right', va='bottom')

        # Save the plot to a file
        plt.savefig(f'WPH.png')

        plt.show()


    def close_after_time():
        iterate = save_and_close()
        root.after_cancel(close_timer)
        if iterate == "yes":
            writingGame()


    root = tk.Tk()
    root.overrideredirect(True)

    text_area_style = {
        "font": ("Courier", 12),  # Monospaced font for console-like appearance
        "bg": "black",            # Black background
        "fg": "white",            # White text color
        "insertbackground": "white",  # Color of the cursor
        "borderwidth": 0          # No border
    }

    text_area = tk.Text(root, wrap="word",**text_area_style)
    text_area.pack(fill="both",expand=True)

    text_area.focus_force()

    # Schedule close_after_time to be called after 10 seconds (10000 milliseconds)
    close_timer = root.after(time, close_after_time)

    root.state('zoomed')
    root.mainloop()

def editingGame():
    file_path = "Draft.md"
    os.system('cls')
    duration = float(input("How many minutes do you want to edit the file? "))
    time = int(duration * 1000 * 60) # Convert minutes to milliseconds

    def save_and_close():

        edited = text_area.get("1.0", "end-1c")

        with open(file_path, "r") as file: 
            original = file.read()

        originalAr = original.split(" ")
        editedAr = edited.split(" ")
        n = 0
        i = len(originalAr) -1
        for word in editedAr[::-1]:
            if word == originalAr[i]:
                n = n+1
                i = i-1
            else:
                break

        edited_words = len(originalAr) - n
        os.system('cls')
        print("Your edited words are", edited_words)
        print("Your editing speed is", edited_words*60/duration,"words per hour")
        
        
        with open(file_path, "w") as file:
            file.write(edited)

        root.destroy()
        input("Press enter to continue")
        

    def close_after_time():
        save_and_close()
        root.after_cancel(close_timer)

    root = tk.Tk()
    root.overrideredirect(True)

    text_area_style = {
        "font": ("Courier", 12),
        "bg": "black",
        "fg": "white",
        "insertbackground": "white",
        "borderwidth": 0
    }

    text_area = tk.Text(root, wrap="word", **text_area_style)
    text_area.pack(fill="both", expand=True)

    with open(file_path, "r") as file:
        text_area.insert("1.0", file.read())

    text_area.focus_force()

    close_timer = root.after(time, close_after_time)

    root.state('zoomed')
    root.mainloop()

# Add the editingSprint function to the main menu
def startGame():
    os.system('cls')
    choice = input("What do you want to do?\n1. writingGame\n2. editingGame\n3. Exit\n")

    if choice == "1":
        writingGame()
    elif choice == "2":
        editingGame()
    else:
        exit()
    os.system('cls')
    iterate = input("Do you want to play again?")
    if iterate == "yes": 
        startGame()

startGame()
