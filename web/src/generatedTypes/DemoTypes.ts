export interface JobResults {
  id?: string;
  job: Job;
  status: 'running' | 'error' | 'success';
  results?: string;
  metadata?: string;
  inputs?: string;
  updated?: string;
  errors?: string[];
}

export interface JobInput {
    name: string;
    class: string;
    required: boolean;
}

export interface JobType {
    name: string;
    description?: string;
    additionalInputs: JobInput[];
}

export interface Job {
    name: string;
    id: string;
    inputs?: JobInput[];
    resultsType?: 'image' | 'text';
}

export interface JobRun {
    job: Job;
    jobInputs?: string;
}
