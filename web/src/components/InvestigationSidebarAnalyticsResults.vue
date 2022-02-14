<template>
  <v-expansion-panels
    accordian
    flat
  >
    <v-expansion-panel
      v-for="result in jobResults"
      :key="result.id"
    >
      <v-expansion-panel-header>
        <v-row>
          <v-col cols="1">
            <v-icon left>
              {{ iconType(result.status) }}
            </v-icon>
          </v-col>
          <v-col>
            {{ result.job.name }}
          </v-col>
          <v-col align="end">
            {{ result.updated }}
          </v-col>
        </v-row>
        <v-spacer />
      </v-expansion-panel-header>
      <v-expansion-panel-content>
        <span
          v-if="result.job.resultsType === 'image'"
          class="show-white-space"
        >
          Image
        </span>
        <span v-if="result.job.resultsType === 'text'">{{ result.results }}</span>
      </v-expansion-panel-content>
    </v-expansion-panel>
  </v-expansion-panels>
</template>

<style scoped>
.show-white-space {
  white-space: pre;
}
</style>

<script lang="ts">
import { computed, defineComponent } from '@vue/composition-api';
import store from '../store';

export default defineComponent({
  setup() {
    const jobResults = computed(() => store.getters.jobResults);

    const iconType = (jobStatus: string) => {
      switch (jobStatus) {
        case 'running':
          return 'mdi-head-dots-horizontal';
        case 'error':
          return 'mdi-close';
        case 'success':
          return 'mdi-check';
        default:
          return '';
      }
    };
    return { jobResults, iconType };
  },
});
</script>
