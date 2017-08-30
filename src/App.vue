<template>

  <v-app light>
    <v-toolbar fixed>
      <v-btn
        icon
        class='menu-btn'
        @click.native.stop="rightDrawer = !rightDrawer"
      >
        <v-icon class='menu-btn'>menu</v-icon>
      </v-btn>
      </v-toolbar-side-icon>
      <a href='/#'>
      <img src='static/img/favicon@2x.png' class='nvs-logo'>
      </a>
      <v-toolbar-title v-text="title" class='title-logo'></v-toolbar-title>
      <v-spacer></v-spacer>
      <v-chip v-if='monitorStatus.behaving && monitorStatus.connected'
        label
        class='success white--text'>
        <v-icon left class='white--text' style='opacity:1'>
          swap_vert
        </v-icon>
        {{monitorStatus.message}}
      </v-chip>
      <v-chip v-else
        label
        class='error white--text'>
        <v-icon left class='white-text' style='opacity:1'>
          warning
        </v-icon>
        {{monitorStatus.message}}
      </v-chip>
    </v-toolbar>
    <v-navigation-drawer
      temporary
      :clipped='clipped'
      :right="false"
      v-model="rightDrawer"
    >
    <v-list dense>
        <template v-for="(item, i) in items">
          <v-layout
            row
            v-if="item.heading"
            align-left
            :key="i"
          >
            <v-flex xs12>
              <v-subheader v-if="item.heading">
                {{ item.heading }}
              </v-subheader>
            </v-flex>
          </v-layout>
          <v-divider
            light
            v-else-if="item.divider"
            class="my-4 black--text"
            :key="i"
          ></v-divider>
          <v-list-tile
            :key="i"
            v-else
            :to="{name: item.route}">
            <v-list-tile-action>
              <v-icon class='side-icon'>{{ item.icon }}</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>
                {{ item.text }}
              </v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </template>
      </v-list>

    </v-navigation-drawer>
    <!-- <v-footer :fixed="fixed"> -->
    <!--   <span>&copy; 2017, New Vital Signs, LLC.</span> -->
    <!-- </v-footer> -->
    <main>
      <router-view></router-view>
    </main>

    </v-app>

</template>

<script>
export default {
  name: 'app',

  data () {
    return {
      clipped: true,
      drawer: true,
      fixed: true,
      items: [
        { heading: 'Sessions' },
        { icon: 'add_circle', text: 'Add Session', route: 'LandingPage' },
        { icon: 'archive', text: 'Sessions Archive', route: 'LandingPage'  },
        { divider: true },
        { heading: 'Configuration', route: 'LandingPage'  },
        { icon: 'settings', text: 'Settings', route: 'LandingPage'  },
        { icon: 'help', text: 'Help', route: 'LandingPage'  },
      ],
      miniVariant: false,
      right: true,
      rightDrawer: false,
      title: 'new vital signs'
    }
  },

  computed: {

    monitorStatus () {
      return this.$store.state.monitorStatus
    }

  },

  methods: {
    setStatus (data) {
      this.$store.commit('setStatus', data)
    }
  },

  mounted () {
    console.log('App Mounted')
    this.$store.dispatch('establishSocketConnection')
    this.$store.state.socket.on('status', this.setStatus)
  }

}
</script>

<style scoped>
html, body, main {
  background-color: #305580;
}
.title-logo {
  letter-spacing: 1em;
  font-family: 'PT Sans';
  font-weight: bold;
  font-size: 14px;
  color: #c62828;
  text-transform: uppercase;
}
.nvs-logo {
  margin-top: 4px;
  height: 20px;
  margin-left:15px;
  margin-right: 10px;
}
.subheader {
  color: #c62828 !important;
}
</style>
