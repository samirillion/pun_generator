<template>
  <div id="app">
    <!-- <MainHeader /> -->
    <TestPage/>
    <!-- <HomePage/> -->
  </div>
</template>

<script>
import HomePage from './components/HomePage.vue'
import TestPage from './components/TestPage.vue'
// import MainHeader from './components/MainHeader.vue'

export default {
  name: 'app',
  components: {
    HomePage,
    TestPage,
    // MainHeader
  }
}
</script>

<style>
/*<!-- @import '../node_modules/bootstrap/scss/bootstrap.scss'; -->*/
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: black;
  margin-top: 0;
  text-transform: uppercase;
}
h1,h2,h3,h4,h5,h6{
  margin: 0;
}
h1 {
  font-size: 50px;
}
h2 {
  line-height: 40px;
  font-size: 40px;
  margin-bottom: 20px;
}
h3 {
  font-size: 30px;
}
.title {
  margin-top: 10px;
  margin-bottom: 10px;
  line-height: 40px;
  font-size: 30px;
}
button {
  height: 40px;
  width: auto;
  background: black;
  color: white;
  text-transform: uppercase;
  font-size: 18px;
  font-weight: bold;
  padding-left: 20px;
  padding-right: 20px;
  outline: none;
  -webkit-transition: all .1s linear;
  -moz-transition: all .1s linear;
  -o-transition: all .1s linear;
  transition: all .1s linear !important;
  border: none;
}
.generate-btn {
  margin-top: 10px;
  margin-bottom: 10px;
  border-radius: 6px;
}
button:hover {
  color: black;
  background: white;
  -webkit-box-shadow: inset 0 0 0 1.1px black, 0 0 0 1.1px black;
  -moz-box-shadow: inset 0 0 0 1.1px black, 0 0 0 1.1px black;
  box-shadow: inset 0 0 0 1.1px black, 0 0 0 1.1px black;
  cursor: cell;
}
button:focus {
  outline: none;
}
</style>
