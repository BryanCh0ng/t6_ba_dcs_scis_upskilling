from flask import request, jsonify, session
from flask_restx import Namespace, Resource, fields
from allClasses import *
from datetime import datetime, date, time
from sqlalchemy import desc, func, select
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

import re
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer

import logging
app.logger.setLevel(logging.DEBUG)

api = Namespace('recommender', description='Recommender')

def preprocess_text(text):
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text).lower()
    tokens = word_tokenize(text)
    return ' '.join(tokens)

recommender_user_similarity = api.parser()
recommender_user_similarity.add_argument("user_ID", help="Enter user ID")
@api.route("/user_similarity_registration")
@api.doc(description="Recommender function based on user similarity based on student registration")
class RecommenderUserRegistration(Resource):
    @api.expect(recommender_user_similarity)
    def get(self):
        arg = recommender_user_similarity.parse_args().get("user_ID")
        target_user_id = int(arg) if arg else ""
        
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
        df = df.drop_duplicates(subset=["user_ID", "rcourse_ID"])
        df["registered"] = 1
        pivot_df = df.pivot(index="user_ID", columns="rcourse_ID", values="registered").fillna(0).astype(int)
        pivot_df.reset_index(inplace=True)
        pivot_df.columns.name = None 
        pivot_df.set_index("user_ID", inplace=True)

        #cosine similarity table
        user_similarity = cosine_similarity(pivot_df)
        user_similarity_df = pd.DataFrame(user_similarity, index=pivot_df.index, columns=pivot_df.index)

        user_ID = session.get('user_ID')

        reg_courses = Registration.query.filter(
            Registration.user_ID == user_ID,
            Registration.reg_Status.in_(["Enrolled", "Pending"])
        ).all()

        if not reg_courses:
            return jsonify({"code": 200, "data": {"course_list": []}})
        
        rcourse_ids = [course.rcourse_ID for course in reg_courses]
        
        
        def recommend_courses(user, num_recommendations):
            if user not in pivot_df.index:
                return []
            else:
                user_courses = pivot_df.loc[user]

                similar_users = user_similarity_df[user].sort_values(ascending=False)[1:]
                
                recommended_courses = set()
                for similar_user, similarity_score in similar_users.items():
                    if similarity_score > 0:
                        similar_user_courses = pivot_df.loc[similar_user]
                        for course, registration in similar_user_courses.items():
                            if ( registration == 1 and user_courses[course] == 0):
                                registration_status = Registration.query.filter(
                                    (Registration.user_ID == similar_user) &
                                    (Registration.rcourse_ID == course)
                                ).first().reg_Status
                                
                                if registration_status not in ["Pending", "Enrolled"]:
                                    rcourse = RunCourse.query.filter(RunCourse.rcourse_ID == course).first()
                                    if rcourse and rcourse.runcourse_Status == "Ongoing" and course not in rcourse_ids:
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
                coursecat = CourseCategory.query.filter(CourseCategory.coursecat_ID == course.coursecat_ID).first()
                datapoint = course.json()
                
                datapoint["coursecat_Name"] = coursecat.coursecat_Name
                datapoint["rcourse_ID"] = recommondations_rcourse_id

                for field in rcourse.keys():
                    if isinstance(rcourse[field], time):
                        # Convert time objects to strings
                        datapoint[field] = str(rcourse[field])
                    else:
                        datapoint[field] = rcourse[field]
               
                datapoint["reg_Startdate"] = format_date_time(rcourse["reg_Startdate"])
                datapoint["reg_Enddate"] = format_date_time(rcourse["reg_Enddate"])
                datapoint["run_Startdate"] = format_date_time(rcourse["run_Startdate"])
                datapoint["run_Enddate"] = format_date_time(rcourse["run_Enddate"])
                datapoint["reg_Starttime"] = format_date_time(rcourse["reg_Starttime"])
                datapoint["reg_Endtime"] = format_date_time(rcourse["reg_Endtime"])
                datapoint["run_Starttime"] = format_date_time(rcourse["run_Starttime"])
                datapoint["run_Endtime"] = format_date_time(rcourse["run_Endtime"])
                datapoint["feedback_Startdate"] = format_date_time(rcourse["feedback_Startdate"])
                datapoint["feedback_Enddate"] = format_date_time(rcourse["feedback_Enddate"])
                datapoint["feedback_Startime"] = format_date_time(rcourse["feedback_Startime"])
                datapoint["feedback_Endtime"] = format_date_time(rcourse["feedback_Endtime"])

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
        try:
            # Extract the last 3 registered courses from the request JSON
            course_list_req = request.json['params']['course_list_req']
            if not course_list_req:
                return jsonify({"code": 200, "data": {"course_list": []}})
            
            last_three_reg = request.json['params']['course_list_req'][-3:]
            
            rcourse_id_list = [course['rcourse_ID'] for course in last_three_reg]

            user_ID = session.get('user_ID')

            # Fetch user registration data
            regList = Registration.query.all()
            reg_list = []
            
            for reg in regList:
                rcourse_id = reg.rcourse_ID
                userid = reg.user_ID
                registered_course = (
                    db.session.query(Course, RunCourse)
                    .join(RunCourse, Course.course_ID == RunCourse.course_ID)
                    .join(Registration, RunCourse.rcourse_ID == Registration.rcourse_ID)
                    .filter(Registration.user_ID == userid, Registration.rcourse_ID == rcourse_id)
                    .first()
                )

                if registered_course:
                    course_info = registered_course[0].json() 
                    datapoint = {
                        "rcourse_ID": rcourse_id,
                        "user_ID": userid,
                        "course_Name": preprocess_text(course_info["course_Name"]), 
                        "course_Desc": preprocess_text(course_info["course_Desc"],) 
                    }
                    reg_list.append(datapoint)
                else:
                    return jsonify({"code": 200, "data": {"course_list": []}})
            

            # Create a user-course interaction matrix
            df = pd.DataFrame(reg_list)
            df = df.drop_duplicates(subset=['rcourse_ID', 'user_ID'])
            df["registered"] = 1
            pivot_df = df.pivot(index="rcourse_ID", columns="user_ID", values="registered").fillna(0).astype(int)

            # Get the course descriptions
            course_descriptions = [
                preprocess_text(Course.query.filter(Course.course_ID == course_id).first().course_Desc)
                for course_id in pivot_df.index
            ]

            # TF-IDF vectorization of course descriptions
            tfidf_vectorizer = TfidfVectorizer()
            tfidf_matrix = tfidf_vectorizer.fit_transform(course_descriptions)

            # Compute cosine similarity based on TF-IDF vectors
            course_similarity = cosine_similarity(tfidf_matrix, tfidf_matrix)
            course_similarity_df = pd.DataFrame(course_similarity, index=pivot_df.index, columns=pivot_df.index)

            # Get a list of courses the user is registered for (excluding dropped courses)
            reg_courses = Registration.query.filter(
                Registration.user_ID == user_ID,
                Registration.reg_Status.in_(["Enrolled", "Pending"])
            ).all()
            rcourse_ids = [course.rcourse_ID for course in reg_courses]

            # Function to recommend courses for a target course
            def recommend_courses(target_course_id):
                similarity_scores = course_similarity_df[target_course_id]
                similar_courses = similarity_scores.drop(target_course_id).sort_values(ascending=False)
                recommended_courses = []

                for course, score in similar_courses.items():
                    if course not in rcourse_ids:
                        rcourse = RunCourse.query.filter(RunCourse.rcourse_ID == course).first()
                        course_ids = [course['course_ID'] for course in course_list_req]
                        # print(course_ids)
                        if rcourse and rcourse.runcourse_Status == "Ongoing" and rcourse.rcourse_ID not in course_ids:
                            recommended_courses.append(course)

                return recommended_courses

            course_dict = {}
            for course in rcourse_id_list:
                similar_courses = recommend_courses(course)

                for similar_course in similar_courses:
                    if similar_course not in course_dict:
                        course_dict[similar_course] = 1
                    else:
                        course_dict[similar_course] += 1

            # Sort recommended courses by count
            sorted_dict = dict(sorted(course_dict.items(), key=lambda item: item[1], reverse=True))

            # Generate a list of recommended courses with additional information
            course_list = []
            for recommended_rcourse_id in sorted_dict:
                rcourse = RunCourse.query.filter(RunCourse.rcourse_ID == recommended_rcourse_id).first()
                rcourse = rcourse.json()
                course_id = rcourse["course_ID"]
                course = Course.query.filter(Course.course_ID == course_id).first()
                coursecat = CourseCategory.query.filter(CourseCategory.coursecat_ID == course.coursecat_ID).first()
                datapoint = course.json()
                
                datapoint["coursecat_Name"] = coursecat.coursecat_Name
                datapoint["rcourse_ID"] = recommended_rcourse_id

                for field in rcourse.keys():
                    if isinstance(rcourse[field], time):
                        # Convert time objects to strings
                        datapoint[field] = str(rcourse[field])
                    else:
                        datapoint[field] = rcourse[field]
               
                datapoint["reg_Enddate"] = format_date_time(rcourse["reg_Enddate"])
                datapoint["run_Startdate"] = format_date_time(rcourse["run_Startdate"])
                datapoint["run_Enddate"] = format_date_time(rcourse["run_Enddate"])
                datapoint["reg_Endtime"] = format_date_time(rcourse["reg_Endtime"])
                datapoint["run_Starttime"] = format_date_time(rcourse["run_Starttime"])
                datapoint["run_Endtime"] = format_date_time(rcourse["run_Endtime"])
                datapoint["feedback_Startdate"] = format_date_time(rcourse["feedback_Startdate"])
                datapoint["feedback_Enddate"] = format_date_time(rcourse["feedback_Enddate"])
                datapoint["feedback_Startime"] = format_date_time(rcourse["feedback_Startime"])
                datapoint["feedback_Endtime"] = format_date_time(rcourse["feedback_Endtime"])

                course_list.append(datapoint)

            db.session.close()

            return jsonify({"code": 200, "data": {"course_list": course_list}})

        except KeyError:
            return jsonify({"code": 404, "message": "Course does not exist"})

        
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
            
            if user not in pivot_df.index:
                return []
            else:
                user_courses = pivot_df.loc[user]
            
                similar_users = user_similarity_df[user].sort_values(ascending=False)[1:]
                
                recommended_courses = set()  
                for similar_user, similarity_score in similar_users.items():
                    if similarity_score > 0:
                        similar_user_courses = pivot_df.loc[similar_user]
                        for course, registration in similar_user_courses.items():
                            if registration == 1 and user_courses[course] == 0:
                                vcourse = VoteCourse.query.filter(VoteCourse.course_ID == course).first()
                                if vcourse and vcourse.vote_Status == "Ongoing":
                                    recommended_courses.add(course)
                                    if len(recommended_courses) == num_recommendations:
                                        return list(recommended_courses) 
                
                return list(recommended_courses)  
        
        try:
            recommendations_courses_id = recommend_courses(target_user_id, 10)
            if (len(recommendations_courses_id) == 0):
                return jsonify({"code": 200, "data": {"course_list": []}})
            
            course_list = []
            for recommondations_course_id in recommendations_courses_id:
                course = Course.query.filter(Course.course_ID == recommondations_course_id).first()
                coursecat = CourseCategory.query.filter(CourseCategory.coursecat_ID == course.coursecat_ID).first()
                vcourse = VoteCourse.query.filter(VoteCourse.course_ID == recommondations_course_id).first()
                vcourse = vcourse.json()
                datapoint = course.json()
                
                datapoint["coursecat_Name"] = coursecat.coursecat_Name
                for field in vcourse.keys():
                    datapoint[field] = vcourse[field]

                course_list.append(datapoint)

            db.session.close()
            
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "course_list": course_list[:10]
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
@api.doc(description="Recommender function based on improved course similarity based on student interest")
class ImprovedRecommenderCourseInterest(Resource):
    def post(self):
        try:
            # [courseid1, courseid2, courseid3]
            course_list_req = request.json['params']['course_list_req']
        
            if not course_list_req:
                return jsonify({"code": 200, "data": {"course_list": []}})
            
            last_three_voted = request.json['params']['course_list_req'][-3:] # based on the last 3 interested courses
            vcourse_id_list = [course['course_ID'] for course in last_three_voted]
            
            # Fetch all users and their course interests
            interest_list = self.get_interest_data()

            # Create a user-course interaction matrix
            pivot_df = self.create_user_course_matrix(interest_list)

            # Calculate improved course similarity
            course_similarity_df = self.calculate_course_similarity(pivot_df)

            # Recommend courses based on similarity
            recommended_courses = self.recommend_courses(vcourse_id_list, course_similarity_df, course_list_req)
            
            
            return jsonify({"code": 200, "data": {"course_list": recommended_courses[:10]}})
        except Exception as e:
            return jsonify({"code": 404, "message": "Course does not exist"})


    def get_interest_data(self):
        try:
            interest_list = []
            users = User.query.all()

            for user in users:
                user_id = user.user_ID
                user_interests = (
                    db.session.query(Course, VoteCourse)
                    .join(VoteCourse, Course.course_ID == VoteCourse.course_ID)
                    .join(Interest, VoteCourse.vote_ID == Interest.vote_ID)
                    .filter(Interest.user_ID == user_id)
                    .all()
                )
                
                if user_interests:
                    for course, _ in user_interests:
                        course = course.json()
                        course_id = course['course_ID']
                        
                        course_name = preprocess_text(course['course_Name'])
                        course_desc = preprocess_text(course['course_Desc'])
                        
                        interest_list.append(
                            {"course_ID": course_id, "user_ID": user_id, "course_name": course_name, "course_desc": course_desc}
                        )
                else:
                    return jsonify({"code": 200, "data": {"course_list": []}})
                
                return interest_list
                
        except KeyError:
            return jsonify({"code": 404, "message": "No interest data"})

    def create_user_course_matrix(self, interest_list):
        df = pd.DataFrame(interest_list)
        df["registered"] = 1
        pivot_df = df.pivot(index="course_ID", columns="user_ID", values="registered").fillna(0).astype(int)
        
        return pivot_df

    # content-based similarity - course desc
    def calculate_course_similarity(self, pivot_df):
        try:
            # Get the course descriptions
            course_descriptions = [
                preprocess_text(Course.query.filter(Course.course_ID == course_id).first().course_Desc)
                for course_id in pivot_df.index
            ]

            # TF-IDF vectorization of course descriptions
            tfidf_vectorizer = TfidfVectorizer()
            tfidf_matrix = tfidf_vectorizer.fit_transform(course_descriptions)

            # Compute cosine similarity based on TF-IDF vectors
            course_similarity = cosine_similarity(tfidf_matrix, tfidf_matrix)
            course_similarity_df = pd.DataFrame(course_similarity, index=pivot_df.index, columns=pivot_df.index)
            
            return course_similarity_df
        except Exception as e:
            raise e

    def recommend_courses(self, vcourse_id_list, course_similarity_df, course_list_req):
        try:
            course_dict = {}
            
            for course in vcourse_id_list:
                
                similar_courses = course_similarity_df[course].sort_values(ascending=False)[1:]
                for similar_course, score in similar_courses.items():
                    vcourse = VoteCourse.query.filter(VoteCourse.course_ID == similar_course).first()
                    course_ids = [course['course_ID'] for course in course_list_req]
                    if vcourse and vcourse.vote_Status == "Ongoing" and similar_course not in course_ids:
                        if similar_course not in course_dict:
                            course_dict[similar_course] = 1
                        else:
                            course_dict[similar_course] += 1
            
            sorted_dict = dict(sorted(course_dict.items(), key=lambda item: item[1], reverse=True))
                
            course_list = []

            for recommended_course_id in sorted_dict:
                course = Course.query.filter(Course.course_ID == recommended_course_id).first()
                coursecat = CourseCategory.query.filter(CourseCategory.coursecat_ID == course.coursecat_ID).first()
                vcourse = VoteCourse.query.filter(VoteCourse.course_ID == recommended_course_id).first()
                vcourse = vcourse.json()

                datapoint = course.json()
                datapoint["coursecat_Name"] = coursecat.coursecat_Name
                for field in vcourse.keys():
                    datapoint[field] = vcourse[field]
                        
                course_list.append(datapoint)
                    

            db.session.close()
                
            return course_list
            
        except KeyError:
            return jsonify({"code": 404, "message": "Course does not exist"})

