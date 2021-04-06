# -*- coding: utf-8 -*-
import json
import requests


class Crawler:
    def __init__(self):
        self.session = requests.session()

    def set_cookies(self, cookie_list: list):
        for cookie in cookie_list:
            self.session.cookies.set(cookie['name'], cookie['value'])

    def get_courses(self) -> dict:
        course_api_url = "https://eclass3.cau.ac.kr/api/v1/users/self/favorites/courses?" \
                         "include[]=term&exclude[]=enrollments"
        res = self.session.get(course_api_url)
        raw_list = res.text.replace("while(1);", '')
        course_info_list = json.loads(raw_list)

        simple_course_info = dict()
        for course_info in course_info_list:
            simple_course_info[course_info['id']] = course_info['name']
        return simple_course_info

    def get_assignments(self, course_id: str or int) -> list:
        assignment_api_url = f"https://eclass3.cau.ac.kr/api/v1/courses/{course_id}/assignment_groups?" \
                             "include[]=assignments&include[]=discussion_topic&exclude_response_fields[]=description&" \
                             "exclude_response_fields[]=rubric&override_assignment_dates=true&per_page=50"

        res = self.session.get(assignment_api_url)
        raw_list = res.text.replace("while(1);", '')
        return json.loads(raw_list)

    def get_sub_assignment(self, course_id: str or int) -> dict or None:
        simple_sub_assignment_info = dict()

        def get_part_of_this(url: str or None):
            if url is None:
                return None
            res = self.session.get(url)
            if (res.links is not None) and (res.links.get('next') is not None):
                get_part_of_this(res.links.get('next').get('url'))
            raw_list = res.text.replace("while(1);", '')
            sub_assignment_list = json.loads(raw_list)
            if type(sub_assignment_list) != list:
                return None
            for sub_assignment in sub_assignment_list:
                simple_sub_assignment_info[sub_assignment['assignment_id']] = {
                    'grade': sub_assignment['grade'],
                    'submitted_at': sub_assignment['submitted_at'],
                }

        sub_assignment_api_url = f"https://eclass3.cau.ac.kr/api/v1/courses/{course_id}/students/submissions?per_page=50"
        get_part_of_this(sub_assignment_api_url)
        return simple_sub_assignment_info
