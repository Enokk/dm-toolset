import '@/assets/styles/main.scss'
import '@/assets/font.css'
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
    options: {
        darkModeSelector: '.app-dark'
    }
  },
})

import Button from 'primevue/button'

app.component('Button', Button)

app.mount('#app')