# Top 10 Courses avail for Registration
retrieve_top_10_register_course = api.parser()
retrieve_top_10_register_course.add_argument("user_id", type=int, help="Enter user ID")

@api.route("/get_top_10_course_avail_for_register")
@api.doc(description="Get top 10 courses by registration count")
class GetTop10CoursesByRegistrationCount(Resource):
    @api.expect(retrieve_top_10_register_course)
    def get(self):
        args = retrieve_top_10_register_course.parse_args()
        
        user_ID = args.get("user_id")

        current_datetime = datetime.now()
        current_time = current_datetime.strftime('%H:%M:%S')

        valid_reg_statuses = ["pending", "enrolled", "not enrolled"]

        registered_course_ids = db.session.query(Registration.rcourse_ID).filter(
            Registration.user_ID == user_ID,
            Registration.reg_Status.in_(valid_reg_statuses)
        ).subquery()

        register = db.session.query(
            Course,
            RunCourse,
            func.coalesce(func.count(Registration.reg_ID), 0).label("registration_count")
        ).select_from(Course).join(RunCourse, Course.course_ID == RunCourse.course_ID).outerjoin(
            Registration, RunCourse.rcourse_ID == Registration.rcourse_ID
        ).join(CourseCategory, Course.coursecat_ID == CourseCategory.coursecat_ID).group_by(Course.course_ID, RunCourse.rcourse_ID).subquery()

        query = db.session.query(
            Course,
            CourseCategory.coursecat_Name,
            RunCourse,
            register.c.registration_count
        ).select_from(Course).join(RunCourse, Course.course_ID == RunCourse.course_ID).join(
            CourseCategory, Course.coursecat_ID == CourseCategory.coursecat_ID
        ).outerjoin(
            register,
            RunCourse.rcourse_ID == register.c.rcourse_ID
        ).filter(
            ~RunCourse.rcourse_ID.in_(select([registered_course_ids])),
            Course.course_Status == "active",
            RunCourse.runcourse_Status == "ongoing",
            RunCourse.reg_Enddate >= current_datetime.date(),
            (RunCourse.reg_Enddate > current_datetime.date()) | (RunCourse.reg_Endtime > current_time),
        ).order_by(
            register.c.registration_count.desc()
        ).limit(10)

        results = query.all()
        db.session.close()

        if results:
            result_data = []
            for result in results:
                run_course_attrs = {
                    'run_Startdate': format_date_time(result[2].run_Startdate),
                    'run_Enddate': format_date_time(result[2].run_Enddate),
                    'run_Starttime': format_date_time(result[2].run_Starttime),
                    'run_Endtime': format_date_time(result[2].run_Endtime),
                    'reg_Startdate': format_date_time(result[2].reg_Startdate),
                    'reg_Enddate': format_date_time(result[2].reg_Enddate),
                    'reg_Starttime': format_date_time(result[2].reg_Starttime),
                    'reg_Endtime': format_date_time(result[2].reg_Endtime),
                    'feedback_Startdate': format_date_time(result[2].feedback_Startdate),
                    'feedback_Enddate': format_date_time(result[2].feedback_Enddate),
                    'feedback_Starttime': format_date_time(result[2].feedback_Starttime),
                    'feedback_Endtime': format_date_time(result[2].feedback_Endtime)
                }

                modified_run_course = {**result[2].json(), **run_course_attrs}

                course_info = {
                    **result[0].json(),
                    "coursecat_Name": result[1],
                    **modified_run_course,
                    "registration_count": result[3]
                }
                result_data.append(course_info)
            return jsonify({"code": 200, "data": result_data})

        return jsonify({"code": 404, "message": "No courses found"})

