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
import ast
import contractions
import gensim
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

# To get course average ratings - all and specific
average_course_ratings = api.parser()
average_course_ratings.add_argument("course_ID", help="Enter course_ID")
average_course_ratings.add_argument("runcourse_ID", help="Enter runcourse_ID")

@api.route("/course_average_ratings")
@api.doc(description="Course specific feedback")
class CourseAverageRatings(Resource):
    def get(self):
        args = average_course_ratings.parse_args()
        course_ID = args.get("course_ID", "")
        runcourse_ID = args.get("runcourse_ID", "")

        keywords = ['course']  # Define keywords to identify relevant questions

        try:
            total_ratings = []
            total_questions = 0

            # To retrieve relevant questions and calculate average rating
            relevant_questions = db.session.query(FeedbackTemplate, TemplateAttribute) \
                .join(TemplateAttribute, FeedbackTemplate.template_ID == TemplateAttribute.template_ID) \
                .join(Feedback, Feedback.template_Attribute_ID == TemplateAttribute.template_Attribute_ID) \
                .join(RunCourse, RunCourse.rcourse_ID == Feedback.rcourse_ID) \
                .filter(TemplateAttribute.input_Type == 'Likert Scale')

            for keyword in keywords:
                relevant_questions = relevant_questions.filter(func.lower(TemplateAttribute.question).contains(keyword))

            if runcourse_ID:
                relevant_questions = relevant_questions.filter(RunCourse.rcourse_ID == runcourse_ID)  # Filter by a specific "Run Course" if runcourse_ID is provided
            
            if course_ID:
                relevant_questions = relevant_questions.filter(RunCourse.course_ID == course_ID)

            for feedback_template, template_attribute in relevant_questions:
                question_id = template_attribute.template_Attribute_ID
                feedback_entries = db.session.query(Feedback) \
                    .filter(Feedback.template_Attribute_ID == question_id)

                if runcourse_ID:
                    feedback_entries = feedback_entries.filter(Feedback.rcourse_ID == runcourse_ID)  # Filter by a specific "Run Course" if runcourse_ID is provided
                
                if course_ID:
                    feedback_entries = feedback_entries.filter(Feedback.rcourse_ID.in_(db.session.query(RunCourse.rcourse_ID).filter(RunCourse.course_ID == course_ID)))

                feedback_entries = feedback_entries.all()

                if feedback_entries:
                    for entry in feedback_entries:
                        total_ratings.append(int(entry.answer))  # Assuming 'answer' contains the Likert Scale value as an integer
                        total_questions += 1
            
            total_feedback = int(total_questions / len(relevant_questions.all()))

            # Calculate the overall average rating
            if total_ratings and total_questions > 0:
                overall_average_rating = round(sum(total_ratings) / total_questions, 2)
                message = "Course ratings calculated successfully."
            else:
                overall_average_rating = 0
                message = "No ratings"

            db.session.close()

            response_data = {
                "code": 200,
                "data": {
                    "course_ID": course_ID,
                    "runcourse_ID": runcourse_ID,
                    "overall_average_rating": overall_average_rating,
                    "total_feedback": total_feedback
                },
                "message": message,
            }
        
        except Exception as e:
            response_data = {
                "code": 500,
                "message": str(e)
            }

        return jsonify(response_data)


# To get instructor specific average ratings
instructor_average_ratings = api.parser()
instructor_average_ratings.add_argument("course_ID", help="Enter course_ID")
instructor_average_ratings.add_argument("runcourse_ID", help="Enter runcourse_ID")

