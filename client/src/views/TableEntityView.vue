<template>
  <div v-if="table && entity">
    <BaseTitle :title="'Entity view'" />

    <BaseCard :title="`Table – ${table.name}`">
      <BaseTable :data="[entity]" :fields="table.fields" />
    </BaseCard>

    <template v-if="tableLinks">
      <BaseCard
        :title="`Table – ${link.table.name}`"
        v-for="(link, index) in tableLinks"
        :key="`tableLink${link.table.id}`"
      >
        <template #actions>
          <a class="is-size-4 button-close" @click.prevent="removeLink(index)"
            ><b-icon icon="close"
          /></a>
        </template>

        <BaseTableAsync
          :table="link.table"
          :tableEntries="link.tableEntries || {}"
          tableActionsComponent="ActionsTableEntity"
          @update="getTableEntries(index, $event)"
          :fixedHeader="link.tableEntries && link.tableEntries.count > 3"
        />
        <template #title v-if="link.tableEntries">
          <span class="entries">
            {{ link.tableEntries.count }}
            {{ link.tableEntries.count > 1 ? 'entries' : 'entry' }}
          </span>
        </template>
      </BaseCard>
    </template>

    <TableEntityLinkCard :table="table" @input="addLinkTable" />
  </div>
</template>

<script>
import TableEntityLinkCard from '@/components/table/TableEntityLinkCard'
import { TableService } from '@/services/data'
import { mapState } from 'vuex'

export default {
  name: 'TableEntityView',
  components: { TableEntityLinkCard },
  data() {
    return {
      entity: null,
      tableLinks: []
    }
  },
  computed: {
    ...mapState({
      table: function(state) {
        return state.data.table[this.idTable]
      },
      links: state => state.data.tableLinks
    }),
    idTable() {
      return this.$route.params.idTable
    }
  },
  mounted() {
    if (!this.table) this.$store.dispatch('data/getTable', this.idTable)
    this.tableLinks =
      this.links != null ? JSON.parse(JSON.stringify(this.links)) : []

    this.getEntity()
  },
  methods: {
    getEntity() {
      TableService.getEntity(this.idTable, this.$route.params.idEntity).then(
        response => {
          this.entity = response
        }
      )
    },
    addLinkTable({ sourceField, table, linkField }) {
      const query = {
        [linkField]: this.entity.data[sourceField]
      }

      const linkTable = { query, table }
      this.tableLinks.push(linkTable)

      this.$store.commit('data/setTableLinks', this.tableLinks)

      this.getTableEntries(this.tableLinks.length - 1)
    },
    getTableEntries(index, queryPagination) {
      const tableLink = this.tableLinks[index]

      if (tableLink) {
        const query = Object.assign({}, tableLink.query, queryPagination)

        tableLink.query = query

        this.$store.commit('data/setLoading', {
          idTable: tableLink.table.id,
          status: true
        })

        TableService.getEntries(tableLink.table.id, query).then(response => {
          this.$set(tableLink, 'tableEntries', response)

          this.$store.commit('data/setLoading', {
            idTable: tableLink.table.id,
            status: false
          })
        })
      }
    },
    removeLink(index) {
      this.$delete(this.tableLinks, index)
    }
  },
  watch: {
    idTable() {
      // if (!this.table) this.$store.dispatch('data/getTable', this.idTable)
      // this.getEntity()
    }
  }
}
</script>
