import UserService from "../../api/services/UserService.js"

import { getExternalUserDetails } from "../externaluser/externaluser.js"

async function getAllInstructors() {
  var response  = await UserService.getAllInstructors();
  var instructor_details = []
  if (response.code == 200) {
    var all_instructors = response.data['instructor']
    for (const instructor of all_instructors) {
      instructor_details.push({ ...instructor, organisation_Name: "SMU", ratings: '4.5 / 5' })
    }
    var results = {code: response.code, instructor: instructor_details};
    return results;
  } else {
    return response;
  }
}

async function getAllTrainers() {
  var response  = await UserService.getAllTrainers();
  var trainer_details = []
  if (response.code == 200) {
    var all_trainers = response.data['trainer']
    for (const trainer of all_trainers) { 
      var external_user_details = await getExternalUserDetails(trainer.user_ID);
      console.log(external_user_details)
      if (external_user_details.code == 200) {
        var trainer_details_data = external_user_details.data['externalUser']
        console.log(trainer_details_data)
        trainer_details.push({ ...trainer, ...trainer_details_data[0], ratings: '4.5 / 5' })
      }
      else {
        trainer_details.push({ ...trainer})
      }
    }
    var results = {code: response.code, trainer: trainer_details};
    return results;
  } else {
    return response;
  }
}


export { getAllInstructors, getAllTrainers };
 
