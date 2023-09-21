from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from allClasses import *
import json

api = Namespace('dashboard', description='Dashboard related operations')

# ==================== USER FUNCTIONS ====================#

# Overall Average Course Ratings
