from flask import request, jsonify, sessions
from flask_restx import Namespace, Resource, fields
from allClasses import *

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

api = Namespace('recommender', description='Recommender')

# data = pd.read_csv(r'C:\Users\yakry\Desktop\RawData2021.csv')
# data.columns = ["Name", "Quantum Leap", "FISCOS BCOS Blockchain", "Python Programming for Data Analysis", "Cybersecurity - Introduction to SSL Certificates"]

recommender_user_similarity = api.parser()
recommender_user_similarity.add_argument("user_ID", help="Enter user ID")
@api.route("/user_similarity_registration")
@api.doc(description="Recommender function based on user similarity based on student registration")
class RecommenderUserRegistration(Resource):
    @api.expect(recommender_user_similarity)
    def get(self):
        arg = recommender_user_similarity.parse_args().get("user_ID")
        target_user_id = int(arg) if arg else ""

        #userid as rows and courseid as columns
        regList = Registration.query.all()
        reg_list = []
        for reg in regList:
            reg = reg.json()
            rcourseid = reg["rcourse_ID"]
            userid = reg["user_ID"]
            datapoint = {
                "rcourse_ID": rcourseid,
                "user_ID": userid
            }
            reg_list.append(datapoint)

        #put into dataframe
        df = pd.DataFrame(reg_list)
        df["registered"] = 1
        pivot_df = df.pivot(index="user_ID", columns="rcourse_ID", values="registered").fillna(0).astype(int)
        pivot_df.reset_index(inplace=True)
        pivot_df.columns.name = None 
        pivot_df.set_index("user_ID", inplace=True)

        #cosine similarity table
        user_similarity = cosine_similarity(pivot_df)
        user_similarity_df = pd.DataFrame(user_similarity, index=pivot_df.index, columns=pivot_df.index)

        def recommend_courses(user, num_recommendations):
            user_courses = pivot_df.loc[user]
            similar_users = user_similarity_df[user].sort_values(ascending=False)[1:]  
            
            recommended_courses = set()  
            for similar_user, similarity_score in similar_users.iteritems():
                if similarity_score > 0:
                    similar_user_courses = pivot_df.loc[similar_user]
                    for course, registration in similar_user_courses.iteritems():
                        if registration == 1 and user_courses[course] == 0:
                            recommended_courses.add(course)
                            if len(recommended_courses) == num_recommendations:
                                return list(recommended_courses) 
            
            return list(recommended_courses)  

        try:
            recommendations_rcourses_id = recommend_courses(target_user_id, 10)
            course_list = []
            for recommondations_rcourse_id in recommendations_rcourses_id:
                rcourse = RunCourse.query.filter(RunCourse.rcourse_ID == recommondations_rcourse_id).first()
                rcourse = rcourse.json()
                course_id = rcourse["course_ID"]
                course = Course.query.filter(Course.course_ID == course_id).first()
                datapoint = course.json()

                datapoint["rcourse_ID"] = recommondations_rcourse_id
                datapoint["run_Startdate"] = rcourse["run_Startdate"]
                datapoint["run_Enddate"] = rcourse["run_Enddate"]
                datapoint["run_Starttime"] = rcourse["run_Starttime"].strftime('%H:%M:%S')
                datapoint["run_Endtime"] = rcourse["run_Endtime"].strftime('%H:%M:%S')

                course_list.append(datapoint)

            db.session.close()
            
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "course_list": course_list
                    }
                }
            )
        except KeyError:
            return jsonify(
                {
                    "code": 404,
                    "message": "User does not exist"
                }
            )
        

