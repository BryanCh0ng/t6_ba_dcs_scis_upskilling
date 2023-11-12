# Standard Library Imports
import json
import logging

# Third-party Imports
from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import wordnet
nltk.download('punkt') # Download NLTK's punkt tokenizer models
nltk.download('stopwords') # Download NLTK's stopwords dataset
nltk.download('wordnet') # Download NLTK's WordNet lexical database
wordnet.ensure_loaded()
import nltk.data
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
from gensim import corpora
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import silhouette_score
from sklearn.model_selection import train_test_split
from sqlalchemy import func, and_, exists, or_

# Local Imports
from allClasses import *

stop_words = set(stopwords.words('english')) # Setup stop words
custom_stop_words = ['the', 'course', 'content', 'instructor', 'professor', 'prof', 'apply', 'learn', 'really', 'allow', 'provide', 'help', 'gave', 'give', 'think', 'could', 'would', 'can', 'will', 'check', 'make', 'made', 'time', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'many', 'sure', 'able', 'quite', 'need', 'want', 'bit', 'lot', 'look', 'try', 'let', 'tried', 'suggestion', 'current', 'currently', 'instead', 'come', 'dont', 'came', 'does', 'doesnt', 'furthermore', 'especially']
stop_words.update(custom_stop_words) # Add custom stop word
lemmatizer = WordNetLemmatizer() # Set up Lemmatizer

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from collections import Counter
from sqlalchemy.orm import aliased

api = Namespace('dashboard', description='Dashboard related operations')

# ================================================== DASHBOARD FUNCTIONS ================================================== #

# To get instructor specific average ratings
total_no_of_feedbacks = api.parser()
total_no_of_feedbacks.add_argument("course_ID", help="Enter course ID")
total_no_of_feedbacks.add_argument("coursecat_ID", help="Enter course category ID")
total_no_of_feedbacks.add_argument("rcourse_ID", help="Enter runcourse ID")
total_no_of_feedbacks.add_argument("instructor_ID", help="Enter instructor ID")
total_no_of_feedbacks.add_argument("run_Startdate", help="Enter run start date")
total_no_of_feedbacks.add_argument("run_Enddate", help="Enter run end date")

@api.route("/total_no_of_feedbacks")
@api.doc(description="Total number of feedbacks")
class TotalFeedbacks(Resource):
    @api.expect(total_no_of_feedbacks)
    def get(self):
        args = total_no_of_feedbacks.parse_args()
        courseID = args.get("course_ID", "")
        coursecatID = args.get("coursecat_ID", "")
        rcourseID = args.get("rcourse_ID", "")
        instructorID = args.get("instructor_ID", "")
        start_date = args.get('run_Startdate', "")
        end_date = args.get("run_Enddate", "")

        formatted_start_date = None
        formatted_end_date = None

        try:
            total_feedbacks = 0

            query = (
                db.session.query(Course, RunCourse, Feedback, TemplateAttribute)
                .join(RunCourse, Course.course_ID == RunCourse.course_ID)  # Join Course and RunCourse using course_id
                .join(Feedback, RunCourse.rcourse_ID == Feedback.rcourse_ID)  # Join RunCourse and Feedback using rcourse_id
                .join(TemplateAttribute, Feedback.template_Attribute_ID == TemplateAttribute.template_Attribute_ID)  # Join Feedback and TemplateAttribute using attribute_id
                #.filter(or_(func.lower(TemplateAttribute.question).like("%instructor%"), func.lower(TemplateAttribute.question).like("%course%")))
                #.filter(or_(TemplateAttribute.input_Type == "Text Field", TemplateAttribute.input_Type == "Likert Scale"))
            )

            if courseID and courseID != "[]":
                courseID = json.loads(courseID)
                #print(courseID)
                query = query.filter(RunCourse.course_ID.in_(courseID))
                #print("running", str(query))

            if coursecatID and coursecatID != "[]":
                coursecatID = json.loads(coursecatID)
                query = query.filter(Course.coursecat_ID.in_(coursecatID))

            if rcourseID and rcourseID != "[]":
                # Filter by rcourse_ID
                rcourseID = json.loads(rcourseID)
                query = query.filter(Feedback.rcourse_ID.in_(rcourseID))

            if instructorID and instructorID != "[]":
                instructorID = json.loads(instructorID)
                query = query.filter(RunCourse.instructor_ID.in_(instructorID))

            if start_date:
                formatted_start_date = datetime.strptime(start_date, '%Y-%m-%d').date()

            if end_date:
                formatted_end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

            if formatted_start_date and formatted_end_date: 
                query = query.filter(RunCourse.run_Startdate >= formatted_start_date, RunCourse.run_Enddate <= formatted_end_date)

            query = query.group_by(Feedback.rcourse_ID, Feedback.submitted_By)

            feedbacks = query.all()

            total_feedbacks = len(feedbacks)

            db.session.close()

            response_data = {
                "code": 200,
                "data": {
                    "total_feedbacks": total_feedbacks
                },
                "message": "message",
            }

        except Exception as e:
            response_data = {
                "code": 500,
                "message": str(e)
            }

        return jsonify(response_data)


# To get course average ratings - all and specific
average_course_ratings = api.parser()
average_course_ratings.add_argument("course_ID", help="Enter course ID")
average_course_ratings.add_argument("coursecat_ID", help="Enter course category ID")
average_course_ratings.add_argument("rcourse_ID", help="Enter run course ID")
average_course_ratings.add_argument("instructor_ID", help="Enter instructor ID")
average_course_ratings.add_argument("run_Startdate", help="Enter run start date")
average_course_ratings.add_argument("run_Enddate", help="Enter run end date")

@api.route("/course_average_ratings")
@api.doc(description="Course specific feedback")
class CourseAverageRatings(Resource):
    def get(self):
        args = average_course_ratings.parse_args()

        courseID = args.get("course_ID", "")
        coursecatID = args.get("coursecat_ID", "")
        rcourseID = args.get("rcourse_ID", "")
        instructorID = args.get("instructor_ID", "")
        start_date = args.get('run_Startdate', "")
        end_date = args.get("run_Enddate", "")

        formatted_start_date = None
        formatted_end_date = None

        try:
            total_ratings = 0
            total_questions = 0
            sum_of_questions = 0

            query = (
                db.session.query(Course, RunCourse, Feedback, TemplateAttribute)
                .join(RunCourse, Course.course_ID == RunCourse.course_ID)  # Join Course and RunCourse using course_id
                .join(Feedback, RunCourse.rcourse_ID == Feedback.rcourse_ID)  # Join RunCourse and Feedback using rcourse_id
                .join(TemplateAttribute, Feedback.template_Attribute_ID == TemplateAttribute.template_Attribute_ID)  # Join Feedback and TemplateAttribute using attribute_id
                .filter(func.lower(TemplateAttribute.question).like("%course%"))
                .filter(TemplateAttribute.input_Type == "Likert Scale")
            )

            #query_without_keywords_filtering = query 

            if courseID and courseID != "[]":
                courseID = json.loads(courseID)
                #print(courseID)
                query = query.filter(RunCourse.course_ID.in_(courseID))
                #query_without_keywords_filtering = query_without_keywords_filtering.filter(RunCourse.course_ID.in_(courseID))
                #print("running", str(query))

            if coursecatID and coursecatID != "[]":
                coursecatID = json.loads(coursecatID)
                query = query.filter(Course.coursecat_ID.in_(coursecatID))
                #query_without_keywords_filtering = query_without_keywords_filtering.filter(Course.coursecat_ID.in_(coursecatID))

            if rcourseID and rcourseID != "[]":
                # Filter by rcourse_ID
                rcourseID = json.loads(rcourseID)
                query = query.filter(Feedback.rcourse_ID.in_(rcourseID))
                #query_without_keywords_filtering = query_without_keywords_filtering.filter(Feedback.rcourse_ID.in_(rcourseID))

            if instructorID and instructorID != "[]":
                instructorID = json.loads(instructorID)
                query = query.filter(RunCourse.instructor_ID.in_(instructorID))
                #query_without_keywords_filtering = query_without_keywords_filtering.filter(RunCourse.instructor_ID.in_(instructorID))

            if start_date:
                formatted_start_date = datetime.strptime(start_date, '%Y-%m-%d').date()

            if end_date:
                formatted_end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

            if formatted_start_date and formatted_end_date: 
                query = query.filter(RunCourse.run_Startdate >= formatted_start_date, RunCourse.run_Enddate <= formatted_end_date)
                #query_without_keywords_filtering = query_without_keywords_filtering.filter(RunCourse.run_Startdate >= formatted_start_date, RunCourse.run_Enddate <= formatted_end_date)

            course_feedbacks = query.all()

            #feedbacks = query_without_keywords_filtering.all()

            #Get the number of course rating questions
            total_questions = len(course_feedbacks)

            #total_feedbacks = len(feedbacks)            

            if course_feedbacks:
                for course_feedback in course_feedbacks:
                    #Get the ratings for each course rating questions
                    total_ratings += int(course_feedback.Feedback.answer)

            #Calculate the overall average course ratings
            if total_ratings and total_questions > 0:
                overall_average_rating = round( (total_ratings / total_questions), 2)
                message = "Course ratings calculated successfully."
            else:
                overall_average_rating = 0
                message = "No ratings"

            db.session.close()

            response_data = {
                "code": 200,
                "data": {
                    "overall_average_rating": overall_average_rating
                    #"total_feedbacks": total_feedbacks
                },
                "message": "message",
            }

        except Exception as e:
            response_data = {
                "code": 500,
                "message": str(e)
            }

        return jsonify(response_data)

