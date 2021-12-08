import {
  ref, onMounted, Ref,
} from '@vue/composition-api';

export default function useInvestigation(id: Ref<number>) {
  const invesitagtion: Ref<any> = ref(null);

  const getInvestigation = async () => {
    const resp = await fetch(`/api/v1/investigations/${id}/`);
    invesitagtion.value = await resp.json();
  };

  onMounted(getInvestigation);

  return {
    invesitagtion,
    getInvestigation,
  };
}
