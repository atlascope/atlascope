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
    type: 'string' | 'number' | 'boolean';
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
