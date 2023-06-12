<template>
  <div>

    <ActionButtonGoto
      icon="eye-outline"
      :path="{ name: 'entity-view', params: { idTable, idEntity: props.id } }"
    />

    <ActionButtonGoto
      icon="square-edit-outline"
      :path="{ name: 'entity-edit', params: { idTable, idEntity: props.id } }"
    />

    <ActionButtonDelete
      :dialogTitle="$t('entryDeleteTitle')"
      :dialogMessage="$t('entryDeleteMessage')"
      @on-confirm="
        $store.dispatch('data/deleteEntity', {
          idTable,
          idEntity: props.id,
          query: $route.query
        })
      "
    />

    <ActionCheckboxBulkDelete
      :idEntity="props.id"
    />
  </div>
</template>

<script>
import ActionButtonDelete from './ActionButtonDelete'
import ActionButtonGoto from './ActionButtonGoto'
import ActionCheckboxBulkDelete from './ActionCheckboxBulkDelete';

export default {
  components: {
    ActionButtonDelete,
    ActionButtonGoto,
    ActionCheckboxBulkDelete
  },
  props: {
    idTable: Number,
    props: Object
  },
}
</script>
