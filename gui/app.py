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

import os
import shutil
import sys
import tkinter as tk
import traceback
from pathlib import Path
from pprint import pprint
from tkinter import filedialog, messagebox

import customtkinter
import yaml
from PIL import Image

from vuegen import report_generator

# from vuegen.__main__ import main
from vuegen.report import ReportType
from vuegen.utils import get_completion_message, get_logger

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("dark-blue")

app_path = Path(__file__).absolute().resolve()
print("app_path:", app_path)
output_dir = (Path.home() / "vuegen_gen" / "reports").resolve()
print("output_dir:", output_dir)
output_dir.mkdir(exist_ok=True, parents=True)
_PATH = f'{os.environ["PATH"]}'
### config path for app
config_file = Path(Path.home() / ".vuegen_gui" / "config.yaml").resolve()
if not config_file.exists():
    config_file.parent.mkdir(exist_ok=True, parents=True)
    config_app = dict(python_dir_entry="")
else:
    with open(config_file, "r", encoding="utf-8") as f:
        config_app = yaml.safe_load(f)
hash_config_app = hash(yaml.dump(config_app))
##########################################################################################
# Path to example data dependend on how the GUI is run
if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    # PyInstaller bundeled case
    path_to_data_in_bundle = (
        app_path.parent / "example_data/Basic_example_vuegen_demo_notebook"
    ).resolve()
    quarto_bin_path = os.path.join(sys._MEIPASS, "quarto_cli", "bin")
    # /.venv/lib/python3.12/site-packages/quarto_cli/bin
    # source activate .venv/bin/activate
    quarto_share_path = os.path.join(sys._MEIPASS, "quarto_cli", "share")
    os.environ["PATH"] = os.pathsep.join([quarto_bin_path, quarto_share_path, _PATH])
    # This requires that the python version is the same as the one used to create the executable
    # in the Python environment the kernel is started from for quarto based reports
    # os.environ["PYTHONPATH"] = os.pathsep.join(
    #     sys.path
    # )  # ! requires kernel env with same Python env, but does not really seem to help
    os.environ["PYTHONPATH"] = sys._MEIPASS
    # ([[sys.path[0], sys._MEIPASS])  # does not work when built on GitHub Actions
    path_to_example_data = (
        output_dir.parent / "example_data" / "Basic_example_vuegen_demo_notebook"
    ).resolve()
    # copy example data to vuegen_gen folder in home directory
    if not path_to_example_data.exists():
        shutil.copytree(
            path_to_data_in_bundle,
            path_to_example_data,
            # dirs_exist_ok=True,
        )
        messagebox.showinfo(
            "Info",
            f"Example data copied to {path_to_example_data}",
        )
    logo_path = os.path.join(sys._MEIPASS, "vuegen_logo.png")
elif app_path.parent.name == "gui":
    # should be always the case for GUI run from command line
    path_to_example_data = (
        app_path.parent.parent
        / "docs"
        / "example_data"
        / "Basic_example_vuegen_demo_notebook"
    ).resolve()
    logo_path = (
        app_path.parent.parent / "docs" / "images" / "vuegen_logo.png"
    )  # 1000x852 pixels
else:
    path_to_example_data = "docs/example_data/Basic_example_vuegen_demo_notebook"

print(f"{_PATH = }")
##########################################################################################
# callbacks


def create_run_vuegen(
    is_dir,
    config_path,
    report_type,
    run_streamlit,
    output_dir_entry,
    python_dir_entry,
    max_depth: int,
):
    def inner():
        kwargs = {}
        print(f"{is_dir.get() = }")
        if is_dir.get():
            kwargs["dir_path"] = config_path.get()
            report_name = Path(config_path.get()).stem
        else:
            kwargs["config_path"] = config_path.get()
            report_name = Path(config_path.get()).stem
        kwargs["report_type"] = report_type.get()
        print(f"{run_streamlit.get() = }")
        kwargs["streamlit_autorun"] = run_streamlit.get()
        kwargs["output_dir"] = output_dir_entry.get()
        if max_depth.get():
            kwargs["max_depth"] = int(max_depth.get())
        print("kwargs:")
        pprint(kwargs)

        if python_dir_entry.get():
            if python_dir_entry.get() != config_app["python_dir_entry"]:
                config_app["python_dir_entry"] = python_dir_entry.get()
            if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
                os.environ["PATH"] = os.pathsep.join(
                    [
                        quarto_bin_path,
                        quarto_share_path,
                        str(
                            Path(python_dir_entry.get())
                        ),  # ! check if this return WindowsPaths on Windows
                        _PATH,
                    ]
                )
            else:
                messagebox.showwarning(
                    "warning", "Running locally. Ignoring set Python Path"
                )
        if kwargs["max_depth"] < 2:
            messagebox.showwarning(
                "warning", "Maximum depth must be at least 2. Setting to 2."
            )
            kwargs["max_depth"] = 2
        elif kwargs["max_depth"] > 9:
            messagebox.showwarning(
                "warning", "Maximum depth must be at most 9. Setting to 9."
            )
            kwargs["max_depth"] = 9
        try:
            os.chdir(kwargs["output_dir"])  # Change the working directory
            # Define logger suffix based on report type and name
            logger_suffix = f"{report_type.get()}_report_{str(report_name)}"

            # Initialize logger
            kwargs["logger"], log_file = get_logger(
                f"{logger_suffix}",
                folder=(Path(kwargs["output_dir"]) / "logs").as_posix(),
            )
            kwargs["logger"].info("logfile: %s", log_file)
            kwargs["logger"].debug("sys.path: %s", sys.path)
            kwargs["logger"].debug("PATH (in app): %s ", os.environ["PATH"])
            kwargs["quarto_checks"] = True  # for gui check local quarto installation
            report_dir, gen_config_path = report_generator.get_report(**kwargs)
            kwargs["logger"].info("Report generated at %s", report_dir)
            messagebox.showinfo(
                "Success",
                "Report generation completed successfully."
                f"\n\nLogs at:\n{log_file}"
                f"\n\nReport in folder:\n{report_dir}"
                f"\n\nConfiguration file at:\n{gen_config_path}",
            )
            global hash_config_app  # ! fix this
            get_completion_message(report_type.get(), config_path=gen_config_path)
            if hash(yaml.dump(config_app)) != hash_config_app:
                with open(config_file, "w", encoding="utf-8") as f:
                    yaml.dump(config_app, f)
                hash_config_app = hash(yaml.dump(config_app))
        except Exception as e:
            stacktrace = traceback.format_exc()
            messagebox.showerror(
                "Error",
                f"An error occurred: {e}\n\n{stacktrace}"
                f"\n See logs for more details {log_file}",
            )

    return inner


