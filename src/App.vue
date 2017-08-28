<template>
  <v-app id="app">
    <main>
    <router-view></router-view>
    </main>
  </v-app>
</template>

<script>
export default {
  name: 'app'
}
</script>

 <style scoped>
html, body, main {
  background-color: #305580 !important;
}
</style>
