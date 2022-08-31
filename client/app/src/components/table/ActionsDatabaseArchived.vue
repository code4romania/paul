<template>
  <div>
    <ActionButtonGoto
      icon="eye-outline"
      :path="{ name: 'table-view', params: { idTable: props.id } }"
    />
    
    <ActionButtonGoto
      icon="square-edit-outline"
      :path="{ name: 'table-edit', params: { idTable: props.id } }"
    />
    
    <ActionButtonDelete
      dialogTitle="Do you wish to delete this table?"
      dialogMessage="This operation permanently removes all the entries of this table. Please check the data before proceeding."
      @on-confirm="$store.dispatch('data/deleteTable', props.id)"
    />
    <ActionButtonDownload />
  </div>
</template>

<script>
import ActionButtonDownload from './ActionButtonDownload'
import ActionButtonDelete from './ActionButtonDelete'
import ActionButtonGoto from './ActionButtonGoto'

export default {
  components: {
    ActionButtonGoto,
    ActionButtonDownload,
    ActionButtonDelete
  },
  props: {
    props: Object
  }
}
</script>
