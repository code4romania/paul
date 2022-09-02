<template>
  <div>
    <ActionButtonGoto
      icon="eye-outline"
      :path="{ name: 'entity-view', params: { idTable, idEntity: props.id } }"
      class="is-hidden"
    />

    <ActionButtonGoto
      icon="square-edit-outline"
      :path="{ name: 'entity-edit', params: { idTable, idEntity: props.id } }"
    />

    <ActionButtonDelete
      dialogTitle="Do you wish to delete this entity?"
      dialogMessage="This operation permanently removes all the fields of this entry. Please check the data before proceeding."
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
