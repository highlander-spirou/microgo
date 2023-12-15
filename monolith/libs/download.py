from libs.file_access import read_fs, retrieve_file_metadata
from io import BytesIO
from dtypes import Error


def download_func(fs_id, access_user):
    read_result = read_fs(fs_id)
    if isinstance(read_result, Error):
        return read_result
    filename, file_bytes = read_result
    metadata = retrieve_file_metadata(fs_id)
    if metadata['owner'] != access_user:
        return None
    imgIO = BytesIO(file_bytes)
    return filename, imgIO