# To get instructor specific average ratings
instructor_average_ratings = api.parser()
instructor_average_ratings.add_argument("course_ID", help="Enter course ID")
instructor_average_ratings.add_argument("coursecat_ID", help="Enter course category ID")
instructor_average_ratings.add_argument("rcourse_ID", help="Enter runcourse ID")
instructor_average_ratings.add_argument("instructor_ID", help="Enter instructor ID")
instructor_average_ratings.add_argument("run_Startdate", help="Enter run start date")
instructor_average_ratings.add_argument("run_Enddate", help="Enter run end date")

@api.route("/instructor_average_ratings")
@api.doc(description="Instructor specific feedback")
class InstructorAverageRatings(Resource):
    @api.expect(instructor_average_ratings)
    def get(self):
        args = instructor_average_ratings.parse_args()
        courseID = args.get("course_ID", "")
        coursecatID = args.get("coursecat_ID", "")
        rcourseID = args.get("rcourse_ID", "")
        instructorID = args.get("instructor_ID", "")
        start_date = args.get('run_Startdate', "")
        end_date = args.get("run_Enddate", "")

        formatted_start_date = None
        formatted_end_date = None

        try:
            total_ratings = 0
            total_questions = 0

            query = (
                db.session.query(Course, RunCourse, Feedback, TemplateAttribute)
                .join(RunCourse, Course.course_ID == RunCourse.course_ID)  # Join Course and RunCourse using course_id
                .join(Feedback, RunCourse.rcourse_ID == Feedback.rcourse_ID)  # Join RunCourse and Feedback using rcourse_id
                .join(TemplateAttribute, Feedback.template_Attribute_ID == TemplateAttribute.template_Attribute_ID)  # Join Feedback and TemplateAttribute using attribute_id
                .filter(func.lower(TemplateAttribute.question).like("%instructor%"))
                .filter(TemplateAttribute.input_Type == "Likert Scale")
            )

            if courseID and courseID != "[]":
                courseID = json.loads(courseID)
                #print(courseID)
                query = query.filter(RunCourse.course_ID.in_(courseID))
                #print("running", str(query))

            if coursecatID and coursecatID != "[]":
                coursecatID = json.loads(coursecatID)
                query = query.filter(Course.coursecat_ID.in_(coursecatID))

            if rcourseID and rcourseID != "[]":
                # Filter by rcourse_ID
                rcourseID = json.loads(rcourseID)
                query = query.filter(Feedback.rcourse_ID.in_(rcourseID))

            if instructorID and instructorID != "[]":
                instructorID = json.loads(instructorID)
                query = query.filter(RunCourse.instructor_ID.in_(instructorID))

            if start_date:
                formatted_start_date = datetime.strptime(start_date, '%Y-%m-%d').date()

            if end_date:
                formatted_end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

            if formatted_start_date and formatted_end_date: 
                query = query.filter(RunCourse.run_Startdate >= formatted_start_date, RunCourse.run_Enddate <= formatted_end_date)

            instructor_feedbacks = query.all()

            #Get the number of instructor rating questions
            total_questions = len(instructor_feedbacks)

            if instructor_feedbacks:
                for instructor_feedback in instructor_feedbacks:
                    #Get the ratings for each instructor rating questions
                    total_ratings += int(instructor_feedback.Feedback.answer)

            #Calculate the overall average instructor ratings
            if total_ratings and total_questions > 0:
                overall_average_rating = round( total_ratings / total_questions, 2)
                message = "Instructor ratings calculated successfully."
            else:
                overall_average_rating = 0
                message = "No ratings"

            db.session.close()

            response_data = {
                "code": 200,
                "data": {
                    "overall_average_rating": overall_average_rating
                },
                "message": "message",
            }

        except Exception as e:
            response_data = {
                "code": 500,
                "message": str(e)
            }

        return jsonify(response_data)
# ================================================== For Topic Modeling ================================================== #
def drop_col(df):
    df = df.dropna(how='all')
    values_to_drop = ["nil", "none", "-", "na", "nan", "nothing"]
    df = df[~df['answer'].isin(values_to_drop)]
    drop = ['na', 'nil']
    df = df[~df['answer'].apply(lambda x: any(word in x.lower() for word in drop))]


    df.reset_index(drop=True, inplace=True)
    return df

def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return nltk.corpus.wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return nltk.corpus.wordnet.VERB
    elif treebank_tag.startswith('N'):
        return nltk.corpus.wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return nltk.corpus.wordnet.ADV
    else:
        return None
    
def lemmatize_token(token, pos_tag):
    tag = get_wordnet_pos(pos_tag)
    if tag is None:
        return lemmatizer.lemmatize(token)
    else:
        return lemmatizer.lemmatize(token, tag)

def preprocess_text(text_series):
    def process_text(text):
        
        text = text.lower() # Convert text to lowercase

        text = re.sub(r'[^a-zA-Z\s-]', '', text) # Remove non-alphabetic characters and split hyphenated words

        tokens = nltk.word_tokenize(text) # Tokenize text

        pos_tags = nltk.pos_tag(tokens) # Tag part of speech for each token
        # print(pos_tags)
        lemmatized_tokens = [lemmatize_token(token, pos) for token, pos in pos_tags] # Lemmatize tokens with specified part of speech

        tokens = [token for token in lemmatized_tokens if not token in stop_words] # Remove stop words

        tokens = [token for token in tokens if len(token) >= 3] # Remove words with length less than 3 characters

        text = ' '.join(tokens) # Join tokens back into text

        return text
    
    return text_series.apply(process_text)

def tune_nmf_hyperparameters(corpus, n_topics_range, max_df_range):
    best_n_topics = None
    best_max_df = None
    best_silhouette_score = -1

    # Split your data into training and validation sets
    X_train, X_val = train_test_split(corpus, test_size=0.2, random_state=1)

    for n_topics in n_topics_range:
        for max_df_value in max_df_range:
            tfidf_vectorizer = TfidfVectorizer(max_df=max_df_value, stop_words='english')
            tfidf_matrix_train = tfidf_vectorizer.fit_transform(X_train)
            nmf_model = NMF(n_components=n_topics, max_iter=1000, random_state=1)
            nmf_matrix_train = nmf_model.fit_transform(tfidf_matrix_train)

            tfidf_matrix_val = tfidf_vectorizer.transform(X_val)
            nmf_matrix_val = nmf_model.transform(tfidf_matrix_val)

            if 2 <= n_topics <= len(X_val) - 1 and 0.0 <= max_df_value <= 1.0:
                # Calculate Silhouette score only if there are more than one label
                labels = nmf_matrix_val.argmax(axis=1)
                if len(set(labels)) > 1:
                    silhouette_avg = silhouette_score(tfidf_matrix_val, labels=labels)
                else:
                    silhouette_avg = -1  # Handle the case where there's only one label
            else:
                silhouette_avg = -1

            if silhouette_avg > best_silhouette_score:
                best_n_topics = n_topics
                best_max_df = max_df_value
                best_silhouette_score = silhouette_avg
    
    return best_n_topics, best_max_df, best_silhouette_score

