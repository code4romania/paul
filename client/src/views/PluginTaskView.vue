<template>
  <div>
    <BaseTitle :title="`$t('pluginTask') ${$route.params.plugin}`" />

    <BaseCard :title="`$t('task'): ${task.name}`" v-if="task">
      <b-loading :is-full-page="false" v-model="loading" />

      <template #actions>
        <div class="buttons">
          <router-link
            :to="{ name: 'plugin-task-edit', params: { idTask: task.id } }"
            class="button is-primary"
          >
            {{ $t('editTask') }}
          </router-link>
          <p v-if="showText">{{ $t('taskAdded') }}</p>
          <b-button v-else type="is-dark" @click="runTask">{{ $t('run') }}</b-button>
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
      showText: false,
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
            display_name: this.$t('details'),
            component: 'FieldPluginTaskDetail',
            props: { idTask: this.idTask },
            sortable: false
          },
          {
            name: 'date_start',
            display_name: this.$t('runDate'),
            field_type: 'datetime'
          },
          {
            name: 'duration',
            display_name: this.$t('duration'),
          },
          {
            name: 'user.username',
            display_name: this.$t('user'),
          },
          {
            name: 'status',
            display_name: this.$t('status'),
          },
          {
            name: 'success',
            display_name: this.$t('result'),
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
        let taskIsRuning = response.results.filter(function(item){
          return item.status!="Finished"
        });
        if (taskIsRuning.length==0)
        {
          console.log(this.showText);
          this.showText = false
        }else{
          this.showText = true;
        }
       
      })
    },
    runTask() {
      this.loading = true
      this.showText = true

      this.PluginService.runTask(this.idTask).then(() => {
        this.showText = true
        this.loading = false
        this.getLog()
      })
    }
  }
}
</script>
