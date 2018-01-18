<template>
    <div id="index">
        <div class="row">
            <div v-if="info === false">
                Загрузка...
            </div>
            <div v-else>
                <div class="col-xs-12">
                    <p>Привет, {{info.email}}! Осталось {{info.days_remaining}} дней.
                        <router-link class="btn btn-xs btn-default" to="/login">Выход</router-link>
                    </p>
                    <div class="row">
                        <div v-for="show in info.shows" class="col-xs-6 col-sm-3">
                            <router-link :to="'/' + show.type + '/' + show.token">
                                <img :src="show.poster" class="img-responsive show-poster">
                                <br>
                                <div class="text-center show-title">{{show.title}}</div>
                            </router-link>
                        </div>
                    </div>
                </div>
            </div>

        </div>
    </div>
</template>

<script>
    import {api} from "./main";

    export default {
        name: 'index',
        data() {
            return {
                info: false,
            }
        },
        created() {
            var _this = this;
            api({
                'url': '/api/status',
                'method': 'GET',
            }).then(response => {
                var data = response.data;

                _this.info = data;
            }).catch(error => {
                _this.$router.push({path: 'login'});
            });
        },
    }
</script>

<style scoped>
    .show-title {
        font-size: 16px;
        margin-bottom: 10px;
        min-height: 50px;
    }
    @media(max-width: 768px) {
        .show-title {
            min-height: 120px;
        }
    }
    .show-poster {
        width: 100%;
    }
    

</style>
