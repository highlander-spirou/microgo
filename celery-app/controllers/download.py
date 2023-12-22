from instantiation import file_access
from errors import Error, Code
from io import BytesIO


def download_func(fs_id, access_user):
    read_result = file_access.read_fs(fs_id)
    if isinstance(read_result, Error):
        return read_result
    filename, file_bytes = read_result
    metadata = file_access.retrieve_file_metadata(fs_id)
    if metadata['owner_id'] != access_user:
        return Error(err_code=Code.Download_Unauth)
    imgIO = BytesIO(file_bytes)
    return filename, imgIO