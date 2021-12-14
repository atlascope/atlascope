<script lang="ts">
import {
  ref, defineComponent, inject, onMounted,
} from '@vue/composition-api';
import OAuthClient from '@girder/oauth-client';
import useGeoJS from '../utilities/useGeoJS';

export default defineComponent({
  setup() {
    const map = ref(null);

    const oauthClient = inject<OAuthClient>('oauthClient');
    if (oauthClient === undefined) {
      throw new Error('Must provide "oauthClient" into component.');
    }
    const { zoom, center } = useGeoJS(map);

    onMounted(() => {
      setTimeout(() => center(-0.1704, 51.5047), 2000);
      setTimeout(() => zoom(14), 4000);
    });
    return { oauthClient, map };
  },
  computed: {
    loginText(): string {
      return this.oauthClient.isLoggedIn ? 'Logout' : 'Login';
    },
  },
  methods: {
    logInOrOut(): void {
      if (this.oauthClient.isLoggedIn) {
        this.oauthClient.logout();
      } else {
        this.oauthClient.redirectToLogin();
      }
    },
  },
});
</script>

<template>
  <div
    ref="map"
    class="map"
  />
</template>

<style scoped>
.map {
  width: 100%;
  height: 100%;
  padding: 0;
  margin: 0;
  overflow: hidden;
}
</style>
