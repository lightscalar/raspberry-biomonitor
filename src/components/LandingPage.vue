<template>
<v-container>
  <!-- <v-parallax src='static/img/heart-logo@2x.png' class='splash'> -->
    <v-layout align-center justify-center class='form'>
      <h1 class='logo text--white'>NEW VITAL SIGNS</h1>
    </v-layout>
    <v-layout align-center justify-center>
      <v-btn
        large class='large-btn white--text'
        @click.native='createSession'>
        Create New Session
      </v-btn>
    </v-layout>
  <!-- </v-parallax> -->
</v-container>

</template>

<script>
  // import Component from "../component_location"

  export default {

    components: {},

    props: [],

    data () {
      return {
        sessionId: '',
      }
    },

    methods: {

      keyPress () {

      },

      focusInput() {
        this.sessionId = null
      },

      openSession () {

      },

      createSession () {
        this.$store.dispatch('createSession')

      }

    },

    computed: {

    },

    mounted () {

    }
  }

</script>

<style scoped>
.container {
    background-image: url('../../static/img/heart-logo@2x.png');
    background-position: center 10px;
    overflow: hidden !important;
}
.logo {
  font-size: 40px;
  letter-spacing: 1em;
  color: #ffffff;
  font-weight: bold;
}
.code-input {
  font-size: 40px;
  border: 4px solid white;
  color: black;
  background-color: white;
  text-transform: uppercase;
  text-align: center;
  margin-left: 5px;
  margin-right: 5px;
  max-width: 250px;
  outline: 6px solid #afafaf;
  padding: 5px;
}
.splash {
  padding-top: 400px;
  min-height: 600px;
  overflow: hidden !important;
}
.add-patient {
  color: #305580;
}
.large-btn {
  font-size: 50 !important;
  padding: 5px !important;
  min-height: 90px !important;
  background-color: #c62828 !important;
  border: 6px solid #ffffff !important;
}
.form {
  margin-top: 200px;
}
</style>
