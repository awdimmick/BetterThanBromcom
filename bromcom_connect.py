import requests
from settings import Settings
from model import *


class BromcomConnector:

    session = requests.Session()
    session.auth = (Settings.ODataUsername, Settings.ODataPassword)

    @staticmethod
    def get_student_by_id(id:int):
        student_response = BromcomConnector.session.get(
            Settings.BromcomODataURL +
            f"Students?$filter=StudentId eq {id}"
        )

        return Student(student_response.json()['value'][0])

    @staticmethod
    def get_students_for_tutor_group(tutor_group:str):
        students_response = BromcomConnector.session.get(
            Settings.BromcomODataURL +
            f"Students?$filter=TutorGroup eq '{tutor_group}'"
        )

        students_dict = {}

        for student in students_response.json()['value']:
            students_dict[int(student['StudentId'])] = Student(student)

        return students_dict

    @staticmethod
    def get_students_for_class(class_name:str):

        student_ids = []
        students = []
        students_remaining = True

        student_classes = BromcomConnector.session.get(
            Settings.BromcomODataURL +
            f"StudentClasses?$filter=ClassName eq '{class_name}'"
        ).json()['value']

        for sc in student_classes:
            student_ids.append(int(sc['StudentId']))

        while len(student_ids) > 0:
            students_filter_string = ""
            # Multi select maxes out at 20 so need to process in batches
            for i in range(20):
                try:
                    students_filter_string += f"StudentId eq {student_ids[0]} or "
                    del student_ids[0]
                except:
                    pass
            students_filter_string = students_filter_string[:-4]

            students_response_url = Settings.BromcomODataURL + "Students?$filter=" + students_filter_string

            student_dicts = BromcomConnector.session.get(students_response_url).json()['value']

            for student_data in student_dicts:
                students.append(Student(student_data))

        return students

    @staticmethod
    def get_collection_by_id(collection_id:int):

        collection_response = BromcomConnector.session.get(
            Settings.BromcomODataURL +
            f"Collections?$filter=CollectionID eq {collection_id}"
        )

        return Collection(collection_response.json()['value'][0])

