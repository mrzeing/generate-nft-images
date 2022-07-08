import os
from PIL import Image
import pandas as pd
import shutil
from config import FOLDERS, EXTENSION, W, H


def get_files_path(folders=FOLDERS):
    """
    helper function to get source layer files path

    Args:
        folders (str, optional): root folder save source layer files. Defaults to FOLDERS.

    Returns:
        List[str]: all source layer files path
    """
    files_path = []
    for folder in folders:
        assert os.path.exists(
            folder
        ), f"{folder} folder does not exist, please check PARTS_DICT in config.py"
        for root, _, _ in os.walk(folder):
            if root not in FOLDERS:
                for _, _, files in os.walk(root):
                    assert (
                        len(files) > 0
                    ), f"{root} is empty, if you don't want to use this trait, please add an empty.png in this folder"
                    for file in files:
                        if file != ".DS_Store":
                            files_path.append(os.path.join(root, file))
    files_path.sort()
    return files_path


files_path = get_files_path()

if __name__ == "__main__":
    # clean old folder
    folders = ["images", "metadata"]
    for folder in folders:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"{folder} folder cleaned")
        os.mkdir(folder)

    # Validate image format and size
    for path in files_path:
        assert (
            path.split(".")[-1] in EXTENSION
        ), f"{path}'s extension is not {EXTENSION} "
        im = Image.open(path)
        w, h = im.size
        assert w == W, f"{path} width not equal {W}"
        assert h == H, f"{path} height not equal {H}"

    # Validate path name has -
    for path in files_path:
        assert (
            "-" not in path.split("/")[-1]
        ), f"{path} is invalid, files should not have '-' symbol"

    # export tables
    attrs = [os.path.split(path) for path in files_path]
    d = {
        "folder": [a[0].split(os.sep)[-2] for a in attrs],
        "prop": [a[0].split("_")[1] for a in attrs],
        "value": [a[1].split(".")[0] for a in attrs],
        "ratio": 1,
    }
    df = pd.DataFrame(data=d)
    df.to_csv("ratio.csv", index=False)

    if os.path.exists("ratio.csv"):
        print("generate table success!")
        print("You can modify ratio.csv to change the ratio of each parts")
        print("PS: Don't use Excel to save csv, use notepad instead")

