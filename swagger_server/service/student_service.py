import pymongo
import os
url = os.environ['MONGO_URI'] or "mongodb://localhost:27017/"
dbClient = pymongo.MongoClient(url)
student_db = dbClient["students"]
studentCol = student_db["student"]


def add(student=None):
    res = studentCol.find_one({"student_id": student.student_id})
    if res:
        return 'already exists', 409
    studentCol.insert_one(student.to_dict())
    student_obj = get_by_id(student.student_id)
    return student_obj['student_id']


def get_by_id(student_id=None, subject=None):
    student = studentCol.find_one(dict(student_id=int(student_id)))
    if not student:
        return 'not found', 404
    student['_id'] = str(student['_id'])
    return student


def delete(student_id=None):
    student = get_by_id(student_id)
    studentCol.delete_one({"student_id": student['student_id']})
    return student_id
