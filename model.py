from datetime import datetime

import bromcom_connect


class Collection:

    def __init__(self, data):

        self.__id = int(data['CollectionID'])
        self.__name = data['CollectionName']
        self.__description = data['CollectionDescription']
        self.__startDate = data['StartDate']
        self.__endDate = data['EndDate']
        self.__collectionTypeName = data['CollectionTypeName']
        self.__collectionTypeDescription = data['CollectionTypeDescription']

        self.__students = None

        """
        If the Collection has a type CLASS then we can also get the students by reference to StudentClasses
        If the Collection has a type TUTORGRP the we can get the students by referene to the Students entity, filtering 
        on Student.TutorGroup = Collection.CollectionDescription
        """

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def description(self):
        return self.__description

    @property
    def type_description(self):
        return self.__collectionTypeDescription

    @property
    def students(self):

        if self.__students is None:
            if self.__collectionTypeName == 'TUTORGRP':
                self.__students = bromcom_connect.BromcomConnector.get_students_for_tutor_group(self.name)
            elif self.__collectionTypeName == "CLASS":
                self.__students = bromcom_connect.BromcomConnector.get_students_for_class(self.name)

        return self.__students

    def load_behaviour_events_for_students(self):

        student_id_queue = [self.students[s].id for s in self.students]

        behaviour_dicts = []

        while len(student_id_queue) > 0:

            filter_string = ""

            for i in range(20):

                try:
                    filter_string += f"StudentId eq {student_id_queue[0]} or "
                    del student_id_queue[0]

                except IndexError:
                    break

            filter_string = filter_string[:-4]

            response = bromcom_connect.BromcomConnector.session.get(
                bromcom_connect.Settings.BromcomODataURL +
                f"BehaviourEventRecords?$filter={filter_string}"
            )

            for behaviour_data in response.json()['value']:
                behaviour_dicts.append(behaviour_data)

        for behaviour_data in behaviour_dicts:

            self.__students[behaviour_data['StudentId']]\
                .add_behaviour_event(BehaviourEvent(behaviour_data))


class Student:

    def __init__(self, data):

        self.__id = data['StudentId']
        self.__preferredFirstName = data['PreferredFirstName']
        self.__preferredLastName = data['PreferredLastName']
        self.__legalFirstName = data['LegalFirstName']
        self.__legalLastName = data['LegalLastName']
        self.__middleName = data['MiddleName']
        # self.__dateOfBirth = datetime.utcfromtimestamp(data['DateOfBirth'])
        # self.__dateOfEntry = datetime.fromisoformat(data['DateOfEntry'])
        self.__dateOfBirth = data['DateOfBirth']
        self.__dateOfEntry = data['DateOfEntry']
        self.__eal = data['EAL'] == "Yes"
        self.__fsm = data['FSM'] == "Yes"
        self.__pp = data['PupilPremium'] == "Yes"
        self.__lac = data['LAC'] == "Yes"
        self.__sen = False if data['SENNeed'] == "" else True
        self.__serviceChild = not data['ServiceChildDescription'] == ""
        self.__senProvision = data['Provision']
        self.__house = data['House']
        self.__tutorGroup = data['TutorGroup']
        self.__yearGroup = int(data['YearGroup'])
        self.__behaviourEvents = []

    @property
    def id(self):
        return self.__id

    @property
    def first_name(self):
        return self.__preferredFirstName

    @property
    def last_name(self):
        return self.__preferredLastName

    @property
    def middle_name(self):
        return self.__middleName

    @property
    def display_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def house(self):
        return self.__house

    @property
    def year_group(self):
        return self.__yearGroup

    @property
    def behaviour_events(self):
        if len(self.__behaviourEvents) == 0:
            self.load_behaviour_events()

        return self.__behaviourEvents

    @property
    def behaviour_net_total(self):
        total = 0

        for b in self.behaviour_events:
            total += b.adjustment

        return total

    @property
    def behaviour_negative_total(self):

        total = 0

        for b in self.behaviour_events:
            if b.type == "Negative":
                total += b.adjustment

        return total

    @property
    def behaviour_positive_total(self):

        total = 0

        for b in self.behaviour_events:
            if b.type == "Positive":
                total += b.adjustment

        return total

    @property
    def tutor_group(self):
        return self.__tutorGroup

    def add_behaviour_event(self, behaviour):
        self.__behaviourEvents.append(behaviour)

    def load_behaviour_events(self):
        response = bromcom_connect.BromcomConnector.session.get\
                (
                    bromcom_connect.Settings.BromcomODataURL +
                    f"BehaviourEventRecords?$filter=StudentId eq {self.__id}"
                )

        self.__behaviourEvents = []

        for behaviour_data in response.json()['value']:
            self.__behaviourEvents.append(BehaviourEvent(behaviour_data))


class BehaviourEvent:

    def __init__(self, data):

        self.__eventRecordId = data['EventRecordId']
        self.__studentId = data['StudentId']
        self.__eventType = data['EventType']
        self.__eventName = data['EventName']
        self.__eventDescription = data['EventDescription']
        self.__eventDate = data['EventDate']
        self.__adjustment = int(data['Adjustment'])
        self.__comment = data['Comment']
        self.__internalComment = data['InternalComment']
        self.__dayOfWeek = data['DayOfWeek']
        self.__timetablePeriod = data['TimetablePeriod']
        self.__room = data['TimetablePeriod']
        self.__staffCode = data['StaffCode']
        self.__collectionName = data['CollectionName']
        self.__subject = data['Subject']
        self.__department = data['Department']

    @property
    def id(self):
        return self.__eventRecordId

    @property
    def studentId(self):
        return self.__studentId

    @property
    def student(self):
        return bromcom_connect.BromcomConnector.get_student_by_id(self.studentId)

    @property
    def name(self):
        return self.__eventName

    @property
    def type(self):
        return self.__eventType

    @property
    def description(self):
        return self.__eventDescription

    @property
    def comment(self):
        return self.__comment

    @property
    def staff_code(self):
        return self.__staffCode

    @property
    def date(self):
        return self.__eventDate

    @property
    def day_of_week(self):
        return self.__dayOfWeek

    @property
    def adjustment(self):
        return self.__adjustment

    @property
    def collection_name(self):
        return self.__collectionName

    @property
    def collection(self):
        return bromcom_connect.BromcomConnector.get_collection_by_description(self.collection_name)

    @property
    def subject(self):
        return self.__subject

    def __repr__(self):
        return f"{self.type}, {self.adjustment} - {self.description}: {self.comment} ({self.staff_code}, {self.date})"
