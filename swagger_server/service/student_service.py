import pymongo
import os

# Get the MONGO URI, first check if there is an env var, if not use localhost
# Since the code quality is not a priority I will leave as is,
# but in production this should be in a config file by itself to be able to
# configure dynamically
url = os.environ['MONGO_URI'] or "mongodb://localhost:27017/"
dbClient = pymongo.MongoClient(url)
student_db = dbClient["students"]
studentCol = student_db["student"]


# Create a new student, first check if the student ID exists in the DB
# if it does, return 409, if not insert one into the DB and return the student_id
def add(student=None):
    res = studentCol.find_one({"student_id": student.student_id})
    if res:
        return 'already exists', 409
    studentCol.insert_one(student.to_dict())
    student_obj = get_by_id(student.student_id)
    return student_obj['student_id']


# Returns a student object based on the student_id
# If the student_id is not found, 404 is returned
def get_by_id(student_id=None, subject=None):
    student = studentCol.find_one(dict(student_id=int(student_id)))
    if not student:
        return 'not found', 404
    student['_id'] = str(student['_id'])
    return student


# Check the student exists by using the get_by_id function
# If it exists, delete the student by student_id and return the student_id
def delete(student_id=None):
    student = get_by_id(student_id)
    studentCol.delete_one({"student_id": student['student_id']})
    return student_id
