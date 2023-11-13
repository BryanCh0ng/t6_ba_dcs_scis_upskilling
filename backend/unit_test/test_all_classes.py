import unittest

import os
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from allClasses import *

### this test file runs unit tests to see if each class in allClasses.py can be initialised and jsonified ###

class TestUser(unittest.TestCase):
    def test_json(self):
        user = User(
            user_Name = "John",
            user_Email = "jonathan.2020@smu.edu.sg",
            user_Password = "john123",
            role_Name = "Student"
        )

        self.assertEqual(user.json(), {
                "user_ID": None,
                "user_Name": "John",
                "user_Email": "jonathan.2020@smu.edu.sg",
                "user_Password": "john123",
                "role_Name": "Student"
            }
        )

class TestExternalUser(unittest.TestCase):
    def test_json(self):
        externalUser = ExternalUser(
            user_ID = 1,
            organisation_Name = "NCS",
            is_Alumni = True
        )

        self.assertEqual(externalUser.json(), {
                "external_ID": None,
                "user_ID": 1,
                "organisation_Name": "NCS",
                "is_Alumni": True
            }
        )

class TestCourseCategory(unittest.TestCase):
    def test_json(self):
        courseCategory = CourseCategory(
            coursecat_ID = 1,
            coursecat_Name = "SCIS"
        )

        self.assertEqual(courseCategory.json(), {
                "coursecat_ID": 1,
                "coursecat_Name": "SCIS"
            }
        )

class TestFeedbackTemplate(unittest.TestCase):
    def test_json(self):
        feedbackTemplate = FeedbackTemplate(
            template_ID = 1,
            template_Name = "template1",
            created_On = "2023-07-25"
        )

        self.assertEqual(feedbackTemplate.json(), {
                "template_ID": 1,
                "template_Name": "template1",
                "created_On": "2023-07-25"
            }
        )

class TestCourse(unittest.TestCase):
    def test_json(self):
        course = Course(
            course_ID = 1,
            course_Name = 'Dashboard Specialist',
            course_Desc = "test description",
            coursecat_ID = 1,
            course_Status = "Inactive"
        )

        self.assertEqual(course.json(), {
                "course_ID": 1,
                "course_Name": 'Dashboard Specialist',
                "course_Desc": "test description",
                "coursecat_ID": 1,
                "course_Status": "Inactive"
            }
        )

class TestProposedCourse(unittest.TestCase):
    def test_json(self):
        proposedCourse = ProposedCourse(
            pcourse_ID = 1,
            submitted_By = 3,
            action_Done_By = 1,
            course_ID = 1,
            pcourse_Status = 'Approved',
            reason = None,
            proposed_Date = "2023-08-25",
            voteCount = 21
        )

        self.assertEqual(proposedCourse.json(), {
                "pcourse_ID": 1,
                "submitted_By": 3,
                "action_Done_By": 1,
                "course_ID": 1,
                "pcourse_Status": 'Approved',
                "reason": None,
                "proposed_Date": "2023-08-25",
                "voteCount": 21
            }
        )

class TestVoteCourse(unittest.TestCase):
    def test_json(self):
        voteCourse = VoteCourse(
            course_ID = 1,
            vote_Status = 'Ongoing'
        )

        self.assertEqual(voteCourse.json(), {
                "vote_ID": None,
                "course_ID": 1,
                "vote_Status": 'Ongoing'
            }
        )

class TestInterest(unittest.TestCase):
    def test_json(self):
        interest = Interest(
            interest_ID = 5,
            vote_ID = 3,
            user_ID = 7
        )

        self.assertEqual(interest.json(), {
                "interest_ID": 5,
                "vote_ID": 3,
                "user_ID": 7
            }
        )

class TestTemplateAttribute(unittest.TestCase):
    def test_json(self):
        templateAttribute = TemplateAttribute(
            template_Attribute_ID = 1,
            question = "Nice?",
            input_Type = 'Likert Scale',
            template_ID = 1
        )

        self.assertEqual(templateAttribute.json(), {
                "template_Attribute_ID": 1,
                "question": "Nice?",
                "input_Type": 'Likert Scale',
                "template_ID": 1
            }
        )

        templateAttribute = TemplateAttribute(
            question = "Nice?",
            input_Type = 'Likert Scale',
            template_ID = 1
        )

        self.assertEqual(templateAttribute.json(), {
                "template_Attribute_ID": None,
                "question": "Nice?",
                "input_Type": 'Likert Scale',
                "template_ID": 1
            }
        )
    
class TestInputOption(unittest.TestCase):
    def test_json(self):
        inputOption = InputOption(
            template_Attribute_ID = 1,
            position = 1,
            textlabel = "Low"
        )

        self.assertEqual(inputOption.json(), {
                "input_Option_ID": None,
                "template_Attribute_ID": 1,
                "position": 1,
                "textlabel": "Low"
            }
        )
    
