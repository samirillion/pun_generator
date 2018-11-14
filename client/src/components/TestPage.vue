<template>
  <div>
    <h1 class="title">Stupid Holiday Drink Name Generator</h1>
    <form @submit.prevent="generateName(form)">
       <p class="forgot-something" v-if="form.error">
        {{ form.error }}
      </p>
      <div class="input-wrapper">
        <input type="text" class="form-field" placeholder="Plus Ingredient" v-model="form.plusOne">
        <h3>+</h3>
        <input type="text" class="form-field" placeholder="Plus Ingredient" v-model="form.plusTwo">
        <h3>-</h3>
        <input type="text" class="form-field" placeholder="Minus Ingredient" v-model="form.minusOne">
      </div>
      <h3>=</h3>
        <div class="drink-name-wrapper">
      <div class="your-drink">
        <h3>
          {{ stupidName }}
        </h3>
      </div>
    </div>
      <button type="submit" class="generate-btn">Generate</button>
    </form>
    <h4 class="monospace" v-if="form.name != ''">Made by '{{ form.name.trim() }}'</h4>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      form: {
        error: "",
        rumOrWhiskey: 'Whiskey',
        plusOne: 'bourbon',
        plusTwo: 'lemon',
        minusOne: '',
        name: '',
      },
      stupidName: ""
    }
  },
  methods: {
    generateName (form) {
      if (form.plusOne && form.plusTwo && form.minusOne)
      {
        this.form.error = ''
        const path = `http://localhost:5000/api/name`
        axios.post(path, form)
        .then(response => {
          let nameObject = response.data
          this.stupidName = nameObject.adjective + " " + nameObject.noun
        })
        } else {
          this.form.error = 'Looks like you forgot something there'
        }
    },
    getRandom () {
        const path = `http://localhost:5000/api/random`
        axios.get(path)
        .then(response => {
          let nameObject = response.data
          this.stupidName = this.form.rumOrWhiskey + " and " + nameObject.adjective + " " + nameObject.noun
        })
    }
  },
  created () {
    this.getRandom()
  },
}
</script>
<style scoped>
.forgot-something {
    display: inline-block;
    background: black;
    color: white;
    font-weight: bold;
    margin: 0;
    animation: blinker 1s linear 1;
    line-height: 1;
    padding-top: 1px;
}
@keyframes blinker {
  50% {
    color: black;
    background: white;
  }
}
/* Form Fields */
  .input-wrapper {
    width: auto;
    height: auto;
    margin: 0 auto;
    justify-content: space-between;
    display: flex;
    margin-top: 20px;
    margin-bottom: 20px;
    flex-direction: column;
    height: 180px;
  }
  .input-wrapper input, .input-wrapper select {
    margin: 0 auto;
    text-align: center;
    width: 275px;
    height: 33px;
    font-size: 18px;
    line-height: 18px;
    background: white;
    border: 3px solid black;
    text-transform: uppercase;
    font-weight: bold;
  }
  .input-wrapper input::placeholder, .input-wrapper input::-webkit-input-placeholder, .input-wrapper input::-moz-placeholder, .input-wrapper input:-ms-input-placeholder, .input-wrapper input:-moz-placeholder { 
    color: #dddddd;
  }
  .input-wrapper select {
    height: 41px;
    width: 283px;
  }
  .form-field {
    border: 1px solid black;
    height: 20px;
    width: 175px;
  }
  .form-field:focus {
      outline: none;
  }
  .selector-wrapper select {
    background: white;
    border-radius: 0;
    border: 1px solid black;
  }

/* Everything Else */
  form .drink-name-wrapper {
    margin: 0 auto;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 30px;
  }
  .drink-name-wrapper .your-drink {
    margin: 0 auto;
    display: block;
  }
  .drink-name-wrapper .your-drink h3 {
    font-size: 60px;
  }
</style>
