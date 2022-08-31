<template>
  <div class="enable-bulma" :key="visibleTabs.join()">
    <b-tabs v-model="activeTab" @input="reset" :animated="false">
      <b-tab-item
        v-if="visibleTabs.includes('minutes')"
        value="0"
        :label="_$t('minutes')"
        class="minutes-tab"
      >
        <div class="cron-container">
          <b-field grouped>
            <span class="field-item">{{ _$t('every') }}</span>
            <b-numberinput
              :controls="false"
              v-model="editorData.minuteInterval"
            />
            <span class="field-item">{{ _$t('mminutes') }}</span>
          </b-field>
        </div>
      </b-tab-item>
      <b-tab-item
        v-if="visibleTabs.includes('hourly')"
        value="1"
        :label="_$t('hourly')"
        class="hourly-tab"
      >
        <div class="cron-container">
          <b-field grouped>
            <span class="field-item">{{ _$t('every') }}</span>
            <b-numberinput
              :controls="false"
              v-model="editorData.hourInterval"
            />
            <span class="field-item">{{ _$t('hoursOnMinute') }}</span>
            <b-numberinput
              :controls="false"
              :min="0"
              :max="59"
              v-model="editorData.minutes"
            />
          </b-field>
        </div>
      </b-tab-item>

      <b-tab-item
        v-if="visibleTabs.includes('daily')"
        value="2"
        :label="_$t('daily')"
        class="daily-tab"
      >
        <div class="cron-container">
          <b-field grouped>
            <span class="field-item">{{ _$t('every') }}</span>
            <b-numberinput :controls="false" v-model="editorData.dayInterval" />
            <span class="field-item">{{ _$t('daysAt') }}</span>
            <b-timepicker
              icon="clock"
              editable
              @input="setDateTime"
              :value="dateTime"
            />
          </b-field>
        </div>
      </b-tab-item>

      <b-tab-item
        v-if="visibleTabs.includes('weekly')"
        value="3"
        :label="_$t('weekly')"
        class="weekly-tab"
      >
        <div class="cron-container">
          <b-field grouped>
            <span class="field-item">{{ _$t('everyDay') }}</span>
            <div class="centered-checkbox-group field">
              <b-checkbox v-model="editorData.days" native-value="0">
                {{ _$t('sun') }}
              </b-checkbox>
              <b-checkbox v-model="editorData.days" native-value="1">
                {{ _$t('mon') }}
              </b-checkbox>

              <b-checkbox v-model="editorData.days" native-value="2">
                {{ _$t('tue') }}
              </b-checkbox>

              <b-checkbox v-model="editorData.days" native-value="3">
                {{ _$t('wed') }}
              </b-checkbox>

              <b-checkbox v-model="editorData.days" native-value="4">
                {{ _$t('thu') }}
              </b-checkbox>

              <b-checkbox v-model="editorData.days" native-value="5">
                {{ _$t('fri') }}
              </b-checkbox>

              <b-checkbox v-model="editorData.days" native-value="6">
                {{ _$t('sat') }}
              </b-checkbox>
            </div>
            <span class="field-item">{{ _$t('at') }}</span>
            <b-timepicker
              icon="clock"
              editable
              @input="setDateTime"
              :value="dateTime"
            />
          </b-field>
        </div>
      </b-tab-item>

      <b-tab-item
        v-if="visibleTabs.includes('monthly')"
        value="4"
        :label="_$t('monthly')"
        class="monthly-tab"
      >
        <div class="cron-container">
          <b-field grouped>
            <span class="field-item">{{ _$t('onThe') }}</span>
            <b-numberinput :controls="false" v-model="editorData.day" />

            <span class="field-item">{{ _$t('dayOfEvery') }}</span>
            <b-numberinput
              :min="1"
              :max="12"
              v-model="editorData.monthInterval"
              :controls="false"
            />

            <span class="field-item">{{ _$t('monthsAt') }}</span>
            <b-timepicker
              icon="clock"
              editable
              @input="setDateTime"
              :value="dateTime"
            />
          </b-field>
        </div>
      </b-tab-item>

      <b-tab-item
        v-if="visibleTabs.includes('advanced')"
        value="5"
        :label="_$t('advanced')"
        class="advanced-tab"
      >
        <div class="cron-container">
          <b-field grouped>
            <span class="field-item">{{ _$t('cronExpression') }}</span>
            <b-input v-model="editorData.cronExpression"></b-input>
          </b-field>
          <span class="field-item">{{ explanation }}</span>
        </div>
      </b-tab-item>
    </b-tabs>
  </div>
</template>

<script>
import CronEditorMixin from './CronEditorMixin'

export default {
  name: 'CronEditor',
  mixins: [CronEditorMixin],
  components: {},
  data: () => ({
    activeTab: null,
    tabs: [
      { id: 0, key: 'minutes' },
      { id: 1, key: 'hourly' },
      { id: 2, key: 'daily' },
      { id: 3, key: 'weekly' },
      { id: 4, key: 'monthly' },
      { id: 5, key: 'advanced' }
    ]
  }),
  mounted() {
    this.activeTab = this.tabs.find(t => t.key === this.currentTab).id
  },
  watch: {
    currentTab() {
      this.activeTab = this.tabs.find(t => t.key === this.currentTab).id
    }
  },
  computed: {
    dateTime() {
      let dateTime = new Date()
      dateTime.setHours(this.editorData.hours)
      dateTime.setMinutes(this.editorData.minutes)
      return dateTime
    }
  },
  methods: {
    reset(e) {
      const tabKey = this.tabs.find(t => t.id === e).key
      this._resetToTab(tabKey)
    },
    setDateTime(e) {
      if (e == null) {
        return
      }
      this.editorData.hours = e.getHours()
      this.editorData.minutes = e.getMinutes()
    }
  }
}
</script>

<style lang="scss" scoped>
.cron-container {
  // display: flex;
  // align-items: center;

  /deep/ .field-body .field {
    display: flex;
    align-items: center;

    > .control {
      // flex: none;
    }
  }

  .field-item {
    padding: 8px 16px 8px 0;
  }
}
</style>
