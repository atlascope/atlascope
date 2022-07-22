import { Dataset } from '@/generatedTypes/AtlascopeTypes';

export default function visualize(
  data: Dataset,
) {
  console.log('visualize', data.dataset_type, data.metadata);
}
