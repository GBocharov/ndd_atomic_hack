import aspose.words as aw
from pathlib import Path


def del_file(file_path):
    file_path = Path(file_path)
    if file_path.exists():
        file_path.unlink()

def transform_rtf(file_path : str):
    p = Path(file_path)
    if not p.exists():
        return 0
    new_name = file_path[:-3] + 'txt'
    if(file_path.endswith('rtf')):
        print(file_path)
        doc = aw.Document(file_path)
        doc.save(new_name)
        del_file(file_path)
    return new_name

def transform_docx(file_path : str):
    p = Path(file_path)
    if not p.exists():
        return 0
    new_name = file_path[:-4] + 'txt'
    if(file_path.endswith('docx')):
        doc = aw.Document(file_path)
        doc.save(new_name)
        del_file(file_path)
    return new_name

def trans_file(file_path):
    res = ''
    if file_path.endswith('txt'):
        return file_path

    if(file_path.endswith('rtf')):
        res = transform_rtf(file_path)
    elif (file_path.endswith('docx')):
        res = transform_docx(file_path)
    else:
        return 0
    return res

