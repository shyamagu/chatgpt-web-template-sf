<script>
    import { fly,slide } from 'svelte/transition';

    let title = "ChatGPT + FormRecognizer"

    /**
     * @type {{ role: string; content: string; }[]}
     */
    let chats = [];

    let message = "";

    /**
     * @type {{infolink:string; title:string; authors:string[]; description:string; smallThumbnail:string}[]}
     */
    let matches = [];

    let loading = false;

    let loading_pdf = false;

    let isLoaded = false;

    let pdfUrl = "https://core.ac.uk/download/pdf/230297187.pdf"
    pdfUrl = "http://www.jaist.ac.jp/~j-morita/aim.pdf"

    async function analyzePdf() {

      loading_pdf = true;

      const response = await fetch("/pdfanalyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({url:pdfUrl})
      });

      const data = await response.json();

      loading_pdf = false;
      isLoaded = true;

    }

    // send POST request to call ChatGPT
    async function postMessage() {

      loading = true;
      chats = [...chats, {"role":"user","content":message}]
      message = "";
    
      const response = await fetch("/pdfsearch", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(chats)
      });

      const data = await response.json();

      chats = [...chats, {"role":"assistant","content":data.message}]

      matches = data.matched5;

      loading = false;
    }

    function clearAll(){
      chats = [];
      matches = [];
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

<div class="top">
  <h1>{title}</h1>
  <input type="text" class="pdf_url_box" placeholder="PDFのURLを入力してください" bind:value={pdfUrl} />
  <button class="button_send"  on:click={analyzePdf}>Analyze</button>
  {#if loading_pdf}
    <div class="loader"></div>
  {/if}
</div>
{#if isLoaded}
<div class="main">

  <div class="chat_main">
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
      <button class="button_clear" on:click={clearAll}>クリア</button>
      <button class="button_send"  on:click={postMessage}>送信</button>
    </div>
  </div>

  <div class="summary_main">
    {#if matches.length!==0}
    <h3 transition:slide="{{axis:'x'}}">ベクトル検索結果</h3>
    <div class="summary_field" transition:slide="{{axis:'x'}}">
      {#each matches as match}
        <div class="search_field">
          {match}
        </div>
      {/each}
    </div>
    {/if}
  </div>

</div>
{/if}

<style>
@import url('https://fonts.googleapis.com/css?family=Noto+Sans+JP:400,700&display=swap');

:global(body){
  --back_color:#fff6ff;
  --btn_color:#cc44cc;
  --chat_color:#990099;
  --search_color:#ffddff;
  margin:0px;
  background: linear-gradient(to right bottom, #f0f0f0, var(--back_color));
  font-family: 'Noto Sans JP', sans-serif;
  height:100vh;
}

.top{
  text-align: center;
}
h1{
  text-align: center;
}

h3{
  text-align: center;
}

.pdf_url_box{
  width: 400px;
  height: 26px;
  background-color: #ffffff;
  font-size: 1.2em;
  border: 1px solid #666;
  border-radius: 20px;
  font-family: 'Noto Sans JP', sans-serif;
  text-align: center;
}

.pdf_url_box::placeholder {
    text-align: center;
}

.main{
  display: flex;
  width:70%;
  margin:auto;
}

.search_field{
  width: 100%;
  display: flex;
  margin: 10px 10px;
  background-color: var(--search_color);
  border-radius: 5px;
  box-shadow: 1px 2px 2px 0px #ddd;
  padding: 0 10px;
  font-size: 0.9em;
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
    width: 450px;
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

.button_send:active{
  transform: scale(1.2);
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
