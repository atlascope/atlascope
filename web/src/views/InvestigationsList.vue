<template>
  <v-container
    class="pa-6"
    fluid
  >
    <v-banner
      v-if="investigations.length === 0"
      single-line
    >
      <v-icon left>
        mdi-information
      </v-icon>
      Could not find any existing investigations.
    </v-banner>
    <v-row
      v-else
      class="pa-6"
    >
      <v-col
        v-for="investigation in investigations"
        :key="investigation.id"
        md="3"
      >
        <v-card
          elevation="9"
          rounded-lg
          outline
        >
          <v-card-title>{{ investigation.name }}</v-card-title>
          <v-card-subtitle>{{ investigation.owner }}</v-card-subtitle>
          <v-card-text>{{ investigation.description }}</v-card-text>
          <v-card-actions>
            <router-link :to="`/investigations/${investigation.id}`">
              <v-btn
                color="blue"
                text
              >
                Investigate
              </v-btn>
            </router-link>
            <router-link :to="`/investigations/${investigation.id}/embeddings`">
              <v-btn
                color="blue"
                text
              >
                Embeddings
              </v-btn>
            </router-link>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue from 'vue';
import { computed, onMounted } from '@vue/composition-api';

import store from '../store';

export default Vue.extend({
  setup() {
    const investigations = computed(() => store.state.investigations);

    onMounted(async () => {
      store.dispatch.unsetCurrentInvestigation();
      await store.dispatch.fetchInvestigations();
    });

    return {
      investigations,
    };
  },
});
</script>
