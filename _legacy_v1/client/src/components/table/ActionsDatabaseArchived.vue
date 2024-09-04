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
    
    <ActionButtonUnarchive :idTable="props.id" />

    <ActionButtonDelete
      :dialogTitle="$t('tableDeleteTitle')"
      :dialogMessage="$t('tableDeleteMessage')"
      @on-confirm="$store.dispatch('data/deleteTable', props.id)"
    />
    <ActionButtonDownload />
  </div>
</template>

<script>
import ActionButtonUnarchive from './ActionButtonUnarchive'
import ActionButtonDownload from './ActionButtonDownload'
import ActionButtonDelete from './ActionButtonDelete'
import ActionButtonGoto from './ActionButtonGoto'

export default {
  components: {
    ActionButtonGoto,
    ActionButtonUnarchive,
    ActionButtonDownload,
    ActionButtonDelete
  },
  props: {
    props: Object
  }
}
</script>
