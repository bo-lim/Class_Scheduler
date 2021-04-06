# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from pprint import pprint

from crawler.classcrawler import Crawler
from crawler.eclassauth import EClass
from crawler.jsonmanager import JsonManager


class Controller:
    def __init__(self, uid: str, upw: str):
        self.uid = uid
        self.upw = upw
        self.crawler = Crawler()
        self.course_info = None

    def refresh_auth(self):
        e_class = EClass(self.uid, self.upw)  # 이클레스 객체 생성
        login = e_class.login()
        if not login:
            # print("로그인 실패")
            return False
        self.crawler.set_cookies(e_class.auth_cookies)
        e_class.quit()
        return True

    def get_course_info(self) -> dict:
        try:
            self.course_info = self.crawler.get_courses()
            return self.course_info
        except:
            if not self.refresh_auth():
                return {}
            self.course_info = self.crawler.get_courses()
            return self.course_info

    def get_all_assignments(self) -> dict:
        result = {
            'assignment': list(),
            'lecture': list(),
        }

        self.refresh_auth()

        for course_id in self.course_info:
            # 성적
            grades = self.crawler.get_sub_assignment(course_id)

            total_assignments = JsonManager(self.crawler.get_assignments(course_id))
            try:
                assignments = total_assignments.get_assignment()
                week_learnings = total_assignments.get_week_learning()
                for assignment in assignments:
                    name = assignment['name']
                    grade = True if (grades and (
                            grades[assignment['id']]['grade'] or grades[assignment['id']]['submitted_at'])) else False
                    due_date = self.utc_to_asia_time(assignment['due_at'])

                    if not grade:
                        result['assignment'].append((self.course_info[course_id], due_date, name))
                for lectures in week_learnings:
                    name = lectures['name']
                    grade = True if (grades and (
                            grades[lectures['id']]['grade'] or grades[lectures['id']]['submitted_at'])) else False
                    due_date = self.utc_to_asia_time(lectures['due_at'])

                    if not grade:
                        result['lecture'].append((self.course_info[course_id], due_date, name))
            except StopIteration:
                pass
                # print(f"    {course_info[course_id]} has no Assignments.")

        return result

    @staticmethod
    def utc_to_asia_time(utc_str: str or None) -> str:
        if utc_str is None:
            return "없음"
        date_time_obj = datetime.strptime(utc_str, '%Y-%m-%dT%H:%M:%SZ') + timedelta(hours=9)
        return date_time_obj.strftime("%Y년 %m월 %d일 %H:%M")


if __name__ == '__main__':
    cnt = Controller("eclass id", "eclass pw")
    pprint(cnt.get_all_assignments())