# Top 10 Courses available for voting
retrieve_top_10_interest_course = api.parser()
retrieve_top_10_interest_course.add_argument("user_id", type=int, help="Enter user ID")

@api.route("/get_top_10_course_avail_for_voting")
@api.doc(description="Get top 10 course avail for voting")
class GetUnvotedOngoingCourses(Resource):
    @api.expect(retrieve_top_10_interest_course)
    def get(self):
        args = retrieve_top_10_interest_course.parse_args()
        user_ID = args.get("user_id", "")

        # app.logger.debug(user_ID)

        voted_course_ids = db.session.query(Interest.vote_ID).filter_by(user_ID=user_ID).subquery()

        vote_counts_subquery = db.session.query(
            VoteCourse.course_ID,
            func.count(Interest.interest_ID).label("vote_count")
        ).join(Interest, VoteCourse.vote_ID == Interest.vote_ID) \
        .group_by(VoteCourse.course_ID).subquery()

        # Construct the query for unvoted courses with ongoing vote status
        query = db.session.query(
            Course,
            CourseCategory.coursecat_Name,
            VoteCourse,
            vote_counts_subquery.c.vote_count
        ).select_from(Course).join(VoteCourse, Course.course_ID == VoteCourse.course_ID).join(
            CourseCategory, Course.coursecat_ID == CourseCategory.coursecat_ID
        ).outerjoin(
            vote_counts_subquery,
            Course.course_ID == vote_counts_subquery.c.vote_count
        ).filter(
            ~VoteCourse.vote_ID.in_(select([voted_course_ids])),
            VoteCourse.vote_Status == "ongoing"
        ).order_by(
            vote_counts_subquery.c.vote_count.desc()
        ).limit(10)

        results = query.all()
        db.session.close()

        if results:
            result_data = []
            for result in results:
                course_info = {
                    **result[0].json(),
                    "coursecat_Name": result[1],
                    **result[2].json(),
                    "vote_count": result[3]
                }
                result_data.append(course_info)
            return jsonify({"code": 200, "data": result_data})

        return jsonify({"code": 404, "message": "No courses found"})
    