@api.route("/course_similarity_registration")
@api.doc(description="Recommender function based on course similarity based on student registration")
class RecommenderCourseRegistration(Resource): 
    def post(self):
        # [rcourseid1, rcourseid2, rcourseid3]
        course_list_req = request.json

        #userid as rows and courseid as columns
        regList = Registration.query.all()
        reg_list = []
        for reg in regList:
            reg = reg.json()
            rcourseid = reg["rcourse_ID"]
            userid = reg["user_ID"]
            datapoint = {
                "rcourse_ID": rcourseid,
                "user_ID": userid
            }
            reg_list.append(datapoint)

        df = pd.DataFrame(reg_list)
        df["registered"] = 1
        pivot_df = df.pivot(index="rcourse_ID", columns="user_ID", values="registered").fillna(0).astype(int)
        pivot_df.reset_index(inplace=True)
        pivot_df.columns.name = None 
        pivot_df.set_index("rcourse_ID", inplace=True)

        #cosine similarity table
        course_similarity = cosine_similarity(pivot_df)
        course_similarity_df = pd.DataFrame(course_similarity, index=pivot_df.index, columns=pivot_df.index)

        def recommend_courses(target_course_id):
            similarity_scores = course_similarity_df[target_course_id]
            similar_courses = similarity_scores.drop(target_course_id).sort_values(ascending=False)
            recommended_courses = []
            for course, score in similar_courses.iteritems():
                recommended_courses.append(course)
            return recommended_courses

        try: 
            course_dict = {}
            for course in course_list_req:
                similar_courses = recommend_courses(course)
                
                for similar_course in similar_courses:
                    if similar_course not in course_dict:
                        course_dict[similar_course] = 1
                    else:
                        course_dict[similar_course] += 1
            # {rcourseid1: 4, rcourseid2: 2, rcourseid3: 1}
            sorted_dict = dict(sorted(course_dict.items(), key=lambda item: item[1], reverse=True))
            print(sorted_dict)
            
            # descending order (most significant -> least)
            course_list = []
            for recommondations_rcourse_id in sorted_dict:
                rcourse = RunCourse.query.filter(RunCourse.rcourse_ID == recommondations_rcourse_id).first()
                rcourse = rcourse.json()
                course_id = rcourse["course_ID"]
                course = Course.query.filter(Course.course_ID == course_id).first()
                datapoint = course.json()

                datapoint["rcourse_ID"] = recommondations_rcourse_id
                datapoint["run_Startdate"] = rcourse["run_Startdate"]
                datapoint["run_Enddate"] = rcourse["run_Enddate"]
                datapoint["run_Starttime"] = rcourse["run_Starttime"].strftime('%H:%M:%S')
                datapoint["run_Endtime"] = rcourse["run_Endtime"].strftime('%H:%M:%S')

                course_list.append(datapoint)

            db.session.close()
            
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "course_list": course_list
                    }
                }
            )

        except KeyError:
            return jsonify(
                {
                    "code": 404,
                    "message": "Course does not exist"
                }
            )

recommender_user_similarity_interest = api.parser()
recommender_user_similarity_interest.add_argument("user_ID", help="Enter user ID")
@api.route("/user_similarity_interest")
@api.doc(description="Recommender function based on user similarity based on student interest")
class RecommenderUserInterest(Resource):
    @api.expect(recommender_user_similarity_interest)
    def get(self):
        arg = recommender_user_similarity_interest.parse_args().get("user_ID")
        target_user_id = int(arg) if arg else ""

        interest_list = []
        userList = User.query.all()
        for user in userList:
            user = user.json()
            user_id = user["user_ID"]

            query = db.session.query(
                Course,
                VoteCourse
            ).select_from(Course).join(VoteCourse, Course.course_ID == VoteCourse.course_ID).join(
                Interest, VoteCourse.vote_ID == Interest.vote_ID)
            
            query = query.filter(Interest.user_ID == user_id)
            results = query.all()
            
            for res in results:
                course_id = res[0].json()["course_ID"]

                datapoint = {
                    "course_ID": course_id,
                    "user_ID": user_id
                }

                interest_list.append(datapoint)
        
        df = pd.DataFrame(interest_list)
        df["registered"] = 1
        pivot_df = df.pivot(index="user_ID", columns="course_ID", values="registered").fillna(0).astype(int)
        pivot_df.reset_index(inplace=True)
        pivot_df.columns.name = None 
        pivot_df.set_index("user_ID", inplace=True)


        user_similarity = cosine_similarity(pivot_df)
        user_similarity_df = pd.DataFrame(user_similarity, index=pivot_df.index, columns=pivot_df.index)

        def recommend_courses(user, num_recommendations):
            user_courses = pivot_df.loc[user]
            similar_users = user_similarity_df[user].sort_values(ascending=False)[1:]
            
            recommended_courses = set()  
            for similar_user, similarity_score in similar_users.iteritems():
                if similarity_score > 0:
                    similar_user_courses = pivot_df.loc[similar_user]
                    for course, registration in similar_user_courses.iteritems():
                        if registration == 1 and user_courses[course] == 0:
                            recommended_courses.add(course)
                            if len(recommended_courses) == num_recommendations:
                                return list(recommended_courses) 
            
            return list(recommended_courses)  
        
        try:
            recommendations_courses_id = recommend_courses(target_user_id, 10)
            course_list = []
            for recommondations_course_id in recommendations_courses_id:
                course = Course.query.filter(Course.course_ID == recommondations_course_id).first()
                course_data = course.json()

                course_list.append(course_data)

            db.session.close()
            
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "course_list": course_list
                    }
                }
            )
        except KeyError:
            return jsonify(
                {
                    "code": 404,
                    "message": "User does not exist"
                }
            )

