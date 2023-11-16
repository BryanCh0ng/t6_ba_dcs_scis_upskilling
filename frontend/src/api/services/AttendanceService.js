import { axiosClient } from "../axiosClient";
import BaseApiService from "../BaseApiService";

class AttendanceService extends BaseApiService {

    async getAttendanceByLessonId(lesson_id) {
      try {
        let response = await axiosClient.get("/attendance/get_attendance_by_lesson_id", { params: { lesson_id: lesson_id } });
        return response.data
      } catch (error) {
        return this.handleError(error);
        }
    }

    async updateAttendanceByLessonId(lesson_id, student_ids, action, absentReason, reasonInput) {
      try {
          let response = await axiosClient.post("/attendance/update_attendance_by_lesson_id", {
            lesson_id: lesson_id, 
            student_ids: student_ids, 
            action: action,
            absentReason: absentReason,
            reasonInput: reasonInput
          });
          console.log(response)
          return response.data;
      } catch (error) {
          return this.handleError(error);
      }
    }

    async getAttendanceRate(rcourse_id) {
      try {
        let response = await axiosClient.get("/attendance/get_attendance_rate", { params: { rcourse_id: rcourse_id } });
        console.log(response)
        return response.data
      } catch (error) {
        return this.handleError(error);
        }
    }
}

export default new AttendanceService();

