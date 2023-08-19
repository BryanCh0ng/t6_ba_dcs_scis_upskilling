import { createApp } from 'vue'
import App from './App.vue'
import router from './router';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';
import { library } from '@fortawesome/fontawesome-svg-core'
//import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { fas } from '@fortawesome/free-solid-svg-icons'
// import { far } from '@fortawesome/free-regular-svg-icons'
import { fab } from '@fortawesome/free-brands-svg-icons'
import mitt from 'mitt'
const emitter = mitt();

library.add(fas, fab)

// createApp(App)
//     .use(router)
//     .component('font-awesome-icon', FontAwesomeIcon)
//     .mount('#app')

const app = createApp(App);
app.use(router)
app.config.globalProperties.emitter = emitter;
app.mount('#app')