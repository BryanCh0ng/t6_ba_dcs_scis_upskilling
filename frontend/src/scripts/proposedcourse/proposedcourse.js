import ProposedCourseService from "../../api/services/proposedCourseService.js"

import { getCourseDetails } from "../course/course.js"
import { getUserDetails } from "../user/user.js"

async function getAllProposedPendingCourseByStatus(status) {
  var response  = await ProposedCourseService.getProposedCourseByStatus(status); 
  var course_details = []
  if (response.code == 200) {
    var pending_courses = response.data['course']
    for (const course of pending_courses) { 
      var course_response = await getCourseDetails(course.course_ID);
      if (course_response.code == 200) {
        var course_results = course_response['course'];
        console.log(course)
        var owner = await getUserDetails(course.submitted_By);
        course_details.push({ ...course, ...course_results[0], owner: owner.data['user'][0].user_Name})
      }
      else {
        course_details.push({ ...course})
      }
    }
    var results = {code: response.code, course: course_details};
    console.log(results)
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
  