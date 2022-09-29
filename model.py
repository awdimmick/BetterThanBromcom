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
        if self.__collectionTypeName == 'TUTORGRP':
            return bromcom_connect.BromcomConnector.get_students_for_tutor_group(self.name)
        elif self.__collectionTypeName == "CLASS":
            return bromcom_connect.BromcomConnector.get_students_for_class(self.name)


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
        return self.__behaviourEvents

    @property
    def tutor_group(self):
        return self.__tutorGroup

    def add_behaviour_event(self, data):
        self.__behaviourEvents.append(data)

