import RunCourseService from "../../api/services/runCourseService.js"

async function getRunCourseDetails(courseID) {
  var run_course_response = await RunCourseService.getRunCourseByCourseId(courseID);
  return run_course_response
}

export { getRunCourseDetails };