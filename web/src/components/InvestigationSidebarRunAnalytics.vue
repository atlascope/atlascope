<template>
  <div class="ma-2 pa-2">
    <v-select
      v-if="jobs.length > 0"
      v-model="selectedJob"
      label="Select a job to run"
      :items="jobs"
      item-text="name"
      item-value="id"
      return-object
    />
    <!-- For now, just use a big text field and show expected inputs -->
    <span
      v-if="selectedJobInputs"
      class="show-white-space"
    >
      {{ selectedJobInputs }}
    </span>
    <v-textarea
      v-if="selectedJob"
      v-model="jobInputs"
      label="Input Values"
    />
    <v-btn
      v-if="selectedJob"
      color="primary"
      @click="console.log('ROI button clicked')"
    >
      Select ROI
    </v-btn>
    <v-btn
      v-if="selectedJob"
      class="ma-2 pa-2"
      color="success"
      @click="submitJobRun"
    >
      Submit
    </v-btn>
    <v-snackbar
      v-model="snackbar"
      :timeout="2000"
      right
    >
      Job submitted
    </v-snackbar>
  </div>
</template>

<style scoped>
.show-white-space {
  white-space: pre;
}
</style>

<script lang="ts">
import {
  computed, defineComponent, ref, Ref,
} from '@vue/composition-api';
import { JobType } from '../generatedTypes/DemoTypes';
import store from '../store';

export default defineComponent({
  setup() {
    const jobs = computed(() => store.state.jobTypes);
    const selectedJob: Ref<JobType | null> = ref(null);
    const jobInputs = ref('');
    const snackbar = ref(false);
    const selectedJobInputs: Ref<string> = computed(() => {
      if (!selectedJob.value || !selectedJob.value.additionalInputs) {
        return '';
      }
      return JSON.stringify(selectedJob.value.additionalInputs, undefined, 4);
    });

    function submitJobRun(): void {
      if (!selectedJob.value) {
        return;
      }
      // launch job, listen for results
      // jobRun = await store.dispatch.spawnJob({job, inputs});
      // pollForJobResults(jobRun)
      console.log(jobInputs.value);
      // clear the form, maybe navigate to results tab?
      selectedJob.value = null;
      jobInputs.value = '';
      snackbar.value = true;
    }

    return {
      jobs,
      jobInputs,
      selectedJob,
      selectedJobInputs,
      snackbar,
      submitJobRun,
    };
  },
});
</script>