class TestFeedback(unittest.TestCase):
    def test_json(self):
        feedback = Feedback(
            feedback_ID = 1,
            feedback_Template_ID = 1,
            submitted_By = 1,
            template_Attribute_ID = 1,
            answer = "4",
            rcourse_ID = 1
        )

        self.assertEqual(feedback.json(), {
                "feedback_ID": 1,
                "feedback_Template_ID": 1,
                "submitted_By": 1,
                "template_Attribute_ID": 1,
                "answer": "4",
                "rcourse_ID": 1
            }
        )
    
class TestRunCourse(unittest.TestCase):
    def test_json(self):
        runCourse = RunCourse(
            run_Name = 'test',
            run_Startdate = '2023-07-10',
            run_Enddate = '2023-07-12',
            run_Starttime = '12:00:00',
            run_Endtime = '14:00:00',
            instructor_ID = 4,
            course_Format = 'face-to-face',
            course_Venue = 'SCIS SR 2-4',
            runcourse_Status = 'Closed',
            course_Size = 35,
            course_Minsize = 20,
            course_Fee = 0,
            class_Duration = 2,
            reg_Startdate = '2023-06-05',
            reg_Enddate = '2023-06-10',
            reg_Starttime = '10:00:00',
            reg_Endtime = '10:00:00',
            feedback_Startdate = '2023-07-13',
            feedback_Enddate = '2023-07-20',
            feedback_Starttime = '10:00:00',
            feedback_Endtime = '10:00:00',
            course_ID = 1,
            template_ID = 2
        )

        self.assertEqual(runCourse.json(), {
                "rcourse_ID": None,
                "run_Name": 'test',
                "run_Startdate": '2023-07-10',
                "run_Enddate": '2023-07-12',
                "run_Starttime": '12:00:00',
                "run_Endtime": '14:00:00',
                "instructor_ID": 4,
                "course_Format": 'face-to-face',
                "course_Venue": 'SCIS SR 2-4',
                "runcourse_Status": 'Closed',
                "course_Size": 35,
                "course_Minsize": 20,
                "course_Fee": 0,
                "class_Duration": 2,
                "reg_Startdate": '2023-06-05',
                "reg_Enddate": '2023-06-10',
                "reg_Starttime": '10:00:00',
                "reg_Endtime": '10:00:00',
                "feedback_Startdate": '2023-07-13',
                "feedback_Enddate": '2023-07-20',
                "feedback_Starttime": '10:00:00',
                "feedback_Endtime": '10:00:00',
                "course_ID": 1,
                "template_ID": 2
            }
        )
    
class TestRegistration(unittest.TestCase):
    def test_json(self):
        registration = Registration(
            rcourse_ID = 1,
            user_ID = 1,
            reg_Status = 'Enrolled'
        )

        self.assertEqual(registration.json(), {
                "reg_ID": None,
                "rcourse_ID": 1,
                "user_ID": 1,
                "reg_Status": 'Enrolled'
            }
        )
    
class TestLesson(unittest.TestCase):
    def test_json(self):
        lesson = Lesson(
            lesson_ID = 1,
            reg_ID = 1,
            lesson_Date = '2023-07-10',
            lesson_Time = '12:00:00'
        )

        self.assertEqual(lesson.json(), {
                "lesson_ID": 1,
                "reg_ID": 1,
                "lesson_Date": '2023-07-10',
                "lesson_Time": '12:00:00'
            }
        )
    
class TestAttendenceRecord(unittest.TestCase):
    def test_json(self):
        attendenceRecord = AttendenceRecord(
            attrecord_ID = 1,
            lesson_ID = 1,
            status = 'Present',
            reason = None,
            attrecord_Status = 'Submitted'
        )

        self.assertEqual(attendenceRecord.json(), {
                "attrecord_ID": 1,
                "lesson_ID": 1,
                "status": 'Present',
                "reason": None,
                "attrecord_Status": 'Submitted'
            }
        )
    
class TestBlacklist(unittest.TestCase):
    def test_json(self):
        blacklist = Blacklist(
            user_ID = 7
        )

        self.assertEqual(blacklist.json(), {
                "blacklist_ID": None,
                "user_ID": 7
            }
        )
    
class TestContactUs(unittest.TestCase):
    def test_json(self):
        contactUs = ContactUs(
            user_ID = 1,
            msg_Subject = "Test",
            msg_Body = "Testing the contact us function",
            msg_Datetime = "2023-08-25 17:00:00"
        )

        self.assertEqual(contactUs.json(), {
                "msg_ID": None,
                "user_ID": 1,
                "msg_Subject": "Test",
                "msg_Body": "Testing the contact us function",
                "msg_Datetime": "2023-08-25 17:00:00"
            }
        )


if __name__ == "__main__":
    unittest.main()
