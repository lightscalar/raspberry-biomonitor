<template>
    <v-snackbar
      v-model='openMessage'
      :top=true
      :success="type=='success'"
      :info="type=='info'"
      :warning="type=='warning'"
      :error="type=='error'"
      :primary="type=='success'"
      :timeout="timeout">
      {{message}}
    </v-snackbar>
</template>

<script>
  // import Component from "../component_location"

  export default {

    components: {},

    props: {
      message: {default: 'success'},
      isOpen: {default: false},
      type: {default: 'info'},
      position: {default: 'top'},
      timeout: {default: 6000}
    },

    watch: {
      isOpen () {
        this.openMessage = true
      }
    },

    data () {
      return {
        openMessage: false
      }
    },

    methods: {

    },

    computed: {

    },

    mounted () {

    }
  }

</script>

<style>

</style>
