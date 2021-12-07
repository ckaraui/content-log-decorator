<<<<<<< HEAD
'''
Implements the decorator content log
'''
import logging
import sys

FILENAME = __file__

LOGGER_DEBUG = logging.getLogger(FILENAME)
LOGGER_DEBUG.setLevel("DEBUG")
FORMATTER_DEBUG = logging.Formatter('[%(asctime)s][file:%(name)s]%(levelname)s %(message)s')
LOGGER_STREAM = logging.StreamHandler()
LOGGER_STREAM.setLevel(getattr(logging, "DEBUG"))
LOGGER_STREAM.setFormatter(FORMATTER_DEBUG)
LOGGER_DEBUG.addHandler(LOGGER_STREAM)

def log_content(func):
    """
    log content function allows to log the function variables content using the debug context manager
    """
    def decorated_func(*args, **kwargs):
        with DebugContext(func.__name__):
            return_value = func(*args, **kwargs)
        return return_value
    return decorated_func

class DebugContext():
    """
    DebugContext class is a custom context manager that allows to trace any function called inside the context manager
    """
    def __init__(self, name):

        self.name = name

    def __enter__(self):
        '''
        This method is called before the call of context manager
        '''
        sys.settrace(self.trace_calls)

    def __exit__(self, *args, **kwargs):
        '''
        This method is called after the call of context manager
        '''
        sys.settrace = None

    def trace_calls(self, frame, event, arg=None):
        '''
        trace_calls method traces the called function inside the context manager
        :param frame: is the current called object
        :param event: (str) a string which be either 'call', 'line', 'return', 'exception' or 'opcode'
        :param arg: (int) depends on the event type
        :return: the result of trace_lines function
        '''
        if event != 'call' or frame.f_code.co_name != self.name:
            return
        return self.trace_lines

    def trace_lines(self, frame, event, arg=None):
        '''
        trace_lines method logs each line content at result line of the called object
        :param frame: is the current called object
        :param event: (str) a string which be either 'call', 'line', 'return', 'exception' or 'opcode'
        :param arg: (int) depends on the event type
        :return: debug log of variables content
        '''
        if event in ['return']:
            code_object = frame.f_code
            func_name = code_object.co_name
            local_vars = frame.f_locals
            for var_name in local_vars:
                LOGGER_DEBUG.debug(f"{func_name}() variable {var_name} = {local_vars[var_name]}")

@log_content
def function_to_debug(a, b, c):
    e = a + b
    d = b + c
    f = a + c
    result = e + d + f
    return result

function_to_debug(a=10, b=5, c=2)
