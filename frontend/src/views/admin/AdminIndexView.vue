<template>
  <div class="profile-container">
    <div class="profile-card">
      <div class="profile-info">
        <h2 class="info-title">Профиль</h2>

        <div class="info-grid">
          <div class="info-item">
            <label>Email</label>
            <p>{{ userData.email }}</p>
          </div>

          <div class="info-item">
            <label>Имя</label>
            <p>{{ userData.firstname }}</p>
          </div>

          <div class="info-item">
            <label>Фамилия</label>
            <p>{{ userData.lastname }}</p>
          </div>

          <div class="info-item">
            <label>Отчество</label>
            <p>{{ userData.middlename }}</p>
          </div>

          <div class="info-item">
            <label>Роль</label>
            <p>{{ userData.role }}</p>
          </div>
        </div>
      </div>

      <div class="profile-actions">
        <button class="action-btn" @click="openChangePasswordModal()">
          <LockSvg />
          Сменить пароль
        </button>
        <RouterLink :to="{ name: 'logout' }" class="action-btn">
          Выйти из аккаунта
        </RouterLink>
      </div>
    </div>
  </div>
  <Teleport to="#modals">
    <AdminChangePasswordModal
      :open="changePasswordOpen"
      @close="closeChangePasswordModal"
    />
  </Teleport>
</template>

<script setup lang="ts">
import AdminChangePasswordModal from "@/components/admin/modals/AdminChangePasswordModal.vue";
import LockSvg from "@/components/svg/LockSvg.vue";
import { ref } from "vue";

const userData = ref({
  email: "test@mail.ru",
  firstname: "test",
  lastname: "test",
  middlename: "test",
  role: "superuser",
});

const changePasswordOpen = ref(false);
const passwordError = ref("");

const openChangePasswordModal = () => {
  changePasswordOpen.value = true;
  passwordError.value = "";
};

const closeChangePasswordModal = () => {
  changePasswordOpen.value = false;
};
</script>

<style scoped lang="scss">
.profile-container {
  padding: 2rem;
  display: flex;
}
.profile-card {
  max-width: 800px;
  width: 100%;
  background: white;
  border-radius: 20px;
}
.profile-info {
  padding: 2rem;
}

.info-title {
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 1.5rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid #e0e0e0;
}
.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}
.info-item {
  display: flex;
  flex-direction: column;
  label {
    font-size: 0.85rem;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 0.5rem;
  }
  p {
    font-size: 1rem;
    color: #333;
    font-weight: 500;
    margin: 0;
    padding: 0.5rem 0;
    border-bottom: 1px solid #f0f0f0;
  }
}

.profile-actions {
  padding: 1.5rem 2rem 2rem;
  border-top: 1px solid #e0e0e0;
  display: flex;
  flex-direction: column;
  align-items: start;

  gap: 10px;
}
.action-btn {
  background: #007bff;
  color: white;
  border: none;
  height: 48px;
  width: 190px;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition:
    transform 0.2s,
    box-shadow 0.2s;
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
  }
  &:active {
    transform: translateY(0);
  }
}

@media (max-width: 640px) {
  .profile-container {
    padding: 1rem;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .modal-actions {
    flex-direction: column;
  }
}
</style>
