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
from pathlib import Path

import customtkinter

from vuegen.__main__ import main
from vuegen.report import ReportType

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("dark-blue")

app_path = Path(__file__).absolute()
print("app_path:", app_path)

##########################################################################################
# Path to example data dependend on how the GUI is run
if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    # PyInstaller bundeled case
    path_to_dat = (
        app_path.parent / "example_data/Basic_example_vuegen_demo_notebook"
    ).resolve()
elif app_path.parent.name == "gui":
    # should be always the case for GUI run from command line
    path_to_dat = (
        app_path.parent
        / ".."
        / "docs"
        / "example_data"
        / "Basic_example_vuegen_demo_notebook"
    ).resolve()
else:
    path_to_dat = "docs/example_data/Basic_example_vuegen_demo_notebook"


##########################################################################################
# callbacks
def create_run_vuegen(is_dir, config_path, report_type, run_streamlit):
    def inner():
        args = ["vuegen"]
        if is_dir.get():
            args.append("--directory")
        else:
            args.append("--config")
        args.append(config_path.get())
        args.append("--report_type")
        args.append(report_type.get())
        if run_streamlit.get():
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


##########################################################################################
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

config_path = tk.StringVar(value=str(path_to_dat))
config_path_entry = customtkinter.CTkEntry(
    app,
    width=400,
    textvariable=config_path,
)
config_path_entry.grid(row=2, column=0, columnspan=2, padx=20, pady=10)

##########################################################################################
# Report type dropdown
# - get list of report types from Enum
report_types = [report_type.value.lower() for report_type in ReportType]
ctk_label_report = customtkinter.CTkLabel(
    app,
    text="Select type of report to generate (using only streamlit for now)",
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
run_streamlit = tk.IntVar(value=1)
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
