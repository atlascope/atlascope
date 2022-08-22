import { Dataset } from '@/generatedTypes/AtlascopeTypes';

export interface VisOption {
  value: string;
  text: string;
  data: Dataset;
  visFunc: Function;
  options: string[];
  availableOptions: object[];
}
