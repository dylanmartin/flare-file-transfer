from typing import Dict, Any
import os
import numpy as np
from nvflare.apis.shareable import Shareable
from nvflare.apis.fl_context import FLContext
from nvflare.app_common.abstract.aggregator import Aggregator
from nvflare.apis.fl_constant import ReservedKey
from _utils.utils import find_repo_root_path
from .image_utils import load_bmp_as_array, save_array_as_bmp, pixel_wise_average

class MyAggregator(Aggregator):
    """
    MyAggregator performs pixel-wise averaging of grayscale BMP images from multiple clients.
    """

    def __init__(self):
        super().__init__()
        self.site_results: Dict[str, Dict[str, Any]] = {}

        # Define the temporary storage folder
        repo_root_path = find_repo_root_path()
        self.image_storage_path = os.path.join(repo_root_path, "temp_image_storage")

        # Ensure the directory exists
        os.makedirs(self.image_storage_path, exist_ok=True)

    def accept(self, site_result: Shareable, fl_ctx: FLContext) -> bool:
        """
        Accepts an image from a client, saves it as a BMP file inside the temp storage folder.

        :param site_result: The image received from the client site.
        :param fl_ctx: The federated learning context.
        :return: Boolean indicating if the image was successfully saved.
        """
        site_name = site_result.get_peer_prop(key=ReservedKey.IDENTITY_NAME, default="unknown_site")

        # Define the image file path inside temp storage
        image_filename = f"{site_name}.bmp"
        image_file_path = os.path.join(self.image_storage_path, image_filename)

        # Save the received image bytes to a file
        with open(image_file_path, "wb") as f:
            f.write(site_result["image"])

        # Store file path for aggregation
        self.site_results[site_name] = {"image_file": image_file_path}
        return True

    def aggregate(self, fl_ctx: FLContext) -> Shareable:
        """
        Aggregates pixel-wise averages of all received BMP images.

        :param fl_ctx: The federated learning context.
        :return: A Shareable object containing the aggregated global image.
        """
        if not self.site_results:
            self.log_error(fl_ctx, "No images received for aggregation.")
            return Shareable()

        # Load all images as NumPy arrays
        image_arrays = []
        header = None  # BMP header (unchanged across images)

        for site_name, data in self.site_results.items():
            image_file = data["image_file"]
            header, image_array = load_bmp_as_array(image_file)
            if image_array is not None:
                image_arrays.append(image_array)

        # Perform pixel-wise averaging
        averaged_image = pixel_wise_average(image_arrays)

        # Save the averaged image in the temp storage folder
        aggregated_image_path = os.path.join(self.image_storage_path, "aggregated_image.bmp")
        save_array_as_bmp(averaged_image, header, aggregated_image_path)

        # Prepare the output Shareable
        outgoing_shareable = Shareable()
        with open(aggregated_image_path, "rb") as img_file:
            outgoing_shareable["image"] = img_file.read()

        return outgoing_shareable
