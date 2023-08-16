import { createApp } from 'vue'
import App from './App.vue'
import router from './router';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { fas, faEye, faEyeSlash} from '@fortawesome/free-solid-svg-icons'
// import { far } from '@fortawesome/free-regular-svg-icons'
import { fab } from '@fortawesome/free-brands-svg-icons'
import "./assets/style.css" // css
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'
import { faClock } from '@fortawesome/free-regular-svg-icons';

library.add(fas, fab, faEye, faEyeSlash, faClock)

createApp(App)
    .use(router)
    .component('font-awesome-icon', FontAwesomeIcon)
    .component('VueDatePicker', VueDatePicker)
    .mount('#app')