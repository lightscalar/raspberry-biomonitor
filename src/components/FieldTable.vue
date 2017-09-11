<template>

  <v-data-table
    hide-actions
    v-bind:headers='headers'
    class='elevation-1'
    :items='fields'>

    <template slot="items" scope="props">
      <!-- NUMERIC -->
      <td v-if="props.item.type=='numeric'">
        <v-chip
          label
          v-tooltip:right="{html: props.item.description}"
          class='black white--text'>
          {{props.item.name}}
        </v-chip>
      </td>
      <td v-if="props.item.type=='numeric'">
        <v-chip
          v-tooltip:left="{html: props.item.units}"
          label
          class='red darken-3 white--text'>
          {{props.item.value}}
        </v-chip>
      </td>

      <!-- BOOLEAN -->
      <td v-if="props.item.type=='boolean' && props.item.value">
        <v-chip
          label
          v-tooltip:right="{html: props.item.description}"
          class='black white--text'>
          {{props.item.name}}
        </v-chip>
      </td>
      <td v-if="props.item.type=='boolean' && props.item.value">
          {{props.item.details}}
      </td>

      <!-- TEXT -->
      <td v-if="props.item.type=='text'">
        <v-chip
          label
          v-tooltip:right="{html: props.item.name}"
          class='black white--text'>
          {{props.item.name}}
        </v-chip>
      </td>
      <td v-if="props.item.type=='text'">
          {{props.item.value}}
      </td>

    </template>

  </v-data-table>

</template>

<script>
  // import Component from "../component_location"

  export default {

    components: {},

    props: ['fields'],

    data () {
      return {
        headers: [
          {text: 'Report Field', value: 'name', sortable: false, align: 'left'},
          {text: 'Notes/Value', value: 'units', sortable: false, align: 'left'}]
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
