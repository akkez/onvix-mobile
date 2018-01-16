<template>
    <div id="show">
        <div class="row">
            <div v-if="show === false">
                Загрузка...
            </div>
            <div v-else>
                <div class="col-xs-12">
                    <div v-if="show">
                        <h4>{{show.title_ru}}</h4>
                        <p>{{show.description}}</p>
                        <span v-for="stream in show.player_data.streams">
                            <button v-on:click="currentStream = stream.token" v-bind:class="{
                                'btn': true, 'btn-stream': true,
                                'btn-info': currentStream == stream.token,
                                'btn-default': currentStream != stream.token,
                            }">Озвучка: {{stream.translator}}</button>
                        </span>
                        <hr>
                        <div v-if="currentStream !== false">
                            <div v-if="show.type == 'movie'">
                                <button class="btn btn-primary" v-on:click="loadStream(show.type, show.token, currentStream)">Смотреть</button>
                            </div>
                            <div v-if="show.type == 'serial'">
                                <div v-for="(season, season_id) in show['player_data']['streams'][currentStream]['seasons']">
                                    <span v-for="episode in season">
                                        <span class="btn btn-stream" style="pointer-events: none">Сезон {{season_id}} серия {{episode.number}}</span>
                                        <button v-bind:class="{
                                            'btn': true, 'btn-stream': true,
                                            'btn-success': urls[currentStream + season_id + episode.number],
                                            'btn-primary': !urls[currentStream + season_id + episode.number],
                                        }" v-on:click="loadStream(show.type, show.token, currentStream, season_id, episode.number)">
                                            <span v-if="urls[currentStream + season_id + episode.number]">
                                                <span class="glyphicon glyphicon-play"></span>
                                                Смотреть
                                            </span>
                                            <span v-else>
                                                Загрузить
                                            </span>
                                        </button><br>
                                    </span><hr>
                                </div>
                                
                            </div>
                        </div>
                    </div>
                </div>
            </div>

        </div>
    </div>
</template>

<script>
    import {api} from "./main";
    import Vue from 'vue';

    export default {
        name: 'show',
        data() {
            return {
                show: false,
                episodes: false,
                currentStream: false,
                urls: {},
            }
        },
        methods: {
            loadShow: function (show_type, show_hash) {
                var _this = this;

                api({
                    'url': '/api/show/' + show_type + '/' + show_hash,
                    'method': 'GET',
                }).then(response => {
                    var data = response.data;
                    if (data.serial) {
                        _this.show = data.serial;
                        _this.show.type = 'serial';
                    } else if (data.movie) {
                        _this.show = data.movie;
                        _this.show.type = 'movie';
                    }
                }).catch(error => {
                    _this.$router.push({path: '/login'});
                });
            },
            loadStream: function (show_type, show_hash, show_stream, season, episode) {
                var _this = this;
                if (this.urls[show_stream + season + episode] !== undefined) {
                    window.sendMediaOnGoogleCast(this.urls[show_stream + season + episode]);
                    return;
                }

                if (show_type === 'serial') {
                    var url = '/api/play_serial/' + show_hash + '/' + show_stream + '/' + season + '/' + episode;
                } else {
                    var url = '/api/play_movie/' + show_hash + '/' + show_stream;
                }
                api({
                    'url': url,
                    'method': 'GET',
                }).then(response => {
                    var data = response.data;
                    var quality = window.localStorage.getItem('quality') || 'medium';
                    var streamUrl;
                    switch (quality) {
                        case 'low': streamUrl = data.stream_urls[0]; break;
                        case 'medium': streamUrl = data.stream_urls[Math.max(data.stream_urls.length - 2, 0)]; break;
                        case 'high': streamUrl = data.stream_urls[data.stream_urls.length - 1]; break;
                    }
                    console.log("stream(" + quality + ") =", streamUrl);
                    Vue.set(_this.urls, show_stream + season + episode, streamUrl);
                    window.localStorage.setItem('urls', JSON.stringify(_this.urls));
                }).catch(error => {
                    console.log("Also error", error);
                    _this.$router.push({path: '/login'});
                });
            },
        },
        created() {
            var show_hash = this.$route.params.hash;
            var show_type = this.$route.params.type;
            try {
                this.urls = JSON.parse(window.localStorage.getItem('urls'));
            } catch (e) {}

            this.loadShow(show_type, show_hash);
        },
        watch: {
//            '$route' (new_route, old_route) {}
        }
    }
</script>

<style scoped>
    .show-title {
        font-size: 16px;
        margin-bottom: 10px;
    }
    .show-poster {
        width: 100%;
    }
    .btn-stream {
        margin: 0 10px 10px 0;
    }
</style>
