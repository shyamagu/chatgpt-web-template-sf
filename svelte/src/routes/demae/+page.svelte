<script>
    let title = "来々軒 出前ボット"

    /**
     * @type {{ role: string; content: string; }[]}
     */
    let chats = [];

    let summary = "";

    let message = "";

    let loading = false;

    let summary_loading = false;

    // send POST request to call ChatGPT
    async function postMessage() {

      loading = true;
      chats = [...chats, {"role":"user","content":message}]
      message = "";
    
      const response = await fetch("/order", {
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

    // send POST request to call ChatGPT
    async function makeSummary() {

      summary_loading = true;
      summary = "";

      const response = await fetch("/order/summary", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(chats)
      });

      const data = await response.json();

      summary = data.message;

      summary_loading = false;
    }

    // KeyDown EventHandler
    /**
     * @param {{ keyCode: number; shiftKey: any; preventDefault: () => void; }} e
     */
     function handleKeyDown(e) {
        if (e.keyCode === 13 && e.shiftKey) {
        // Shift+Enter
        postMessage();
        e.preventDefault();
        }
    }

    // Automatic scrolldown in chatfield
    import { afterUpdate } from "svelte";

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

  <div class="chat_main">
    <h1>{title}</h1>
    <div class="chatfield">
      {#each chats as chat}
        <div class="chat_{chat.role}">
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

  <div class="summary_main">
    <button class="button_summary" on:click={makeSummary}>注文サマリ作成</button>
    {#if summary_loading}
      <div class="loader"></div>
    {/if}
    <div class="chat_message">
      {summary}
    </div>
  </div>

</div>

<style>
@import url('https://fonts.googleapis.com/css?family=Noto+Sans+JP:400,700&display=swap');

:global(body){
  --back_color:#fff6f6;
  --btn_color:#ff7744;
  --chat_color:#cc3311;
  margin:0px;
  background: linear-gradient(to right bottom, #f0f0f0, var(--back_color));
  font-family: 'Noto Sans JP', sans-serif;
}

h1{
  text-align: center;
}

.main{
  display: flex;
}
.chat_main {
    width: 70%;
    min-width: 500px;
    max-width: 700px;
    height:calc(100vh - 151px);
    margin: 10px auto;
    display: flex;
    flex-direction: column;
}

.summary_main {
    width: 30%;
    min-width:200px;
    max-width:400px;
    height:calc(100vh - 100px);
    margin: 10px auto 0px 0px;
    display: flex;
    flex-direction: column;
}

.chatfield{
    width: 95%;
    margin: 0px auto;
    height: calc(100vh - 400px);
    border: 1px solid #f0f0f0;
    overflow-y: scroll;
}

.chat_user{
    width:80%;
    border: 1px solid #ccc;
    color: #fff;
    background-color: var(--chat_color);
    padding: 5px 5px 5px 10px;
    margin: 10px auto 20px 30px;
    border-radius: 10px 10px 10px 0;
    box-shadow: 1px 2px 2px 0px #ccc;
}

.chat_assistant{
    width:80%;
    border: 1px solid #ccc;
    background-color: #fff;
    margin-left: auto;
    padding: 5px 5px 5px 10px;
    margin: 10px 30px 20px auto;
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

.button_summary {
  font-size: 1.2em;
    padding: 10 20px;
    margin: 50px auto 0px auto;
    width:200px;
    background-color: var(--btn_color);
    color:#fff;
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

@keyframes spin {
    from {
        transform: rotate(0deg);
    }

    to {
        transform: rotate(360deg);
    }
}


</style>