# Get the topic for specific course or all courses (done well)
feedback_course_done_well_specific = api.parser()
feedback_course_done_well_specific.add_argument("course_ID", help="Enter course_ID")
feedback_course_done_well_specific.add_argument("coursecat_ID", help="Enter course category ID")
feedback_course_done_well_specific.add_argument("rcourse_ID", help="Enter run course ID")
feedback_course_done_well_specific.add_argument("instructor_ID", help="Enter instructor ID")
feedback_course_done_well_specific.add_argument("run_Startdate", help="Enter run start date")
feedback_course_done_well_specific.add_argument("run_Enddate", help="Enter run end date")

@api.route("/feedback_course_done_well_specific")
@api.doc(description="Course-specific feedback")
class CourseDoneWellFeedback(Resource):
    @api.expect(feedback_course_done_well_specific)
    def get(self):
        # Parse the course_ID from the request arguments
        args = feedback_course_done_well_specific.parse_args()
        course_ID = args.get("course_ID", "")
        coursecatID = args.get("coursecat_ID", "")
        rcourse_ID = args.get("rcourse_ID", "")
        instructorID = args.get("instructor_ID", "")
        start_date = args.get('run_Startdate', "")
        end_date = args.get("run_Enddate", "")

        formatted_start_date = None
        formatted_end_date = None

        keywords = ['course']
        optional_keywords = ['done well', 'contributed', 'did well']

        query = (
                db.session.query(Feedback.answer)
                .join(TemplateAttribute, Feedback.template_Attribute_ID == TemplateAttribute.template_Attribute_ID)
                .filter(TemplateAttribute.input_Type == "Text Field")
            )

        for keyword in keywords:
            query = query.filter(func.lower(TemplateAttribute.question).contains(keyword))

        optional_keyword_filter = or_(
            *[
                func.lower(TemplateAttribute.question).contains(keyword)
                for keyword in optional_keywords
            ]
        )
        query = query.filter(optional_keyword_filter)

        if course_ID and course_ID != "[]":
            course_ID = json.loads(course_ID)
            #print(courseID)
            query = query.filter(RunCourse.course_ID.in_(course_ID))
            #print("running", str(query))

        if coursecatID and coursecatID != "[]":
            coursecatID = json.loads(coursecatID)
            query = query.filter(Course.coursecat_ID.in_(coursecatID))

        if rcourse_ID and rcourse_ID != "[]":
            # Filter by rcourse_ID
            rcourse_ID = json.loads(rcourse_ID)
            query = query.filter(Feedback.rcourse_ID.in_(rcourse_ID))

        if instructorID and instructorID != "[]":
            instructorID = json.loads(instructorID)
            query = query.filter(RunCourse.instructor_ID.in_(instructorID))

        if start_date:
            formatted_start_date = datetime.strptime(start_date, '%Y-%m-%d').date()

        if end_date:
            formatted_end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        if formatted_start_date and formatted_end_date: 
            query = query.filter(RunCourse.run_Startdate >= formatted_start_date, RunCourse.run_Enddate <= formatted_end_date)


        results = query.all()
        # print(results)

        db.session.close()

        if results:
            result_data = []
            for result in results:
                feedback = {
                    "answer": result[0],
                }
                result_data.append(feedback)

            # Create a Pandas DataFrame from the result_data list
            df_course_improve = pd.DataFrame(result_data)
            df_course_improve = drop_col(df_course_improve)
            
            df_course_improve['preprocessed_text'] = preprocess_text(df_course_improve['answer'])
            corpus = df_course_improve['preprocessed_text']

            n_topics_range = range(3, 9)
            max_df_range = [0.70, 0.75, 0.80, 0.85, 0.9, 0.95]
            best_n_topics, best_max_df, best_silhouette_score = tune_nmf_hyperparameters(corpus, n_topics_range, max_df_range)

            if best_n_topics is None:
                return jsonify({"code": 200, "data": [], "topic_words_list": []})

            tfidf_vectorizer = TfidfVectorizer(max_df=best_max_df, stop_words='english')
            tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)

            nmf_model = NMF(n_components=best_n_topics, random_state=1)
            nmf_matrix = nmf_model.fit_transform(tfidf_matrix)

            feature_names = tfidf_vectorizer.get_feature_names_out()
            topic_words_list = []

            for topic_idx, topic in enumerate(nmf_model.components_):
                top_words_indices = topic.argsort()[:-15 - 1:-1]
                top_words = [feature_names[i] for i in top_words_indices]
                top_word_probabilities = [topic[i] for i in top_words_indices]
                topic_data = [{"word": word, "size": prob} for word, prob in zip(top_words, top_word_probabilities)]
                topic_words_list.append(topic_data)
            
            topic_words_list_formatted = []

            for topic_words in topic_words_list:
                word_data = {"wordData": topic_words}
                topic_words_list_formatted.append(word_data)

            dominant_topics = nmf_matrix.argmax(axis=1) + 1
            df_course_improve['topic_number'] = dominant_topics

            # Convert the DataFrame to JSON
            response_data = df_course_improve.to_dict(orient='records')

            return jsonify({"code": 200, "data": response_data, "topic_words_list": topic_words_list_formatted})

        return jsonify({"code": 404, "message": "No matching course interest information found"})

# Get the topic for specific course or all courses (improve)
feedback_course_improve_specific = api.parser()
feedback_course_improve_specific.add_argument("course_ID", help="Enter course_ID")
feedback_course_improve_specific.add_argument("coursecat_ID", help="Enter course category ID")
feedback_course_improve_specific.add_argument("rcourse_ID", help="Enter run course ID")
feedback_course_improve_specific.add_argument("instructor_ID", help="Enter instructor ID")
feedback_course_improve_specific.add_argument("run_Startdate", help="Enter run start date")
feedback_course_improve_specific.add_argument("run_Enddate", help="Enter run end date")

@api.route("/feedback_course_improve_specific")
@api.doc(description="Course-specific feedback")
class CourseImproveFeedback(Resource):
    @api.expect(feedback_course_improve_specific)
    def get(self):
        # Parse the course_ID from the request arguments
        args = feedback_course_improve_specific.parse_args()
        course_ID = args.get("course_ID", "")
        coursecatID = args.get("coursecat_ID", "")
        rcourse_ID = args.get("rcourse_ID", "")
        instructorID = args.get("instructor_ID", "")
        start_date = args.get('run_Startdate', "")
        end_date = args.get("run_Enddate", "")

        formatted_start_date = None
        formatted_end_date = None

        keywords = ['course']
        optional_keywords = ['improve', 'suggestions']

        query = (
                db.session.query(Feedback.answer)
                .join(TemplateAttribute, Feedback.template_Attribute_ID == TemplateAttribute.template_Attribute_ID)
                .filter(TemplateAttribute.input_Type == "Text Field")
            )       

        for keyword in keywords:
            query = query.filter(func.lower(TemplateAttribute.question).contains(keyword))

        optional_keyword_filter = or_(
            *[
                func.lower(TemplateAttribute.question).contains(keyword)
                for keyword in optional_keywords
            ]
        )

        query = query.filter(optional_keyword_filter)

        if course_ID and course_ID != "[]":
            course_ID = json.loads(course_ID)
            
            query = query.filter(RunCourse.course_ID.in_(course_ID))
            

        if coursecatID and coursecatID != "[]":
            coursecatID = json.loads(coursecatID)
            query = query.filter(Course.coursecat_ID.in_(coursecatID))

        if rcourse_ID and rcourse_ID != "[]":
            # Filter by rcourse_ID
            rcourse_ID = json.loads(rcourse_ID)
            query = query.filter(Feedback.rcourse_ID.in_(rcourse_ID))

        if instructorID and instructorID != "[]":
            instructorID = json.loads(instructorID)
            query = query.filter(RunCourse.instructor_ID.in_(instructorID))

        if start_date:
            formatted_start_date = datetime.strptime(start_date, '%Y-%m-%d').date()

        if end_date:
            formatted_end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        if formatted_start_date and formatted_end_date: 
            query = query.filter(RunCourse.run_Startdate >= formatted_start_date, RunCourse.run_Enddate <= formatted_end_date)


        results = query.all()
        
        db.session.close()

        if results:
            result_data = []
            for result in results:
                feedback = {
                    "answer": result[0],
                }
                result_data.append(feedback)
            

            # Create a Pandas DataFrame from the result_data list
            df_course_improve = pd.DataFrame(result_data)
            df_course_improve = drop_col(df_course_improve)
            df_course_improve['preprocessed_text'] = preprocess_text(df_course_improve['answer'])
            
            corpus = df_course_improve['preprocessed_text']
            
            topics_range = range(2, 11)
            
            max_df_range = [0.70, 0.75, 0.80, 0.85, 0.9, 0.95]
            
            best_n_topics, best_max_df, best_silhouette_score = tune_nmf_hyperparameters(corpus, topics_range, max_df_range)

            if best_n_topics is None:
                return jsonify({"code": 200, "data": [], "topic_words_list": []})


            tfidf_vectorizer = TfidfVectorizer(max_df=best_max_df, stop_words='english')
            tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)

            nmf_model = NMF(n_components=best_n_topics, random_state=1)
            nmf_matrix = nmf_model.fit_transform(tfidf_matrix)

            feature_names = tfidf_vectorizer.get_feature_names_out()
            topic_words_list = []

            for topic_idx, topic in enumerate(nmf_model.components_):
                top_words_indices = topic.argsort()[:-15 - 1:-1]
                top_words = [feature_names[i] for i in top_words_indices]
                top_word_probabilities = [topic[i] for i in top_words_indices]
                topic_data = [{"word": word, "size": prob} for word, prob in zip(top_words, top_word_probabilities)]
                topic_words_list.append(topic_data)
            
            topic_words_list_formatted = []

            for topic_words in topic_words_list:
                word_data = {"wordData": topic_words}
                topic_words_list_formatted.append(word_data)

            dominant_topics = nmf_matrix.argmax(axis=1) + 1
            df_course_improve['topic_number'] = dominant_topics

            # Convert the DataFrame to JSON
            response_data = df_course_improve.to_dict(orient='records')

            return jsonify({"code": 200, "data": response_data, "topic_words_list": topic_words_list_formatted})

        return jsonify({"code": 404, "message": "No matching course interest information found"})

