<template>
  <div>
    <ActionButtonGoto
      icon="eye-outline"
      :path="{ name: 'plugin-task-view', params: { idTask: props.id } }"
    />

    <ActionButtonGoto
      icon="square-edit-outline"
      :path="{ name: 'plugin-task-edit', params: { idTask: props.id } }"
    />

    <ActionButtonDelete
      :dialogTitle="$t('pluginTaskDeleteTitle')"
      :dialogMessage="$t('pluginTaskDeleteMessage')"
      @on-confirm="
        $store
          .dispatch('plugin/deleteTask', {
            idTask: props.id
          })
          .then(() => {
            $emit('update')
          })
      "
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
