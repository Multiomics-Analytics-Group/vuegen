"""GUI for vuegen command-line tool.

usage: VueGen [-h] [-c CONFIG] [-dir DIRECTORY] [-rt REPORT_TYPE]
              [-st_autorun]

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Path to the YAML configuration file.
  -dir DIRECTORY, --directory DIRECTORY
                        Path to the directory from which the YAML
                        config will be inferred.
  -rt REPORT_TYPE, --report_type REPORT_TYPE
                        Type of the report to generate (streamlit,
                        html, pdf, docx, odt, revealjs, pptx, or
                        jupyter).
  -st_autorun, --streamlit_autorun
                        Automatically run the Streamlit app after
                        report generation.
"""

import sys
import tkinter as tk

import customtkinter

from vuegen.__main__ import main
from vuegen.report import ReportType

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("dark-blue")


# callbacks
def create_run_vuegen(is_dir, config_path, report_type, run_streamlit):
    def inner():
        args = ["vuegen"]
        if is_dir:
            args.append("--directory")
        else:
            args.append("--config")
        args.append(config_path.get())
        args.append("--report_type")
        args.append(report_type.get())
        if run_streamlit:
            args.append("--streamlit_autorun")
        print("args:", args)
        sys.argv = args
        main()  # Call the main function from vuegen

    return inner


def optionmenu_callback(choice):
    """Good for logging changes?"""
    print("optionmenu dropdown clicked:", choice)


def radiobutton_event(value):
    def radio_button_callback():
        print("radiobutton toggled, current value:", value.get())

    return radio_button_callback


# Options

# get list of report types from Enum
report_types = [report_type.value.lower() for report_type in ReportType]


# APP
app = customtkinter.CTk()
app.geometry("460x400")
app.title("VueGen GUI")

##########################################################################################
# Config or directory input
ctk_label_config = customtkinter.CTkLabel(
    app,
    text="Add path to config file or directory. Select radio button accordingly",
)
ctk_label_config.grid(row=0, column=0, columnspan=2, padx=20, pady=20)
is_dir = tk.IntVar(value=1)
callback_radio_config = radiobutton_event(is_dir)
ctk_radio_config_0 = customtkinter.CTkRadioButton(
    app,
    text="Use config",
    command=callback_radio_config,
    variable=is_dir,
    value=0,
)
ctk_radio_config_0.grid(row=1, column=0, padx=20, pady=2)
ctk_radio_config_1 = customtkinter.CTkRadioButton(
    app,
    text="Use dir",
    command=callback_radio_config,
    variable=is_dir,
    value=1,
)
ctk_radio_config_1.grid(row=1, column=1, padx=20, pady=2)

config_path = tk.StringVar()
config_path_entry = customtkinter.CTkEntry(
    app,
    width=400,
    textvariable=config_path,
)
config_path_entry.grid(row=2, column=0, columnspan=2, padx=20, pady=10)

##########################################################################################
# Report type dropdown
ctk_label_report = customtkinter.CTkLabel(
    app,
    text="Select type of report to generate (use streamlit for now)",
)
ctk_label_report.grid(row=3, column=0, columnspan=2, padx=20, pady=20)
report_type = tk.StringVar(value=report_types[0])
report_dropdown = customtkinter.CTkOptionMenu(
    app,
    values=report_types,
    variable=report_type,
    command=optionmenu_callback,
)
report_dropdown.grid(row=4, column=0, columnspan=2, padx=20, pady=20)

_report_type = report_dropdown.get()
print("report_type value:", _report_type)

##########################################################################################
# Run Streamlit radio button
run_streamlit = tk.IntVar(value=0)
callback_radio_st_run = radiobutton_event(run_streamlit)
ctk_radio_st_autorun_1 = customtkinter.CTkRadioButton(
    app,
    text="autorun streamlit",
    value=1,
    variable=run_streamlit,
    command=callback_radio_st_run,
)
ctk_radio_st_autorun_1.grid(row=5, column=0, padx=20, pady=20)
ctk_radio_st_autorun_0 = customtkinter.CTkRadioButton(
    app,
    text="skip starting streamlit",
    value=0,
    variable=run_streamlit,
    command=callback_radio_st_run,
)
ctk_radio_st_autorun_0.grid(row=5, column=1, padx=20, pady=20)

##########################################################################################
# Run VueGen button
run_vuegen = create_run_vuegen(is_dir, config_path, report_type, run_streamlit)
run_button = customtkinter.CTkButton(
    app,
    text="Run VueGen",
    command=run_vuegen,
)
run_button.grid(row=6, column=0, columnspan=2, padx=20, pady=20)

##########################################################################################
# Run the app in the mainloop
app.mainloop()