@api.route("/instructor_average_ratings")
@api.doc(description="Instructor specific feedback")
class InstructorAverageRatings(Resource):
    @api.expect(instructor_average_ratings)
    def get(self):
        args = instructor_average_ratings.parse_args()
        course_ID = args.get("course_ID", "")
        runcourse_ID = args.get("runcourse_ID", "")
        instructor_ID = args.get("instructor_ID", "")

        keywords = ['instructor']  # Define keywords to identify relevant questions
        try:
            total_ratings = []
            total_questions = 0

            # To retrieve relevant questions and calculate average rating
            relevant_questions = db.session.query(FeedbackTemplate, TemplateAttribute) \
                .join(TemplateAttribute, FeedbackTemplate.template_ID == TemplateAttribute.template_ID) \
                .join(Feedback, Feedback.template_Attribute_ID == TemplateAttribute.template_Attribute_ID) \
                .join(RunCourse, Feedback.rcourse_ID == RunCourse.rcourse_ID) \
                .filter(TemplateAttribute.input_Type == 'Likert Scale')
            
            for keyword in keywords:
                relevant_questions = relevant_questions.filter(func.lower(TemplateAttribute.question).contains(keyword))
                
            # Filter by course_ID and runcourse_ID
            if course_ID:
                relevant_questions = relevant_questions.filter(RunCourse.course_ID == course_ID)
            if runcourse_ID:
                relevant_questions = relevant_questions.filter(RunCourse.rcourse_ID == runcourse_ID)
            
            # Filter by instructor ID if provided
            if instructor_ID:
                relevant_questions = relevant_questions.filter(RunCourse.instructor_ID == instructor_ID)

            relevant_questions = relevant_questions.all()

            for feedback_template, template_attribute in relevant_questions:
                question_id = template_attribute.template_Attribute_ID
                feedback_entries = db.session.query(Feedback) \
                    .filter(Feedback.template_Attribute_ID == question_id)

                # Filter by course_ID and runcourse_ID
                if course_ID:
                    feedback_entries = feedback_entries.filter(Feedback.rcourse_ID.in_(db.session.query(RunCourse.rcourse_ID).filter(RunCourse.course_ID == course_ID)))
                if runcourse_ID:
                    feedback_entries = feedback_entries.filter(Feedback.rcourse_ID == runcourse_ID)

                # Filter by instructor ID if provided
                if instructor_ID:
                    feedback_entries = feedback_entries.join(RunCourse, Feedback.rcourse_ID == RunCourse.rcourse_ID) \
                        .filter(RunCourse.instructor_ID == instructor_ID)

                feedback_entries = feedback_entries.all()

                if feedback_entries:
                    for entry in feedback_entries:
                        if entry.answer.isdigit():
                            total_ratings.append(int(entry.answer))
                            total_questions += 1

            # Calculate the instructor-specific average rating
            if total_ratings and total_questions > 0:
                instructor_average_rating = round(sum(total_ratings) / total_questions, 2)
                message = "Instructor ratings calculated successfully."
            else:
                instructor_average_rating = 0
                message = "No ratings for this instructor."

            db.session.close()

            response_data = {
                "code": 200,
                "data": {
                    "course_ID": course_ID,
                    "runcourse_ID": runcourse_ID,
                    "instructor_ID": instructor_ID,
                    "instructor_average_rating": instructor_average_rating
                },
                "message": message,
            }

        except Exception as e:
            response_data = {
                "code": 500,
                "message": str(e)
            }

        return jsonify(response_data)


def drop_col(df):
    df = df.dropna(how='all')
    values_to_drop = ["nil", "none", "-", "na", "nan", "nothing"]
    df = df[~df['answer'].isin(values_to_drop)]
    drop = ['na', 'nil']
    df = df[~df['answer'].apply(lambda x: any(word in x.lower() for word in drop))]


    df.reset_index(drop=True, inplace=True)
    return df

# ================================================== For Topic Modeling ================================================== #
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
            
    # print("best_n_topics", best_n_topics)
    # print("best_max_df", best_max_df)
    # print("best_silhouette_score", best_silhouette_score)

    
    return best_n_topics, best_max_df, best_silhouette_score

# Get the topic for specific course or all courses (done well)
feedback_course_done_well_specific = api.parser()
feedback_course_done_well_specific.add_argument("course_ID", help="Enter course_ID")
feedback_course_done_well_specific.add_argument("runcourse_ID", help="Enter runcourse_ID")

