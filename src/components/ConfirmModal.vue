<template>

     <v-dialog v-model='isOpen' persistent>
      <v-card>
        <v-card-title class='red darken-3 white--text text--lighten-2'>
          <v-subheader class='white--text'>
            <v-icon warning class='white--text'>warning</v-icon>
            Are You Certain?
          </v-subheader>
        </v-card-title>

        <v-card-text>{{message}}</v-card-text>

        <v-divider></v-divider>
        <v-card-actions>
          <v-btn @click.native='$emit("cancel")'>
            Cancel
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn error flat @click.native="$emit('confirm')">
            Delete
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

</template>

<script>
  // import Component from "../component_location"

  export default {

    components: {},

    props: {
      message: {
        default: 'Are you sure you want to do this?'
      },
      isOpen: {
        default: false
      }
    },

    data () {
      return {

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

<style scoped>
  .icon {
    margin-right: 15px;
  }
</style>
