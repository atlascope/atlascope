<template>
  <v-list
    dense
    flat
    class="ma-0 pa-0"
  >
    <v-list-item-group
      color="primary"
    >
      <v-list-item
        v-for="(similarNucleus, i) in similarNuclei"
        :key="i"
      >
        <v-list-item-avatar
          :tile="true"
          :color="similarNucleus.color"
        />
        <v-list-item-content>
          <v-list-item-title v-text="`Detected Nucleus ID: ${similarNucleus.id}`" />
        </v-list-item-content>
        <v-list-item-avatar :tile="true">
          <v-img :src="`${baseUrl}/detected-structures/${similarNucleus.id}/fingerprint`" />
        </v-list-item-avatar>
      </v-list-item>
    </v-list-item-group>
  </v-list>
</template>

<script lang="ts">
import {
  defineComponent,
  ref,
} from '@vue/composition-api';
import type {
  PropType,
} from '@vue/composition-api';
import type {
  DetectedStructureWithColor,
} from '../views/InvestigationDetail.vue';

export default defineComponent({
  props: {
    similarNuclei: {
      type: Array as PropType<Array<DetectedStructureWithColor>>,
      required: true,
    },
  },
  setup(props) {
    const baseUrl = ref(process.env.VUE_APP_API_ROOT as string);
    return { baseUrl };
  },
});
</script>
