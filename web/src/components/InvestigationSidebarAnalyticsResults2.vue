<template>
  <div class="ma-2 pa-2">
    <v-select
      v-if="jobResults.length > 0"
      v-model="currentResult"
      label="View results of a job"
      :items="jobResults"
      item-value="id"
      item-text="displayName"
      return-object
    />
    <div v-if="currentResult">
      <span>Id: {{ currentResult.id }}</span><br>
      <span>Status: {{ currentResult.status }}</span><br>
      <span class="show-white-space">Inputs: {{ currentResult.inputs }}</span><br>
      <!-- render results based on type -->
      <div v-if="currentResult.job.resultsType === 'text'">
        <span class="show-white-space">Results: {{ currentResult.results }}</span><br>
      </div>
      <div v-if="currentResult.job.resultsType === 'image'">
        <span>Image Results:</span><br>
        <img
          :src="require(`@/assets/local/images/${currentResult.results}`)"
          alt="Job results"
        >
      </div>
    </div>
  </div>
</template>

<style scoped>
.show-white-space {
  padding: 0px;
  margin: 0px;
  white-space: pre;
}
</style>

<script lang="ts">
import {
  computed, defineComponent, Ref, ref,
} from '@vue/composition-api';
import store from '../store';
import { JobResults } from '../generatedTypes/DemoTypes';

export default defineComponent({
  setup() {
    const jobResults = computed(() => store.getters.jobResults?.map((res) => ({
      ...res, displayName: `${res.updated} - ${res.job.name}`,
    })));
    const currentResult: Ref<JobResults | null> = ref(null);

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
    return {
      jobResults,
      iconType,
      currentResult,
    };
  },
});
</script>
