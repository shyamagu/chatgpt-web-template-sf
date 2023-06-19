<script>
    import { fly } from 'svelte/transition';

    let title = "自律型 ChatGPT マサル"

    /**
     * @type {{ role: string; content: string;}[]}
     */
    export let chats = [];

    let message = "";

    let loading = false;

    let proceeding = false;

    let status = "自律的に起動しました";

    let previous = "";

    let present = "";

    let code = "INIT"

    async function getInitial() {
      //GETメソッドで、/autonomous/initial にアクセスする
      const response = await fetch("/autonomous/initial", {
        method: "GET",
        headers: {
          "Content-Type": "application/json"
        }
      });

      const data = await response.json();

      //codeから_の後ろの文字列を取得
      code = data.code.split("_")[1];

      status = data.status;
      previous = data.previous_status;
      present = data.present_status;
    }

    async function proceedTime() {
      proceeding = true;

      //GETメソッドで、/autonomous/proceed にアクセスする
      const response = await fetch("/autonomous/proceed", {
        method: "GET",
        headers: {
          "Content-Type": "application/json"
        }
      });

      const data = await response.json();

      //codeから_の後ろの文字列を取得
      code = data.code.split("_")[1];

      status = data.status;
      previous = data.previous_status;
      present = data.present_status;

      proceeding = false;

    }

    // send POST request to call ChatGPT
    async function postMessage() {

      loading = true;
      chats = [...chats, {"role":"user","content":message}]
      message = "";

      const response = await fetch("/autonomous/message", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(chats)
      });

      const data = await response.json();

      chats = [...chats, {"role":"assistant","content":data.message}]

      loading = false;
    }

    // KeyDown EventHandler
    /**
     * @param {{ keyCode: number; shiftKey: any; preventDefault: () => void; }} e
     */
     function handleKeyDown(e) {
        if (e.keyCode === 13 && e.shiftKey) {
          // Shift+Enter
          message += "\n";
          e.preventDefault();
        }else if (e.keyCode === 13) {
          // Enter
          postMessage();
          e.preventDefault();
        }
    }
    
    // Automatic scrolldown in chatfield
    import { onMount, afterUpdate } from "svelte";

    onMount(() => {
      getInitial();
    });

    const scrollBottom = () => {
      const chatField = document.querySelector(".chatfield");
      if (chatField) {
        const height = chatField.scrollHeight;
        chatField.scrollTo(0, height);
      }
    };
    afterUpdate(scrollBottom);
</script>

<svelte:head>
  <title>{title}</title>
</svelte:head>

