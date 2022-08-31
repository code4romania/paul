<template>
  <div>
    <ActionButtonGoto
      icon="eye-outline"
      :path="{ name: 'user-profile', params: { idUser: props.id } }"
    />

    <ActionButtonDelete
      dialogTitle="Do you wish to delete this profile?"
      dialogMessage="This operation permanently removes this profile. Please check the data before proceeding."
      @on-confirm="$store.dispatch('data/deleteUser', props.id)"
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
  },
  methods: {}
}
</script>
