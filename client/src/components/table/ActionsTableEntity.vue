<template>
  <div>
    <ActionButtonGoto
      icon="eye-outline"
      :path="{ name: 'entity-view', params: { idTable, idEntity: props.id } }"
      class="is-hidden"
    />

    <ActionButtonGoto
      v-if="props.user_permissions.indexOf('change_table') != -1" 
      icon="square-edit-outline"
      :path="{ name: 'entity-edit', params: { idTable, idEntity: props.id } }"
    />
    <!-- TODO: user_permissions doesn't exist when displaying LinkedTables -->

    <ActionButtonDelete
      :dialogTitle="$t('entryDeleteTitle')"
      :dialogMessage="$t('entryDeleteMessage')"
      @on-confirm="
        $store.dispatch('data/deleteEntity', {
          idTable,
          idEntity: props.id
        }).then(()=> {
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
    idTable: Number,
    props: Object
  },
  methods: {}
}
</script>