# Get the topic for specific instructor or all instructor (done well)
feedback_instructor_done_well_specific = api.parser()
feedback_instructor_done_well_specific.add_argument("course_ID", help="Enter course_ID")
feedback_instructor_done_well_specific.add_argument("rcourse_ID", help="Enter rcourse_ID")
feedback_instructor_done_well_specific.add_argument("course_ID", help="Enter course_ID")
feedback_instructor_done_well_specific.add_argument("coursecat_ID", help="Enter course category ID")
feedback_instructor_done_well_specific.add_argument("rcourse_ID", help="Enter run course ID")
feedback_instructor_done_well_specific.add_argument("instructor_ID", help="Enter instructor ID")
feedback_instructor_done_well_specific.add_argument("run_Startdate", help="Enter run start date")
feedback_instructor_done_well_specific.add_argument("run_Enddate", help="Enter run end date")

@api.route("/feedback_instructor_done_well_specific")
@api.doc(description="Instructor-specific feedback")
class InstructorDoneWellFeedback(Resource):
    @api.expect(feedback_instructor_done_well_specific)
    def get(self):
        # Parse the user_ID from the request arguments
        args = feedback_instructor_done_well_specific.parse_args()
        course_ID = args.get("course_ID", "")
        coursecatID = args.get("coursecat_ID", "")
        rcourse_ID = args.get("rcourse_ID", "")
        instructorID = args.get("instructor_ID", "")
        start_date = args.get('run_Startdate', "")
        end_date = args.get("run_Enddate", "")

        formatted_start_date = None
        formatted_end_date = None

        keywords = ['instructor']
        optional_keywords = ['did well', 'contributed', 'done well', 'strengths']

        query = (
                db.session.query(Feedback.answer)
                .join(TemplateAttribute, Feedback.template_Attribute_ID == TemplateAttribute.template_Attribute_ID)
                .filter(TemplateAttribute.input_Type == "Text Field")
            )

        for keyword in keywords:
            query = query.filter(func.lower(TemplateAttribute.question).contains(keyword))

        optional_keyword_filter = or_(
            *[
                func.lower(TemplateAttribute.question).contains(keyword)
                for keyword in optional_keywords
            ]
        )

        query = query.filter(optional_keyword_filter)

        if course_ID and course_ID != "[]":
            course_ID = json.loads(course_ID)
            
            query = query.filter(RunCourse.course_ID.in_(course_ID))
            

        if coursecatID and coursecatID != "[]":
            coursecatID = json.loads(coursecatID)
            query = query.filter(Course.coursecat_ID.in_(coursecatID))

        if rcourse_ID and rcourse_ID != "[]":
            # Filter by rcourse_ID
            rcourse_ID = json.loads(rcourse_ID)
            query = query.filter(Feedback.rcourse_ID.in_(rcourse_ID))

        if instructorID and instructorID != "[]":
            instructorID = json.loads(instructorID)
            query = query.filter(RunCourse.instructor_ID.in_(instructorID))

        if start_date:
            formatted_start_date = datetime.strptime(start_date, '%Y-%m-%d').date()

        if end_date:
            formatted_end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        if formatted_start_date and formatted_end_date: 
            query = query.filter(RunCourse.run_Startdate >= formatted_start_date, RunCourse.run_Enddate <= formatted_end_date)
        
        results = query.all()
       
        db.session.close()

        if results:
            result_data = []
            for result in results:
                feedback = {
                    "answer": result[0],
                }
                result_data.append(feedback)

            # Create a Pandas DataFrame from the result_data list
            df_instructor_well = pd.DataFrame(result_data)
            df_instructor_well = drop_col(df_instructor_well)
            
            df_instructor_well['preprocessed_text'] = preprocess_text(df_instructor_well['answer'])
            corpus = df_instructor_well['preprocessed_text']

            n_topics_range = range(2, 9)
            max_df_range = [0.70, 0.75, 0.80, 0.85, 0.9, 0.95]
            
            best_n_topics, best_max_df, best_silhouette_score = tune_nmf_hyperparameters(corpus, n_topics_range, max_df_range)

            if best_n_topics is None:
                return jsonify({"code": 200, "data": [], "topic_words_list": []})

            tfidf_vectorizer = TfidfVectorizer(max_df=best_max_df, stop_words='english')
            tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)

            nmf_model = NMF(n_components=best_n_topics, random_state=1)
            nmf_matrix = nmf_model.fit_transform(tfidf_matrix)

            feature_names = tfidf_vectorizer.get_feature_names_out()
            topic_words_list = []

            for topic_idx, topic in enumerate(nmf_model.components_):
                top_words_indices = topic.argsort()[:-15 - 1:-1]
                top_words = [feature_names[i] for i in top_words_indices]
                top_word_probabilities = [topic[i] for i in top_words_indices]
                topic_data = [{"word": word, "size": prob} for word, prob in zip(top_words, top_word_probabilities)]
                topic_words_list.append(topic_data)
            
            topic_words_list_formatted = []

            for topic_words in topic_words_list:
                word_data = {"wordData": topic_words}
                topic_words_list_formatted.append(word_data)

            dominant_topics = nmf_matrix.argmax(axis=1) + 1
            df_instructor_well['topic_number'] = dominant_topics

            # Convert the DataFrame to JSON
            response_data = df_instructor_well.to_dict(orient='records')

            return jsonify({"code": 200, "data": response_data, "topic_words_list": topic_words_list_formatted})

        return jsonify({"code": 404, "message": "No matching course interest information found"})
    
# Get the topic for specific instructor or all instructor (improve)
feedback_instructor_improve_specific = api.parser()
feedback_instructor_improve_specific.add_argument("course_ID", help="Enter course_ID")
feedback_instructor_improve_specific.add_argument("coursecat_ID", help="Enter course category ID")
feedback_instructor_improve_specific.add_argument("rcourse_ID", help="Enter run course ID")
feedback_course_improve_specific.add_argument("instructor_ID", help="Enter instructor ID")
feedback_instructor_improve_specific.add_argument("run_Startdate", help="Enter run start date")
feedback_instructor_improve_specific.add_argument("run_Enddate", help="Enter run end date")

