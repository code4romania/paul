<template>
  <div>
    <!-- <pre>{{props.user_permissions}}</pre> -->
    <ActionButtonGoto
      v-if="props.user_permissions.indexOf('view_table') != -1"
      icon="eye-outline"
      :path="{ name: 'table-view', params: { idTable: props.id } }"
    />

    <ActionButtonGoto
      v-if="props.user_permissions.indexOf('change_table') != -1"
      icon="square-edit-outline"
      :path="{ name: 'table-edit', params: { idTable: props.id } }"
    />

    <ActionButtonArchive  v-if="props.user_permissions.indexOf('change_table') != -1" :idTable="props.id" />
    
    <ActionButtonDelete
      v-if="props.user_permissions.indexOf('delete_table') != -1"
      :dialogTitle="$t('tableDeleteTitle')"
      :dialogMessage="$t('tableDeleteMessage')"
      @on-confirm="$store.dispatch('data/deleteTable', props.id)"
    />
  </div>
</template>

<script>
import ActionButtonArchive from './ActionButtonArchive'
import ActionButtonDelete from './ActionButtonDelete'
import ActionButtonGoto from './ActionButtonGoto'

export default {
  components: {
    ActionButtonArchive,
    ActionButtonDelete,
    ActionButtonGoto
  },
  props: {
    props: Object
  }
}
</script>