@api.route("/feedback_course_done_well_specific")
@api.doc(description="Course-specific feedback")
class CourseDoneWellFeedback(Resource):
    @api.expect(feedback_course_done_well_specific)
    def get(self):
        # Parse the course_ID from the request arguments
        args = feedback_course_done_well_specific.parse_args()
        course_ID = args.get("course_ID", "")
        runcourse_ID = args.get("runcourse_ID", "")

        keywords = ['course']
        optional_keywords = ['done well', 'contributed', 'did well']

        query = (
                db.session.query(Feedback.answer)
                .join(TemplateAttribute, Feedback.template_Attribute_ID == TemplateAttribute.template_Attribute_ID)
                .filter(TemplateAttribute.input_Type == "Text Field")
            )

        if runcourse_ID:
            # Filter by rcourse_ID
            query = query.filter(Feedback.rcourse_ID == runcourse_ID)

        elif course_ID:
            # Join with RunCourse table and filter by course_ID
            query = query.join(RunCourse, Feedback.rcourse_ID == RunCourse.rcourse_ID)
            query = query.filter(RunCourse.course_ID == course_ID)
        

        for keyword in keywords:
            query = query.filter(func.lower(TemplateAttribute.question).contains(keyword))

        optional_keyword_filter = or_(
            *[
                func.lower(TemplateAttribute.question).contains(keyword)
                for keyword in optional_keywords
            ]
        )
        query = query.filter(optional_keyword_filter)

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
feedback_course_improve_specific.add_argument("runcourse_ID", help="Enter runcourse_ID")

@api.route("/feedback_course_improve_specific")
@api.doc(description="Course-specific feedback")
class CourseImproveFeedback(Resource):
    @api.expect(feedback_course_improve_specific)
    def get(self):
        # Parse the course_ID from the request arguments
        args = feedback_course_improve_specific.parse_args()
        course_ID = args.get("course_ID", "")
        runcourse_ID = args.get("runcourse_ID", "")

        keywords = ['course']
        optional_keywords = ['improve', 'suggestions']

        query = (
                db.session.query(Feedback.answer)
                .join(TemplateAttribute, Feedback.template_Attribute_ID == TemplateAttribute.template_Attribute_ID)
                .filter(TemplateAttribute.input_Type == "Text Field")
            )

        if runcourse_ID:
            # Filter by rcourse_ID
            query = query.filter(Feedback.rcourse_ID == runcourse_ID)

        elif course_ID:
            # Join with RunCourse table and filter by course_ID
            query = query.join(RunCourse, Feedback.rcourse_ID == RunCourse.rcourse_ID)
            query = query.filter(RunCourse.course_ID == course_ID)
        

        for keyword in keywords:
            query = query.filter(func.lower(TemplateAttribute.question).contains(keyword))

        optional_keyword_filter = or_(
            *[
                func.lower(TemplateAttribute.question).contains(keyword)
                for keyword in optional_keywords
            ]
        )
        query = query.filter(optional_keyword_filter)

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

@api.route("/feedback_instructor_done_well_specific")
@api.doc(description="Instructor-specific feedback")
class InstructorDoneWellFeedback(Resource):
    @api.expect(feedback_instructor_done_well_specific)
    def get(self):
        # Parse the user_ID from the request arguments
        args = feedback_instructor_done_well_specific.parse_args()
        courseID = args.get("course_ID", "")
        rcourseID = args.get("rcourse_ID", "")

        keywords = ['instructor']
        optional_keywords = ['did well', 'contributed', 'done well', 'strengths']

        query = (
                db.session.query(Feedback.answer)
                .join(TemplateAttribute, Feedback.template_Attribute_ID == TemplateAttribute.template_Attribute_ID)
                .filter(TemplateAttribute.input_Type == "Text Field")
            )

        if rcourseID:
            # Filter by rcourse_ID
            query = query.filter(Feedback.rcourse_ID == rcourseID)

        elif courseID:
            # Join with RunCourse table and filter by course_ID
            query = query.join(RunCourse, Feedback.rcourse_ID == RunCourse.rcourse_ID)
            query = query.filter(RunCourse.course_ID == courseID)

        for keyword in keywords:
            query = query.filter(func.lower(TemplateAttribute.question).contains(keyword))

        optional_keyword_filter = or_(
            *[
                func.lower(TemplateAttribute.question).contains(keyword)
                for keyword in optional_keywords
            ]
        )

        query = query.filter(optional_keyword_filter)
        
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
feedback_instructor_improve_specific.add_argument("rcourse_ID", help="Enter rcourse_ID")