@api.route("/feedback_instructor_improve_specific")
@api.doc(description="Instructor-specific feedback")
class InstructorDoneWellFeedback(Resource):
    @api.expect(feedback_instructor_improve_specific)
    def get(self):
        # Parse the user_ID from the request arguments
        args = feedback_instructor_improve_specific.parse_args()
        course_ID = args.get("course_ID", "")
        coursecatID = args.get("coursecat_ID", "")
        rcourse_ID = args.get("rcourse_ID", "")
        instructorID = args.get("instructor_ID", "")
        start_date = args.get('run_Startdate', "")
        end_date = args.get("run_Enddate", "")

        formatted_start_date = None
        formatted_end_date = None

        keywords = ['instructor']
        optional_keywords = ['improve', 'suggestions']

        query = (
            db.session.query(Feedback.answer)
            .join(TemplateAttribute, Feedback.template_Attribute_ID == TemplateAttribute.template_Attribute_ID)
            .filter(TemplateAttribute.input_Type == "Text Field")
        )
        
        for keyword in keywords:
            query = query.filter(func.lower(TemplateAttribute.question).contains(keyword))
        
        optional_keyword_filter = or_(
            *[
                func.lower(TemplateAttribute.question).contains(keyword)
                for keyword in optional_keywords
            ]
        )
        query = query.filter(optional_keyword_filter)

        if course_ID and course_ID != "[]":
            course_ID = json.loads(course_ID)
            
            query = query.filter(RunCourse.course_ID.in_(course_ID))
           
        if coursecatID and coursecatID != "[]":
            coursecatID = json.loads(coursecatID)
            query = query.filter(Course.coursecat_ID.in_(coursecatID))

        if rcourse_ID and rcourse_ID != "[]":
            # Filter by rcourse_ID
            rcourse_ID = json.loads(rcourse_ID)
            query = query.filter(Feedback.rcourse_ID.in_(rcourse_ID))

        if instructorID and instructorID != "[]":
            instructorID = json.loads(instructorID)
            query = query.filter(RunCourse.instructor_ID.in_(instructorID))

        if start_date:
            formatted_start_date = datetime.strptime(start_date, '%Y-%m-%d').date()

        if end_date:
            formatted_end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        if formatted_start_date and formatted_end_date: 
            query = query.filter(RunCourse.run_Startdate >= formatted_start_date, RunCourse.run_Enddate <= formatted_end_date)
        
        results = query.all()
        
        db.session.close()

        if results:
            result_data = []
            for result in results:
                feedback = {
                    "answer": result[0],
                }
                result_data.append(feedback)

            # Create a Pandas DataFrame from the result_data list
            df_instructor_improve = pd.DataFrame(result_data)
            df_instructor_improve = drop_col(df_instructor_improve)
            
            df_instructor_improve['preprocessed_text'] = preprocess_text(df_instructor_improve['answer'])
            corpus = df_instructor_improve['preprocessed_text']

            n_topics_range = range(2, 9)
            max_df_range = [0.70, 0.75, 0.80, 0.85, 0.9, 0.95]
            
            best_n_topics, best_max_df, best_silhouette_score = tune_nmf_hyperparameters(corpus, n_topics_range, max_df_range)

            if best_n_topics is None:
                return jsonify({"code": 200, "data": [], "topic_words_list": []})

            tfidf_vectorizer = TfidfVectorizer(max_df=best_max_df, stop_words='english')
            tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)

            nmf_model = NMF(n_components=best_n_topics, random_state=1)
            nmf_matrix = nmf_model.fit_transform(tfidf_matrix)

            feature_names = tfidf_vectorizer.get_feature_names_out()
            topic_words_list = []

            for topic_idx, topic in enumerate(nmf_model.components_):
                top_words_indices = topic.argsort()[:-15 - 1:-1]
                top_words = [feature_names[i] for i in top_words_indices]
                top_word_probabilities = [topic[i] for i in top_words_indices]
                topic_data = [{"word": word, "size": prob} for word, prob in zip(top_words, top_word_probabilities)]
                topic_words_list.append(topic_data)
            
            topic_words_list_formatted = []

            for topic_words in topic_words_list:
                word_data = {"wordData": topic_words}
                topic_words_list_formatted.append(word_data)

            dominant_topics = nmf_matrix.argmax(axis=1) + 1
            df_instructor_improve['topic_number'] = dominant_topics

            # Convert the DataFrame to JSON
            response_data = df_instructor_improve.to_dict(orient='records')

            return jsonify({"code": 200, "data": response_data, "topic_words_list": topic_words_list_formatted})

        return jsonify({"code": 404, "message": "No matching course interest information found"})

# ================================================== For Sentiment Analysis ================================================== #
def filter_dataframe(df):
    # Define a list of values to drop (in lowercase)
    values_to_drop = ['nil', '-', 'na', 'none', 'nan', 'nothing']

    # Apply the mask to filter the DataFrame
    filtered_df = df[~df['Feedback'].str.lower().isin(values_to_drop)]

    return filtered_df

def text_preprocess(text):

    # Remove characters that are not letters or whitespace, but retain punctuation, case and hyphen words
    cleaned_text = re.sub(r'[^a-zA-Z\s.,!?-]', '', text)

    return cleaned_text

def count_words(text):
    words = text.split()
    return len(words)

def Sentiment(x):
    if x>= 0.05:
        return "Positive"
    elif x<= -0.05:
        return "Negative"
    else:
        return "Neutral"

# Get the sentiment for all courses
course_sentiment_data = api.parser()
# Define the course_ID parameter to accept either an integer or an array of integers
course_sentiment_data.add_argument("course_ID", help="Enter course ID")
course_sentiment_data.add_argument("coursecat_ID", help="Enter course category ID")
course_sentiment_data.add_argument("rcourse_ID",  help="Enter run course ID")
course_sentiment_data.add_argument("instructor_ID", help="Enter instructor ID")
course_sentiment_data.add_argument("run_Startdate", help="Enter run start date")
course_sentiment_data.add_argument("run_Enddate", help="Enter run end date")

