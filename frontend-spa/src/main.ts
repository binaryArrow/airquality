import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import './styles/global.scss'
import { library } from "@fortawesome/fontawesome-svg-core";
import { fas } from "@fortawesome/free-solid-svg-icons";

require("@/styles/global.scss")
library.add(fas)

createApp(App).use(router)
    .component('fa', FontAwesomeIcon)
    .mount('#app')
