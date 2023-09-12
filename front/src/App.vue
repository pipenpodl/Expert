<template>
  <div class="app">
    <nav class="navigator">
      <p>{{ currentTime }}</p>
    </nav>

    <div>
      <div v-if="showModal" class="modal" @click.self="showModal = false">
        <div class="modal-content">
          <form @submit.prevent>
            <div class="mem_inp">
              <input 
                v-bind:value="name" 
                @input="name = $event.target.value"
                type="text" 
                placeholder="Имя">
              <input 
                v-bind:value="surname" 
                @input="surname = $event.target.value"
                type="text" 
                placeholder="Фамилия">
              <input 
                v-bind:value="place" 
                @input="place = $event.target.value"
                type="number" 
                placeholder="Место">
            </div>
            <div class="add_member_button">
              <button @click="add_new_member">Добавить</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <div class="member_list">
      <div class="member" v-for="mem in members" :key="mem">
        <div class="member_info">
          <div>
            <p>Имя: {{ mem.name }}</p>
            <p>Фамилия: {{ mem.surname }}</p>
            <p>Место: {{ mem.place }}</p>
          </div>
          
          <div class="add_time_info">
            <p>Доп время: {{ mem.add_time }} минут</p>

            <div class="add_time_info_button">
              <button 
                class="count_button"
                @click="counter_time(mem.id)"
              >
              {{ start_name }}
              </button>
              <button 
                class="count_button"
                @click="reset(mem.id)"
              >
              Сброс
              </button>
            </div>
          </div>
        </div>
  
        <div class="member_button">
          <button class="delete_button" @click="delete_member(mem.id)">Удалить</button>
        </div>
      </div>
    </div>

    <div class="add_member_button_modal">
      <button @click="showModal = true">Добавить Участника</button>
    </div>

  </div>
</template>

<script>
  export default {
    data() {
      return {
        currentTime: new Date().toLocaleDateString() + " - " + new Date().toLocaleTimeString(),

        members: "",
        name: "",
        surname: "",
        place: "",
        add_time: 0,

        id: 0,

        showModal: false,

        start_name: "Старт",
        now: "",
        is_stop: false,
      };
    },

    methods: {
      send(data) {
        fetch('http://127.0.0.1:8000/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({"message": data})
          });
      },

      add_new_member() {
        if (this.name != "" & this.surname != "" & this.place != "") {
          const new_member = {
            id: Date.now(),
            name: this.name,
            surname: this.surname,
            place: this.place,
            add_time: this.add_time,
          }

          this.members.push(new_member)
          this.send(this.members)

          this.name = ""
          this.surname = ""
          this.place = ""
          this.add_time = ""

          this.showModal = false
        }
      },

      delete_member(id) {
        let index, len;
        for (index = 0, len = this.members.length; index < len; ++index) {
            if (this.members[index]['id'] == id) {
              this.members.splice(index, 1)

              this.send(this.members)
              break
            }
        }
      },

      get_data() {
        return fetch("http://127.0.0.1:8000/data")
          .then(response => response.json())
          .then(function (data) {
            const jsonData = data;
            return jsonData;
          })
          .catch(error => console.error(error));
      },

      counter_time(id) {
        if (!this.is_stop) {
          this.now = Date.now()
          this.start_name = "Стоп"
          this.is_stop = true

        }
        else {
          this.start_name = "Старт"
          this.is_stop = false

          let index, len;
          for (index = 0, len = this.members.length; index < len; ++index) {
              if (this.members[index]['id'] == id) {
                this.members[index]['add_time'] += parseFloat(((Date.now() - this.now) / 60000).toFixed(2))
                this.send(this.members)
                break
              }
          }
        }
        
      },

      reset(id) {
        let index, len;
          for (index = 0, len = this.members.length; index < len; ++index) {
              if (this.members[index]['id'] == id) {
                this.members[index]['add_time'] = 0
                this.send(this.members)
                break
              }
        }
      }
    },
      
    mounted() {
      this.get_data().then(data => this.members = data['members'])
      setInterval(() => {
        this.currentTime = new Date().toLocaleDateString() + " - " + new Date().toLocaleTimeString();
      }, 1000);
    },
  };
</script>


<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans:wght@500&display=swap');

  body {
    margin: 0;
    font-family: 'Noto Sans', sans-serif;
  }

  .navigator {
    font-size: 36px;
    display: grid;
    justify-content: center;
    align-items: center;
    color: white;
    background-color: dodgerblue;
    min-height: 80px;
  }

  .navigator p {
    margin: 0;
  }

  .member_list {
    display: grid;
    grid-template-columns: 1fr 1fr;
  }

  .member {
    display: grid;
    grid-template-columns: 4fr 1fr;
    border: 4px solid dodgerblue;
    margin: 0;
    margin: 10px;
    border-radius: 10px;
  }

  .member_info {
    display: grid;
    grid-template-columns: 1fr 1fr;
  }

  .member_info div {
    border: 2px solid dodgerblue;
    padding: 10px;
  }

  .member_button {
    display: grid;
  }

  .delete_button, .count_button {
    background-color: dodgerblue;
    color: rgb(255, 255, 255);
    border: none;
  }

  .count_button {
    border-radius: 10px;
  }

  .delete_button:active, .count_button:active {
    background-color: rgb(22, 107, 191);
  }

  .add_time_info {
    display: grid;
    justify-content: center;
  }

  .add_time_info_button {
    display: grid;
    grid-template-columns: 1fr 1fr;
    border: none;
  }

  .mem_inp {
    display: grid;
    grid-template-rows: 1fr 1fr 1fr;
  }

  .mem_inp input {
    margin: 5px;
  }

  .add_member_button, .add_member_button_modal {
    display: grid;
    align-items: center;
    justify-content: center;
  }

  .add_member_button_modal {
    margin: 10px;
    height: 60px;
    border-radius: 10px;
  }

  .add_member_button button, .add_member_button_modal button {
    background-color: dodgerblue;
    width: 100%;
    height: 100%;
    color: rgb(255, 255, 255);
    border-radius: 10px;
    border: none;
  }

  .add_member_button button {
    margin-top: 17px;
  }

  .add_member_button button:hover, .add_member_button_modal button:hover,  .delete_button:hover, .count_button:hover {
    background-color: rgb(22, 107, 191);
  }
  
  .add_member_button button:active, .add_member_button_modal button:active {
    background-color: rgb(22, 107, 191);
    width: 102%;
    height: 102%;
  }

  .member_button button:active {
    background-color: rgb(22, 107, 191);
  }

  .modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0,0,0,0.5);
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .modal-content {
    background-color: white;
    padding: 20px;
    border-radius: 5px;
  }
</style>