@api.route("/feedback_instructor_improve_specific")
@api.doc(description="Instructor-specific feedback")
class InstructorDoneWellFeedback(Resource):
    @api.expect(feedback_instructor_improve_specific)
    def get(self):
        # Parse the user_ID from the request arguments
        args = feedback_instructor_improve_specific.parse_args()
        user_ID = args.get("user_ID", "")

        keywords = ['instructor']
        optional_keywords = ['improve', 'suggestions']

        courseID = args.get("course_ID", "")
        rcourseID = args.get("rcourse_ID", "")

        query = (
            db.session.query(Feedback.answer)
            .join(TemplateAttribute, Feedback.template_Attribute_ID == TemplateAttribute.template_Attribute_ID)
            .filter(TemplateAttribute.input_Type == "Text Field")
        )

        if rcourseID:
            # Filter by rcourse_ID
            query = query.filter(Feedback.rcourse_ID == rcourseID)

        elif courseID:
            # Join with RunCourse table and filter by course_ID
            query = query.join(RunCourse, Feedback.rcourse_ID == RunCourse.rcourse_ID)
            query = query.filter(RunCourse.course_ID == courseID)
        
        for keyword in keywords:
            query = query.filter(func.lower(TemplateAttribute.question).contains(keyword))
        
        optional_keyword_filter = or_(
            *[
                func.lower(TemplateAttribute.question).contains(keyword)
                for keyword in optional_keywords
            ]
        )
        query = query.filter(optional_keyword_filter)
        
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


def filter_dataframe(df):
    # Define a list of values to drop
    values_to_drop = ['NIL', 'nil', 'Nil', '-']

    # Create a boolean mask to select rows to keep (rows not in the values_to_drop list)
    mask = ~df['Feedback'].isin(values_to_drop)

    # Apply the mask to filter the DataFrame
    filtered_df = df[mask]

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
course_sentiment_data.add_argument("course_ID", help="Enter course_ID")
course_sentiment_data.add_argument("rcourse_ID", help="Enter rcourse_ID")

@api.route("/course_sentiment_data")
@api.doc(description="Get sentiment data from course feedbacks")
class CourseSentimentData(Resource):
    @api.expect(course_sentiment_data)
    def get(self):
        try: 

            # Parse the course_ID from the request arguments
            args = course_sentiment_data.parse_args()
            courseID = args.get("course_ID", "")
            rcourseID = args.get("rcourse_ID", "")

            query = (
                db.session.query(Feedback, TemplateAttribute)
                .join(TemplateAttribute, Feedback.template_Attribute_ID == TemplateAttribute.template_Attribute_ID)
                .filter(func.lower(TemplateAttribute.question).like("%course%"))
                .filter(TemplateAttribute.input_Type == "Text Field")
            )

            if rcourseID:
                # Filter by rcourse_ID
                query = query.filter(Feedback.rcourse_ID == rcourseID)

            elif courseID:
                # Join with RunCourse table and filter by course_ID
                query = query.join(RunCourse, Feedback.rcourse_ID == RunCourse.rcourse_ID)
                query = query.filter(RunCourse.course_ID == courseID)

            # Fetch the results
            filtered_results = query.all()
            db.session.close()
                        
            if filtered_results:
                # Serialize each object within the list dynamically
                serialized_results = []
                for feedback, attribute in filtered_results:
                    serialized_result = {}
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

                # Output the labels and counts lists
                #print("Sentiment Labels:", labels)
                #print("Sentiment Counts:", percentages)

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
            print("Error:", str(e))
            #return "Failed" + str(e), 500
            return jsonify(
                {
                    "code": 500,
                    "message": "Failed to retreive course feedbacks: " + str(e)
                }
            )

#Get sentiment for all instructors 
instructor_sentiment_data = api.parser()
instructor_sentiment_data.add_argument("course_ID", help="Enter course_ID")
instructor_sentiment_data.add_argument("rcourse_ID", help="Enter rcourse_ID")

