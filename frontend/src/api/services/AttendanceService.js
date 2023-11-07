import { axiosClient } from "../axiosClient";
import BaseApiService from "../BaseApiService";

class AttendanceService extends BaseApiService {

    async getAttendanceByLessonId(lesson_id) {
      try {
        let response = await axiosClient.get("/attendance/get_attendance_by_lesson_id", { params: { lesson_id: lesson_id } });
        console.log(response)
        return response.data
      } catch (error) {
        return this.handleError(error);
        }
    }
}

export default new AttendanceService();

