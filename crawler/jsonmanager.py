# -*- coding: utf-8 -*-


class JsonManager:
    def __init__(self, data: list):
        self.data = data

    def get_assignment(self) -> list:
        assignment = next(item for item in self.data if item["name"] == "과제")
        if not assignment['assignments']:
            raise StopIteration
        return assignment['assignments']

    def get_week_learning(self) -> list:
        learn = next(item for item in self.data if item["name"] == "주차학습")
        return learn['assignments']

    def get_all(self) -> list:
        return self.get_assignment() + self.get_week_learning()
