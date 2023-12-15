from libs.file_access import filter_fs
from datetime import datetime
from typing import TypedDict

class Metadict(TypedDict):
    id: str
    filename: str
    tag: str
    original: str | None
    uploadDate: str

def list_imgs(username: str):
    metadict:list[Metadict] = []
    for i in filter_fs('owner', username):
        format_string = "%H:%M on %d/%m/%Y"
        metadict.append({
            'id': str(i.get('_id')),
            'filename': i.get('filename'),
            'tag': i.get('tag'),
            'uploadDate': datetime.strftime(i.get('uploadDate'), format_string),
            'original': i.get('original')
            })
    return metadict
