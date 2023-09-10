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
@api.route("/recommender_user_similarity ")
@api.doc(description="Recommender function based on user similarity")
class Recommender(Resource):
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
            similar_users = user_similarity_df[user].sort_values(ascending=False)[1:]  # Exclude the user itself
            
            recommended_courses = set()  # Use a set to store unique course titles
            for similar_user, similarity_score in similar_users.iteritems():
                if similarity_score > 0:
                    similar_user_courses = pivot_df.loc[similar_user]
                    for course, registration in similar_user_courses.iteritems():
                        if registration == 1 and user_courses[course] == 0:
                            recommended_courses.add(course)
                            if len(recommended_courses) == num_recommendations:
                                return list(recommended_courses)  # Return when reaching the desired number of recommendations
            
            return list(recommended_courses)  # Convert the set to a list and return all unique recommended courses

        try:
            recommendations_rcourses_id = recommend_courses(target_user_id, 4)
            course_list = []
            for recommondations_rcourse_id in recommendations_rcourses_id:
                rcourse = RunCourse.query.filter(RunCourse.rcourse_ID == recommondations_rcourse_id).first()
                course_id = rcourse.json()["course_ID"]
                course = Course.query.filter(Course.course_ID == course_id).first()
                course_list.append(course.json())

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

