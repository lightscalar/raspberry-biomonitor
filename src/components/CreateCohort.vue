<template>
  <v-container>
    <v-layout>
      <v-flex xs12 lg8 offset-lg2>
        <v-card class='elevation-0'>
          <v-card-title>
            <v-breadcrumbs  icons divider="forward" class='pa-0 ma-0'>
              <v-breadcrumbs-item href='/#' class='white--text'>
                Home
              </v-breadcrumbs-item>
              <v-breadcrumbs-item href='/#' class='brighten'>
                Create New Cohort
              </v-breadcrumbs-item>
            </v-breadcrumbs>
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <v-layout wrap>
              <v-flex lg9 xs12>
                <v-text-field class='all-caps' label='Cohort Name'
                                  v-model='cohort.name'>
                </v-text-field>
              </v-flex>
            </v-layout>

          </v-card-text>
          <v-divider></v-divider>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn primary @click.native='createCohort'>Create</v-btn>
          </v-card-actions>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
// import Component from "../component_location"

  export default {
    components: {},

    data () {
      return {
        cohort: {name: null, includeVitals: true, reports: [], histories: []}
      }
    },

    methods: {
      createCohort() {
        this.$store.dispatch('createCohort', this.cohort)
      }

    },

    computed: {

    },

    mounted() {

    }
  }

</script>

<style scoped>

.container {
  padding-top: 75px;
}
.card {
}
.card__title {
  color: #ff2861;;
  font-size: 20px;
}
.all-caps {
  text-transform: capitalize !important;
}
.header {
  background-color: #305580 !important;
  font-size: 16px;
}
.icon {
}

</style>
