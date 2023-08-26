import { createApp } from 'vue'
import App from './App.vue'
import router from './router';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { fas, faEye, faEyeSlash} from '@fortawesome/free-solid-svg-icons'
// import { fas } from '@fortawesome/free-solid-svg-icons'
// import { far } from '@fortawesome/free-regular-svg-icons'
import { fab } from '@fortawesome/free-brands-svg-icons'
// import { VuePaginate } from 'vue-paginate';
// import mitt from 'mitt'
// const emitter = mitt();

library.add(fas, fab, faEye, faEyeSlash)

// createApp(App)
//     .use(router)
//     .component('font-awesome-icon', FontAwesomeIcon)
//     .mount('#app')

const app = createApp(App);
app.use(router)
// app.use(VuePaginate)
app.component('font-awesome-icon', FontAwesomeIcon)
// app.config.globalProperties.emitter = emitter;
app.mount('#app')
