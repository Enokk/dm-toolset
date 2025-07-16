import 'primeicons/primeicons.css'
import '@/assets/main.css'
import '@/assets/tailwind.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import PrimeVue from 'primevue/config'

import App from '@/App.vue'
import router from '@/router'
import MyTheme from '@/themes/myTheme'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(PrimeVue, {
  theme: {
    preset: MyTheme,
  },
})

import Button from 'primevue/button'
import ToggleSwitch from 'primevue/toggleswitch';

app.component('Button', Button)
app.component('ToggleSwitch', ToggleSwitch)

app.mount('#app')
