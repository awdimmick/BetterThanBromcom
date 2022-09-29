import bromcom_connect
from bromcom_connect import BromcomConnector as bc

# TODO: Add behaviour event retrieval to student records
# - to happen when .behaviour_events property is called, not on constructor

"""
print("Obtaining behaviour event data...")
behaviour_event_records_list = []
behaviour_response = session.get(Settings.BromcomODataURL + "BehaviourEventRecords")

for behaviour_event in behaviour_response.json()['value']:
    if int(behaviour_event['StudentId']) in students_dict:
        students_dict[behaviour_event['StudentId']].add_behaviour_event(behaviour_event)

for id in students_dict:
    print(f"Processed: {students_dict[id].displayName} - Total behaviour events: {len(students_dict[id].behaviourEvents)}")
"""

#s = bc.get_student_by_id(1056)
#tg_students = bc.get_students_for_tutor_group("PS")
# class_students = bc.get_students_for_class("13B/Cm")
# for s in class_students:
#     print(s.display_name)

c = bc.get_collection_by_id(89)
print(f"Got collection: {c.name}")
for s in c.students:
    print (s.display_name)
