<template>
  <v-container
    class="pa-6"
    fluid
  >
    <login-banner v-if="!userInfo" />
    <v-banner
      v-else-if="investigations.length === 0"
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
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue from 'vue';
import { computed, onMounted } from '@vue/composition-api';
import LoginBanner from '../components/LoginBanner.vue';

import store from '../store';

export default Vue.extend({
  components: {
    LoginBanner,
  },

  setup() {
    const investigations = computed(() => store.state.investigations);
    const userInfo = computed(() => store.state.userInfo);

    onMounted(async () => {
      store.dispatch.unsetCurrentInvestigation();
      await store.dispatch.fetchInvestigations();
      await store.dispatch.fetchJobTypes();
    });

    return {
      investigations,
      userInfo,
    };
  },
});
</script>
