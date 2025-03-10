import logging
import json
import os

from nvflare.apis.executor import Executor
from nvflare.apis.fl_constant import FLContextKey
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable
from nvflare.apis.signal import Signal
from _utils.utils import get_data_directory_path, get_output_directory_path

TASK_NAME_GET_LOCAL_IMAGE = "GET_LOCAL_IMAGE"
TASK_NAME_ACCEPT_GLOBAL_AVERAGE_IMAGE = "ACCEPT_GLOBAL_AVERAGE_IMAGE"

class MyExecutor(Executor):
    def execute(
        self,
        task_name: str,
        shareable: Shareable,
        fl_ctx: FLContext,
        abort_signal: Signal,
    ) -> Shareable:

        logging.info(f"Task Name: {task_name}")

        if task_name == TASK_NAME_GET_LOCAL_IMAGE:

            shareable = Shareable()
            return shareable

        if task_name == TASK_NAME_ACCEPT_GLOBAL_AVERAGE_IMAGE:
            
            shareable = Shareable()
            return Shareable()
