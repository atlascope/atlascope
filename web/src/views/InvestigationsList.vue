<template>
  <v-container
    class="pa-6"
    fluid
  >
    <v-row
      v-if="!userInfo"
      class="pa-6"
    >
      <v-col md="9">
        <v-card
          elevation="9"
          rounded-lg
          outline
        >
          <v-card-title>Info:</v-card-title>
          <v-card-text>Please log in to begin using Atlascope</v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row
      v-else-if="investigations.length === 0"
      class="pa-6"
    >
      <v-col md="9">
        <v-card
          elevation="9"
          rounded-lg
          outline
        >
          <v-card-title>Info:</v-card-title>
          <v-card-text>Could not find existing investigations.</v-card-text>
        </v-card>
      </v-col>
    </v-row>
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
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { AxiosInstance } from 'axios';
import Vue from 'vue';
import { computed, inject, onMounted } from '@vue/composition-api';

import store from '../store';

export default Vue.extend({
  setup() {
    const axiosInstance = inject<AxiosInstance>('axios');
    const investigations = computed(() => store.state.investigations);
    const userInfo = computed(() => store.state.userInfo);

    onMounted(async () => {
      if (axiosInstance) {
        await store.dispatch.fetchInvestigations(axiosInstance);
      }
    });

    return {
      axiosInstance,
      investigations,
      userInfo,
    };
  },
});
</script>
