<template>
  <v-sheet
    max-width="33vw"
    min-width="33vw"
  >
    <v-tabs
      centered
      grow
    >
      <v-tab>
        Investigation Data
      </v-tab>
      <v-tab-item>
        <investigation-sidebar-info />
      </v-tab-item>
      <v-tab>
        Run Analytics
      </v-tab>
      <v-tab-item>
        <investigation-sidebar-run-analytics />
      </v-tab-item>
      <v-tab>
        Analytics Results
      </v-tab>
      <v-tab-item>
        <!--<investigation-sidebar-analytics-results />-->
        <investigation-sidebar-analytics-results-2 />
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
import InvestigationSidebarRunAnalytics from './InvestigationSidebarRunAnalytics.vue';
import InvestigationSidebarAnalyticsResults from './InvestigationSidebarAnalyticsResults.vue';
import InvestigationSidebarAnalyticsResults2 from './InvestigationSidebarAnalyticsResults2.vue';

export default defineComponent({
  components: {
    PinList,
    InvestigationSidebarInfo,
    InvestigationSidebarRunAnalytics,
    InvestigationSidebarAnalyticsResults,
    InvestigationSidebarAnalyticsResults2,
  },
});
</script>
