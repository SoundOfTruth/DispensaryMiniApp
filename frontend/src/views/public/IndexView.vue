<template>
  <div class="about">
    <div class="info">
      <div class="title">Полное наименование</div>
      <div class="text">
        БЮДЖЕТНОЕ УЧРЕЖДЕНИЕ ЗДРАВООХРАНЕНИЯ ОМСКОЙ ОБЛАСТИ «КЛИНИЧЕСКИЙ ОНКОЛОГИЧЕСКИЙ ДИСПАНСЕР»
      </div>
      <div class="title">Фактический адрес</div>
      <div class="text">г. Омск, ул. Завертяева, д. 9, к.1.</div>
      <div class="title">График работы</div>
      <div class="text">
        Пн-Пт с 8-00 до 16-00.<br />
        Сб-Вс выходной.
      </div>
      <div class="title">Контактная информация</div>
      <div class="sub-title">Электронная почта</div>
      <div>omonkol_mail@minzdrav.omskportal.ru</div>
      <div class="sub-title">Телефон поликлиники</div>
      <div>+7 (3812) 60-18-89</div>
      <div class="sub-title">Телефон приемной глав. врача</div>
      <div>+7 (3812) 60-18-12</div>
      <div>+7 (908) 801-48-26</div>
    </div>
    <div class="map">
      <div class="iframe-wraper" :class="{ loaded: loaded }">
        <div v-if="!loaded" class="iframe-placeholder">
          <div class="spinner"></div>
        </div>
        <iframe
          src="https://yandex.ru/map-widget/v1/?ll=73.444809%2C55.040125&mode=poi&poi%5Bpoint%5D=73.444243%2C55.040772&poi%5Buri%5D=ymapsbm1%3A%2F%2Forg%3Foid%3D1356235732&z=10.5"
          loading="lazy"
          @load="handleLoad"
          title="Карта: Клинический онкологический диспансер"
          class="map-iframe"
          allowfullscreen
        ></iframe>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
$desctop-start: 720px;
.about {
  display: flex;
  gap: 10px;
  flex-direction: column;
  padding: 20px 15px;
  @media (min-width: $desctop-start) {
    flex-direction: row;
    padding-top: 30px;
    gap: 5px;
  }
}
.title {
  font-size: 140%;
  font-weight: 500;
}
.text {
  font-size: 100%;
  color: #475569;
  line-height: 1.5;
}
.sub-title {
  font-size: 100%;
  font-weight: 600;
  color: #3b82f6;
  margin-top: 5px;
  margin-bottom: 6px;
}
.info {
  display: flex;
  flex-direction: column;
  gap: 2px;
  background: white;
  padding: 20px;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  @media (min-width: $desctop-start) {
    margin-left: 10px;
    max-width: 270px;
  }
  @media (min-width: 800px) {
    margin-left: 10px;
    max-width: 320px;
  }
}
.map {
  min-height: 380px;
  display: flex;
  width: 100%;
  padding: 1px;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  border: 1px solid #e2e8f0;
  .iframe-wraper {
    position: relative;
    width: 100%;
    max-width: 860px;
    margin: 0 auto;
    aspect-ratio: 16 / 9;
    background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
    overflow: hidden;
    display: block;

    &.loaded .iframe-placeholder {
      display: none;
    }

    .iframe-placeholder {
      position: absolute;
      inset: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      background: linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%);
      z-index: 2;
    }

    .spinner {
      width: 48px;
      height: 48px;
      border-radius: 50%;
      border: 4px solid rgba(59, 130, 246, 0.15);
      border-top-color: #3b82f6;
      animation: spin 1s linear infinite;
    }

    .map-iframe {
      width: 100%;
      height: 100%;
      border: 0;
      display: block;
      z-index: 1;
    }

    @keyframes spin {
      0% {
        transform: rotate(0deg);
      }
      100% {
        transform: rotate(360deg);
      }
    }
  }
}
.content {
  padding-top: 87px;
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  @media (min-width: 800px) {
    width: 100% !important;
  }
}
</style>

<script setup lang="ts">
import { ref } from 'vue';
const loaded = ref(false);
const handleLoad = () => {
  loaded.value = true;
};
</script>
