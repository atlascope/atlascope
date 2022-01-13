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
      <v-btn
        v-if="userInfo"
        text
        @click="logInOrOut"
      >
        Logout
      </v-btn>
      <v-btn
        v-if="!userInfo"
        text
        @click="logInOrOut"
      >
        Login
      </v-btn>
    </v-app-bar>
  </div>
</template>

<script lang="ts">
import {
  defineComponent, inject, computed, onMounted,
} from '@vue/composition-api';
import OAuthClient from '@girder/oauth-client';
import store from '../store';

export default defineComponent({
  setup() {
    const oauthClient = inject<OAuthClient>('oauthClient');
    const axios = inject('axios');
    const userInfo = computed(() => store.state.userInfo);

    if (oauthClient === undefined) {
      throw new Error('Must provide "oauthClient" into component.');
    }

    onMounted(async () => {
      await store.dispatch.fetchUserInfo(axios);
    });

    return { oauthClient, userInfo };
  },

  methods: {
    async logInOrOut(): Promise<void> {
      if (this.oauthClient.isLoggedIn) {
        await this.oauthClient.logout();
        store.dispatch.logout();
        if (this.$router.currentRoute.name !== 'investigationsList') {
          this.$router.push({ name: 'investigationsList' });
        }
      } else {
        this.oauthClient.redirectToLogin();
      }
    },
  },
});
</script>
