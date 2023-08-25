import { axiosClient } from "../axiosClient";
import BaseApiService from "../BaseApiService";

class runCourseService extends BaseApiService {
    async getAllRunCourses(filter) {
        try {
            let courses = await axiosClient.get("/runcourse/get_all_runcourses", {params: {course_id: courseId}});
            return courses.data

        } catch (error) {
            return this.handleError(error);
        }
    }
    

}

export default new runCourseService();