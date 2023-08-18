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
    async deleteCourse(courseDetails) {
        try {
            let course = await axiosClient.delete("/course/delete_course", { params: { course_id: courseId } })
            .then(response => {
              console.log("Deleted post with ID ${course_id}");
            })

        } catch (error) {
            return this.handleError(error);
        }
    }
}

// export default new CourseService();