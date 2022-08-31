<template>
  <div>
    <BaseTitle :title="`Plug-in task ${$route.params.plugin}`" />

    <BaseCard :title="`Task: ${task.name}`" v-if="task">
      <b-loading :is-full-page="false" v-model="loading" />

      <template #actions>
        <div class="buttons">
          <router-link
            :to="{ name: 'plugin-task-edit', params: { idTask: task.id } }"
            class="button is-primary"
          >
            Edit task
          </router-link>

          <b-button type="is-dark" @click="runTask">Run</b-button>
          <b-button type="" class="is-size-4" @click="getLog()"
            ><b-icon icon="refresh"></b-icon
          ></b-button>
        </div>
      </template>

      <BaseTableAsync
        :table="taskTable"
        :tableEntries="log"
        tableActionsComponent="ActionsPlugin"
        @update="getLog"
        filterMode
      />
    </BaseCard>
  </div>
</template>

<script>
import PluginService from '@/services/plugins'
import { mapState } from 'vuex'

export default {
  name: 'PluginTaskView',
  components: {},
  data() {
    return {
      idTask: this.$route.params.idTask,
      log: null,
      loading: false,
      taskTable: {
        id: 'tasks',
        default_fields: [
          'details',
          'date_start',
          'duration',
          'user.username',
          'status',
          'success'
        ],
        fields: [
          {
            name: 'details',
            display_name: 'Details',
            component: 'FieldPluginTaskDetail',
            props: { idTask: this.idTask },
            sortable: false
          },
          {
            name: 'date_start',
            display_name: 'Run date',
            field_type: 'datetime'
          },
          {
            name: 'duration',
            display_name: 'Duration'
          },
          {
            name: 'user.username',
            display_name: 'User'
          },
          {
            name: 'status',
            display_name: 'Status'
          },
          {
            name: 'success',
            display_name: 'Result',
            component: 'FieldStatusTag'
          }
        ]
      }
    }
  },
  computed: mapState('plugin', {
    plugin: state => state.plugin,
    task: state => state.task
  }),
  mounted() {
    this.$store.commit('plugin/setPlugin', this.$route.params.plugin)
    this.$store.dispatch('plugin/getTask', this.idTask)
    this.PluginService = new PluginService(this.$route.params.plugin)
    
    this.getLog()
  },
  methods: {
    getLog(query) {
      this.PluginService.getTaskResults(this.idTask, query).then(response => {
        this.log = response
      })
    },
    runTask() {
      this.loading = true

      this.PluginService.runTask(this.idTask).then(() => {
        this.getLog()
        this.loading = false
      })
    }
  }
}
</script>
