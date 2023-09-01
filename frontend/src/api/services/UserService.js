import { axiosClient } from "../axiosClient";
import BaseApiService from "../BaseApiService";

class UserService extends BaseApiService {
    // Login
    async login(email, password) {
        try {
            const response = await axiosClient.post("user/login", {
                email: email,
                password: password
            });
            return response.data;
        } catch (error) {
            // Handle errors
            console.error(error);
            throw error;
        }
    }

    // Verify Email
    async verifyEmail(email) {
        try {
            const response = await axiosClient.post("user/verify_email", {
                email: email
            });
            return response.data;
        } catch (error) {
            console.error(error);
            throw error;
        }
    }

    async register(userData) {
        try {
            const response = await axiosClient.post("user/register", userData);
            return response.data;
        } catch (error) {
            console.error(error);
            throw error;
        }
    }

    async forgotPassword(email) {
        try {
            const response = await axiosClient.post("user/forgot_password", {
                email: email
            });
            return response.data;
        } catch (error) {
            console.error(error);
            throw error;
        }
    }

    async resetPassword(password, confirmPassword, email) {
        try {
            const response = await axiosClient.post("user/reset_password", {
                email: email,
                password: password,
                confirmpassword: confirmPassword
            });
            return response.data;
        } catch (error) {
            console.error(error);
            throw error;
        }
    }
    
    async getUserID() {
        try {
            const response = await axiosClient.get("user/get_user_id");
            return response.data;
        } catch (error) {
            console.error(error);
            throw error;
        }
    }

    async getUserName() {
        try {
            const response = await axiosClient.get("user/get_user_name");
            return response.data;
        } catch (error) {
            console.error(error);
            throw error;
        }
    }
    
    async getUserRole() {
        try {
            const response = await axiosClient.get("user/get_role");
            return response.data;
        } catch (error) {
            console.error(error);
            throw error;
        }
    }
    
    async logout() {
        try {
            const response = await axiosClient.get("user/logout");
            return response.data;
        } catch (error) {
            console.error(error);
            throw error;
        }
    }
    
}


export default new UserService();