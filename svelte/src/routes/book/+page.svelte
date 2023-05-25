<script>
    import { fly,slide } from 'svelte/transition';

    let title = "ChatGPT + GoogleBooksAPI"

    /**
     * @type {{ role: string; content: string; }[]}
     */
    let chats = [];

    let message = "";

    let totalnum = 0;

    let query = "";

    /**
     * @type {{infolink:string; title:string; authors:string[]; description:string; smallThumbnail:string}[]}
     */
    let books = [];

    let loading = false;

    // send POST request to call ChatGPT
    async function postMessage() {

      loading = true;
      chats = [...chats, {"role":"user","content":message}]
      message = "";
    
      const response = await fetch("/booksearch", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(chats)
      });

      const data = await response.json();

      chats = [...chats, {"role":"assistant","content":data.message}]

      books = data.bookresult;

      totalnum = data.totalnum;

      query = data.query;

      loading = false;
    }

    function clearAll(){
      totalnum = 0;
      chats = [];
      books = [];
      query = "";
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

  <div class="chat_main">
    <h1>{title}</h1>
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
    {#if totalnum!==0}
      <h4>{totalnum} 件の書籍が見つかりました。うち {books.length} 件を表示します</h4>
      <div class="query">検索クエリ―: {query}</div>
    {/if}
    {#each books as book}
      <div class="book_field" transition:slide="{{axis:'x'}}">
        <div class="book_image_field">
          <img class="book_image" src={book.smallThumbnail} alt={book.title} />
        </div>
        <div class="book_detail">
          <a href={book.infolink} target="_blank"><h3>{book.title}</h3></a>
          <p>{book.authors}</p>
          <p>{book.description}</p>
        </div>
      </div>
    {/each}
  </div>

</div>

<style>
@import url('https://fonts.googleapis.com/css?family=Noto+Sans+JP:400,700&display=swap');

:global(body){
  --back_color:#f6fff6;
  --btn_color:#33cc55;
  --chat_color:#22aa00;
  --book_color:#ddffdd;
  margin:0px;
  background: linear-gradient(to right bottom, #f0f0f0, var(--back_color));
  font-family: 'Noto Sans JP', sans-serif;
  height:100vh;
}

h1{
  text-align: center;
}

h4{
  text-align: left;
  margin: 40px 0 0 20px;
}

.query{
  font-size: 0.8em;
  margin: 0 0 0 20px;
}

.main{
  display: flex;
  width:70%;
  margin:auto;
}

.book_field{
  width: 100%;
  display: flex;
  margin: 10px 10px;
  background-color: var(--book_color);
  border-radius: 5px;
  box-shadow: 1px 2px 2px 0px #ddd;
  padding: 0 10px;
}

.book_image_field{
  width:100px;
}

.book_image{
  width:90px;
  margin: 20px 5px;
}

.book_detail{
  width:350px;
  font-size: 0.7em;
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
    margin: 30px auto 0px 0px;
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