def optionmenu_callback(choice):
    """Good for logging changes?"""
    print("optionmenu dropdown clicked:", choice)


def create_radio_button_callback(value, name="radiobutton"):
    def radio_button_callback():
        print(f"{name} toggled, current value:", value.get())

    return radio_button_callback


def create_select_directory(string_var):
    def select_directory():
        inital_dir = string_var.get()
        if not inital_dir:
            inital_dir = Path.home()
        directory = filedialog.askdirectory(initialdir=inital_dir)
        if directory:
            string_var.set(directory)

    return select_directory


##########################################################################################
# APP
app = customtkinter.CTk()
app.geometry("620x840")
app.title("VueGen GUI")
row_count = 0
##########################################################################################
# Logo
_factor = 4
logo_image = customtkinter.CTkImage(
    Image.open(logo_path), size=(int(1000 / _factor), int(852 / _factor))
)
logo_label = customtkinter.CTkLabel(app, image=logo_image, text="")
logo_label.grid(row=0, column=0, columnspan=2, padx=10, pady=5)
row_count += 1
##########################################################################################
# Config or directory input
ctk_label_config = customtkinter.CTkLabel(
    app,
    text="Add path to config file or directory. Select radio button accordingly",
)
ctk_label_config.grid(row=row_count, column=0, columnspan=2, padx=20, pady=20)
is_dir = tk.BooleanVar(value=True)
callback_radio_config = create_radio_button_callback(is_dir, name="is_dir")
ctk_radio_config_0 = customtkinter.CTkRadioButton(
    app,
    text="Use config",
    command=callback_radio_config,
    variable=is_dir,
    value=False,
)
row_count += 1
##########################################################################################
ctk_radio_config_0.grid(row=row_count, column=0, padx=20, pady=2)
ctk_radio_config_1 = customtkinter.CTkRadioButton(
    app,
    text="Use dir",
    command=callback_radio_config,
    variable=is_dir,
    value=True,
)
ctk_radio_config_1.grid(row=row_count, column=1, padx=20, pady=2)

config_path = tk.StringVar(value=str(path_to_example_data))
config_path_entry = customtkinter.CTkEntry(
    app,
    width=400,
    textvariable=config_path,
)
row_count += 1
##########################################################################################
config_path_entry.grid(row=row_count, column=0, columnspan=2, padx=5, pady=10)
select_directory = create_select_directory(config_path)
select_button = customtkinter.CTkButton(
    app, text="Select Directory", command=select_directory
)
select_button.grid(row=row_count, column=2, columnspan=2, padx=5, pady=10)
row_count += 1
##########################################################################################
# Report type dropdown
# - get list of report types from Enum
report_types = [report_type.value.lower() for report_type in ReportType]
# report_types = report_types[:2]  # only streamlit and html for now
ctk_label_report = customtkinter.CTkLabel(
    app,
    text="Select type of report to generate (using only streamlit for now)",
)
ctk_label_report.grid(row=row_count, column=0, columnspan=2, padx=20, pady=20)
row_count += 1
##########################################################################################
report_type = tk.StringVar(value=report_types[1])
report_dropdown = customtkinter.CTkOptionMenu(
    app,
    values=report_types,
    variable=report_type,
    command=optionmenu_callback,
)
report_dropdown.grid(row=row_count, column=0, columnspan=2, padx=20, pady=20)
row_count += 1
##########################################################################################
# Run Streamlit radio button
run_streamlit = tk.BooleanVar(value=True)
callback_radio_st_run = create_radio_button_callback(
    run_streamlit, name="run_streamlit"
)
ctk_radio_st_autorun_1 = customtkinter.CTkRadioButton(
    app,
    text="autorun streamlit",
    value=True,
    variable=run_streamlit,
    command=callback_radio_st_run,
)
ctk_radio_st_autorun_1.grid(row=row_count, column=0, padx=20, pady=20)
ctk_radio_st_autorun_0 = customtkinter.CTkRadioButton(
    app,
    text="skip starting streamlit",
    value=False,
    variable=run_streamlit,
    command=callback_radio_st_run,
)
ctk_radio_st_autorun_0.grid(row=row_count, column=1, padx=20, pady=20)
row_count += 1
##########################################################################################
# output directory selection
ctk_label_outdir = customtkinter.CTkLabel(app, text="Select output directory:")
ctk_label_outdir.grid(row=row_count, column=0, columnspan=1, padx=10, pady=5)
CTK_ENTRY_MAX_DEPTH_DEFAULT = 2
# Maximum Depth input
ctk_label_max_depth = customtkinter.CTkLabel(
    app,
    text=f"Maximum Depth: (default {CTK_ENTRY_MAX_DEPTH_DEFAULT})",
)
ctk_label_max_depth.grid(
    row=row_count, column=1, columnspan=1, padx=10, pady=5, sticky="e"
)


