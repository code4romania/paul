<template>
  <div>
    <ActionButtonGoto
      icon="eye-outline"
      :path="{ name: 'card-view', params: { idCard: props.id } }"
    />

    <ActionButtonGoto
      icon="square-edit-outline"
      :path="{ name: 'card-edit', params: { idCard: props.id } }"
    />

    <ActionButtonDelete
      dialogTitle="Do you wish to delete this card?"
      dialogMessage="This operation permanently removes this card. Please check the data before proceeding."
      @on-confirm="$store.dispatch('data/deleteCard', props.id)"
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
