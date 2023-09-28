import { axiosClient } from "../axiosClient";
import BaseApiService from "../BaseApiService";

class CommonService extends BaseApiService {

    async sortRecords(sort_column, sort_direction, records) {
        try {

            let response = await axiosClient.post("/common/sort_records", {sort_column: sort_column, sort_direction: sort_direction, records: records});
            return response.data;
        } catch (error) {
            return this.handleError(error);
        }
    }

}


export default new CommonService();