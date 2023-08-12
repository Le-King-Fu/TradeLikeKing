import analysisPositions as an
import Signal_TradingView as si
import tradePosition as tr
import lnmkt as ln

import tkinter as tk
import os
import datetime as dt
import yaml
import pandas as pd
import time



current_directory = os.getcwd()
current_dir = os.path.join(current_directory,)
output_dir = os.path.join(current_directory,'output_data')

config = 'config.yml'
signal_current = 'signal_current.json'
trade_summary = 'trade_summary.json'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)
file_path_config = os.path.join(current_dir, config)
file_path_signal = os.path.join(output_dir, signal_current)
file_path_trades = os.path.join(output_dir, signal_current)

with open("config.yml", "r") as yaml_file:
    config_data = yaml.safe_load(yaml_file)

total_duration = config_data['total_duration']
time_interval = config_data['time_interval']
interval_main = config_data['interval_main']
interval_list = config_data['interval_list']
#start_time = time.time()

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

        #signal.get_historic_signal()

def start_program(counter=0):

    if not is_running:
        return  # Stop the loop if is_running is set to False
    if counter <= total_duration:  # Stop after 24 hours (86,400 seconds)    
    #while time.time() - start_time < total_duration:
        #is_running.set(True)
        status_label.config(text="Running", fg="green")
        #log_text_main.delete('1.0', tk.END)
        start_time = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        start_str = start_time + " - Let's gooooooo!\n"
        log_text_main.see(tk.END)
        log_text_main.insert(tk.END,"\n" + start_str)  # Insert DataFrame string into Text widget
        show_price()
        log_text_main.update_idletasks()
        log_text_main.see(tk.END)
        show_signal()
        count_sh = str(si.get_short_seq())
        count_lg = str(si.get_long_seq())
        log_text_main.update_idletasks()
        log_text_main.see(tk.END)
        show_consecutive_signal(count_lg, count_sh)
        tr.open_futures_long_aggro(count_lg)
        tr.open_futures_short_aggro(count_sh)
        ln.get_info()
        if ln.get_nb_trx() == 0:
            print("No transaction")
            print()
        else: 
            show_trades()
            log_text_main.update_idletasks()
            log_text_main.see(tk.END)
            show_margin()
            tr.add_margin()
            log_text_main.update_idletasks()
            log_text_main.see(tk.END)
            show_closing_id()
            log_text_main.update_idletasks()
            log_text_main.see(tk.END)
            tr.close_futures_short_aggro()
            tr.close_futures_long_aggro()
            an.get_trades_closed()
            an.get_closing_msg_long()
            an.get_closing_msg_long()
            log_text_main.update_idletasks()
            log_text_main.see(tk.END)
            #if show_closing_msg is not None:
                #show_closing_msg()

        #si.get_all_signal(interval_list)
        #an.get_trades_running()
        #show_trades()
        #time.sleep(time_interval)
        end_time = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')   
        end_str = end_time + " - Iteration done!\n"
        log_text_main.see(tk.END)
        log_text_main.insert(tk.END,"\n" + end_str)  # Insert DataFrame string into Text widget
        log_text_main.update_idletasks()
        repeat_id = root.after(time_interval*1000, start_program, counter + time_interval)

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
    log_text_main.insert(tk.END,"\nSIGNAUX \n" + data_str)

def show_trades():
    an.get_trades_running()
    data_col = an.print_trades_running()
    data_str = data_col.to_string(index=False)
    log_text_main.insert(tk.END,"\n \nTRADES SUMMARY \n" + data_str)

def show_margin():
    data = str(an.get_list_margin())
    #data_col = an.print_trades_running()
    #data_str = data_col.to_string(index=False)
    log_text_main.insert(tk.END,"\n \nMargin call : " + data)

def show_closing_id():
    close_long = str(an.get_list_close_long_aggro())
    close_short = str(an.get_list_close_short_aggro())
    log_text_main.insert(tk.END,"\n \nClosing time ! \n Long : " + close_long + "\n Short : " + close_short)

def show_closing_msg():
    msg_long = str(an.get_closing_msg_long())
    msg_short = str(an.get_closing_msg_short())
    if msg_long is not None:
        log_text_main.insert(tk.END,"\n \n " + msg_long)
        return msg_long
    elif msg_short is not None:
        log_text_main.insert(tk.END,"\n \n " + msg_short)
        return msg_short
    else:
        log_text_main.insert(tk.END,"\n \nNo closing this time...")

def show_consecutive_signal(count_lg, count_sh):
    #count_sh = str(si.get_short_seq())
    #count_lg = str(si.get_long_seq())
    log_text_main.insert(tk.END,"\n \nConsecutive STRONG SELL : " + count_sh + "\nConsecutive STRONG BUY : " + count_lg)

def stop_program():
    #is_running.set(False)
    status_label.config(text="Not Running", fg="red")
    log_text_main.delete('1.0', tk.END)
    #toggle_button.config(text="Show trades")
    #log_text.insert(tk.END, "Program Stopped\n")
    #cancel_program()
    

