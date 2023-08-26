import ProposedCourseService from "../../api/services/proposedCourseService.js"

import { getCourseDetails } from "../course/course.js"

async function getAllProposedPendingCourseByStatus(status) {
  var response  = await ProposedCourseService.getProposedCourseByStatus(status); 
  var course_details = []
  if (response.code == 200) {
    var pending_courses = response.data['course']
    for (const course of pending_courses) { 
      var course_response = await getCourseDetails(course.course_ID);
      console.log(course_response)
      if (course_response.code == 200) {
        var course_results = course_response.data['course']
        console.log(course_results)
        course_details.push({ ...course, ...course_results[0]})
      }
      else {
        course_details.push({ ...course})
      }
    }
    var results = {code: response.code, course: course_details};
    return results;
  }
  else {
    return response
  }
}


async function getProposedCourseDetails(courseID) {
  var proposed_course_response = await ProposedCourseService.getProposedCourseByCourseId(courseID);
  return proposed_course_response
}

export { getAllProposedPendingCourseByStatus, getProposedCourseDetails };
  