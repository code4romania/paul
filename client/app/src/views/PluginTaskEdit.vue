<template>
  <div v-if="taskOptions">
    <BaseTitle :title="`Task editor`" />

    <ValidationObserver v-slot="{ passes }" @submit.prevent slim>
      <BaseCard title="Task settings"
        ><template #footer>
          <b-button class="is-primary" @click="passes(save)">
            Save changes
          </b-button>
        </template>

        <template #default>
          <div class="card-container card-form">
            <div class="columns is-multiline">
              <div class="column is-6">
                <VField label="Name" rules="required">
                  <b-input v-model="model.name" />
                </VField>

                <VField label="Task type" rules="required">
                  <b-select
                    v-model="model.task_type"
                    expanded
                    :disabled="idTask != null"
                  >
                    <option
                      v-for="(option, key) in taskOptions.task_type.choices"
                      :key="key"
                      :value="option.value"
                      v-text="option.display_name"
                    />
                  </b-select>
                </VField>

                <template v-if="model.task_type == 'segmentation'">
                  <VField label="Filtered view" rules="required">
                    <b-select
                      v-model="model.segmentation_task.filtered_view"
                      expanded
                    >
                      <option
                        v-for="(view, key) in views"
                        :key="key"
                        :value="view.id"
                        v-text="view.data.name"
                      />
                    </b-select>
                  </VField>

                  <VField label="Tag">
                    <b-input v-model="model.segmentation_task.tag" />
                  </VField>
                </template>
              </div>

              <div class="column is-12">
                <VField>
                  <b-checkbox v-model="model.periodic_task.enabled"
                    >Periodic task</b-checkbox
                  >
                </VField>

                <VField v-if="model.periodic_task.enabled">
                  <CronEditor v-model="model.periodic_task.crontab" />
                </VField>
              </div>
            </div>
          </div>
        </template>
      </BaseCard>
    </ValidationObserver>
  </div>
</template>

<script>
import CronEditor from '@/components/form/cron/CronEditor'
import PluginService from '@/services/plugins'
import { ToastService } from '@/services/buefy'
import { mapState } from 'vuex'

export default {
  name: 'PluginTaskEdit',
  components: { CronEditor },
  data() {
    return {
      model: {
        name: '',
        task_type: null,
        segmentation_task: {
          filtered_view: null,
          tag: ''
        },
        periodic_task: {
          enabled: false,
          crontab: '*/1 * * * *'
        }
      },
      idTask: this.$route.params.idTask
    }
  },
  computed: {
    ...mapState('plugin', {
      plugin: state => state.plugin,
      task: state => state.task,
      taskOptions: state => state.taskOptions
    }),
    ...mapState('data', {
      views: state => state.tableViews
    })
  },
  mounted() {
    this.$store.commit('plugin/setPlugin', this.$route.params.plugin)
    this.PluginService = new PluginService(this.$route.params.plugin)

    if (this.idTask)
      this.$store.dispatch('plugin/getTask', this.idTask).then(() => {
        this.model = { ...this.task }

        if (this.model.periodic_task == null) {
          this.model.periodic_task = {
            enabled: false,
            crontab: '*/1 * * * *'
          }
        }
      })

    this.$store.dispatch('plugin/getTaskOptions')
    this.$store.dispatch('data/getTableViews', { all: true })
  },
  methods: {
    save() {
      if (this.idTask)
        this.PluginService.putTask(this.idTask, this.model).then(() => {
          ToastService.open('Task updated')
          this.$router.go(-1)
        })
      else
        this.PluginService.postTask(this.model).then(() => {
          ToastService.open('Task created')
          this.$router.go(-1)
        })
    }
  }
}
</script>
