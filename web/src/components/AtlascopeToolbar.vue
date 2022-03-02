<template>
  <div>
    <v-app-bar
      color="teal darken-2"
      dense
      dark
    >
      <v-toolbar-title>
        <router-link
          :to="{name: 'investigationsList'}"
          tag="button"
        >
          Atlascope
        </router-link>
      </v-toolbar-title>
      <v-spacer />
      <v-toolbar-title> {{ investigationName }}</v-toolbar-title>
    </v-app-bar>
  </div>
</template>

<script lang="ts">
import {
  defineComponent, computed,
} from '@vue/composition-api';
import store from '../store';

export default defineComponent({
  setup() {
    const investigationName = computed(() => store.state.currentInvestigation?.name);

    return { investigationName };
  },
});
</script>
