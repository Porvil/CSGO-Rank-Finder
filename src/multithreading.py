from PyQt5.QtCore import *

import traceback
import sys

"""
WorkerSignals class to hold signals
    finished -> no data
    error -> tuple (exctype, value, traceback.format_exc())
    result -> object
    progress -> tuple(progress, data)
"""
class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(tuple)

"""
Worker class to call background tasks
    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function
"""
class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    """
    Initialise the runner function with passed args, kwargs.
    """
    @pyqtSlot()
    def run(self):
        # retrieve args/kwargs here and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            # return the error and traceback
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            # return the result of the processing
            self.signals.result.emit(result)  
        finally:
            # done
            self.signals.finished.emit()