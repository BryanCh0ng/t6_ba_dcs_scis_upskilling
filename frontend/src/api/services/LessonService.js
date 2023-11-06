import { axiosClient } from "../axiosClient";
import BaseApiService from "../BaseApiService";

class LessonService extends BaseApiService {
    async getAllLessons() {
        try {
            let response = await axiosClient.get("/lesson/get_all_lessons")
            console.log(response)
            return response.data
        } catch (error) {
            return this.handleError(error)
        }
    } 

    async getRunCourseById(runcourseId) {
      try {
        let runcourse_lessons = await axiosClient.get("/lesson/get_lessons_by_rcourse_id", { params: { runcourse_id: runcourseId } });
        console.log(runcourse_lessons)
        return runcourse_lessons.data
      } catch (error) {
        return this.handleError(error);
        }
    }
}

export default new LessonService();

