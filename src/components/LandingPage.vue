<template>
  <v-parallax src='static/img/heart-logo@2x.png' class='splash'>
    <v-layout align-center justify-center>
      <h1 class='logo text--white'>NEW VITAL SIGNS</h1>
    </v-layout>
    <v-layout align-center justify-center>
      <input autofocus maxlength="6" class='code-input' v-model='sessionId'
         @focus='focusInput'
         @keyup='keyPress'
         pattern='[a-zA-Z]{6}' type='text'
         placeholder='Session ID' name='patientCode'>
      </input>
      <v-btn dark primary large class='large-btn' @click.native='loadSession'>
        <v-icon class='add-patient' large>add</v-icon>
      </v-btn>
    </v-layout>
  </v-parallax>
</template>

<script>
  // import Component from "../component_location"

  export default {

    components: {},

    props: [],

    data () {
      return {
        sessionId: ''

      }
    },

    methods: {
      keypress () {

      }

    },

    computed: {

    },

    mounted () {

    }
  }

</script>

<style scoped>
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
    min-height: 1000px;
}
.add-patient {
    color: #305580;
}
.container {
}
.large-btn {
    font-size: 50 !important;
    padding: 5px !important;
    min-height: 90px !important;
    background-color: #305580 !important;
    border: 6px solid #afafaf !important;
}
</style>
