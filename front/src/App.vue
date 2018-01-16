<template>
  <div id="app">
    <nav class="navbar navbar-default navbar-static-top">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" @click="showNavbar=!showNavbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <router-link class="navbar-brand" v-on:click.native="showNavbar = false" to="/">{{ projectName }}</router-link>
        </div>
        <collapse class="navbar-collapse collapse" v-model="showNavbar">
          <ul class="nav navbar-nav">
            <!--<li>-->
              <!--<router-link v-on:click.native="showNavbar = false" to="/logout">Выход</router-link>-->
            <!--</li>-->
          </ul>

        </collapse><!--/.nav-collapse -->
      </div>
    </nav>

    <div class="container">
      <router-view></router-view>
    </div>
    <div class="footer"></div>

  </div>
</template>

<script>
    export default {
        name: 'app',
        data() {
            return {
                projectName: 'OnvixMobile',
                showNavbar: false,
            }
        },
        created() {
        },
        mounted() {
        },
        computed: {
        },
        methods: {
            hasRoute: function (partial) {
                return (this.$route.path.indexOf(partial) > -1)
            },
        }
    }
</script>

<style scoped>
  .navbar {
    margin-bottom: 10px;
  }
  .footer {
    height: 60px;
  }
</style>
