import { axiosClient } from "../axiosClient";
import BaseApiService from "../BaseApiService";

class ManagementService extends BaseApiService {
    // All Admin
    async getAllAdmin(user_Name) {
        try {
            let admin = await axiosClient.get("/management/get_all_admin", {
                params: {
                    admin_name: user_Name,
                }
            });
            return admin.data;
        } catch (error) {
            return this.handleError(error);
        }
    }

    // All Student
    async getAllStudent(user_Name, blacklisted) {
        try {
            let student = await axiosClient.get("/management/get_all_student", {
                params: {
                    student_name: user_Name,
                    blacklisted: blacklisted
                }
            });
            return student.data;
        } catch (error) {
            return this.handleError(error);
        }
    }

    // All Instructors
    async getAllInstructorsAndTrainers(user_Name, role_Name, organization_Name) {
        try {
            let instructorsAndTrainers = await axiosClient.get("/management/get_all_instructors_and_trainers", {
                params: {
                    instructor_name: user_Name,
                    role_name: role_Name,
                    organization_name: organization_Name
                }
            });
            return instructorsAndTrainers.data;
        } catch (error) {
            return this.handleError(error);
        }
    }

    // Student Name
    async getStudentName(user_id) {
        try {
            let student_name = await axiosClient.get("/management/get_student_name", {
                params: {
                    user_id: user_id,
                }
            });
            return student_name.data;
        } catch (error) {
            return this.handleError(error);
        }
    }
}

export default new ManagementService();