<div class="main">
  <h1>{title}</h1>
  {#if proceeding}
  <button class="button_proceed"><div class="proceeder"></div></button>
  {:else}
  <button class="button_proceed" on:click={proceedTime}>時間を進める ▶</button>
  {/if}
  <div class="display_masaru">
    <div class="display_masaru_panel">
      <div class="status">
        "{status}"
      </div>
      <img class="masaru_image" src={"auto/"+code+".png"} alt={status}/>
      <div class="status_translation">
        {#if previous != ""}
        <div class="status_header">
          前回の状態
          <pre class="status_body">{previous}</pre>
        </div>
        <div class="translate">▶</div>
        {/if}
        {#if present != ""}
        <div class="status_header">
          今の状態
          <pre class="status_body">{present}</pre>
        </div>
        {/if}
      </div>
    </div>
    <div class="display_masaru_chat">
      <div class="chatfield">
          {#each chats as chat}
          <div class="chat_{chat.role}" transition:fly="{{ y: 50, duration: 500 }}">
            <pre class="chat_message">{chat.content}</pre>
          </div>
        {/each}
        {#if loading}
          <div class="loader"></div>
        {/if}
      </div>
      <textarea class="messagebox" title="chat" name="chat" id="chat" placeholder="メッセージを入力してください" bind:value={message} on:keydown={handleKeyDown}></textarea>
      <div class="messagebox_bottom">
        <button class="button_clear" on:click={() => chats = []}>クリア</button>
        <button class="button_send" on:click={postMessage}>送信</button>
      </div>
    </div>
  </div>  
</div>

<style>
@import url('https://fonts.googleapis.com/css?family=Noto+Sans+JP:400,700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=M+PLUS+Rounded+1c:wght@400&family=Varela+Round&display=swap'); 

:global(body){
  --back_color:#f6f6ff;
  --btn_color:#6666ff;
  --chat_color:#444499;
  margin:0px;
  background: linear-gradient(to right bottom, #f0f0f0, var(--back_color));
  font-family: 'Noto Sans JP', sans-serif;
}

h1{
  text-align: center;
}

.main {
    width: 1100px;
    height:calc(100vh - 20px);
    margin: 10px auto;
    display: flex;
    flex-direction: column;
}

.display_masaru{
  display:flex;
  width:100%;
}

.display_masaru_panel{
  display: flex;
  flex-direction: column;
  width:800px;
}

.display_masaru_chat{
  display: flex;
  flex-direction: column;
  width:300px;
}

.status {
  width: 95%;
  margin: 30px auto 10px auto;
  font-family: "Yu Gothic", "Hiragino Kaku Gothic ProN", "Hiragino Sans", "Meiryo", "sans-serif";
  font-size: 1.4em;
  font-weight: bold;
  text-align: center;
  font-family: 'M PLUS Rounded 1c', sans-serif;
}

.masaru_image{
  width:300px;
  margin: auto;
}

.status_translation{
  margin-top:30px;
  width:100%;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}

.status_header{
  text-align: center;
  font-weight: bold;
}

.status_body{
  text-align: left;
  font-weight: none;
}

.translate{
  font-size: 2em;
  margin: auto 30px;
}

.chatfield{
    width: 100%;
    margin: 0px auto;
    height: 300px;
    border: 1px solid #f0f0f0;
    overflow-y: scroll;
}

.chat_user{
    width:80%;
    border: 1px solid #ccc;
    color: #fff;
    background-color: var(--chat_color);
    padding: 5px 5px 5px 10px;
    margin: 5px auto 10px 15px;
    border-radius: 10px 10px 10px 0;
    box-shadow: 1px 2px 2px 0px #ccc;
}

.chat_assistant{
    width:80%;
    border: 1px solid #ccc;
    background-color: #fff;
    margin-left: auto;
    padding: 5px 5px 5px 10px;
    margin: 5px 15px 10px auto;
    border-radius: 10px 10px 0 10px;
    box-shadow: 1px 2px 2px 0px #ccc;
}

.chat_message{
    white-space: pre-wrap;
    font-size: 1.0em;
    font-family: 'Noto Sans JP', sans-serif;
}

.messagebox {
    width: 90%;
    height: 100px;
    resize: none;
    outline: none;
    background-color: #ffffff;
    margin:20px auto 0px auto;
    font-size: 1.0em;
    border: 3px solid #666;
    border-radius: 10px;
    font-family: 'Noto Sans JP', sans-serif;
}

.messagebox_bottom {
    width: 95%;
    height: 50px;
    text-align: right;
}

.button_proceed {
  font-size: 1.1em;
  padding: 10 20px;
  margin: 10px auto;
  width:200px;
  background-color: var(--btn_color);
  color:#fff;
  font-family: 'Noto Sans JP', sans-serif;
  border: none;
  border-radius: 20px;
  font-weight: bold;
}

.button_send {
    font-size: 1.1em;
    padding: 10 20px;
    margin: 10px 0 0 10px;
    width:100px;
    background-color: var(--btn_color);
    color:#fff;
    font-family: 'Noto Sans JP', sans-serif;
    border: none;
    border-radius: 20px;
    font-weight: bold;
}

.button_send:active{
  transform: scale(1.2);
}

.button_dangerous {
    font-size: 1.1em;
    padding: 10 20px;
    margin: 10px 0 0 10px;
    width:100px;
    background-color: #ff9999;
    color:#000;
    font-family: 'Noto Sans JP', sans-serif;
    border: none;
    border-radius: 20px;
    font-weight: bold;
}

.button_clear {
    font-size: 1.1em;
    padding: 10 20px;
    margin: 10px 0 0 10px;
    width:100px;
    background-color: #999999;
    color:#fff;
    font-family: 'Noto Sans JP', sans-serif;
    border: none;
    border-radius: 20px;
    font-weight: bold;
}

.error{
    color: red;
}

.loader {
    margin: auto;
    margin-top: 10px;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    border: 5px solid #ccc;
    border-top-color: #333;
    animation: spin 1s linear infinite;
}

.proceeder {
    margin: auto;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    border: 5px solid #fff;
    border-top-color: #ccc;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    from {
        transform: rotate(0deg);
    }

    to {
        transform: rotate(360deg);
    }
}


</style>
