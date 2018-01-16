import Vue from 'vue'
import VueRouter from 'vue-router'
import * as uiv from 'uiv'
import axios from 'axios'

import App from './App.vue'
import Login from './Login.vue'
import Index from './Index.vue'
import Show from './Show.vue'

Vue.use(uiv);
Vue.use(VueRouter);

export let api = axios.create({
    baseURL: '',
    withCredentials: true,
    crossDomain: true,
});
const Page404 = {template: `<div><h3>Страница не найдена</h3></div>`};

const routes = [
    {path: '/', component: Index},
    {path: '/login', component: Login},
    {path: '/:type(movie|serial)/:hash([0-9a-f]+)', component: Show},
    {path: '*', component: Page404},
];

const router = new VueRouter({
    routes: routes,
});

new Vue({
    el: '#app',
    router: router,
    render: (h) => h(App),
});
