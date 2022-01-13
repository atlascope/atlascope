<template>
  <v-app>
    <atlascope-toolbar />
    <router-view />
  </v-app>
</template>

<script lang="ts">
import Vue from 'vue';
import AtlascopeToolbar from './components/AtlascopeToolbar.vue';

export default Vue.extend({
  name: 'App',

  components: {
    AtlascopeToolbar,
  },
});
</script>
