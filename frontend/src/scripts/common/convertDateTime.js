export function convertDate(date) {
  if (date) {
    const parsedDate = new Date(date);
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    const formattedDate = parsedDate.toLocaleDateString('en-US', options);
    return formattedDate
  } else {
    return '';
  }
}

export function convertTime(time) {
  if (time) {
    const [hours, minutes, seconds] = time.split(":").map(Number);
    const date = new Date();
    date.setHours(hours);
    date.setMinutes(minutes);
    date.setSeconds(seconds);
  
    const options = { hour: "numeric", minute: "2-digit", hour12: true };
    const formattedTime = date.toLocaleTimeString(undefined, options);
  
    return formattedTime;
  } else {
    return '';
  }
}