@api.route("/course_sentiment_data")
@api.doc(description="Get sentiment data from course feedbacks")
class CourseSentimentData(Resource):
    @api.expect(course_sentiment_data)
    def get(self):
        try: 

            # Parse the course_ID from the request arguments
            args = course_sentiment_data.parse_args()
            courseID = args.get("course_ID", "")
            coursecatID = args.get("coursecat_ID", "")
            rcourseID = args.get("rcourse_ID", "")
            instructorID = args.get("instructor_ID", "")
            start_date = args.get('run_Startdate', "")
            end_date = args.get("run_Enddate", "")

            formatted_start_date = None
            formatted_end_date = None

            query = (
                db.session.query(Course, RunCourse, Feedback, TemplateAttribute)
                .join(RunCourse, Course.course_ID == RunCourse.course_ID)  # Join Course and RunCourse using course_id
                .join(Feedback, RunCourse.rcourse_ID == Feedback.rcourse_ID)  # Join RunCourse and Feedback using rcourse_id
                .join(TemplateAttribute, Feedback.template_Attribute_ID == TemplateAttribute.template_Attribute_ID)  # Join Feedback and TemplateAttribute using attribute_id
                .filter(func.lower(TemplateAttribute.question).like("%course%"))
                .filter(TemplateAttribute.input_Type == "Text Field")
            )

            if courseID and courseID != "[]":
                courseID = json.loads(courseID)
                
                query = query.filter(RunCourse.course_ID.in_(courseID))
                

            if coursecatID and coursecatID != "[]":
                coursecatID = json.loads(coursecatID)
                query = query.filter(Course.coursecat_ID.in_(coursecatID))

            if rcourseID and rcourseID != "[]":
                # Filter by rcourse_ID
                rcourseID = json.loads(rcourseID)
                query = query.filter(Feedback.rcourse_ID.in_(rcourseID))

            if instructorID and instructorID != "[]":
                instructorID = json.loads(instructorID)
                query = query.filter(RunCourse.instructor_ID.in_(instructorID))

            if start_date:
                formatted_start_date = datetime.strptime(start_date, '%Y-%m-%d').date()

            if end_date:
                formatted_end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

            if formatted_start_date and formatted_end_date: 
                query = query.filter(RunCourse.run_Startdate >= formatted_start_date, RunCourse.run_Enddate <= formatted_end_date)

            # Fetch the results
            filtered_results = query.all()
            
            db.session.close()
                        
            if filtered_results:

                # Serialize each object within the list dynamically
                serialized_results = []
                for course, runcourse, feedback, attribute in filtered_results:
                    serialized_result = {}
                    for field in course.__table__.columns.keys():
                        serialized_result[field] = getattr(course, field)
                    for field in runcourse.__table__.columns.keys():
                        serialized_result[field] = getattr(runcourse, field)    
                    for field in feedback.__table__.columns.keys():
                        serialized_result[field] = getattr(feedback, field)
                    for field in attribute.__table__.columns.keys():
                        serialized_result[field] = getattr(attribute, field)
                    serialized_results.append(serialized_result)

                # Extract all "answer" values into a list
                answers = [entry["answer"] for entry in serialized_results]

                # Create a DataFrame from the "answer" values
                df = pd.DataFrame({"Feedback": answers})
                
                df.dropna(inplace=True)

                filtered_df = filter_dataframe(df)

                filtered_df['Preprocessed_Feedback'] = filtered_df['Feedback'].apply(text_preprocess)

                # Apply the count_words function to the "text" column
                filtered_df['Total_Length'] = filtered_df['Preprocessed_Feedback'].apply(count_words)

                analyser = SentimentIntensityAnalyzer()

                filtered_df['Scores'] = filtered_df['Preprocessed_Feedback'].apply(lambda review: analyser.polarity_scores(review))

                filtered_df['Compound']  = filtered_df['Scores'].apply(lambda score_dict: score_dict['compound'])

                filtered_df['Sentiment'] = filtered_df['Compound'].apply(Sentiment)

                data_list = filtered_df.to_dict(orient="records")

                # Calculate sentiment counts
                sentiment_counts = Counter(filtered_df['Sentiment'])

                # Calculate the total count of all sentiment labels
                total_count = sum(sentiment_counts.values())

                # Extract labels and counts from the sentiment_counts dictionary
                labels = list(sentiment_counts.keys())
                counts = list(sentiment_counts.values())
                percentages = [round(count / total_count * 100, 1) for count in counts]  # Format to 2 decimal places

                return jsonify(
                    {
                        "code": 200,
                        #"data": data_list,
                        "sentiment_labels": labels,
                        "sentiment_percentages": percentages
                    }
                )


            return jsonify(
                {
                    "code": 400,
                    "message": "No course feedbacks found"
                }
            )

        except Exception as e:
            
            return jsonify(
                {
                    "code": 500,
                    "message": "Failed to retreive course feedbacks: " + str(e)
                }
            )

#Get sentiment for all instructors 
instructor_sentiment_data = api.parser()

instructor_sentiment_data.add_argument("course_ID", help="Enter course ID")
instructor_sentiment_data.add_argument("coursecat_ID", help="Enter course category ID")
instructor_sentiment_data.add_argument("rcourse_ID", help="Enter run course ID")
instructor_sentiment_data.add_argument("instructor_ID", help="Enter instructor ID")
instructor_sentiment_data.add_argument("run_Startdate", help="Enter run start date")
instructor_sentiment_data.add_argument("run_Enddate", help="Enter run end date")

@api.route("/instructor_sentiment_data")
@api.doc(description="Get sentiment data from instructor feedbacks")
class InstructorSentimentData(Resource):
    @api.expect(instructor_sentiment_data)
    def get(self):
        try: 
            # Parse the course_ID from the request arguments
            args = instructor_sentiment_data.parse_args()
            courseID = args.get("course_ID", "")
            coursecatID = args.get("coursecat_ID", "")
            rcourseID = args.get("rcourse_ID", "")
            instructorID = args.get("instructor_ID", "")
            start_date = args.get('run_Startdate', "")
            end_date = args.get("run_Enddate", "")

            formatted_start_date = None
            formatted_end_date = None

            query = (
                db.session.query(Course, RunCourse, Feedback, TemplateAttribute)
                .join(RunCourse, Course.course_ID == RunCourse.course_ID)  # Join Course and RunCourse using course_id
                .join(Feedback, RunCourse.rcourse_ID == Feedback.rcourse_ID)  # Join RunCourse and Feedback using rcourse_id
                .join(TemplateAttribute, Feedback.template_Attribute_ID == TemplateAttribute.template_Attribute_ID)  # Join Feedback and TemplateAttribute using attribute_id
                .filter(func.lower(TemplateAttribute.question).like("%instructor%"))
                .filter(TemplateAttribute.input_Type == "Text Field")
            )

            if courseID and courseID != "[]":
                courseID = json.loads(courseID)
                query = query.filter(RunCourse.course_ID.in_(courseID))
                #print("running", str(query))

            if coursecatID and coursecatID != "[]":
                coursecatID = json.loads(coursecatID)
                query = query.filter(Course.coursecat_ID.in_(coursecatID))

            if rcourseID and rcourseID != "[]":
                # Filter by rcourse_ID
                rcourseID = json.loads(rcourseID)
                query = query.filter(Feedback.rcourse_ID.in_(rcourseID))

            if instructorID and instructorID != "[]":
                instructorID = json.loads(instructorID)
                query = query.filter(RunCourse.instructor_ID.in_(instructorID))

            if start_date:
                formatted_start_date = datetime.strptime(start_date, '%Y-%m-%d').date()

            if end_date:
                formatted_end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

            if formatted_start_date and formatted_end_date: 
                query = query.filter(RunCourse.run_Startdate >= formatted_start_date, RunCourse.run_Enddate <= formatted_end_date)

            # Fetch the results
            filtered_results = query.all()
            db.session.close()
            
            if filtered_results:
                # Serialize each object within the list dynamically
                serialized_results = []
                for course, runcourse, feedback, attribute in filtered_results:
                    serialized_result = {}
                    for field in course.__table__.columns.keys():
                        serialized_result[field] = getattr(course, field)
                    for field in runcourse.__table__.columns.keys():
                        serialized_result[field] = getattr(runcourse, field)    
                    for field in feedback.__table__.columns.keys():
                        serialized_result[field] = getattr(feedback, field)
                    for field in attribute.__table__.columns.keys():
                        serialized_result[field] = getattr(attribute, field)
                    serialized_results.append(serialized_result)

                # Extract all "answer" values into a list
                answers = [entry["answer"] for entry in serialized_results]

                # Create a DataFrame from the "answer" values
                df = pd.DataFrame({"Feedback": answers})
                
                df.dropna(inplace=True)

                filtered_df = filter_dataframe(df)

                filtered_df['Preprocessed_Feedback'] = filtered_df['Feedback'].apply(text_preprocess)

                # Apply the count_words function to the "text" column
                filtered_df['Total_Length'] = filtered_df['Preprocessed_Feedback'].apply(count_words)

                analyser = SentimentIntensityAnalyzer()

                filtered_df['Scores'] = filtered_df['Preprocessed_Feedback'].apply(lambda review: analyser.polarity_scores(review))

                filtered_df['Compound']  = filtered_df['Scores'].apply(lambda score_dict: score_dict['compound'])

                filtered_df['Sentiment'] = filtered_df['Compound'].apply(Sentiment)

                data_list = filtered_df.to_dict(orient="records")

                # Calculate sentiment counts
                sentiment_counts = Counter(filtered_df['Sentiment'])

                # Calculate the total count of all sentiment labels
                total_count = sum(sentiment_counts.values())

                # Extract labels and counts from the sentiment_counts dictionary
                labels = list(sentiment_counts.keys())
                counts = list(sentiment_counts.values())
                percentages = [round(count / total_count * 100, 1) for count in counts]  # Format to 2 decimal places

                return jsonify(
                    {
                        "code": 200,
                        #"data": data_list,
                        "sentiment_labels": labels,
                        "sentiment_percentages": percentages
                    }
                )


            return jsonify(
                {
                    "code": 400,
                    "message": "No instructor feedbacks found"
                }
            )

        except Exception as e:
           
            #return "Failed" + str(e), 500
            return jsonify(
                {
                    "code": 500,
                    "message": "Failed to retreive instructor feedbacks: " + str(e)
                }
            )

def remove_punctuations(text):
    
    # Remove characters that are not letters, spaces, or hyphens
    text = re.sub(r'[^\w\s-]', '', text)
    
    return text 

