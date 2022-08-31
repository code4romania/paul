<template>
  <ValidationProvider
    :mode="mode"
    :name="name || label"
    :rules="rules"
    v-slot="{ errors }"
    :slim="column == null"
    :class="column != null ? `column ${column}` : null"
    tag="div"
  >
    <b-field
      v-bind="{ grouped, expanded }"
      :type="{ 'is-danger': errors[0] }"
      :class="{ 'is-danger': errors[0] }"
      :message="errors.length ? errors : null"
    >
      <template slot="label" v-if="label">
        {{ label }} <span v-if="rules.indexOf('required') != -1">*</span>
        <b-tooltip
          v-if="labelInfo"
          type="is-dark"
          :label="labelInfo"
          multilined
        >
          <b-icon icon="help-circle-outline" class="is-size-5"></b-icon>
        </b-tooltip>
      </template>

      <div class="description" v-if="description">{{ description }}</div>

      <slot></slot>
      <slot name="footer"></slot>
    </b-field>
  </ValidationProvider>
</template>

<script>
import { ValidationProvider } from 'vee-validate'

export default {
  components: {
    ValidationProvider
  },
  props: {
    rules: {
      type: [Object, String],
      default: ''
    },
    name: String,
    label: String,
    column: String,
    description: String,
    labelInfo: String,
    mode: String,
    grouped: Boolean,
    expanded: Boolean
  }
}
</script>
