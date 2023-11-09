import { axiosClient } from "../axiosClient";
import BaseApiService from "../BaseApiService";

class RegistrationService extends BaseApiService {
    async createNewRegistration(rcourse_ID, user_ID, reg_Status) {
        try {
            const response = await axiosClient.post("registration/create_new_registration", {
                rcourse_ID: rcourse_ID,
                user_ID: user_ID,
                reg_Status: reg_Status
            });
            // console.log(response.data);
            return response.data;
            
        } catch (error) {
            return this.handleError(error);
        }
    }

    async dropRegisteredCourse(rcourse_ID, user_ID) {
        try {
            const response = await axiosClient.put("/registration/drop_registered_course", {
                rcourse_ID: rcourse_ID,
                user_ID: user_ID,
            });
            // console.log(response);
            return response.data;

        } catch (error) {
            return this.handleError(error);
        }
    }

    async getRegistrationByRunCourseID(rcourse_ID, student_name, reg_status) {
        try {
            const response = await axiosClient.get("/registration/get_registration_by_rcourseid", {
                params: {
                    rcourse_ID: rcourse_ID,
                    student_name: student_name,
                    reg_status: reg_status
                }
            });
          
            return response.data;

        } catch (error) {
            return this.handleError(error);
        }
    }

    async updateRegistration(reg_ID, data) {
        try {
            const response = await axiosClient.put(`/registration/update_registration/${reg_ID}`, data);
            return response.data;
        } catch (error) {
            return this.handleError(error);
        }
    }

    async enrollStudent(reg_IDs) {
        try {
            const response = await axiosClient.post("/registration/enroll_student", {
                reg_IDs: reg_IDs
            });
        
            return response;
    
        } catch (error) {
            return this.handleError(error);
        }
    }    

    async dropStudent(reg_IDs) {
        try {
            const response = await axiosClient.post("/registration/drop_student", {
                reg_IDs: reg_IDs
            });
        
            return response;
    
        } catch (error) {
            return this.handleError(error);
        }
    }  

}

export default new RegistrationService();