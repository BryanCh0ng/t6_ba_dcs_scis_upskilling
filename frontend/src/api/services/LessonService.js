import { axiosClient } from "../axiosClient";
import BaseApiService from "../BaseApiService";

class LessonService extends BaseApiService {
    async getAllLessons() {
        try {
            let response = await axiosClient.get("/lesson/get_all_lessons")
            // console.log(response)
            return response.data
        } catch (error) {
            return this.handleError(error)
        }
    } 

    async getRunCourseById(runcourseId) {
      try {
        let runcourse_lessons = await axiosClient.get("/lesson/get_lessons_by_rcourse_id", { params: { runcourse_id: runcourseId } });
        // console.log(runcourse_lessons)
        return runcourse_lessons.data
      } catch (error) {
        return this.handleError(error);
        }
    }

    async addLesson(lessonData) {
        try {
            let response = await axiosClient.post("/lesson/add_lesson", lessonData);
            // console.log(response);
            return response.data;
        } catch (error) {
            return this.handleError(error);
        }
    }

    async removeLesson(lesson_ID) {
        try {
            let response = await axiosClient.delete("/lesson/remove_lesson", { params: { lesson_ID: lesson_ID } });
            // console.log(response);
            return response.data;
        } catch (error) {
            return this.handleError(error);
        }
    }

    async getLessonById(lessonId) {
        try {
            const response = await axiosClient.get(`/lesson/get_lesson_by_id`, { params: { lesson_ID: lessonId } });
            // console.log(response);
            return response.data;
        } catch (error) {
            return this.handleError(error);
        }
    }

    async updateLesson(lessonId, updateData) {
        try {
            const url = `/lesson/update_lesson/${lessonId}`; // Update the URL to include the lesson ID in the path
            const response = await axiosClient.put(url, updateData);
            // console.log(response);
            return response.data;
        } catch (error) {
            return this.handleError(error);
        }
    }
}

export default new LessonService();