def remove_contractions(text):

    #Removes contractions from text input using regular expressions.
    return re.sub(r"(\w+)('ve|'m)", r"\1", text)

def remove_stopwords(text):
    words = text.split()
    filtered_words = [word for word in words if word.lower() not in stop_words]
    return ' '.join(filtered_words)

def load_words_from_file():
    """
    Read words from fixed files and return them as sets.

    Returns:
        tuple: A tuple containing two sets - positive words and negative words.
    """
    # Get the current working directory
    current_directory = os.getcwd()

    # Construct the path using os.path.join()
    positive_words_file = os.path.join(current_directory, 'lexicons', 'positive-words.txt')
    # Read the positive-words.txt file
    with open(positive_words_file, 'r') as file:
        positive_words = file.read()

    # Construct the path using os.path.join()
    negative_words_file = os.path.join(current_directory, 'lexicons', 'negative-words.txt')
    # Read the negative-words.txt file
    with open(negative_words_file, 'r') as file:
        negative_words = file.read()

    return positive_words, negative_words
    
# Get the sentiment for all courses
course_wordcloud_data = api.parser()

course_wordcloud_data.add_argument("course_ID", help="Enter course ID")
course_wordcloud_data.add_argument("coursecat_ID", help="Enter course category ID")
course_wordcloud_data.add_argument("rcourse_ID", help="Enter run course ID")
course_wordcloud_data.add_argument("instructor_ID", help="Enter instructor ID")
course_wordcloud_data.add_argument("run_Startdate", help="Enter run start date")
course_wordcloud_data.add_argument("run_Enddate", help="Enter run end date")

@api.route("/course_wordcloud_data")
@api.doc(description="Get wordcloud data from course feedbacks")
class CourseWordcloudData(Resource):
    @api.expect(course_wordcloud_data)
    def get(self):
        try: 

            # Parse the course_ID from the request arguments
            args = course_wordcloud_data.parse_args()
            courseID = args.get("course_ID", "")
            coursecatID = args.get("coursecat_ID", "")
            rcourseID = args.get("rcourse_ID", "")
            instructorID = args.get("instructor_ID", "")
            start_date = args.get('run_Startdate', "")
            end_date = args.get("run_Enddate", "")

            formatted_start_date = None
            formatted_end_date = None

            query = (
                db.session.query(Course, RunCourse, Feedback, TemplateAttribute)
                .join(RunCourse, Course.course_ID == RunCourse.course_ID)  # Join Course and RunCourse using course_id
                .join(Feedback, RunCourse.rcourse_ID == Feedback.rcourse_ID)  # Join RunCourse and Feedback using rcourse_id
                .join(TemplateAttribute, Feedback.template_Attribute_ID == TemplateAttribute.template_Attribute_ID)  # Join Feedback and TemplateAttribute using attribute_id
                .filter(func.lower(TemplateAttribute.question).like("%course%"))
                .filter(TemplateAttribute.input_Type == "Text Field")
            )

            if courseID and courseID != "[]":
                courseID = json.loads(courseID)
                query = query.filter(RunCourse.course_ID.in_(courseID))
                

            if coursecatID and coursecatID != "[]":
                coursecatID = json.loads(coursecatID)
                query = query.filter(Course.coursecat_ID.in_(coursecatID))

            if rcourseID and rcourseID != "[]":
                # Filter by rcourse_ID
                rcourseID = json.loads(rcourseID)
                query = query.filter(Feedback.rcourse_ID.in_(rcourseID))

            if instructorID and instructorID != "[]":
                instructorID = json.loads(instructorID)
                query = query.filter(RunCourse.instructor_ID.in_(instructorID))

            if start_date:
                formatted_start_date = datetime.strptime(start_date, '%Y-%m-%d').date()

            if end_date:
                formatted_end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

            if formatted_start_date and formatted_end_date: 
                query = query.filter(RunCourse.run_Startdate >= formatted_start_date, RunCourse.run_Enddate <= formatted_end_date)

            # Fetch the results
            filtered_results = query.all()
            db.session.close()
            
            if filtered_results:
                # Serialize each object within the list dynamically
                serialized_results = []
                for course, runcourse, feedback, attribute in filtered_results:
                    serialized_result = {}
                    for field in course.__table__.columns.keys():
                        serialized_result[field] = getattr(course, field)
                    for field in runcourse.__table__.columns.keys():
                        serialized_result[field] = getattr(runcourse, field)    
                    for field in feedback.__table__.columns.keys():
                        serialized_result[field] = getattr(feedback, field)
                    for field in attribute.__table__.columns.keys():
                        serialized_result[field] = getattr(attribute, field)
                    serialized_results.append(serialized_result)

                # Extract all "answer" values into a list
                answers = [entry["answer"] for entry in serialized_results]

                # Create a DataFrame from the "answer" values
                df = pd.DataFrame({"Feedback": answers})
                
                df.dropna(inplace=True)

                filtered_df = filter_dataframe(df)

                filtered_df['Preprocessed_Feedback'] = filtered_df['Feedback'].apply(text_preprocess)

                # Apply the count_words function to the "text" column
                filtered_df['Total_Length'] = filtered_df['Preprocessed_Feedback'].apply(count_words)

                analyser = SentimentIntensityAnalyzer()

                filtered_df['Scores'] = filtered_df['Preprocessed_Feedback'].apply(lambda review: analyser.polarity_scores(review))

                filtered_df['Compound']  = filtered_df['Scores'].apply(lambda score_dict: score_dict['compound'])

                filtered_df['Sentiment'] = filtered_df['Compound'].apply(Sentiment)

                filtered_df['Cleaned_Feedback'] = filtered_df['Preprocessed_Feedback'].apply(lambda x: x.lower())

                filtered_df['Cleaned_Feedback'] = filtered_df['Cleaned_Feedback'].apply(remove_punctuations)
                
                filtered_df['Cleaned_Feedback'] = filtered_df['Cleaned_Feedback'].apply(remove_contractions)

                filtered_df['Cleaned_Feedback'] = filtered_df['Cleaned_Feedback'].apply(remove_stopwords)

                positive_words, negative_words = load_words_from_file()

                # Filter words based on positive lexicon
                positive_feedback_words = [word for feedback in filtered_df[filtered_df['Sentiment'] == 'Positive']['Cleaned_Feedback'] for word in feedback.split() if word.lower() in positive_words]

                # Filter words based on negative lexicon
                negative_feedback_words = [word for feedback in filtered_df[filtered_df['Sentiment'] == 'Negative']['Cleaned_Feedback'] for word in feedback.split() if word.lower() in negative_words]

                # Count the frequency of each word in positive feedback
                positive_word_counts = Counter(positive_feedback_words)

                # Count the frequency of each word in negative feedback
                negative_word_counts = Counter(negative_feedback_words)

                # Convert the word counts to the desired format: [{"word": word, "size": count}, ...]
                positive_word_data = [{"word": word, "size": count} for word, count in positive_word_counts.items()]
                negative_word_data = [{"word": word, "size": count} for word, count in negative_word_counts.items()]

                return jsonify(
                    {
                        "code": 200,
                        "positive_word_data": positive_word_data,
                        "negative_word_data": negative_word_data
                    }
                )

            return jsonify(
                {
                    "code": 400,
                    "message": "No course feedbacks found"
                }
            )

        except Exception as e:
           
            #return "Failed" + str(e), 500
            return jsonify(
                {
                    "code": 500,
                    "message": "Failed to retreive course feedbacks: " + str(e)
                }
            )

#Get sentiment for all instructors 
instructor_wordcloud_data = api.parser()

instructor_wordcloud_data.add_argument("course_ID", help="Enter course ID")
instructor_wordcloud_data.add_argument("coursecat_ID", help="Enter course category ID")
instructor_wordcloud_data.add_argument("rcourse_ID", help="Enter run course ID")
instructor_wordcloud_data.add_argument("instructor_ID", help="Enter instructor ID")
instructor_wordcloud_data.add_argument("run_Startdate", help="Enter run start date")
instructor_wordcloud_data.add_argument("run_Enddate", help="Enter run end date")

