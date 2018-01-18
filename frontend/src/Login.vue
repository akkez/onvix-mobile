<template>
    <div id="login">
        <div class="row">
            <div class="col-sm-6 col-sm-offset-3 col-xs-12">
                <div class="form-group">
                    <label>Email</label>
                    <input v-model="login" placeholder="Email" class="form-control">
                </div>
                <div class="form-group">
                    <label>Пароль</label>
                    <input v-model="password" type="password" placeholder="Password" class="form-control">
                </div>
                <div class="form-group">
                    <label>Качество видео</label>
                    <select v-model="quality" class="form-control">
                        <option value="low">Низкое</option>
                        <option value="medium">Среднее</option>
                        <option value="high">Высокое</option>
                    </select>
                </div>
                <div class="form-group">
                    <button class="btn btn-primary btn-fit" v-on:click="authorize">Войти</button>
                </div>
                <div v-if="error !== false" class="text-danger">{{error}}</div>
            </div>


        </div>
    </div>
</template>

<script>
    import {api} from "./main";

    export default {
        name: 'login',
        data() {
            return {
                login: '',
                password: '',
                quality: '',
                error: false,
            }
        },
        created() {
            var ls = window.localStorage;
            this.login = ls.getItem('login') || '';
            this.password = ls.getItem('password') || '';
            this.quality = ls.getItem('quality') || 'medium';
        },
        methods: {
            authorize: function (event) {
                var ls = window.localStorage;
                //console.log("My login password", this.login, this.password);
                ls.setItem('login', this.login.toString());
                ls.setItem('password', this.password.toString());
                ls.setItem('quality', this.quality.toString());

                this.error = false;
                var _this = this;
                api({
                    'url': '/api/auth',
                    'method': 'POST',
                    'data': {
                        login: this.login,
                        password: this.password
                    },
                }).then(function (response) {
                    if (response.data.success) {
                        ls.setItem('urls', '{}');
                        _this.$router.push({path: '/'});
                    } else {
                        _this.error = 'Authorization error';
                    }
                });
            }
        }
    }
</script>

<style scoped>
    .btn-fit {
        width: 100%;
    }
</style>
