# coding: utf-8
from __future__ import unicode_literals


def test_get_usage(ws):
    result = ws.rms.cabinet.get_usage()
    expected_keys = ['resultCode', 'MaxSpace', 'FolderMax', 'FileMax', 'UseSpace', 'AvailSpace', 'UseFolderCount',
                     'AvailFolderCount']
    keys = list(result.keys())
    assert keys == expected_keys


def test_folder_operations(ws):
    test_folder_name = 'H35TX4FO6J697AX'
    result = ws.rms.cabinet.insert_folder(folder={'folderName': test_folder_name})
    assert result.status['systemStatus'] == "OK"
    result = ws.rms.cabinet.get_folders()
    folders_names = [f['FolderName'] for f in result['folders']['folder']]
    assert test_folder_name in folders_names
