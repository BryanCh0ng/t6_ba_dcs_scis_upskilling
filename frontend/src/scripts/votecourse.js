import VoteCourseService from "../api/services/VoteCourseService.js"
import { getCourseDetails } from "./course.js"
import { getInterestCount } from "./interest.js"

async function getAllVoteCourse() {
  var response  = await VoteCourseService.getAllVoteCourses(); 
  var course_details = []
  var interest_count = 0;
  if (response.code == 200) {
    var vote_course = response.data['course']
    for (const course of vote_course) { 
      interest_count = await getInterestCount(course.course_ID)
      var course_response = await getCourseDetails(course.course_ID);
      if (course_response.code == 200) {
        var course_results = course_response['course'];
        course_details.push({ ...course, ...course_results[0], interest_count: interest_count})
      }
      else {
        course_details.push({ ...course, interest_count: interest_count})
      }
    }
    var results = {code: response.code, course: course_details};
    return results;
  }
  else {
    return response
  }
}


export { getAllVoteCourse };
  