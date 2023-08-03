import tkinter as tk
import launch
import analysisPositions as an
from tkinter import filedialog
import os
import datetime as dt
import lnmkt as ln
import yaml
import Signal_TradingView as si
import pandas as pd
import json


current_directory = os.getcwd()
current_dir = os.path.join(current_directory,)
output_dir = os.path.join(current_directory,'output')

config = 'config.yml'
signal_current = 'signal_current.json'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)
file_path_config = os.path.join(current_dir, config)
file_path_signal = os.path.join(output_dir, signal_current)

with open("config.yml", "r") as yaml_file:
    config_data = yaml.safe_load(yaml_file)

total_duration = config_data['total_duration']
time_interval = config_data['time_interval']
interval_main = config_data['interval_main']
interval_list = config_data['interval_list']


is_running = False

def toggle_status():
    global is_running
    if is_running:
        is_running = False
        start_button.grid()  # Show the "Start Program" button
        stop_button.grid_remove()  # Hide the "Stop Program" button
        stop_program()
        
    else:
        is_running = True
        start_button.grid_remove()  # Hide the "Start Program" button
        stop_button.grid()  # Show the "Stop Program" button
        start_program()
        show_price()
        #si.get_all_signal(interval_list)
        show_signal()



def start_program():
    #is_running.set(True)
    status_label.config(text="Running", fg="green")
    start_time = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    start_str = start_time + " - Let's gooooooo!\n"
    log_text_main.insert(tk.END, start_str)  # Insert DataFrame string into Text widget
    #si.get_all_signal(interval_list)
    an.get_trades_running()


def show_price():
    log_text_main.insert(tk.END, ln.get_price_LNMarket() + "\n")  # Insert DataFrame string into Text widget
    log_text_main.insert(tk.END, ln.get_price_Binance() + "\n")  # Insert DataFrame string into Text widget

def show_signal():
    si.get_all_signal(interval_list)
    #def show_dataframe_in_text_widget(df, text_widget):
    # Convert the DataFrame to a string
    with open(file_path_signal, 'r') as json_file:
        data = pd.read_json(json_file)
        data_col = data[["Timestamp", "1m","5m","15m","30m","1h","2h","1W","1M"]]
        #return data_col
    
    data_str = data_col.to_string(index=False)
    log_text_main.insert(tk.END, data_str)




def stop_program():
    #is_running.set(False)
    status_label.config(text="Not Running", fg="red")
    log_text_main.delete('1.0', tk.END)
    #toggle_button.config(text="Show trades")
    #log_text.insert(tk.END, "Program Stopped\n")

def show_dataframe():
    df_trades = an.print_trades_running()
    df_string = df_trades.to_string(index=False)  # Convert DataFrame to string
    
    log_text_main.insert(tk.END, df_string)  # Insert DataFrame string into Text widget

def open_config_file():
    #file_path = filedialog.askopenfilename(filetypes=[("YAML Files", "*.yml")])
    file_path = file_path_config
    if file_path:
        with open(file_path, 'r') as file:
            config_data = file.read()
            # Display the content of the config file in the log_text widget
            #log_text_config.delete(1.0, tk.END)
            #log_text_config.insert(tk.END, config_data)
            show_config_window(config_data)
    
    #log_text_config = tk.Text(root, wrap=tk.WORD, width=50, height=10)
    #log_text_config.pack()

def show_config_window(config_data):
    # Create a new window to display the config file contents
    config_window = tk.Toplevel(root)
    config_window.title("Config File")

    # Create a Text widget to display the config data
    config_text = tk.Text(config_window, wrap="word", width=80, height=20)
    config_text.grid(row=0, column=0, padx=10, pady=10)
    config_text.insert(tk.END, config_data)

    # Create the "Save" button to save changes made in the new window
    def save_config_and_close():
        file_path = file_path_config #filedialog.asksaveasfilename(filetypes=[("YAML Files", "*.yml")])
        if file_path:
            with open(file_path, 'w') as file:
                # Get the content from the config_text widget and save it to the file
                config_data = config_text.get(1.0, tk.END)
                file.write(config_data)
            # Close the window after saving
            config_window.destroy()

    # Save button
    save_button = tk.Button(config_window, text="Save", command=save_config_and_close)
    save_button.grid(row=1, column=0, padx=10, pady=10)
    
    # Cancel button
    cancel_button = tk.Button(config_window, text="Cancel", fg="red",command=config_window.destroy)
    cancel_button.grid(row=2, column=0, padx=10, pady=10)


#def on_close():
#    root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Program Status and Log")

    # Add the big green button to start the program
    start_button = tk.Button(root, text="Start Program", bg="green", fg="white", font=("Helvetica", 16), command=toggle_status)
    #start_button.pack(pady=20)
    start_button.grid(row=0, column=0, padx=20, pady=20)

    # Add the medium stylish red X button to stop the program
    stop_button = tk.Button(root, text="STOP", bg="red", fg="white", font=("Helvetica", 18, "bold"), width=5, height=2, command=toggle_status)
    #stop_button.pack()
    stop_button.grid(row=0, column=0, padx=20, pady=20)

    status_label = tk.Label(root, text="Not Running", fg="red")
    status_label.grid(row=1, column=0, padx=20, pady=20)

    log_text_main = tk.Text(root, wrap=tk.WORD, width=50, height=10)
    log_text_main.grid(row=2, column=0, padx=20, pady=20)

    open_config_button = tk.Button(root, text="Open Config", command=open_config_file)
    #open_config_button.pack()
    open_config_button.grid(row=3, column=0, columnspan=2, padx=20, pady=20)  # Place the button in row 0 and spans 2 columns

# Set initial button states based on the value of is_running
    if is_running:
        start_button.grid_remove()
    else:
        stop_button.grid_remove()



    #save_config_button = tk.Button(root, text="Save Config", command=save_config_file)
    #save_config_button.pack()

    #root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()
