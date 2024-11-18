import os
import sys
from datetime import datetime
import logging

## CHECKS
def assert_path(filepath: str):
    """
    Checks that fpath is a string and that it exists

    PARAMS
    -----
    - filepath (str): the filepath or folderpath

    OUTPUTS
    -----
    - raises assertion error if filepath is not a string or doesn't exist
    """

    assert isinstance(filepath, str), f"filepath must be a string: {filepath}"
    assert os.path.exists(
        os.path.abspath(filepath)
    ), f"filepath does not exist: {os.path.abspath(filepath)}"


## LOGGING
def get_basename(fname: None | str = None) -> str:
    """
    - For a given filename, returns basename WITHOUT file extension
    - If no fname given (i.e., None) then return basename that the function is called in

    PARAMS
    -----
    - fname (None or str): the filename to get basename of, or None

    OUTPUTS
    -----
    - basename of given filepath or the current file the function is executed

    EXAMPLES
    -----
    1)
    >>> get_basename()
    utils

    2)
    >>> get_basename('this/is-a-filepath.csv')
    is-a-filepath
    """
    if fname is not None:
        # PRECONDITION
        assert_path(fname)
        # MAIN FUNCTIONS
        return os.path.splitext(os.path.basename(fname))[0]
    else:
        return os.path.splitext(os.path.basename(sys.argv[0]))[0]


def get_time(incl_time: bool = True, incl_timezone: bool = True) -> str:
    """
    Gets current date, time (optional) and timezone (optional) for file naming

    PARAMETERS
    -----
    - incl_time (bool): whether to include timestamp in the string
    - incl_timezone (bool): whether to include the timezone in the string

    RETURNS
    -----
    - fname (str): includes date, timestamp and/or timezone
        connected by '_' in one string e.g. yyyyMMdd_hhmm_timezone

    EXAMPLES
    -----
    1)
    >>> get_time()
    '20231019_101758_CEST'

    2)
    >>> get_time(incl_time=False)
    '20231019_CEST'

    """

    # PRECONDITIONALS
    assert isinstance(incl_time, bool), "incl_time must be True or False"
    assert isinstance(incl_timezone, bool), "incl_timezone must be True or False"

    # MAIN FUNCTION
    # getting current time and timezone
    the_time = datetime.now()
    timezone = datetime.now().astimezone().tzname()
    # convert date parts to string
    y = str(the_time.year)
    M = str(the_time.month)
    d = str(the_time.day)
    h = str(the_time.hour)
    m = str(the_time.minute)
    s = str(the_time.second)
    # putting date parts into one string
    if incl_time and incl_timezone:
        fname = "_".join([y + M + d, h + m + s, timezone])
    elif incl_time:
        fname = "_".join([y + M + d, h + m + s])
    elif incl_timezone:
        fname = "_".join([y + M + d, timezone])
    else:
        fname = y + M + d

    # POSTCONDITIONALS
    parts = fname.split("_")
    if incl_time and incl_timezone:
        assert len(parts) == 3, f"time and/or timezone inclusion issue: {fname}"
    elif incl_time or incl_timezone:
        assert len(parts) == 2, f"time/timezone inclusion issue: {fname}"
    else:
        assert len(parts) == 1, f"time/timezone inclusion issue: {fname}"

    return fname


def generate_log_filename(folder: str = "logs", suffix: str = "") -> str:
    """
    Creates log file name and path

    PARAMETERS
    -----
    folder (str): name of the folder to put the log file in
    suffix (str): anything else you want to add to the log file name

    RETURNS
    -----
    log_filepath (str): the file path to the log file
    """
    # PRECONDITIONS
    assert_path(folder)

    # MAIN FUNCTION
    log_filename = get_time(incl_timezone=False) + "_" + suffix + ".log"
    log_filepath = os.path.join(folder, log_filename)

    return log_filepath


def init_log(filename: str, display: bool = False, logger_id: str | None = None):
    """
    - Custom python logger configuration (basicConfig())
        with two handlers (for stdout and for file)
    - from: https://stackoverflow.com/a/44760039
    - Keeps a log record file of the python application, with option to
        display in stdout

    PARAMETERS
    -----
    - filename (str): filepath to log record file
    - display (bool): whether to print the logs to whatever standard output
    - logger_id (str): an optional identifier for yourself,
        if None then defaults to 'root'

    RETURNS
    -----
    - logger object

    EXAMPLE
    -----
    >>> logger = init_log('logs/tmp.log', display=True)
    >>> logger.info('Loading things')
    [2023-10-20 10:38:03,074] root: INFO - Loading things
    """
    # PRECONDITIONALS
    assert isinstance(filename, str), "filename must be a string"
    assert (
        isinstance(logger_id, str) or logger_id is None
    ), "logger_id must be a string or None"

    # MAIN FUNCTION
    # init handlers
    file_handler = logging.FileHandler(filename=filename)
    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    if display:
        handlers = [file_handler, stdout_handler]
    else:
        handlers = [file_handler]

    # logger configuration
    logging.basicConfig(
        # level=logging.DEBUG,
        format="[%(asctime)s] %(name)s: %(levelname)s - %(message)s",
        handlers=handlers,
    )
    logging.getLogger("matplotlib.font_manager").disabled = True

    # instantiate the logger
    logger = logging.getLogger(logger_id)
    logger.setLevel(logging.DEBUG)

    return logger


def get_logger():
    """
    Putting at all together to init the log file.
    """
    # get log suffix, which will be the current script's base file name
    log_suffix = get_basename()
    # generate log file name
    log_file = generate_log_filename(suffix=log_suffix)
    # init logger
    logger = init_log(log_file, display=True)
    # log it
    logger.info(f"Path to log file: {log_file}")

    return logger