@api.route("/instructor_sentiment_data")
@api.doc(description="Get sentiment data from instructor feedbacks")
class InstructorSentimentData(Resource):
    @api.expect(instructor_sentiment_data)
    def get(self):
        try: 
            # Parse the course_ID from the request arguments
            args = instructor_sentiment_data.parse_args()
            courseID = args.get("course_ID", "")
            rcourseID = args.get("rcourse_ID", "")

            query = (
                db.session.query(Feedback, TemplateAttribute)
                .join(TemplateAttribute, Feedback.template_Attribute_ID == TemplateAttribute.template_Attribute_ID)
                .filter(func.lower(TemplateAttribute.question).like("%instructor%"))
                .filter(TemplateAttribute.input_Type == "Text Field")
            )

            if rcourseID:
                # Filter by rcourse_ID
                query = query.filter(Feedback.rcourse_ID == rcourseID)

            elif courseID:
                # Join with RunCourse table and filter by course_ID
                query = query.join(RunCourse, Feedback.rcourse_ID == RunCourse.rcourse_ID)
                query = query.filter(RunCourse.course_ID == courseID)


            # Fetch the results
            filtered_results = query.all()
            db.session.close()
            
            if filtered_results:
                # Serialize each object within the list dynamically
                serialized_results = []
                for feedback, attribute in filtered_results:
                    serialized_result = {}
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

                # Output the labels and counts lists
                #print("Sentiment Labels:", labels)
                #print("Sentiment Counts:", percentages)

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
            print("Error:", str(e))
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
course_wordcloud_data.add_argument("course_ID", help="Enter course_ID")
course_wordcloud_data.add_argument("rcourse_ID", help="Enter rcourse_ID")

@api.route("/course_wordcloud_data")
@api.doc(description="Get wordcloud data from course feedbacks")
class CourseWordcloudData(Resource):
    @api.expect(course_wordcloud_data)
    def get(self):
        try: 

            # Parse the course_ID from the request arguments
            args = course_wordcloud_data.parse_args()
            courseID = args.get("course_ID", "")
            rcourseID = args.get("rcourse_ID", "")

            query = (
                db.session.query(Feedback, TemplateAttribute)
                .join(TemplateAttribute, Feedback.template_Attribute_ID == TemplateAttribute.template_Attribute_ID)
                .filter(func.lower(TemplateAttribute.question).like("%course%"))
                .filter(TemplateAttribute.input_Type == "Text Field")
            )

            if rcourseID:
                # Filter by rcourse_ID
                query = query.filter(Feedback.rcourse_ID == rcourseID)

            elif courseID:
                # Join with RunCourse table and filter by course_ID
                query = query.join(RunCourse, Feedback.rcourse_ID == RunCourse.rcourse_ID)
                query = query.filter(RunCourse.course_ID == courseID)

            # Fetch the results
            filtered_results = query.all()
            db.session.close()
            
            if filtered_results:
                # Serialize each object within the list dynamically
                serialized_results = []
                for feedback, attribute in filtered_results:
                    serialized_result = {}
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
            print("Error:", str(e))
            #return "Failed" + str(e), 500
            return jsonify(
                {
                    "code": 500,
                    "message": "Failed to retreive course feedbacks: " + str(e)
                }
            )

#Get sentiment for all instructors 
instructor_wordcloud_data = api.parser()
instructor_wordcloud_data.add_argument("course_ID", help="Enter course_ID")
instructor_wordcloud_data.add_argument("rcourse_ID", help="Enter rcourse_ID")

@api.route("/instructor_wordcloud_data")
@api.doc(description="Get wordcloud data from instructor feedbacks")
class InstructorWordcloudData(Resource):
    @api.expect(instructor_wordcloud_data)
    def get(self):
        try: 

            # Parse the course_ID from the request arguments
            args = course_wordcloud_data.parse_args()
            courseID = args.get("course_ID", "")
            rcourseID = args.get("rcourse_ID", "")

            query = (
                db.session.query(Feedback, TemplateAttribute)
                .join(TemplateAttribute, Feedback.template_Attribute_ID == TemplateAttribute.template_Attribute_ID)
                .filter(func.lower(TemplateAttribute.question).like("%instructor%"))
                .filter(TemplateAttribute.input_Type == "Text Field")
            )

            if rcourseID:
                # Filter by rcourse_ID
                query = query.filter(Feedback.rcourse_ID == rcourseID)

            elif courseID:
                # Join with RunCourse table and filter by course_ID
                query = query.join(RunCourse, Feedback.rcourse_ID == RunCourse.rcourse_ID)
                query = query.filter(RunCourse.course_ID == courseID)

            # Fetch the results
            filtered_results = query.all()
            db.session.close()
            
            if filtered_results:
                # Serialize each object within the list dynamically
                serialized_results = []
                for feedback, attribute in filtered_results:
                    serialized_result = {}
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
