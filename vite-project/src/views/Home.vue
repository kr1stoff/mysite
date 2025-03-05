<template>
  <el-container class="hero-section">
    <el-main class="hero-content">
      <div class="text-overlay">
        <h1>助力医药研发，造福人类健康</h1>
        <p>Accelerating drug development, advancing human health</p>
      </div>
    </el-main>
  </el-container>
</template>

<style scoped>
.hero-section {
  height: 100%;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  background-color: #f5f5f5;
  background-image: url("@/assets/images/company1.png");
  background-position: center;
  background-size: cover;
  background-repeat: no-repeat;
}

.hero-content {
  position: relative;
  width: 100%;
  height: 100%;
}

.text-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: rgba(255, 255, 255, 0.8);
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 80%;
  max-width: 800px;
}

.text-overlay h1 {
  margin: 0;
  color: #333;
  width: 100%; /* 设置宽度为80% */
  max-width: 800px; /* 设置最大宽度 */
}

.text-overlay p {
  margin: 0;
  color: #333;
}
</style>
