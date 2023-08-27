// services
import CourseService from "../api/services/CourseService.js"

// scripts
import { convertDate, convertTime } from "./common/convertDateTime.js"
import { getRegCount } from "./registration.js"
import { getRunCourseDetails } from "./runcourse.js"
import { getProposedCourseDetails } from "./proposedcourse.js"
import { getCategory } from "./coursecat.js"

async function getAllCourseDetails() {
  var response  = await CourseService.getAllCoursesAdmin(); 
  var course_details = []
  if (response.code == 200) {
    var all_courses = response.data['course']
    for (const course of all_courses) {
      var run_course_response = await getRunCourseDetails(course.course_ID); 
      var reg_count = await getRegCount(course.course_ID)
      if (run_course_response.code == 200) {
        var run_course_details = run_course_response.data['course']
        course_details.push({ ...course, ...run_course_details[0], 
          reg_Enddate: convertDate(run_course_details[0].reg_Enddate),
          reg_Startdate: convertDate(run_course_details[0].reg_Startdate),
          run_Startdate: convertDate(run_course_details[0].run_Startdate),
          run_Enddate: convertDate(run_course_details[0].run_Enddate),
          reg_Endtime: convertTime(run_course_details[0].reg_Endtime),
          reg_Starttime: convertTime(run_course_details[0].reg_Starttime),
          run_Starttime: convertTime(run_course_details[0].run_Starttime),
          run_Endtime: convertTime(run_course_details[0].run_Endtime),
          course_cat: await getCategory(course.coursecat_ID),
          status: run_course_details[0].course_Status, 
          reg_count: reg_count
        })
      }
      else {
        var proposed_course_response = await getProposedCourseDetails(course.course_ID); 
        if (proposed_course_response.code == 200) {
          var proposed_course_details = proposed_course_response.data['course']
          course_details.push({ ...course, ...proposed_course_details[0], 
            status: proposed_course_details[0].pcourse_Status, 
            course_cat: await getCategory(course.coursecat_ID),
            reg_count: reg_count, 
          })
        }
        else {
          course_details.push({ ...course, reg_count: reg_count, course_cat: await getCategory(course.coursecat_ID) })
        }
      }
    }
    var results = {code: response.code, courses: course_details};
    return results;
  } else {
    return response;
  }
}

async function getCourseDetails(courseID) {
  var course_response = await CourseService.getCourseById(courseID);
  var course_details = []
  if (course_response.code == 200) {
    var coursecat = await getCategory(course_response['data']['course'][0].coursecat_ID)
    course_details.push({ ...course_response['data']['course'][0], course_cat: coursecat})

  }
  var results = {code: course_response.code, course: course_details}
  return results;
}

export { getAllCourseDetails, getCourseDetails };
 
