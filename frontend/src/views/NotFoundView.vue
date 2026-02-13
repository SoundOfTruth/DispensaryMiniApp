<template>
  <div class="not-found-container">
    <div>
      <div class="error-code">404</div>
      <h2>Страница не найдена</h2>
      <div class="actions">
        <router-link to="/" class="btn"> Перейти на главную </router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
.not-found-container {
  display: flex;
  justify-content: center;
}

.error-code {
  font-size: 8rem;
  font-weight: bold;
  color: #e0e0e0;
  line-height: 1;
  text-align: center;
}

.actions {
  display: flex;
  justify-content: center;
}

.btn {
  padding: 0.6rem 1rem;
  font-size: 1rem;
  font-weight: 500;
  border-radius: 8px;
  background-color: #007bff;
  color: white;
  transition: all 0.3s ease;
}
</style>
