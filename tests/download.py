# Sample Test passing with nose and pytest
from google_images_download import google_images_download
from skimage import io
import shutil
import os

def test_pass():
    argumnets = {
        "keywords": "ebay toys images",
        "limit": 500,
        "print_urls": True,
        "output_directory": "/home/eugene/_DATASETS/studio_shot/eval",
        "chromedriver": "/home/eugene/Downloads/chromedriver"
    }

    response = google_images_download.googleimagesdownload()
    response.download(argumnets)

if __name__ == '__main__':
    test_pass()
    # import glob
    # img_paths = glob.glob('/home/eugene/_DATASETS/studio_shot/eval/car studio shot/*')
    # for img_path in img_paths:
    #     try:
    #         img = io.imread(img_path)
    #     except:
    #         dst_path = os.path.join('/home/eugene/_DATASETS/studio_shot/eval/Untitled Folder', os.path.basename(img_path))
    #         shutil.move(img_path, dst_path)

