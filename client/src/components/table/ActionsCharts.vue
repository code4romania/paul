<template>
  <div>
    <ActionButtonGoto
      icon="eye-outline"
      :path="{ name: 'chart-view', params: { idChart: props.id } }"
    />

    <ActionButtonGoto
      icon="square-edit-outline"
      :path="{ name: 'chart-edit', params: { idChart: props.id } }"
    />

    <ActionButtonDelete
      :dialogTitle="$t('chartDeleteTitle')"
      :dialogMessage="$t('chartDeleteMessage')"
      @on-confirm="$store.dispatch('data/deleteChart', props.id)"
    />
  </div>
</template>

<script>
import ActionButtonDelete from './ActionButtonDelete'
import ActionButtonGoto from './ActionButtonGoto'

export default {
  components: {
    ActionButtonDelete,
    ActionButtonGoto
  },
  props: {
    props: Object
  }
}
</script>
