<script lang="ts">
import { defineComponent, inject } from '@vue/composition-api';
import OAuthClient from '@girder/oauth-client';
import useGeoJS from '../utilities/useGeoJS';

export default defineComponent({
  setup() {
    const oauthClient = inject<OAuthClient>('oauthClient');
    if (oauthClient === undefined) {
      throw new Error('Must provide "oauthClient" into component.');
    }
    useGeoJS();
    return { oauthClient };
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
<template />
