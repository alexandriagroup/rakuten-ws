# coding: utf-8
from __future__ import unicode_literals


def test_get_usage(ws):
    result = ws.rms.cabinet.get_usage()
    expected_keys = ['resultCode', 'MaxSpace', 'FolderMax', 'FileMax', 'UseSpace', 'AvailSpace', 'UseFolderCount',
                     'AvailFolderCount']
    keys = list(result.keys())
    assert keys == expected_keys
