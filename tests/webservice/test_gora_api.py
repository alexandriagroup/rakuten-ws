# coding: utf-8
from __future__ import unicode_literals


def test_golf_search(ws):
    response = ws.gora.golf.search(latitude="35.9061664",
                                   longitude="140.0397556")
    expected_keys = [
        'highway', 'golfCourseDetailUrl', 'golfCourseId', 'golfCourseCaption',
        'golfCourseImageUrl', 'latitude', 'longitude', 'address', 'evaluation',
        'ratingUrl', 'golfCourseAbbr', 'reserveCalUrl', 'golfCourseNameKana',
        'golfCourseName'
    ]
    assert set(response['Items'][0].keys()) == set(expected_keys)


def test_golf_detail(ws):
    response = ws.gora.golf.search(latitude="35.9061664",
                                   longitude="140.0397556")

    golf_course_id = response['Items'][0]['golfCourseId']
    result = ws.gora.golf.detail(golf_course_id=golf_course_id)
    expected_keys = [
        'highway', 'information', 'faxNo', 'meal', 'postalCode', 'staff',
        'golfCourseName', 'carrier', 'nearPin', 'evaluation', 'voiceUrl',
        'golfCourseCaption', 'costperformance', 'creditCard', 'designer',
        'dimension', 'golfCourseAbbr', 'telephoneNo', 'layoutUrl',
        'otherFacility', 'shoes', 'holeCount', 'ratingNum',
        'courseVerticalInterval', 'lodgingFacility', 'ratings', 'address',
        'longitude', 'icDistance', 'longDrivingContest', 'parCount', 'ic',
        'courseName', 'courseDistance', 'courseType', 'newPlans',
        'reserveCalUrl', 'facility', 'fairway', 'greenCount',
        'practiceFacility', 'green', 'golfCourseNameKana', 'closeDay',
        'openDay', 'dressCode', 'routeMapUrl', 'distance', 'golfCourseId',
        'course', 'latitude', 'golfCourseImageUrl1', 'golfCourseImageUrl2',
        'golfCourseImageUrl3', 'golfCourseImageUrl4', 'golfCourseImageUrl5'
    ]
    assert set(result['Item'].keys()) == set(expected_keys)


def test_plan_detail(ws):
    assert True
