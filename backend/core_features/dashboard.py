# from flask import request, jsonify
# from flask_restx import Namespace, Resource, fields
# from allClasses import *
# import json
# from sqlalchemy import func, and_, exists
# import logging
# app.logger.setLevel(logging.DEBUG)

# import pandas as pd 
# import numpy as np
# import nltk
# from nltk.corpus import stopwords # Import NLTK's stopwords corpus
# from nltk.stem import WordNetLemmatizer # Import the WordNet lemmatizer from NLTK
# import re # Import the regular expressions library for text processing
# import ast
# from sklearn.decomposition import NMF
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics import silhouette_score
# from sklearn.model_selection import train_test_split

# nltk.download('punkt') # Download NLTK's punkt tokenizer models
# nltk.download('stopwords') # Download NLTK's stopwords dataset
# nltk.download('wordnet') # Download NLTK's WordNet lexical database

# stop_words = set(stopwords.words('english')) # Setup stop words
# custom_stop_words = ['the', 'course', 'content', 'instructor', 'professor', 'prof', 'apply', 'learn', 'really', 'allow', 'provide', 'help', 'gave', 'give', 'think', 'could', 'would', 'can', 'will', 'check', 'make', 'made', 'time', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'many', 'sure']
# stop_words.update(custom_stop_words) # Add custom stop word
# lemmatizer = WordNetLemmatizer() # Set up Lemmatizer


# api = Namespace('dashboard', description='Dashboard related operations')

# # ==================== USER FUNCTIONS ====================#

# # To get course average ratings - all and specific
# average_course_ratings = api.parser()
# average_course_ratings.add_argument("course_ID", help="Enter course_ID")

# @api.route("/course_average_ratings")
# @api.doc(description="Course specific feedback")
# class CourseAverageRatings(Resource):
#     def get(self):
#         args = average_course_ratings.parse_args()
#         course_ID = args.get("course_ID", "")

#         keywords = ['rate', 'course']  # Define keywords to identify relevant questions

#         try:
#             total_ratings = []
#             total_questions = 0

#             # To retrieve relevant questions and calculate average rating
#             relevant_questions = db.session.query(FeedbackTemplate, TemplateAttribute) \
#                 .join(TemplateAttribute, FeedbackTemplate.template_ID == TemplateAttribute.template_ID) \
#                 .join(Feedback, Feedback.template_Attribute_ID == TemplateAttribute.template_Attribute_ID) \
#                 .join(RunCourse, RunCourse.rcourse_ID == Feedback.rcourse_ID) \
#                 .join(Course, Course.course_ID == RunCourse.course_ID) \
#                 .filter(TemplateAttribute.input_Type == 'Likert Scale') \
#                 .filter(func.lower(TemplateAttribute.question).contains(keywords[0])) \
#                 .filter(func.lower(TemplateAttribute.question).contains(keywords[1]))

#             if course_ID:
#                 relevant_questions = relevant_questions.filter(Course.course_ID == course_ID)  # Filter by a specific course if course_ID is provided

#             for feedback_template, template_attribute in relevant_questions:
#                 question_id = template_attribute.template_Attribute_ID
#                 feedback_entries = db.session.query(Feedback) \
#                     .filter(Feedback.template_Attribute_ID == question_id)

#                 if course_ID:
#                     feedback_entries = feedback_entries.filter(Course.course_ID == course_ID)  # Filter by a specific course if course_ID is provided

#                 feedback_entries = feedback_entries.all()

#                 if feedback_entries:
#                     for entry in feedback_entries:
#                         # print(entry)
#                         total_ratings.append(int(entry.answer))  # Assuming 'answer' contains the Likert Scale value as an integer
#                         total_questions += 1
            
#             total_feedback = int(total_questions / len(relevant_questions.all()))

#             # Calculate the overall average rating
#             if total_ratings and total_questions > 0:
#                 overall_average_rating = round(sum(total_ratings) / total_questions, 2)
#                 message = "Course ratings calculated successfully."
#             else:
#                 overall_average_rating = 0
#                 message = "No ratings"

#             db.session.close()

#             response_data = {
#                 "code": 200,
#                 "data": {
#                     "course_ID": course_ID,
#                     "overall_average_rating": overall_average_rating,
#                     "total_feedback": total_feedback
#                 },
#                 "message": message,
#             }
        
#         except Exception as e:
#             response_data = {
#                 "code": 500,
#                 "message": str(e)
#             }

#         return jsonify(response_data)


# # To get instructor specific average ratings
# instructor_average_ratings = api.parser()
# instructor_average_ratings.add_argument("instructor_ID", help="Enter instructor_ID")

# @api.route("/instructor_average_ratings")
# @api.doc(description="Instructor specific feedback")
# class InstructorAverageRatings(Resource):
#     @api.expect(instructor_average_ratings)
#     def get(self):
#         args = instructor_average_ratings.parse_args()
#         instructor_ID = args.get("instructor_ID", "")

