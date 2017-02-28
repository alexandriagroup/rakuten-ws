# coding: utf-8
from __future__ import unicode_literals


def test_get_usage(ws):
    result = ws.rms.cabinet.get_usage()
    expected_keys = set(['resultCode', 'MaxSpace', 'FolderMax', 'FileMax', 'UseSpace', 'AvailSpace', 'UseFolderCount',
                         'AvailFolderCount'])
    keys = set(list(result.keys()))
    assert keys == expected_keys


def test_folder_operations(ws):
    test_folder_name = 'H35TX4FO6J697AX'
    result = ws.rms.cabinet.insert_folder(folder={'folderName': test_folder_name})
    assert result.status['systemStatus'] == "OK"
    result = ws.rms.cabinet.get_folders()
    folders_names = [f['FolderName'] for f in result['folders']['folder']]
    assert test_folder_name in folders_names


def test_upload_file(ws):
    item_file = {
        'file_name': "ZZZ",
        'folder_id': 5503240,
    }
    result = ws.rms.cabinet.insert_file(file=item_file, filename="https://httpbin.org/image/png")
    assert result.status['systemStatus'] == "OK"
