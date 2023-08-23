import { axiosClient } from "../axiosClient";
import BaseApiService from "../BaseApiService";

class ProposedCourseService extends BaseApiService {
    async getAllProposedCourses(filter) {
        try {
            let courses = await axiosClient.get("/proposedcourse/get_all_proposedcourses", {params: {course_id: courseId}});
            return courses.data

        } catch (error) {
            return this.handleError(error);
        }
    }
    

}

export default new ProposedCourseService();