#         keywords = ['rate', 'instructor']  # Define keywords to identify relevant questions
#         try:

#             total_ratings = []
#             total_questions = 0

#             # To retrieve relevant questions and calculate average rating
#             relevant_questions = db.session.query(FeedbackTemplate, TemplateAttribute) \
#                 .join(TemplateAttribute, FeedbackTemplate.template_ID == TemplateAttribute.template_ID) \
#                 .join(Feedback, Feedback.template_Attribute_ID == TemplateAttribute.template_Attribute_ID) \
#                 .join(RunCourse, Feedback.rcourse_ID == RunCourse.rcourse_ID) \
#                 .filter(TemplateAttribute.input_Type == 'Likert Scale') \
#                 .filter(func.lower(TemplateAttribute.question).contains(keywords[0])) \
#                 .filter(func.lower(TemplateAttribute.question).contains(keywords[1]))

#             if instructor_ID:  # Filter by instructor ID if provided
#                 relevant_questions = relevant_questions.filter(RunCourse.instructor_ID == instructor_ID)

#             relevant_questions = relevant_questions.all()

#             for feedback_template, template_attribute in relevant_questions:
#                 question_id = template_attribute.template_Attribute_ID
#                 feedback_entries = db.session.query(Feedback) \
#                     .filter(Feedback.template_Attribute_ID == question_id)

#                 if instructor_ID:
#                     feedback_entries = feedback_entries.join(RunCourse, Feedback.rcourse_ID == RunCourse.rcourse_ID) \
#                         .filter(RunCourse.instructor_ID == instructor_ID)  # Filter by instructor ID if provided

#                 feedback_entries = feedback_entries.all()

#                 if feedback_entries:
#                     for entry in feedback_entries:
#                         total_ratings.append(int(entry.answer))  # assuming 'answer' contains the Likert Scale value as an integer
#                         total_questions += 1

#             # Calculate the instructor-specific average rating
#             if total_ratings and total_questions > 0:
#                 instructor_average_rating = round(sum(total_ratings) / total_questions, 2)
#                 message = "Instructor ratings calculated successfully."
#             else:
#                 instructor_average_rating = 0
#                 message = "No ratings for this instructor."

#             db.session.close()

#             response_data = {
#                 "code": 200,
#                 "data": {
#                     "instructor_ID": instructor_ID,
#                     "instructor_average_rating": instructor_average_rating
#                 },
#                 "message": message,
#             }

#         except Exception as e:
#             response_data = {
#                 "code": 500,
#                 "message": str(e)
#             }

#         return jsonify(response_data)


# def drop_col(df):
#     df = df.dropna(how='all')
#     values_to_drop = ["nil", "none", "-", "na", "nan", "nothing"]
#     df = df[~df['answer'].isin(values_to_drop)]
#     drop = ['na', 'nil']
#     df = df[~df['answer'].apply(lambda x: any(word in x.lower() for word in drop))]

#     df.reset_index(drop=True, inplace=True)
#     return df

# def get_wordnet_pos(treebank_tag):
#     if treebank_tag.startswith('J'):
#         return nltk.corpus.wordnet.ADJ
#     elif treebank_tag.startswith('V'):
#         return nltk.corpus.wordnet.VERB
#     elif treebank_tag.startswith('N'):
#         return nltk.corpus.wordnet.NOUN
#     elif treebank_tag.startswith('R'):
#         return nltk.corpus.wordnet.ADV
#     else:
#         return None
    
# def lemmatize_token(token, pos_tag):
#     tag = get_wordnet_pos(pos_tag)
#     if tag is None:
#         return lemmatizer.lemmatize(token)
#     else:
#         return lemmatizer.lemmatize(token, tag)

# def preprocess_text(text_series):
#     def process_text(text):
        
#         text = text.lower() # Convert text to lowercase

#         text = re.sub(r'[^a-zA-Z\s-]', '', text) # Remove non-alphabetic characters and split hyphenated words

#         tokens = nltk.word_tokenize(text) # Tokenize text

#         pos_tags = nltk.pos_tag(tokens) # Tag part of speech for each token

#         lemmatized_tokens = [lemmatize_token(token, pos) for token, pos in pos_tags] # Lemmatize tokens with specified part of speech

#         tokens = [token for token in lemmatized_tokens if not token in stop_words] # Remove stop words

#         tokens = [token for token in tokens if len(token) >= 3] # Remove words with length less than 3 characters

#         text = ' '.join(tokens) # Join tokens back into text

#         return text
    
#     return text_series.apply(process_text)

# def tune_nmf_hyperparameters(corpus, n_topics_range, max_df_range):
#     best_n_topics = None
#     best_max_df = None
#     best_silhouette_score = -1

#     # Split your data into training and validation sets
#     X_train, X_val = train_test_split(corpus, test_size=0.2, random_state=1)

#     for n_topics in n_topics_range:
#         for max_df_value in max_df_range:
#             # Vectorize the training data using TfidfVectorizer with the current max_df
#             tfidf_vectorizer = TfidfVectorizer(max_df=max_df_value, stop_words='english')
#             tfidf_matrix_train = tfidf_vectorizer.fit_transform(X_train)

