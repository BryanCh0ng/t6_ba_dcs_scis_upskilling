import { axiosClient } from "../axiosClient";
import BaseApiService from "../BaseApiService";

class CourseService extends BaseApiService {
    async getAllCourses(filter) {
        try {
            let courses = await axiosClient.get("/course/get_all_courses", {params: {skill_name: filter}});
            return courses.data

        } catch (error) {
            return this.handleError(error);
        }
    }
    async getCourseById(courseId) {
        try {
            let course = await axiosClient.get("/course/get_course_by_id", { params: { course_id: courseId } });
            return course.data
        } catch (error) {
            return this.handleError(error);
        }
    }
    async searchFilterCourses(courseId, coursecatId) {
        try {
            let courses = await axiosClient.get("/course/retrieve_all_courses_filter_search", { params: { course_id: courseId, coursecat_id: coursecatId } })
            return courses.data
            

        } catch (error) {
            return this.handleError(error);
        }
    }
    async deleteCourse(course_ID) {
        try {
            let deleteCourse = await axiosClient.delete("/course/delete_Course", {params: { course_id: course_ID }});
            return deleteCourse.data

        } catch (error) {
            return this.handleError(error);
        }
}
}

export default new CourseService();