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
    res = studentCol.find_one({"first_name": student.first_name, "last_name": student.last_name})
    if res:
        return 'already exists', 409
    # Since student_id is not required, we generate a new id based on the count of documents
    # This should be better automated with a "table" that stores the maximum value of the student_id
    # and increment that before each insertion
    new_student_id = studentCol.count_documents({}) + 1

    new_student_id_count = studentCol.count_documents({"student_id": new_student_id})
    # Check if the new student id exists or not
    # This is not a full proof solution, but it will suffice for this implementation
    if new_student_id_count > 0:
        new_student_id = new_student_id + 1

    student_obj = student.to_dict()
    student_obj["student_id"] = new_student_id
    studentCol.insert_one(student_obj)
    return new_student_id


# Returns a student object based on the student_id
# If the student_id is not found, 404 is returned
# def get_by_id(student_id=None, subject=None):
#     student = studentCol.find_one(dict(student_id=int(student_id)))
#     if not student:
#         return 'not found', 404
#     student['_id'] = str(student['_id'])
#     return student
def get_by_id(student_id=None, subject=None):
    student = studentCol.find_one(dict(student_id=int(student_id)))
    if not student:
        return 'not found', 404
    student['student_id'] = student_id
    student['_id'] = str(student['_id'])
    print(student)
    return student


# Check the student exists by using the get_by_id function
# If it exists, delete the student by student_id and return the student_id
def delete(student_id=None):
    student = studentCol.find_one(dict(student_id=int(student_id)))
    if not student:
        return 'not found', 404
    studentCol.delete_one({"student_id": student['student_id']})
    return student_id
