from flask import request, jsonify, session
from flask_restx import Namespace, Resource
from core_features import common
from allClasses import *
from datetime import datetime, date, time
from sqlalchemy import func, select
import pandas as pd
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

# ======================================================= Registration =======================================================

# Others like you also like
recommender_user_similarity = api.parser()
recommender_user_similarity.add_argument("user_ID", help="Enter user ID")
@api.route("/user_similarity_registration")
@api.doc(description="Recommender function based on user similarity based on student registration")
class RecommenderUserRegistration(Resource):
    @api.expect(recommender_user_similarity)
    def get(self):
        arg = recommender_user_similarity.parse_args().get("user_ID")
        target_user_id = int(arg) if arg else ""

        if target_user_id is None:
            return jsonify({"code": 404, "message": "User ID is required"})
        
        all_registration_list = Registration.query.filter(Registration.reg_Status.in_(['Enrolled', 'Pending'])).all()
        
        reg_list = []
        for reg in all_registration_list:
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

        reg_courses = Registration.query.filter(
            Registration.user_ID == target_user_id,
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
                                
                                if registration_status in ["Pending", "Enrolled"]:
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
               
                datapoint["reg_Startdate"] = common.format_date_time(rcourse["reg_Startdate"])
                datapoint["reg_Enddate"] = common.format_date_time(rcourse["reg_Enddate"])
                datapoint["run_Startdate"] = common.format_date_time(rcourse["run_Startdate"])
                datapoint["run_Enddate"] = common.format_date_time(rcourse["run_Enddate"])
                datapoint["reg_Starttime"] = common.format_date_time(rcourse["reg_Starttime"])
                datapoint["reg_Endtime"] = common.format_date_time(rcourse["reg_Endtime"])
                datapoint["run_Starttime"] = common.format_date_time(rcourse["run_Starttime"])
                datapoint["run_Endtime"] = common.format_date_time(rcourse["run_Endtime"])
                datapoint["feedback_Startdate"] = common.format_date_time(rcourse["feedback_Startdate"])
                datapoint["feedback_Enddate"] = common.format_date_time(rcourse["feedback_Enddate"])
                datapoint["feedback_Starttime"] = common.format_date_time(rcourse["feedback_Starttime"])
                datapoint["feedback_Endtime"] = common.format_date_time(rcourse["feedback_Endtime"])

                course_list.append(datapoint)

            db.session.close()
            
            return jsonify({"code": 200, "data": {"course_list": course_list}})
        except KeyError:
            return jsonify({"code": 404, "message": "User does not exist"})

# Just For You
@api.route("/course_similarity_registration")
@api.doc(description="Recommender function based on course similarity based on student registration")
class RecommenderCourseRegistration(Resource):
    def post(self):
        try:
            course_list_req = request.json['params']['course_list_req']

            if not course_list_req:
                return jsonify({"code": 200, "data": {"course_list": []}})
            
            last_three_reg = request.json['params']['course_list_req'][-3:]

            rcourse_id_list = [course['rcourse_ID'] for course in last_three_reg]

            user_ID = session.get('user_ID')
            
            reg_list = self.get_registration_data()

            pivot_df = self.create_user_course_matrix(reg_list)

            course_similarity_df = self.calculate_course_similarity(pivot_df)

            rcourse_ids = self.get_registered_courses(user_ID, course_list_req)

            recommended_courses_course_similarity = self.recommend_courses(rcourse_id_list, course_similarity_df, rcourse_ids, course_list_req)

            recommended_courses_user_similarity = self.recommend_courses_user_similarity(user_ID, rcourse_ids, 10)

            combined_recommendations = list(set(tuple(course.items()) for course in recommended_courses_course_similarity + recommended_courses_user_similarity))

            recommendations = [dict(course) for course in combined_recommendations]

            db.session.close()
                        
            return jsonify({"code": 200, "data": {"course_list": recommendations}})
        except KeyError:
            return jsonify({"code": 404, "message": "Error occurred during recommendation"})

    def get_registration_data(self):
        reg_list = []
        all_registration_list = Registration.query.filter(Registration.reg_Status.in_(['Enrolled', 'Pending'])).all()

        for reg in all_registration_list:
            rcourse_id = reg.rcourse_ID
            userid = reg.user_ID
            registered_course = self.get_registered_course_info(rcourse_id, userid)

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

        return reg_list

    def get_registered_course_info(self, rcourse_id, userid):
        return db.session.query(Course, RunCourse) \
            .join(RunCourse, Course.course_ID == RunCourse.course_ID) \
            .join(Registration, RunCourse.rcourse_ID == Registration.rcourse_ID) \
            .filter(Registration.user_ID == userid, Registration.rcourse_ID == rcourse_id) \
            .first()

    def create_user_course_matrix(self, reg_list):
        df = pd.DataFrame(reg_list)
        df = df.drop_duplicates(subset=['rcourse_ID', 'user_ID'])
        df["registered"] = 1
        pivot_df = df.pivot(index="rcourse_ID", columns="user_ID", values="registered").fillna(0).astype(int)
        return pivot_df

    def calculate_course_similarity(self, pivot_df):
        # Define weights for each feature
        weights = {'description': 0.5, 'name': 0.2, 'category': 0.3}

        # Prepare the combined corpus for fitting the vectorizer
        combined_corpus = []
        descriptions = []
        names = []
        categories = []

        for course_id in pivot_df.index:
            course = Course.query.filter(Course.course_ID == course_id).first()
            description = preprocess_text(course.course_Desc)
            name = preprocess_text(course.course_Name)
            category_entry = CourseCategory.query.filter(CourseCategory.coursecat_ID == course.coursecat_ID).first()
            category = category_entry.coursecat_Name if category_entry else ""

            combined_corpus.append(f"{description} {name} {category}")
            descriptions.append(description)
            names.append(name)
            categories.append(category)

        # Fit the vectorizer on the combined corpus
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_vectorizer.fit(combined_corpus)

        # Transform each feature set using the common vocabulary
        tfidf_descriptions = tfidf_vectorizer.transform(descriptions)
        tfidf_names = tfidf_vectorizer.transform(names)
        tfidf_categories = tfidf_vectorizer.transform(categories)

        # Apply weights to the TF-IDF matrices
        weighted_tfidf_descriptions = tfidf_descriptions.multiply(weights['description'])
        weighted_tfidf_names = tfidf_names.multiply(weights['name'])
        weighted_tfidf_categories = tfidf_categories.multiply(weights['category'])

        # Verify the shape of weighted matrices before adding
        assert weighted_tfidf_descriptions.shape == weighted_tfidf_names.shape == weighted_tfidf_categories.shape, "The TF-IDF matrices have inconsistent shapes."

        # Combine the weighted matrices by summing them up
        combined_weighted_tfidf = weighted_tfidf_descriptions + weighted_tfidf_names + weighted_tfidf_categories

        # Calculate cosine similarity on the combined weighted matrix
        course_similarity = cosine_similarity(combined_weighted_tfidf)
        course_similarity_df = pd.DataFrame(course_similarity, index=pivot_df.index, columns=pivot_df.index)

        return course_similarity_df


    def get_registered_courses(self, user_ID, course_list_req):
        reg_courses = Registration.query.filter(
            Registration.user_ID == user_ID,
            Registration.reg_Status.in_(["Enrolled", "Pending"])
        ).all()
        return [course.rcourse_ID for course in reg_courses]

    def recommend_courses(self, rcourse_id_list, course_similarity_df, rcourse_ids, course_list_req):
        course_dict = {}
        
        for course in rcourse_id_list:
            similar_courses = self.find_similar_courses(course, course_similarity_df, rcourse_ids, course_list_req)

            for similar_course in similar_courses:
                if similar_course not in course_dict:
                    course_dict[similar_course] = 1
                else:
                    course_dict[similar_course] += 1

        sorted_dict = dict(sorted(course_dict.items(), key=lambda item: item[1], reverse=True))
        course_list = self.generate_course_list(sorted_dict)

        return course_list

    def find_similar_courses(self, target_course_id, course_similarity_df, rcourse_ids, course_list_req):
        current_date = datetime.now()

        similarity_scores = course_similarity_df[target_course_id]
        similar_courses = similarity_scores.drop(target_course_id).sort_values(ascending=False)
        recommended_courses = []

        for course, score in similar_courses.items():
            if course not in rcourse_ids:
                rcourse = RunCourse.query.filter(RunCourse.rcourse_ID == course).first()
                course_ids = [course['course_ID'] for course in course_list_req]

                if rcourse and rcourse.runcourse_Status == "Ongoing" and rcourse.rcourse_ID not in course_ids:
                    if rcourse.reg_Startdate <= current_date.date() and rcourse.reg_Enddate >= current_date.date():
                        recommended_courses.append(course)

        return recommended_courses

    def generate_course_list(self, sorted_dict):
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
                    datapoint[field] = str(rcourse[field])
                else:
                    datapoint[field] = rcourse[field]

            datapoint["reg_Enddate"] = common.format_date_time(rcourse["reg_Enddate"])
            datapoint["run_Startdate"] = common.format_date_time(rcourse["run_Startdate"])
            datapoint["run_Enddate"] = common.format_date_time(rcourse["run_Enddate"])
            datapoint["reg_Endtime"] = common.format_date_time(rcourse["reg_Endtime"])
            datapoint["run_Starttime"] = common.format_date_time(rcourse["run_Starttime"])
            datapoint["run_Endtime"] = common.format_date_time(rcourse["run_Endtime"])
            datapoint["feedback_Startdate"] = common.format_date_time(rcourse["feedback_Startdate"])
            datapoint["feedback_Enddate"] = common.format_date_time(rcourse["feedback_Enddate"])
            datapoint["feedback_Starttime"] = common.format_date_time(rcourse["feedback_Starttime"])
            datapoint["feedback_Endtime"] = common.format_date_time(rcourse["feedback_Endtime"])
            
            course_list.append(datapoint)

        return course_list

    def recommend_courses_user_similarity(self, user_ID, rcourse_ids, num_recommendations):
        all_registration_list = Registration.query.filter(Registration.reg_Status.in_(['Enrolled', 'Pending'])).all()
        
        reg_list = []
        for reg in all_registration_list:
            reg = reg.json()
            rcourseid = reg["rcourse_ID"]
            userid = reg["user_ID"]
            datapoint = {
                "rcourse_ID": rcourseid,
                "user_ID": userid
            }
            reg_list.append(datapoint)

        # Put into dataframe
        df = pd.DataFrame(reg_list)
        df = df.drop_duplicates(subset=["user_ID", "rcourse_ID"])
        df["registered"] = 1
        pivot_df = df.pivot(index="user_ID", columns="rcourse_ID", values="registered").fillna(0).astype(int)
        pivot_df.reset_index(inplace=True)
        pivot_df.columns.name = None
        pivot_df.set_index("user_ID", inplace=True)

        # Cosine similarity table
        user_similarity = cosine_similarity(pivot_df)
        user_similarity_df = pd.DataFrame(user_similarity, index=pivot_df.index, columns=pivot_df.index)

        if user_ID not in pivot_df.index:
            return []

        else:
            user_courses = pivot_df.loc[user_ID]
            similar_users = user_similarity_df[user_ID].sort_values(ascending=False)[1:]

            recommended_courses = set()

            for similar_user, similarity_score in similar_users.items():
                if similarity_score > 0:
                    similar_user_courses = pivot_df.loc[similar_user]
                    for course, registration in similar_user_courses.items():
                        if registration == 1 and user_courses[course] == 0:
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

# ======================================================= Interest =======================================================
    
# Others like you also like
recommender_user_similarity_interest = api.parser()
recommender_user_similarity_interest.add_argument("user_ID", help="Enter user ID")
@api.route("/user_similarity_interest")
@api.doc(description="Recommender function based on user similarity based on student interest")
class RecommenderUserInterest(Resource):
    @api.expect(recommender_user_similarity_interest)
    def get(self):
        arg = recommender_user_similarity_interest.parse_args().get("user_ID")
        target_user_id = int(arg) if arg else ""

        if target_user_id is None:
            return jsonify({"code": 400, "message": "Invalid or missing user_ID"}), 400
        
        try:
            interest_list = self.fetch_interest_data()
            pivot_df = self.create_pivot_table(interest_list)
            recommendations = self.recommend_courses(pivot_df, target_user_id, 10)
            
            if not recommendations:
                return jsonify({"code": 200, "data": {"course_list": []}})
            
            course_list = self.get_course_details(recommendations)
            
            return jsonify({"code": 200, "data": {"course_list": course_list[:10]}})
        except KeyError:
            return jsonify({"code": 404, "message": "User does not exist"}), 404

    def fetch_interest_data(self):
        interest_list = []
        user_list = User.query.all()
        for user in user_list:
            user_dict = user.json()
            user_id = user_dict["user_ID"]
            
            query = db.session.query(
                Course,
                VoteCourse
            ).join(VoteCourse, Course.course_ID == VoteCourse.course_ID).join(
                Interest, VoteCourse.vote_ID == Interest.vote_ID).filter(
                Interest.user_ID == user_id)
            
            results = query.all()
            for course, _ in results:
                interest_list.append({"course_ID": course.json()["course_ID"], "user_ID": user_id})
        return interest_list

    def create_pivot_table(self, interest_list):
        df = pd.DataFrame(interest_list)
        df["interested"] = 1
        pivot_df = df.pivot(index="user_ID", columns="course_ID", values="interested").fillna(0).astype(int)
        pivot_df.reset_index(inplace=True)
        pivot_df.columns.name = None
        pivot_df.set_index("user_ID", inplace=True)
        return pivot_df

    def recommend_courses(self, pivot_df, user_id, num_recommendations):
        if user_id not in pivot_df.index:
            return []

        user_similarity = cosine_similarity(pivot_df)
        user_similarity_df = pd.DataFrame(user_similarity, index=pivot_df.index, columns=pivot_df.index)
        user_courses = pivot_df.loc[user_id]
        similar_users = user_similarity_df[user_id].sort_values(ascending=False)[1:]
        
        recommended_courses = set()
        for similar_user_id, similarity_score in similar_users.items():
            if similarity_score > 0:
                similar_user_courses = pivot_df.loc[similar_user_id]
                for course_id, registered in similar_user_courses.items():
                    if registered and not user_courses[course_id]:
                        ongoing_course = VoteCourse.query.filter(
                            VoteCourse.course_ID == course_id, 
                            VoteCourse.vote_Status == "Ongoing"
                        ).first()
                        if ongoing_course:
                            recommended_courses.add(course_id)
                            if len(recommended_courses) == num_recommendations:
                                return list(recommended_courses)
        return list(recommended_courses)

    def get_course_details(self, recommendations):
        course_list = []
        for course_id in recommendations:
            course = Course.query.filter(Course.course_ID == course_id).first()
            coursecat = CourseCategory.query.filter(CourseCategory.coursecat_ID == course.coursecat_ID).first()
            vcourse = VoteCourse.query.filter(VoteCourse.course_ID == course_id).first()
            datapoint = course.json()
            datapoint["coursecat_Name"] = coursecat.coursecat_Name
            datapoint.update(vcourse.json())
            course_list.append(datapoint)
        db.session.close()
        return course_list

# Just for you
@api.route("/course_similarity_interest")
@api.doc(description="Recommender function based on improved course similarity based on student interest")
class RecommenderCourseInterest(Resource):
    def post(self):
        try:
            course_list_req = request.json['params']['course_list_req']        
            if not course_list_req:
                return jsonify({"code": 200, "data": {"course_list": []}})
            
            last_three_voted = request.json['params']['course_list_req'][-3:]
        
            vcourse_id_list = [course['course_ID'] for course in last_three_voted]
           
            user_ID = session.get('user_ID')

            interest_list = self.get_interest_data()
            
            pivot_df = self.create_user_course_matrix(interest_list)
            
            course_similarity_df = self.calculate_course_similarity(pivot_df)
            
            vcourse_ids = self.get_user_interests(user_ID)

            recommended_courses_course_similarity = self.recommend_courses_course_similarity(vcourse_id_list, course_similarity_df, vcourse_ids, course_list_req)

            recommended_courses_user_similarity = self.recommend_courses_user_similarity(user_ID, vcourse_ids, 10)

            combined_recommendations = list(set(tuple(course.items()) for course in recommended_courses_course_similarity + recommended_courses_user_similarity))
        
            recommendations = [dict(course) for course in combined_recommendations]

            db.session.close()

            return jsonify({"code": 200, "data": {"course_list": recommendations}})
        except Exception as e:
            return jsonify({"code": 404, "message": "Course does not exist"})

    def get_interest_data(self):
        interest_list = []
        users = User.query.all()

        for user in users:
            user_id = user.user_ID
            user_interests = self.get_user_interests(user_id)
            
            if user_interests:
                for course, _ in user_interests:
                    course = course.json()
                    course_id = course['course_ID']
                    course_name = preprocess_text(course['course_Name'])
                    course_desc = preprocess_text(course['course_Desc'])
                    interest_list.append(
                        {"course_ID": course_id, "user_ID": user_id, "course_name": course_name, "course_desc": course_desc}
                    )
        
        return interest_list

    def get_user_interests(self, user_id):
        
        return db.session.query(Course, VoteCourse) \
            .join(VoteCourse, Course.course_ID == VoteCourse.course_ID) \
            .join(Interest, VoteCourse.vote_ID == Interest.vote_ID) \
            .filter(Interest.user_ID == user_id) \
            .all()

    def create_user_course_matrix(self, interest_list):
        df = pd.DataFrame(interest_list)
        df["interested"] = 1
        pivot_df = df.pivot(index="course_ID", columns="user_ID", values="interested").fillna(0).astype(int)
        return pivot_df

    def calculate_course_similarity(self, pivot_df):
        # Define weights for each feature
        weights = {'description': 0.5, 'name': 0.2, 'category': 0.3}

        # Prepare the combined corpus for fitting the vectorizer
        combined_corpus = []
        descriptions = []
        names = []
        categories = []

        for course_id in pivot_df.index:
            course = Course.query.filter(Course.course_ID == course_id).first()
            description = preprocess_text(course.course_Desc)
            name = preprocess_text(course.course_Name)
            category_entry = CourseCategory.query.filter(CourseCategory.coursecat_ID == course.coursecat_ID).first()
            category = category_entry.coursecat_Name if category_entry else ""

            combined_corpus.append(f"{description} {name} {category}")
            descriptions.append(description)
            names.append(name)
            categories.append(category)

        # Fit the vectorizer on the combined corpus
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_vectorizer.fit(combined_corpus)

        # Transform each feature set using the common vocabulary
        tfidf_descriptions = tfidf_vectorizer.transform(descriptions)
        tfidf_names = tfidf_vectorizer.transform(names)
        tfidf_categories = tfidf_vectorizer.transform(categories)

        # Apply weights to the TF-IDF matrices
        weighted_tfidf_descriptions = tfidf_descriptions.multiply(weights['description'])
        weighted_tfidf_names = tfidf_names.multiply(weights['name'])
        weighted_tfidf_categories = tfidf_categories.multiply(weights['category'])

        # Verify the shape of weighted matrices before adding
        assert weighted_tfidf_descriptions.shape == weighted_tfidf_names.shape == weighted_tfidf_categories.shape, "The TF-IDF matrices have inconsistent shapes."

        # Combine the weighted matrices by summing them up
        combined_weighted_tfidf = weighted_tfidf_descriptions + weighted_tfidf_names + weighted_tfidf_categories

        # Calculate cosine similarity on the combined weighted matrix
        course_similarity = cosine_similarity(combined_weighted_tfidf)
        course_similarity_df = pd.DataFrame(course_similarity, index=pivot_df.index, columns=pivot_df.index)

        return course_similarity_df

    def recommend_courses_course_similarity(self, vcourse_id_list, course_similarity_df, vcourse_ids, course_list_req):
        try:
            course_dict = {}
            
            for course in vcourse_id_list:
                similar_courses = self.find_similar_courses(course, course_similarity_df, vcourse_ids, course_list_req)

                for similar_course, score in similar_courses.items():
                    vcourse = VoteCourse.query.filter(VoteCourse.course_ID == similar_course).first()
                    course_ids = [course['course_ID'] for course in course_list_req]

                    if vcourse and vcourse.vote_Status == "Ongoing" and similar_course not in course_ids:
                        if similar_course not in course_dict:
                            course_dict[similar_course] = 1
                        else:
                            course_dict[similar_course] += 1
            
            sorted_dict = dict(sorted(course_dict.items(), key=lambda item: item[1], reverse=True))
            course_list = self.generate_course_list(sorted_dict)
            
            return course_list
            
        except KeyError:
            return jsonify({"code": 404, "message": "Course does not exist"})
    
    def recommend_courses_user_similarity(self, user_ID, vcourse_ids, num_recommendations):
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
        df["interested"] = 1
        pivot_df = df.pivot(index="user_ID", columns="course_ID", values="interested").fillna(0).astype(int)
        pivot_df.reset_index(inplace=True)
        pivot_df.columns.name = None 
        pivot_df.set_index("user_ID", inplace=True)


        user_similarity = cosine_similarity(pivot_df)
        user_similarity_df = pd.DataFrame(user_similarity, index=pivot_df.index, columns=pivot_df.index)

        if user_ID not in pivot_df.index:
            return []
        else:
            user_courses = pivot_df.loc[user_ID]
            
            similar_users = user_similarity_df[user_ID].sort_values(ascending=False)[1:]
                
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
            
            course_list = self.generate_course_list(recommended_courses)
            return list(course_list)

    def find_similar_courses(self, target_course_id, course_similarity_df, vcourse_ids, course_list_req):
        similarity_scores = course_similarity_df[target_course_id]
        similar_courses = similarity_scores.drop(target_course_id).sort_values(ascending=False)
        recommended_courses = {}

        for similar_course, score in similar_courses.items():
            if similar_course not in vcourse_ids:
                vcourse = VoteCourse.query.filter(VoteCourse.course_ID == similar_course).first()
                course_ids = [course['course_ID'] for course in course_list_req]

                if vcourse and vcourse.vote_Status == "Ongoing" and similar_course not in course_ids:
                    recommended_courses[similar_course] = score

        return recommended_courses

    def generate_course_list(self, sorted_dict):
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

        return course_list

# ======================================================= Top Picks (Register & Interest) =======================================================

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
                    'run_Startdate': common.format_date_time(result[2].run_Startdate),
                    'run_Enddate': common.format_date_time(result[2].run_Enddate),
                    'run_Starttime': common.format_date_time(result[2].run_Starttime),
                    'run_Endtime': common.format_date_time(result[2].run_Endtime),
                    'reg_Startdate': common.format_date_time(result[2].reg_Startdate),
                    'reg_Enddate': common.format_date_time(result[2].reg_Enddate),
                    'reg_Starttime': common.format_date_time(result[2].reg_Starttime),
                    'reg_Endtime': common.format_date_time(result[2].reg_Endtime),
                    'feedback_Startdate': common.format_date_time(result[2].feedback_Startdate),
                    'feedback_Enddate': common.format_date_time(result[2].feedback_Enddate),
                    'feedback_Starttime': common.format_date_time(result[2].feedback_Starttime),
                    'feedback_Endtime': common.format_date_time(result[2].feedback_Endtime),
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
                    'run_Startdate': common.format_date_time(result[2].run_Startdate),
                    'run_Enddate': common.format_date_time(result[2].run_Enddate),
                    'run_Starttime': common.format_date_time(result[2].run_Starttime),
                    'run_Endtime': common.format_date_time(result[2].run_Endtime),
                    'reg_Startdate': common.format_date_time(result[2].reg_Startdate),
                    'reg_Enddate': common.format_date_time(result[2].reg_Enddate),
                    'reg_Starttime': common.format_date_time(result[2].reg_Starttime),
                    'reg_Endtime': common.format_date_time(result[2].reg_Endtime),
                    'feedback_Startdate': common.format_date_time(result[2].feedback_Startdate),
                    'feedback_Enddate': common.format_date_time(result[2].feedback_Enddate),
                    'feedback_Starttime': common.format_date_time(result[2].feedback_Starttime),
                    'feedback_Endtime': common.format_date_time(result[2].feedback_Endtime),
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
    
