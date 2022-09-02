<template>
  <component :is="icon[1]" />
</template>

<script>
import Account from 'vue-material-design-icons/Account.vue'
import AccountDetailsOutline from 'vue-material-design-icons/AccountDetailsOutline.vue'
import AlertCircleOutline from 'vue-material-design-icons/AlertCircleOutline.vue'
import ApplicationImport from 'vue-material-design-icons/ApplicationImport.vue'
import ArchiveOutline from 'vue-material-design-icons/ArchiveOutline.vue'
import ArrowLeft from 'vue-material-design-icons/ArrowLeft.vue'
import ArrowRight from 'vue-material-design-icons/ArrowRight.vue'
import ArrowUp from 'vue-material-design-icons/ArrowUp.vue'
import CalendarBlankOutline from 'vue-material-design-icons/CalendarBlankOutline.vue'
import ChartBoxOutline from 'vue-material-design-icons/ChartBoxOutline.vue'
import ChevronLeft from 'vue-material-design-icons/ChevronLeft.vue'
import ChevronRight from 'vue-material-design-icons/ChevronRight.vue'
import Clock from 'vue-material-design-icons/Clock.vue'
import Close from 'vue-material-design-icons/Close.vue'
import CloseCircleOutline from 'vue-material-design-icons/CloseCircleOutline.vue'
import CogOutline from 'vue-material-design-icons/CogOutline.vue'
import DnsOutline from 'vue-material-design-icons/DnsOutline.vue'
import Download from 'vue-material-design-icons/Download.vue'
import EyeOutline from 'vue-material-design-icons/EyeOutline.vue'
import FlagOutline from 'vue-material-design-icons/FlagOutline.vue'
import HelpCircleOutline from 'vue-material-design-icons/HelpCircleOutline.vue'
import MenuIcon from 'vue-material-design-icons/Menu.vue'
import MenuDown from 'vue-material-design-icons/MenuDown.vue'
import MenuOpen from 'vue-material-design-icons/MenuOpen.vue'
import MenuUp from 'vue-material-design-icons/MenuUp.vue'
import MonitorDashboard from 'vue-material-design-icons/MonitorDashboard.vue'
import Power from 'vue-material-design-icons/Power.vue'
import Refresh from 'vue-material-design-icons/Refresh.vue'
import SquareEditOutline from 'vue-material-design-icons/SquareEditOutline.vue'
import TrashCanOutline from 'vue-material-design-icons/TrashCanOutline.vue'
import Tune from 'vue-material-design-icons/Tune.vue'
import MonitorScreenshot from 'vue-material-design-icons/MonitorScreenshot.vue'
import School from 'vue-material-design-icons/School.vue'

export default {
  name: 'IconMdi',
  components: {
    Account,
    AccountDetailsOutline,
    AlertCircleOutline,
    ApplicationImport,
    ArchiveOutline,
    ArrowLeft,
    ArrowRight,
    ArrowUp,
    CalendarBlankOutline,
    ChartBoxOutline,
    ChevronLeft,
    ChevronRight,
    Clock,
    Close,
    CloseCircleOutline,
    CogOutline,
    DnsOutline,
    Download,
    EyeOutline,
    FlagOutline,
    HelpCircleOutline,
    MenuIcon,
    MenuDown,
    MenuOpen,
    MenuUp,
    MonitorDashboard,
    Power,
    Refresh,
    School,
    SquareEditOutline,
    TrashCanOutline,
    Tune,
    MonitorScreenshot
  },
  props: {
    icon: Array,
    size: String
  }
}
</script>