# Student Registration Search - course name, course cat, status
retrieve_registration_info_filter_search = api.parser()
retrieve_registration_info_filter_search.add_argument("user_id", type=int, help="Enter user ID")

@api.route("/get_course_registration_info")
@api.doc(description="Get course registration information")
class GetCourseRegistrationInfo(Resource):
    @api.expect(retrieve_registration_info_filter_search)
    def get(self):
        args = retrieve_registration_info_filter_search.parse_args()
        user_ID = args.get("user_id")

        current_datetime = datetime.now()

        valid_reg_statuses = ["enrolled", "pending"]

        query = db.session.query(
            Course,
            CourseCategory.coursecat_Name,
            RunCourse,
            Registration
        ).select_from(Course).join(RunCourse, Course.course_ID == RunCourse.course_ID).join(
            Registration, RunCourse.rcourse_ID == Registration.rcourse_ID
        ).join(CourseCategory, Course.coursecat_ID == CourseCategory.coursecat_ID)  \
            .filter(RunCourse.run_Enddate > current_datetime,
                    Registration.reg_Status.in_(valid_reg_statuses))

        if user_ID:
            query = query.filter(Registration.user_ID == user_ID)
       
        
        results = query.all()
        

        if results:
            result_data = []
            for result in results:
                run_course_attrs = {
                    "run_Startdate": result[2].run_Startdate.strftime('%Y-%m-%d'),
                    "run_Enddate": result[2].run_Enddate.strftime('%Y-%m-%d'),
                    "run_Starttime": result[2].run_Starttime.strftime('%H:%M:%S'),
                    "run_Endtime": result[2].run_Endtime.strftime('%H:%M:%S'),
                    "reg_Startdate": result[2].reg_Startdate.strftime('%Y-%m-%d'),
                    "reg_Enddate": result[2].reg_Enddate.strftime('%Y-%m-%d'),
                    "reg_Starttime": result[2].reg_Starttime.strftime('%H:%M:%S'),
                    "reg_Endtime": result[2].reg_Endtime.strftime('%H:%M:%S'),
                    "feedback_Startdate": result[2].feedback_Startdate.strftime('%Y-%m-%d'),
                    "feedback_Enddate": result[2].feedback_Enddate.strftime('%Y-%m-%d'),
                    "feedback_Starttime": result[2].feedback_Starttime.strftime('%H:%M:%S'),
                    "feedback_Endtime": result[2].feedback_Endtime.strftime('%H:%M:%S')
                }

                modified_run_course = {**result[2].json(), **run_course_attrs}

                course_info = {
                    **result[0].json(),
                    "coursecat_Name": result[1],
                    **modified_run_course,
                    **result[3].json()
                }
                result_data.append(course_info)
            # app.logger.debug("Debug message")
            # app.logger.debug(result_data)
            return jsonify({"code": 200, "data": result_data})

        
        return jsonify({"code": 404, "message": "No matching course registration information found"})
    
def format_date_time(value):
    if isinstance(value, (date, datetime)):
        return value.strftime('%Y-%m-%d')
    elif isinstance(value, time):
        return value.strftime('%H:%M:%S')
    else:
        return None