@api.route("/course_similarity_interest")
@api.doc(description="Recommender function based on course similarity based on student interest")
class RecommenderCourseInterest(Resource): 
    def post(self):
        # [courseid1, courseid2, courseid3]
        course_list_req = request.json

        #userid as rows and courseid as columns
        interest_list = []
        userList = User.query.all()
        for user in userList:
            user = user.json()
            user_id = user["user_ID"]

            query = db.session.query(
                Course,
                VoteCourse
            ).select_from(Course).join(VoteCourse, Course.course_ID == VoteCourse.course_ID).join(
                Interest, VoteCourse.vote_ID == Interest.vote_ID)
            
            query = query.filter(Interest.user_ID == user_id)
            results = query.all()
            
            for res in results:
                course_id = res[0].json()["course_ID"]

                datapoint = {
                    "course_ID": course_id,
                    "user_ID": user_id
                }

                interest_list.append(datapoint)

        df = pd.DataFrame(interest_list)
        df["registered"] = 1
        pivot_df = df.pivot(index="course_ID", columns="user_ID", values="registered").fillna(0).astype(int)
        pivot_df.reset_index(inplace=True)
        pivot_df.columns.name = None 
        pivot_df.set_index("course_ID", inplace=True)

        #cosine similarity table
        course_similarity = cosine_similarity(pivot_df)
        course_similarity_df = pd.DataFrame(course_similarity, index=pivot_df.index, columns=pivot_df.index)

        def recommend_courses(target_course_id):
            similarity_scores = course_similarity_df[target_course_id]
            similar_courses = similarity_scores.drop(target_course_id).sort_values(ascending=False)
            recommended_courses = []
            for course, score in similar_courses.iteritems():
                recommended_courses.append(course)
            return recommended_courses

        try: 
            course_dict = {}
            for course in course_list_req:
                similar_courses = recommend_courses(course)
                
                for similar_course in similar_courses:
                    if similar_course not in course_dict:
                        course_dict[similar_course] = 1
                    else:
                        course_dict[similar_course] += 1
            # {rcourseid1: 4, rcourseid2: 2, rcourseid3: 1}
            sorted_dict = dict(sorted(course_dict.items(), key=lambda item: item[1], reverse=True))
            print(sorted_dict)
            
            # descending order (most significant -> least)
            course_list = []
            for recommondations_course_id in sorted_dict:
                course = Course.query.filter(Course.course_ID == recommondations_course_id).first()
                course_data = course.json()

                course_list.append(course_data)

            db.session.close()
            
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "course_list": course_list
                    }
                }
            )

        except KeyError:
            return jsonify(
                {
                    "code": 404,
                    "message": "Course does not exist"
                }
            )