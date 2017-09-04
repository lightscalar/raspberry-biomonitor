<template>

  <v-container>
    <v-card>
      <v-card-title>
        <v-subheader>
          Sessions
        </v-subheader>
      </v-card-title>
    </v-card>
    <br/>

    <v-card>
      <v-card-text>
        <v-data-table
          v-bind:pagination.sync="pagination"
          v-bind:search="search"
          v-bind:headers='headers'
          no-data-text='No Sessions Available'
          :items='sessions'>
          <template slot="items" scope="props" >
            <tr @click='visitSession(props.item)'>
              <td><h5>{{ props.item.hid }}</h5></td>
              <td>{{ props.item.createdAt }}</td>
            </tr>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>

  </v-container>
</template>

<script>
// import Component from "../component_location"

  export default {

    components: {},

    props: [],

    data () {
      return {
        search: '',
        headers: [{text: 'Code', value: 'hid', sortable: false, align: 'left'},
          {text: 'Created At', value: 'createdAt', sortable: true, align: 'left'}],
        pagination: {sortBy: 'createdAt'}
      }
    },

    methods: {

      visitSession (session) {
        this.$router.push({name: 'Session', params: {'id': session._id}})
      },

    },

    computed: {
      sessions () {
        this.pagination.descending = true
        return this.$store.state.sessions
      }
    },

    mounted () {
      this.$store.dispatch('getSessions')

    }
  }

</script>

<style scoped>
html, body, main, .container {
  overflow: hidden !important;
}
.container {
  padding-top: 85px;
}
tr {
  cursor: pointer;
}
h5 {
  margin-top: 10px;
  color: #c62828;
}
</style>
