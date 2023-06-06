<script>
    import { fly,slide } from 'svelte/transition';
    import Modal from './Modal.svelte';

    let showModal = false;
    /**
   * @type {number[]}
   */
    let modal_embedding = [];

    let modal_content = "";
    /**
   * @param {number[]} embedding
   * @param {string} content
   */
    function openModal(embedding, content){
      showModal = true;
      modal_embedding = embedding;
      modal_content = content;
    }

    let title = "Embedding Playground"

    /**
     * @type {{ content: string; similarity: number; embedding: number[]; searched: string; }[]}
     */
    let list_data = [];

    list_data = [
      {content:"味噌ラーメンはラーメンの1種です。", similarity:-1.0, embedding:[], searched:""},
      {content:"味噌ラーメンの発祥は札幌と言われています。", similarity:-1.0, embedding:[], searched:""},
      {content:"醤油ラーメンは最もオーソドックスなラーメンです。", similarity:-1.0, embedding:[], searched:""},
      {content:"味噌は日本の伝統的な調味料です。", similarity:-1.0, embedding:[], searched:""},
      {content:"味噌には赤味噌や白味噌など様々な種類があります。", similarity:-1.0, embedding:[], searched:""},
    ]

    let query = "";

    let new_content = "";

    async function addContent() {
      list_data = [...list_data, {content:new_content, similarity:-1.0, embedding:[], searched:""}];
      new_content = "";
    }

    async function vectorSearch() {

      //list_dataでループする
      for (let i = 0; i < list_data.length; i++) {

        if(list_data[i].searched == query){
          continue;
        }

        const response = await fetch("/embedding", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({word:query, target:list_data[i].content})
        });

        const data = await response.json();

        list_data[i].similarity = data.similarity;
        list_data[i].embedding = data.embedding;
        list_data[i].searched = query;

      }

      //list_dataをsimilarityでソートする
      list_data.sort(function(a,b){
        if(a.similarity < b.similarity) return 1;
        if(a.similarity > b.similarity) return -1;
        return 0;
      });

    }

    function clearAll(){
      list_data = [];
      query = "";
      new_content = "";
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
  <input type="text" class="query_box" placeholder="検索ワードを入力してください" bind:value={query} />
  <button class="button_send"  on:click={vectorSearch}>検索</button>
</div>
<div class="main">

  <div class="vector_main">
    <div class="chatfield">
      {#each list_data as data}
        <div class="target_content" transition:fly="{{ y: 50, duration: 500 }}">
          <pre class="content">{data.content}</pre>
          <div class="similarity">
            {#if data.embedding.length > 0}
              <button class="emb_button" on:click={()=>openModal(data.embedding,data.content)}>ベクトル確認</button>
            {:else}
              --
            {/if}
          </div>
          <!-- similarityがマイナスの場合は、"--"表記にする-->
          {#if data.similarity < 0}
            <div class="similarity">--</div>
          {:else}
            <div class="similarity">{data.similarity}</div>
          {/if}
        </div>
      {/each}
    </div>
    <textarea class="messagebox" title="chat" name="chat" id="chat" placeholder="コンテンツ追加" bind:value={new_content}></textarea>
    <div class="messagebox_bottom">
      <button class="button_clear" on:click={clearAll}>クリア</button>
      <button class="button_send"  on:click={addContent}>追加</button>
    </div>
  </div>
</div>

<Modal bind:showModal>
	<h2 slot="header">
		Embedding
		<small>({modal_embedding.length})</small><br/>
		<small>"{modal_content}"</small>
	</h2>

  <div class="emb_field">
    {modal_embedding}
  </div>
</Modal>

<style>
@import url('https://fonts.googleapis.com/css?family=Noto+Sans+JP:400,700&display=swap');

:global(body){
  --back_color:#f0f0ff;
  --btn_color:#9933ff;
  --sub_btn_color:#aa66cc;
  --chat_color:#6600cc;
  margin:0px;
  background: linear-gradient(to right bottom, #f0f0f0, var(--back_color));
  font-family: 'Noto Sans JP', sans-serif;
  height: calc(100vh - 30px);
}

.top{
  text-align: center;
}
h1{
  text-align: center;
}

.emb_field{
  width: 100%;
  min-width:600px;
  height: 400px;
  min-height:calc(100vh - 400px);
  word-wrap: break-word;
  overflow: scroll;
}

.query_box{
  width: 400px;
  height: 30px;
  background-color: #ffffff;
  font-size: 1.1em;
  border: 1px solid #666;
  border-radius: 20px;
  font-family: 'Noto Sans JP', sans-serif;
  text-align: center;
}

.query_box::placeholder {
    text-align: center;
}

.main{
  display: flex;
  width:80%;
  margin:auto;
}

.target_content {
  width:100%;
  min-width:600px;
  vertical-align: bottom;
  display:flex;
}

.content{
  min-height: 50px;
  width: 100%;
  background-color: #fff;
  margin: 10px 10px;
  font-size: 1.1em;
  padding-left: 10px;
  vertical-align: middle;
  display: flex;
  align-items: center;
  white-space: pre-wrap;
}

.emb_button{
  font-size: 1.1em;
  width:120px;
  background-color: var(--sub_btn_color);
  color:#fff;
  font-family: 'Noto Sans JP', sans-serif;
  border: none;
  border-radius: 20px;
  font-weight: bold;
}

.similarity{
  font-size: 0.9em;
  width: 250px;
  min-height: 50px;
  background-color: #fff;
  text-align: center;
  line-height: 100%;
  margin: 10px 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.vector_main {
    width: 90%;
    min-width: 600px;
    max-width: 900px;
    height:calc(100vh - 151px);
    margin: 10px auto;
    display: flex;
    flex-direction: column;
}

.chatfield{
    width: 95%;
    margin: 0px auto;
    height: calc(100vh - 350px);
    border: 1px solid #f0f0f0;
    overflow-y: scroll;
}

.messagebox {
    width: 90%;
    height: 70px;
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

</style>