max_depth = tk.IntVar(value=CTK_ENTRY_MAX_DEPTH_DEFAULT)


def slider_event(value):
    max_depth.set(value)
    ctk_label_max_depth.configure(text=f"Maximum Depth: {int(value)}")


ctk_entry_max_depth = customtkinter.CTkSlider(
    app,
    from_=2,
    to=9,
    variable=max_depth,
    width=150,
    command=slider_event,
    number_of_steps=7,
)
ctk_entry_max_depth.set(
    CTK_ENTRY_MAX_DEPTH_DEFAULT
)  # Set the initial value of the slider
ctk_entry_max_depth.grid(
    row=row_count, column=2, columnspan=1, padx=10, pady=5, sticky="w"
)
row_count += 1
##########################################################################################
output_dir_entry = tk.StringVar(value=str(output_dir))
select_output_dir = create_select_directory(output_dir_entry)
select_output_dir_button = customtkinter.CTkButton(
    app, text="Select Output Directory", command=select_output_dir
)
select_output_dir_button.grid(row=row_count, column=2, columnspan=1, padx=5, pady=10)
ctk_entry_outpath = customtkinter.CTkEntry(
    app,
    width=400,
    textvariable=output_dir_entry,
)
ctk_entry_outpath.grid(row=row_count, column=0, columnspan=2, padx=10, pady=10)
row_count += 1
##########################################################################################
# Python binary selection
# ctk_label_python = customtkinter.CTkLabel
ctk_label_outdir = customtkinter.CTkLabel(app, text="Select Python binary:")
ctk_label_outdir.grid(row=row_count, column=0, columnspan=1, padx=10, pady=5)
row_count += 1
##########################################################################################
python_dir_entry = tk.StringVar(value=config_app["python_dir_entry"])
select_python_bin = create_select_directory(python_dir_entry)
select_python_bin_button = customtkinter.CTkButton(
    app, text="Select Python binary", command=select_python_bin
)
select_python_bin_button.grid(row=row_count, column=2, columnspan=1, padx=5, pady=5)

ctk_entry_python = customtkinter.CTkEntry(
    app,
    width=400,
    textvariable=python_dir_entry,
)
ctk_entry_python.grid(row=row_count, column=0, columnspan=2, padx=10, pady=5)
row_count += 1
##########################################################################################
ctk_label_env_path = customtkinter.CTkLabel(app, text="PATH:")
ctk_label_env_path.grid(row=row_count, column=0, columnspan=1, padx=2, pady=5)
env_path = tk.StringVar(value=_PATH)
ctk_entry_path_env = customtkinter.CTkEntry(
    app,
    width=400,
    textvariable=env_path,
)
ctk_entry_path_env.grid(row=row_count, column=1, columnspan=2, padx=10, pady=5)
row_count += 1
##########################################################################################
# ctk_label_appath = customtkinter.CTkLabel(
#     app,
#     text=f"App path: {app_path}",
#     wraplength=600,
# )
# ctk_label_appath.grid(row=row_count, column=0, columnspan=3, padx=10, pady=5)
# row_count += 1
##########################################################################################
# Run VueGen button
run_vuegen = create_run_vuegen(
    is_dir=is_dir,
    config_path=config_path,
    report_type=report_type,
    run_streamlit=run_streamlit,
    output_dir_entry=output_dir_entry,
    python_dir_entry=python_dir_entry,
    max_depth=max_depth,
)
run_button = customtkinter.CTkButton(
    app,
    text="Run VueGen",
    command=run_vuegen,
)
run_button.grid(row=row_count, column=0, columnspan=2, padx=20, pady=20)
row_count += 1
##########################################################################################
# Run the app in the mainloop
app.mainloop()
