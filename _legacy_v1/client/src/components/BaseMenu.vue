<template>
  <b-menu class="is-size-6" id="base-menu">
    <router-link :to="{ name: 'dashboard' }" class="menu-logo-container">
      <Logo
        :class="menuActive ? 'menu-logo' : 'menu-logo menu-logo-small'"
        :src="menuActive ? 'logo-default' : 'logo-small'"
      />
    </router-link>
    <b-menu-list>
      <b-menu-item
        :icon="menuActive ? 'menu-open' : 'menu-icon'"
        :label="$t('menuLabel')"
        class="menu-header"
        @click="toggleMenu"
      />

      <b-menu-item
        tag="router-link"
        icon="monitor-screenshot"
        :label="$t('dashboardLabel')"
        :to="{ name: 'dashboard' }"
      />

      <b-menu-item
        tag="router-link"
        icon="dns-outline"
        :label="$t('manageTablesLabel')"
        :to="{ name: 'database-view' }"
      />

      <b-menu-item
        tag="router-link"
        icon="tune"
        :label="$t('processedDataLabel')"
        :to="{ name: 'filter-view' }"
      />

      <b-menu-item
        icon="chart-box-outline"
        :active="isActive.charts"
        @click="!menuActive && toggleMenu()"
      >
        <template #label="props">
          <span>{{ $t('viewData') }}</span>
          <b-icon
            class="menu-tick"
            :icon="props.expanded ? 'menu-up' : 'menu-down'"
          ></b-icon>
        </template>
        <b-menu-item
          tag="router-link"
          :label="$t('chartsLabel')"
          :to="{ name: 'charts-view' }"
        />
        <b-menu-item
          tag="router-link"
          :label="$t('cardsLabel')"
          :to="{ name: 'cards-view' }"
        />
      </b-menu-item>

      <b-menu-item
        tag="router-link"
        icon="account-details-outline"
        :label="$t('usersLabel')"
        v-if="isAdmin"
        :to="{ name: 'users-view' }"
      />

      <b-menu-item
        tag="router-link"
        icon="application-import"
        :label="$t('updateDataLabel')"
        :to="{ name: 'table-import', query: { manual: true } }"
      />

      <b-menu-item
        icon="cog-outline"
        :active="isActive.plugins"
        @click="!menuActive && toggleMenu()"
      >
        <template #label="props">
          <span>{{ $t('integrations') }}</span>
          <b-icon
            class="menu-tick"
            :icon="props.expanded ? 'menu-up' : 'menu-down'"
          ></b-icon>
        </template>

        <b-menu-item
          tag="router-link"
          :label="$t('mailchimpLabel')"
          :to="{ name: 'plugin-view', params: { plugin: 'mailchimp' } }"
        />

        <!-- <b-menu-item
          tag="router-link"
          :label="$t('wooCommerceLabel')"
          :to="{ name: 'plugin-view', params: { plugin: 'woocommerce' } }"
        /> -->
      </b-menu-item>

      <b-menu-item tag="a" icon="school" :label="$t('tutorialsLabel')" disabled />
    </b-menu-list>
  </b-menu>
</template>

<script>
import Logo from '@/components/Logo.vue'

export default {
  name: 'BaseMenu',
  components: {
    Logo
  },
  props: {
    isAdmin: Boolean,
    menuActive: Boolean
  },
  data() {
    return {
      isActive: {
        plugins: false,
        import: false
      }
    }
  },
  methods: {
    toggleMenu() {
      this.$emit('toggleMenu')
    }
  }
}
</script>