#             # Perform NMF with the current n_topics
#             nmf_model = NMF(n_components=n_topics, random_state=1)
#             nmf_matrix_train = nmf_model.fit_transform(tfidf_matrix_train)

#             # Calculate silhouette score on the validation set
#             tfidf_matrix_val = tfidf_vectorizer.transform(X_val)
#             nmf_matrix_val = nmf_model.transform(tfidf_matrix_val)
#             silhouette_avg = silhouette_score(nmf_matrix_val, labels=nmf_matrix_val.argmax(axis=1))

#             # Check if the current score is better than the best score
#             if silhouette_avg > best_silhouette_score:
#                 best_n_topics = n_topics
#                 best_max_df = max_df_value
#                 best_silhouette_score = silhouette_avg

#     return best_n_topics, best_max_df, best_silhouette_score

# # Get the topic for specific course or all courses
# feedback_course_done_well_specific = api.parser()
# feedback_course_done_well_specific.add_argument("course_ID", help="Enter course_ID")

# @api.route("/feedback_course_done_well_specific")
# @api.doc(description="Course-specific feedback")
# class CourseDoneWellFeedback(Resource):
#     @api.expect(feedback_course_done_well_specific)
#     def get(self):
#         # Parse the course_ID from the request arguments
#         args = feedback_course_done_well_specific.parse_args()
#         course_ID = args.get("course_ID", "")

#         # Query the database to retrieve feedback related to the specified course (using rcourse_ID)
#         if not course_ID:
#             # If course_ID is empty, retrieve feedback for all courses
#             course_well_query = (
#                 db.session.query(Feedback.answer)
#                 .join(RunCourse, Feedback.rcourse_ID == RunCourse.rcourse_ID)
#                 .join(TemplateAttribute, Feedback.template_Attribute_ID == TemplateAttribute.template_Attribute_ID)
#                 .filter(TemplateAttribute.question.contains('course'))
#                 .filter(TemplateAttribute.question.contains("done well"))
#                 .filter(TemplateAttribute.input_Type == 'Text')
#             )
#         else:
#             # If course_ID is provided, filter feedback for the specific course
#             course_well_query = (
#                 db.session.query(Feedback.answer)
#                 .join(RunCourse, Feedback.rcourse_ID == RunCourse.rcourse_ID)
#                 .filter(RunCourse.course_ID == course_ID)
#                 .join(TemplateAttribute, Feedback.template_Attribute_ID == TemplateAttribute.template_Attribute_ID)
#                 .filter(TemplateAttribute.question.contains('course'))
#                 .filter(TemplateAttribute.question.contains("done well"))
#                 .filter(TemplateAttribute.input_Type == 'Text')
#             )
        
#         results = course_well_query.all()
#         db.session.close()

#         if results:
#             result_data = []
#             for result in results:
#                 feedback = {
#                     "answer": result[0],
#                 }
#                 result_data.append(feedback)

#             # Create a Pandas DataFrame from the result_data list
#             df = pd.DataFrame(result_data)
#             df = drop_col(df)
            
#             df['preprocessed_text'] = preprocess_text(df['answer'])
#             corpus = df['preprocessed_text']

#             n_topics_range = range(3, 11)
#             max_df_range = [0.70, 0.75, 0.80, 0.85, 0.9, 0.95]
#             best_n_topics, best_max_df, best_silhouette_score = tune_nmf_hyperparameters(corpus, n_topics_range, max_df_range)

#             tfidf_vectorizer = TfidfVectorizer(max_df=best_max_df, stop_words='english')
#             tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)

#             nmf_model = NMF(n_components=best_n_topics, random_state=1)
#             nmf_matrix = nmf_model.fit_transform(tfidf_matrix)

#             feature_names = tfidf_vectorizer.get_feature_names_out()
#             topic_words_list = []

#             for topic_idx, topic in enumerate(nmf_model.components_):
#                 top_words_indices = topic.argsort()[:-10 - 1:-1]
#                 top_words = [feature_names[i] for i in top_words_indices]
#                 top_word_probabilities = [topic[i] for i in top_words_indices]
#                 topic_data = [{"word": word, "size": prob} for word, prob in zip(top_words, top_word_probabilities)]
#                 topic_words_list.append(topic_data)
            
#             topic_words_list_formatted = []

#             for topic_words in topic_words_list:
#                 word_data = {"wordData": topic_words}
#                 topic_words_list_formatted.append(word_data)

#             dominant_topics = nmf_matrix.argmax(axis=1) + 1
#             df['topic_number'] = dominant_topics

#             # Convert the DataFrame to JSON
#             response_data = df.to_dict(orient='records')

#             return jsonify({"code": 200, "data": response_data, "topic_words_list": topic_words_list_formatted})

#         return jsonify({"code": 404, "message": "No matching course interest information found"})
