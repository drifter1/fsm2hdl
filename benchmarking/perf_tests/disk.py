import os


def disk_space_utilization(file_path: str):
    st = os.stat(file_path)

    return st.st_size
