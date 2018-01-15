import zipfile
import os


def zip_dir(filename: str, dir_name: str):
    z = zipfile.ZipFile(filename, 'w')

    if os.path.isdir(dir_name):
        for d in os.listdir(dir_name):
            z.write(dir_name + os.sep + d)

    z.close()


if __name__ == "__main__":
    import sys

    input_path = sys.path[0][0: sys.path[0].index("scorpio")] + "scorpio/config"
    output_path = sys.path[0][0: sys.path[0].index("scorpio")] + "scorpio/logfile/config.zip"
    zip_dir(output_path, input_path)
