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
import "./assets/css/style.css" // css
// import { VuePaginate } from 'vue-paginate';

library.add(fas, fab, faEye, faEyeSlash)

createApp(App)
    .use(router)
    // .use(VuePaginate)
    .component('font-awesome-icon', FontAwesomeIcon)
    .mount('#app')
