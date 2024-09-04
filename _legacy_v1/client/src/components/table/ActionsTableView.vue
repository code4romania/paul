<template>
  <div>
    <ActionButtonGoto
      icon="eye-outline"
      :path="{ name: 'filter-table-view', params: { idTable: props.id } }"
    />

    <ActionButtonGoto
      icon="square-edit-outline"
      :path="{ name: 'filter-edit', params: { idTable: props.id } }"
    />

    <ActionButtonDelete
      :dialogTitle="$t('tableDeleteTitle')"
      :dialogMessage="$t('tableDeleteMessage')"
      @on-confirm="$store.dispatch('data/deleteTableView', props.id)"
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
