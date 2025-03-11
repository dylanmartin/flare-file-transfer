import logging
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
        """
        Executes tasks based on the task name and handles the given Shareable object.

        :param task_name: Name of the task to execute.
        :param shareable: The received Shareable object.
        :param fl_ctx: The federated learning context.
        :param abort_signal: Signal for task abortion.
        :return: A Shareable object containing the result.
        """
        logging.info(f"Executing task: {task_name}")

        if task_name == TASK_NAME_GET_LOCAL_IMAGE:
            return do_task_get_local_image(fl_ctx)

        elif task_name == TASK_NAME_ACCEPT_GLOBAL_AVERAGE_IMAGE:
            return do_task_accept_global_average_image(shareable, fl_ctx)

        else:
            logging.warning(f"Unknown task: {task_name}")
            return Shareable()  # Return an empty Shareable for unrecognized tasks


def file_to_bytes(file_path: str) -> bytes:
    """Reads any file as bytes."""
    try:
        with open(file_path, "rb") as f:
            return f.read()
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return b""  # Return empty bytes to avoid crashes


def do_task_get_local_image(fl_ctx: FLContext) -> Shareable:
    """
    Loads a local image file and packages it into a Shareable object.

    :param fl_ctx: The federated learning context.
    :return: A Shareable containing the image data.
    """
    data_directory_path = get_data_directory_path(fl_ctx)
    my_image_path = os.path.join(data_directory_path, "my_image.bmp")

    my_image_bytes = file_to_bytes(my_image_path)

    shareable = Shareable()
    shareable["image"] = my_image_bytes

    logging.info(f"Packaged local image into Shareable: {my_image_path}")
    return shareable


def do_task_accept_global_average_image(shareable: Shareable, fl_ctx: FLContext) -> Shareable:
    """
    Accepts the global average image and stores it.

    :param shareable: The received Shareable containing the global image.
    :param fl_ctx: The federated learning context.
    :return: An acknowledgment Shareable.
    """
    output_directory_path = get_output_directory_path(fl_ctx)  # Adjusted to use the correct function
    os.makedirs(output_directory_path, exist_ok=True)  # Ensure the directory exists

    # Define the filename
    global_image_path = os.path.join(output_directory_path, "global_average.bmp")

    # Extract image bytes and save to a file
    global_image_bytes = shareable.get("image", b"")
    if global_image_bytes:
        with open(global_image_path, "wb") as f:
            f.write(global_image_bytes)
        logging.info(f"Saved global average image to: {global_image_path}")
    else:
        logging.warning("Received empty image data for global average image.")

    return Shareable()  # Return an empty Shareable as acknowledgment
