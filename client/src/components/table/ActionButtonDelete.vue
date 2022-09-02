<template>
  <a href="#" class="has-text-danger" @click.prevent="deleteAction">
    <b-icon icon="trash-can-outline" />
  </a>
</template>

<script>
export default {
  props: {
    path: String,
    dialogTitle: String,
    dialogMessage: String,
    bypassDialog: Boolean
  },
  methods: {
    deleteAction() {
      if (this.bypassDialog) this.$emit('on-confirm')
      else
        this.$buefy.dialog.confirm({
          title: this.dialogTitle,
          message: this.dialogMessage,
          type: 'is-danger',
          onConfirm: () => {
            this.$emit('on-confirm')
          },
          confirmText: 'Șterge',
          cancelText: 'Anulează'
        })
    }
  }
}
</script>
