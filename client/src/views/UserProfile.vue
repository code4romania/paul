<template>
  <div>
    <BaseTitle title="Utilizatori" />

    <BaseCard title="Setări cont" v-if="user && activeUser">
      <template #actions>
        <div class="buttons">
          <router-link
            v-if="user.id === activeUser.id"
            class="button is-dark"
            :to="{ name: 'change-password' }"
          >
            Change password
          </router-link>

          <b-button
            v-if="activeUser.is_admin && notCurrentUser"
            type="is-dark"
            @click="toggleUserActive"
          >
            <span v-if="user.is_active">Dezactivează</span>
            <span v-else>Activează</span>
            user
          </b-button>
        </div>
      </template>

      <template #footer>
        <b-button type="is-primary" @click="save(false)">Save changes</b-button>
      </template>

      <template #default>
        <div class="card-container">
          <b-loading :is-full-page="false" v-model="loading.profile" />

          <div class="columns">
            <div class="column is-narrow">
              <figure class="avatar-image image">
                <img
                  v-if="userModel.avatar"
                  :src="userModel.avatar"
                  class="is-rounded"
                />
                <div v-else class="placeholder is-size-2">
                  <b-icon icon="account"></b-icon>
                </div>
              </figure>
            </div>

            <div class="column is-8-widescreen">
              <fieldset>
                <VField label="Nume și prenume" grouped>
                  <b-input
                    placeholder="Prenume"
                    v-model="userModel.first_name"
                  />
                  <b-input
                    placeholder="Nume"
                    v-model="userModel.last_name"
                  />
                </VField>

                <VField label="E-mail" rules="required">
                  <b-input v-model="userModel.email" />
                </VField>

                <VField label="Schimbă avatar">
                  <div class="file is-right is-dark is-fullwidth">
                    <b-upload v-model="userModel.file" expanded>
                      <span class="file-cta">
                        <span class="file-label">Caută</span>
                      </span>
                      <span class="file-name">
                        <span v-if="userModel.file">{{
                          userModel.file.name
                        }}</span>
                      </span>
                    </b-upload>
                  </div>
                </VField>
              </fieldset>
            </div>
          </div>
        </div>
      </template>
    </BaseCard>

    <BaseCard
      title="Listă de permisiuni"
      v-if="user && activeUser && activeUser.is_admin && notCurrentUser"
      style="width: 600px;"
    >
      <template #footer>
        <b-button type="is-primary" @click="save(true)">Salvează</b-button>
      </template>
      <template #default>
        <b-loading :is-full-page="false" v-model="loading.permissions" />
        <fieldset>
          <ul class="card-list">
            <li
              v-for="(table, index) in user.tables_permissions"
              :key="`table-${table.id}`"
            >
              <div class="columns is-vcentered">
                <div class="column is-6" v-text="table.name"></div>
                <div class="column is-6">
                  <b-select
                    v-model="userModel.tables_permissions[index].permissions"
                    expanded
                  >
                    <option
                      v-for="(p, pindex) in permissions"
                      :key="`p-${pindex}`"
                      :value="p"
                      >{{ p }}</option
                    >
                  </b-select>
                </div>
              </div>
            </li>
          </ul>
        </fieldset>
      </template>
    </BaseCard>
  </div>
</template>

<script>
import UserService from '@/services/user'
import { ToastService } from '@/services/buefy'
import { mapState } from 'vuex'

export default {
  name: 'UserProfile',
  data() {
    return {
      file: null,
      editMode: false,
      user: null,
      userModel: {
        file: null,
        tables_permissions: []
      },
      permissions: UserService.getRights(),
      loading: {
        profile: false,
        permissions: false
      }
    }
  },
  computed: {
    ...mapState({
      activeUser: state => state.user
    }),
    notCurrentUser() {
      return this.user.username != this.activeUser.username
    }
  },
  watch: {
    $route() {
      this.getUser()
    }
  },
  mounted() {
    this.getUser()
  },
  methods: {
    getUser() {
      UserService.getUser(this.$route.params.idUser).then(response => {
        this.user = response
        this.userModel = { ...this.user, file: null }
      })
    },

    toggleUserActive() {
      this.$buefy.dialog.confirm({
        title: 'Status utilizator',
        message: 'Ești sigur?',
        type: this.user.is_active ? 'is-danger' : 'is-success',
        onConfirm: () => {
          this.loading.profile = true

          UserService.toggleActivate(this.user.id).then(response => {
            this.user = response
            this.loading.profile = false

            ToastService.open(
              'User account has been ' +
                (this.user.is_active ? 'activated' : 'deactivated')
            )
          })
        },
        confirmText: this.user.is_active ? 'Dezactivează' : 'Activează'
      })
    },

    save(patch) {
      if (patch) {
        this.loading.permissions = true

        UserService.patchUser(this.userModel.id, {
          tables_permissions: this.userModel.tables_permissions
        })
          .then(() => {
            this.loading.permissions = false
            ToastService.open('User permissions have been updated')
          })
          .catch(() => {
            this.loading.permissions = false
          })
      } else {
        this.loading.profile = true

        const formData = new FormData()

        this.userModel.file && formData.append('avatar', this.userModel.file)
        formData.append('first_name', this.userModel.first_name)
        formData.append('last_name', this.userModel.last_name)
        formData.append('email', this.userModel.email)

        UserService.putUser(this.userModel.id, formData)
          .then(response => {
            this.loading.profile = false
            ToastService.open('User profile has been updated')
            this.userModel.avatar = response.avatar
            this.$store.dispatch('getActiveUser')
          })
          .catch(() => {
            this.loading.profile = false
          })
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.avatar-image {
  width: 140px;
  height: 140px;
}
</style>
