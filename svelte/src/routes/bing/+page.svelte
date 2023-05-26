<script>
    import { fly } from 'svelte/transition';

    let title = "Bing Search + ChatGPT"

    /**
     * @type {{ role: string; content: string; query:string; urls:string[]; titles:string[]}[]}
     */
    export let chats = [];

    let message = "";

    let loading = false;

    // send POST request to call ChatGPT
    async function postMessage() {

      loading = true;
      chats = [...chats, {"role":"user","content":message,"query":"","urls":[],"titles":[]}]
      message = "";

      // chats から role、contentのみを抽出
      const send_chats = chats.map(({role, content}) => ({role, content}));

    
      const response = await fetch("/bingsearch", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(send_chats)
      });

      const data = await response.json();

      const query = data.query;

      /**
       * @type {{ url: string; title: string; message:string}[]}
       */
      const searchResult = data.searchResult;

      const titles = searchResult.map(({title}) => title);
      const urls = searchResult.map(({url}) => url);
      

      chats = [...chats, {"role":"assistant","content":data.message,"query":query,"urls":urls,"titles":titles}]

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
  <h1>{title}</h1>
  <div class="chatfield">
      {#each chats as chat}
      {#if chat.role == "assistant" && chat.query}
       <div class="bing_query" transition:fly="{{ y: 50, duration: 500 }}">検索ワード:{chat.query}</div>
      {/if}
      <div class="chat_{chat.role}" transition:fly="{{ y: 50, duration: 500 }}">
        <pre class="chat_message">{chat.content}</pre>
        {#if chat.role == "assistant"}
          {#each chat.titles as title, i}
            <div>
              {#if title}
                *{i+1} <a href="{chat.urls[i]}" target="_blank" class="bing_link">{title}</a>
              {:else}
                *{i+1} <a href="{chat.urls[i]}" target="_blank" class="bing_link">{chat.urls[i]}</a>
              {/if}
            </div>
          {/each}
        {/if}
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

<style>
@import url('https://fonts.googleapis.com/css?family=Noto+Sans+JP:400,700&display=swap');

:global(body){
  --back_color:#f0f0ff;
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
    width: 50%;
    min-width: 500px;
    height:calc(100vh - 151px);
    margin: 10px auto;
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

.bing_query{
    font-size: 0.8em;
    width:80%;
    margin-left: auto;
    padding: 5px 5px 0px 10px;
    margin: 10px 30px 0px auto;
}

.bing_link{
  font-size:0.9em;
  margin-left: 20px;
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

.button_send:active{
  transform: scale(1.2);
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