@api.route("/instructor_wordcloud_data")
@api.doc(description="Get wordcloud data from instructor feedbacks")
class InstructorWordcloudData(Resource):
    @api.expect(instructor_wordcloud_data)
    def get(self):
        try: 

            # Parse the course_ID from the request arguments
            args = course_wordcloud_data.parse_args()
            courseID = args.get("course_ID", "")
            coursecatID = args.get("coursecat_ID", "")
            rcourseID = args.get("rcourse_ID", "")
            instructorID = args.get("instructor_ID", "")
            start_date = args.get('run_Startdate', "")
            end_date = args.get("run_Enddate", "")

            formatted_start_date = None
            formatted_end_date = None

            query = (
                db.session.query(Course, RunCourse, Feedback, TemplateAttribute)
                .join(RunCourse, Course.course_ID == RunCourse.course_ID)  # Join Course and RunCourse using course_id
                .join(Feedback, RunCourse.rcourse_ID == Feedback.rcourse_ID)  # Join RunCourse and Feedback using rcourse_id
                .join(TemplateAttribute, Feedback.template_Attribute_ID == TemplateAttribute.template_Attribute_ID)  # Join Feedback and TemplateAttribute using attribute_id
                .filter(func.lower(TemplateAttribute.question).like("%instructor%"))
                .filter(TemplateAttribute.input_Type == "Text Field")
            )

            if courseID and courseID != "[]":
                courseID = json.loads(courseID)
                
                query = query.filter(RunCourse.course_ID.in_(courseID))
                

            if coursecatID and coursecatID != "[]":
                coursecatID = json.loads(coursecatID)
                query = query.filter(Course.coursecat_ID.in_(coursecatID))

            if rcourseID and rcourseID != "[]":
                # Filter by rcourse_ID
                rcourseID = json.loads(rcourseID)
                query = query.filter(Feedback.rcourse_ID.in_(rcourseID))

            if instructorID and instructorID != "[]":
                instructorID = json.loads(instructorID)
                query = query.filter(RunCourse.instructor_ID.in_(instructorID))

            if start_date:
                formatted_start_date = datetime.strptime(start_date, '%Y-%m-%d').date()

            if end_date:
                formatted_end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

            if formatted_start_date and formatted_end_date: 
                query = query.filter(RunCourse.run_Startdate >= formatted_start_date, RunCourse.run_Enddate <= formatted_end_date)

            # Fetch the results
            filtered_results = query.all()
            db.session.close()
            
            if filtered_results:
                # Serialize each object within the list dynamically
                serialized_results = []
                for course, runcourse, feedback, attribute in filtered_results:
                    serialized_result = {}
                    for field in course.__table__.columns.keys():
                        serialized_result[field] = getattr(course, field)
                    for field in runcourse.__table__.columns.keys():
                        serialized_result[field] = getattr(runcourse, field)    
                    for field in feedback.__table__.columns.keys():
                        serialized_result[field] = getattr(feedback, field)
                    for field in attribute.__table__.columns.keys():
                        serialized_result[field] = getattr(attribute, field)
                    serialized_results.append(serialized_result)

                # Extract all "answer" values into a list
                answers = [entry["answer"] for entry in serialized_results]

                # Create a DataFrame from the "answer" values
                df = pd.DataFrame({"Feedback": answers})
                
                df.dropna(inplace=True)

                filtered_df = filter_dataframe(df)

                filtered_df['Preprocessed_Feedback'] = filtered_df['Feedback'].apply(text_preprocess)

                # Apply the count_words function to the "text" column
                filtered_df['Total_Length'] = filtered_df['Preprocessed_Feedback'].apply(count_words)

                analyser = SentimentIntensityAnalyzer()

                filtered_df['Scores'] = filtered_df['Preprocessed_Feedback'].apply(lambda review: analyser.polarity_scores(review))

                filtered_df['Compound']  = filtered_df['Scores'].apply(lambda score_dict: score_dict['compound'])

                filtered_df['Sentiment'] = filtered_df['Compound'].apply(Sentiment)

                filtered_df['Cleaned_Feedback'] = filtered_df['Preprocessed_Feedback'].apply(lambda x: x.lower())

                filtered_df['Cleaned_Feedback'] = filtered_df['Cleaned_Feedback'].apply(remove_punctuations)
                
                filtered_df['Cleaned_Feedback'] = filtered_df['Cleaned_Feedback'].apply(remove_contractions)

                filtered_df['Cleaned_Feedback'] = filtered_df['Cleaned_Feedback'].apply(remove_stopwords)

                positive_words, negative_words = load_words_from_file()

                # Filter words based on positive lexicon
                positive_feedback_words = [word for feedback in filtered_df[filtered_df['Sentiment'] == 'Positive']['Cleaned_Feedback'] for word in feedback.split() if word.lower() in positive_words]

                # Filter words based on negative lexicon
                negative_feedback_words = [word for feedback in filtered_df[filtered_df['Sentiment'] == 'Negative']['Cleaned_Feedback'] for word in feedback.split() if word.lower() in negative_words]

                # Count the frequency of each word in positive feedback
                positive_word_counts = Counter(positive_feedback_words)

                # Count the frequency of each word in negative feedback
                negative_word_counts = Counter(negative_feedback_words)

                # Convert the word counts to the desired format: [{"word": word, "size": count}, ...]
                positive_word_data = [{"word": word, "size": count} for word, count in positive_word_counts.items()]
                negative_word_data = [{"word": word, "size": count} for word, count in negative_word_counts.items()]

                return jsonify(
                    {
                        "code": 200,
                        "positive_word_data": positive_word_data,
                        "negative_word_data": negative_word_data
                    }
                )

            return jsonify(
                {
                    "code": 400,
                    "message": "No instructor feedbacks found"
                }
            )

        except Exception as e:
            print("Error:", str(e))
            #return "Failed" + str(e), 500
            return jsonify(
                {
                    "code": 500,
                    "message": "Failed to retreive instructor feedbacks: " + str(e)
                }
            )

retrieve_course_name = api.parser()
retrieve_course_name.add_argument("course_id", help="Enter course id")

@api.route("/get_filtered_course_name")
@api.doc(description="Get course name")
class GetCourseName(Resource):
    @api.expect(retrieve_course_name)
    def get(self):
        args = retrieve_course_name.parse_args()
        course_id = args.get("course_id")

        query = Course.query

        # Filtering based on courseID if it's provided and not an empty list
        if course_id and course_id != "[]":
            courseID = json.loads(course_id)
            query = query.filter(Course.course_ID.in_(courseID))

        courses = query.all()

        db.session.close()

        if courses:
            course_names = [course.course_Name for course in courses]
           
            return jsonify({"code": 200, "data": course_names})
        else:
            
            return jsonify({"code": 404, "message": "Course not found"})
        
retrieve_runcourse_name = api.parser()
retrieve_runcourse_name.add_argument("rcourse_id", help="Enter rcourse id")

@api.route("/get_filtered_runcourse_name")
@api.doc(description="Get run course name")
class GetStudentName(Resource):
    @api.expect(retrieve_runcourse_name)
    def get(self):
        args = retrieve_runcourse_name.parse_args()
        rcourse_id = args.get("rcourse_id", "")

        query = RunCourse.query

        if rcourse_id and rcourse_id != "[]":
            rcourseID = json.loads(rcourse_id)
            query = query.filter(RunCourse.rcourse_ID.in_(rcourseID))

        runcourses = query.all()

        db.session.close()

        if runcourses:
            runcourse_names = [runcourse.run_Name for runcourse in runcourses]
            
            return jsonify({"code": 200, "data": runcourse_names})
        else:
            return jsonify({"code": 404, "message": "Course not found"})


retrieve_instructor_name = api.parser()
retrieve_instructor_name.add_argument("instructor_id", help="Enter rcourse id")

@api.route("/get_filtered_user_name")
class GetUserName(Resource):
    @api.expect(retrieve_instructor_name)
    def get(self):
        args = retrieve_instructor_name.parse_args()
        instructor_id = args.get("instructor_id", "")

        query = User.query

        if instructor_id and instructor_id != "[]":
            instructorIDs = json.loads(instructor_id)
            query = query.filter(User.user_ID.in_(instructorIDs))

        users = query.all()

        db.session.close()

        if users:
            runcourse_names = [user.user_Name for user in users]
            
            return jsonify({"code": 200, "data": runcourse_names})
        else:
            return jsonify({"code": 404, "message": "Course not found"})