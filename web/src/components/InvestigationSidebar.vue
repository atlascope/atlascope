<template>
  <v-sheet
    max-width="33vw"
    min-width="33vw"
  >
    <v-tabs>
      <v-tab>
        Data
      </v-tab>
      <v-tab-item>
        <investigation-sidebar-info />
      </v-tab-item>
      <v-tab>
        Analytics
      </v-tab>
      <v-tab-item>
        Tab content 2
      </v-tab-item>
    </v-tabs>
  </v-sheet>
</template>

<script lang="ts">
import {
  defineComponent,
} from '@vue/composition-api';
import PinList from './PinList.vue';
import InvestigationSidebarInfo from './InvestigationSidebarInfo.vue';

export default defineComponent({
  components: {
    PinList,
    InvestigationSidebarInfo,
  },
});
</script>
