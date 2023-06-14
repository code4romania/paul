<template>
  <div>
    <BaseTitle
      :title="`${$t('managePlugin')}: ${$route.params.plugin}`"
      :hasBackButton="false"
    />

    <BaseForm
      v-if="active.settings && options && settings"
      :title="$t('settings')"
      :options="options"
      v-bind:entity.sync="settings"
      @save="saveSettings"
      @close="active.settings = false"
    />

    <BaseCard title="Tasks" v-if="tasks"
      ><template #actions>
        <div class="buttons">
          <router-link
            :to="{ name: 'plugin-task-edit' }"
            class="button is-primary"
          >
            {{ $t('addNewTask') }}
          </router-link>

          <b-button
            class="is-size-4"
            v-if="activeUser && activeUser.is_admin"
            @click="active.settings = !active.settings"
            ><b-icon icon="cog-outline"></b-icon
          ></b-button>
        </div>
      </template>

      <BaseTableAsync
        :table="taskTable"
        :tableEntries="tasks"
        tableActionsComponent="ActionsPlugin"
        @update="getTasks"
      />
    </BaseCard>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import { ToastService } from '@/services/buefy'
import PluginService from '@/services/plugins'
import BaseForm from '@/components/form/BaseForm'

export default {
  name: 'PluginView',
  components: { BaseForm },
  data() {
    return {
      active: {
        settings: false
      },
      settings: null,
      options: null,
      taskTable: {
        id: 'tasks',
        default_fields: [
          'name',
          'task_type',
          'schedule',
          'last_run_date',
          'last_edit_date',
          'last_edit_user.username',
          'schedule_enabled'
        ],
        fields: [
          {
            name: 'name',
            component: 'FieldRouterLink',
            props: { route: 'plugin-task-view', param: 'idTask' },
            display_name: this.$t('taskName'),
          },
          {
            name: 'task_type',
            display_name: this.$t('type')
          },
          {
            name: 'schedule',
            display_name: this.$t('schedule'),
            component: 'FieldCronInfo'
          },
          {
            name: 'last_run_date',
            display_name: this.$t('lastRunDate'),
            field_type: 'datetime'
          },
          {
            name: 'last_edit_date',
            display_name: this.$t('lastEditDate'),
            field_type: 'datetime'
          },
          {
            name: 'last_edit_user.username',
            display_name: this.$t('lastEditBy'),
          },
          {
            name: 'schedule_enabled',
            display_name: this.$t('status'),
            component: 'FieldLiveTag'
          }
        ]
      }
    }
  },
  computed: {
    ...mapState({
      activeUser: state => state.user,
      tasks: state => state.plugin.tasks
    }),
    type: function() {
      return this.$route.params.plugin
    }
  },
  mounted() {
    this.init()
  },
  methods: {
    init() {
      this.$store.commit('plugin/setPlugin', this.type)
      this.$store.commit('plugin/setTask', null)

      this.PluginService = new PluginService(this.type)
      this.getTasks()

      this.getSettings()
    },
    getSettings() {
      this.PluginService.getSettingsOptions().then(response => {
        this.options = response
      })

      this.PluginService.getSettings().then(response => {
        this.settings = response
      })
    },
    saveSettings() {
      this.PluginService.saveSettings(this.settings).then(() => {
        this.active.settings = false
        ToastService.open(this.$t('pluginSettingsSaved'))
      })
    },
    getTasks(query) {
      this.$store.dispatch('plugin/getTasks', query)
    }
  },
  watch: {
    type() {
      this.init()
    }
  }
}
</script>