#def cancel_program():
#    root.after_cancel(repeat_id)  # Cancel the scheduled loop

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
    config_text = tk.Text(config_window, wrap="word", width=80, height=25)
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

def open_dashboard():
    dashboard_window = tk.Toplevel(root)
    dashboard_window.title("Dashboard")

    results = an.get_fees()
    nb_trx =  results['nb_trx_closed']
    total_fee = "{:.2f}".format(results["total_fee"])
    total_average_fee = "{:.2f}".format(results["total_average_fee"])
    total_max_fee = "{:.2f}".format(results["total_max_fee"])
    total_min_fee = "{:.2f}".format(results["total_min_fee"])
    total_opening_fee = "{:.2f}".format(results["total_opening_fee"])
    average_opening_fee = "{:.2f}".format(results["average_opening_fee"])
    max_opening_fee = "{:.2f}".format(results["max_opening_fee"])
    min_opening_fee = "{:.2f}".format(results["min_opening_fee"])
    total_closing_fee = "{:.2f}".format(results["total_closing_fee"])
    average_closing_fee = "{:.2f}".format(results["average_closing_fee"])
    max_closing_fee = "{:.2f}".format(results["max_closing_fee"])
    min_closing_fee = "{:.2f}".format(results["min_closing_fee"])
    total_carry_fee = "{:.2f}".format(results["total_carry_fee"])
    average_carry_fee = "{:.2f}".format(results["average_carry_fee"])
    max_carry_fee = "{:.2f}".format(results["max_carry_fee"])
    min_carry_fee = "{:.2f}".format(results["min_carry_fee"])

    """
        #num_day_trades = len(df_trades)
    results = {
    'total_opening_fee': total_opening_fee,
    'total_closing_fee': total_closing_fee,
    'total_carry_fee': total_carry_fee,
    "total_fee" : total_fee,
    'average_opening_fee': average_opening_fee,
    'average_closing_fee': average_closing_fee,
    'average_carry_fee': average_carry_fee,
    'max_opening_fee': max_opening_fee,
    'max_closing_fee': max_closing_fee,
    'max_carry_fee': max_carry_fee,
    'min_opening_fee': min_opening_fee,
    'min_closing_fee': min_closing_fee,
    'min_carry_fee': min_carry_fee,
    }
    """

    total_fee_label = tk.Label(dashboard_window, text=f'Total fees: {total_fee} sats')
    total_fee_label.grid(row=0, column=0, padx=10, pady=10)  # Place the button in row 0 and spans 2 columns

    total_trx_label = tk.Label(dashboard_window, text=f'Nbr de trx: {nb_trx} transactions')
    total_trx_label.grid(row=0, column=2, padx=10, pady=10)  # Place the button in row 0 and spans 2 columns   

    title_label = tk.Label(dashboard_window, text="Summary")
    title_label.grid(row=1, column=0, padx=10, pady=10)  # Place the button in row 0 and spans 2 columns   

    title_1_label = tk.Label(dashboard_window, text="Average")
    title_1_label.grid(row=1, column=2, padx=10, pady=10)  # Place the button in row 0 and spans 2 columns

    title_2_label = tk.Label(dashboard_window, text="Max")
    title_2_label.grid(row=1, column=3, padx=10, pady=10)  # Place the button in row 0 and spans 2 columns

    title_3_label = tk.Label(dashboard_window, text="Min")
    title_3_label.grid(row=1, column=4, padx=10, pady=10)  # Place the button in row 0 and spans 2 columns

    title_4_label = tk.Label(dashboard_window, text="Total")
    title_4_label.grid(row=1, column=5, padx=10, pady=10)  # Place the button in row 0 and spans 2 columns

    line_1_label = tk.Label(dashboard_window, text="Total fees")
    line_1_label.grid(row=2, column=0, padx=10, pady=10)  # Place the button in row 0 and spans 2 columns  

    average_fee_label = tk.Label(dashboard_window, text=total_average_fee)
    average_fee_label.grid(row=2, column=2, padx=10, pady=10)  # Place the button in row 0 and spans 2 columns  

    max_fee_label = tk.Label(dashboard_window, text=total_max_fee)
    max_fee_label.grid(row=2, column=3, padx=10, pady=10)  # Place the button in row 0 and spans 2 columns  

    min_fee_label = tk.Label(dashboard_window, text=total_min_fee)
    min_fee_label.grid(row=2, column=4, padx=10, pady=10)  # Place the button in row 0 and spans 2 columns

    total_fee_label2 = tk.Label(dashboard_window, text=total_fee)
    total_fee_label2.grid(row=2, column=5, padx=10, pady=10)  # Place the button in row 0 and spans 2 columns     

    line_2_label = tk.Label(dashboard_window, text="Opening fees")
    line_2_label.grid(row=3, column=0, padx=10, pady=10)  # Place the button in row 0 and spans 2 columns  

    average_fee_label = tk.Label(dashboard_window, text=average_opening_fee)
    average_fee_label.grid(row=3, column=2, padx=10, pady=10)  # Place the button in row 0 and spans 2 columns  

    max_fee_label = tk.Label(dashboard_window, text=max_opening_fee)
    max_fee_label.grid(row=3, column=3, padx=10, pady=10)  # Place the button in row 0 and spans 2 columns  

    min_fee_label = tk.Label(dashboard_window, text=min_opening_fee)
    min_fee_label.grid(row=3, column=4, padx=10, pady=10)  # Place the button in row 0 and spans 2 columns

    total_fee_label2 = tk.Label(dashboard_window, text=total_opening_fee)
    total_fee_label2.grid(row=3, column=5, padx=10, pady=10)  # Place the button in row 0 and spans 2 columns

    line_3_label = tk.Label(dashboard_window, text="Closing fees")
    line_3_label.grid(row=4, column=0, padx=10, pady=10)  # Place the button in row 0 and spans 2 columns  

    average_fee_label = tk.Label(dashboard_window, text=average_closing_fee)
    average_fee_label.grid(row=4, column=2, padx=10, pady=10)  # Place the button in row 0 and spans 2 columns  

    max_fee_label = tk.Label(dashboard_window, text=max_closing_fee)
    max_fee_label.grid(row=4, column=3, padx=10, pady=10)  # Place the button in row 0 and spans 2 columns  

    min_fee_label = tk.Label(dashboard_window, text=min_closing_fee)
    min_fee_label.grid(row=4, column=4, padx=10, pady=10)  # Place the button in row 0 and spans 2 columns

    total_fee_label2 = tk.Label(dashboard_window, text=total_closing_fee)
    total_fee_label2.grid(row=4, column=5, padx=10, pady=10)  # Place the button in row 0 and spans 2 columns

    line_3_label = tk.Label(dashboard_window, text="Carry fees")
    line_3_label.grid(row=5, column=0, padx=10, pady=10)  # Place the button in row 0 and spans 2 columns  

    average_fee_label = tk.Label(dashboard_window, text=average_carry_fee)
    average_fee_label.grid(row=5, column=2, padx=10, pady=10)  # Place the button in row 0 and spans 2 columns  

    max_fee_label = tk.Label(dashboard_window, text=max_carry_fee)
    max_fee_label.grid(row=5, column=3, padx=10, pady=10)  # Place the button in row 0 and spans 2 columns  

    min_fee_label = tk.Label(dashboard_window, text=min_carry_fee)
    min_fee_label.grid(row=5, column=4, padx=10, pady=10)  # Place the button in row 0 and spans 2 columns

    total_fee_label2 = tk.Label(dashboard_window, text=total_carry_fee)
    total_fee_label2.grid(row=5, column=5, padx=10, pady=10)  # Place the button in row 0 and spans 2 columns          

    refresh_button = tk.Button(dashboard_window, text="Refresh", command=an.get_trades_closed)
    refresh_button.grid(row=6, column=0, padx=10, pady=10)  # Place the button in row 0 and spans 2 columns    


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Program Status and Log")
    bitcoin_orange = "#F7931A"
    main_bg_color = "white"
    #repeat_id = 0
    def set_background_color(widget, color):
        widget.configure(bg=color)

    # Set the main background color of the root window
    set_background_color(root, bitcoin_orange)
    # Add the big green button to start the program
    start_button = tk.Button(root, text="Start Program", bg="green", fg="white", font=("Helvetica", 16, "bold"), command=toggle_status)
    #start_button.pack(pady=20)
    start_button.grid(row=0, column=0, padx=20, pady=20)

    # Add the medium stylish red X button to stop the program
    stop_button = tk.Button(root, text="STOP", bg="red", fg="white", font=("Helvetica", 16), command=toggle_status)
    #stop_button.pack()
    stop_button.grid(row=0, column=0, padx=20, pady=20)

    status_label = tk.Label(root, text="Not Running", fg="red", bg="black",font=("Helvetica", 16))
    status_label.grid(row=0, column=1, padx=20, pady=20)

    log_text_main = tk.Text(root, wrap=tk.WORD, width=200, height=40, bg="black", fg="white")
    log_text_main.grid(row=2, column=0, padx=20, pady=20,columnspan=2)

    open_config_button = tk.Button(root, text="Open Config", command=open_config_file)
    #open_config_button.pack()
    open_config_button.grid(row=3, column=0, padx=20, pady=20)  # Place the button in row 0 and spans 2 columns

    dashboard_button = tk.Button(root, text="Dashboard", command=open_dashboard)
    dashboard_button.grid(row=3, column=1, padx=20, pady=20)  # Place the button in row 0 and spans 2 columns

# Set initial button states based on the value of is_running
    if is_running:
        start_button.grid_remove()
    else:
        stop_button.grid_remove()



    #save_config_button = tk.Button(root, text="Save Config", command=save_config_file)
    #save_config_button.pack()

    #root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()
