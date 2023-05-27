<script>
  let title = "ChatGPT Samples"

  /**
   * @param {string | URL | undefined} page
   */
  function movepage(page){
    window.open(page, '_blank')

  }
</script>

<svelte:head>
  <title>{title}</title>
</svelte:head>

<!-- /basicへのリンク、新しいタブで開く -->
<h1>{title}</h1>

<div class="board">

  <!-- svelte-ignore a11y-click-events-have-key-events -->
  <div class="card" on:click={()=>movepage('/basic')}>
    <h2>シンプル</h2>
    <p>ChatGPTの基本系サンプル</p>
  </div>

  <!-- svelte-ignore a11y-click-events-have-key-events -->
  <div class="card" on:click={()=>movepage('/demae')}>
    <h2>注文ボット</h2>
    <p>来々軒の出前受付ボット</p>
  </div>

  <!-- svelte-ignore a11y-click-events-have-key-events -->
  <div class="card" on:click={()=>movepage('/book')}>
    <h2>書籍検索</h2>
    <p>Google Books API との連携 ChatGPT</p>
  </div>
    
  <!-- svelte-ignore a11y-click-events-have-key-events -->
  <div class="card" on:click={()=>movepage('/bing')}>
    <h2>Web検索</h2>
    <p>Bing検索+スクレイピングを取り込んだChatGPT</p>
  </div>

  <!-- svelte-ignore a11y-click-events-have-key-events -->
  <div class="card" on:click={()=>movepage('/pdf')}>
    <h2>PDF分析チャット</h2>
    <p>Azure FormRecognizer と Embedding によるベクトル検索 + ChatGPT</p>
  </div>
</div>

<style>
@import url('https://fonts.googleapis.com/css?family=Noto+Sans+JP:400,700&display=swap');

:global(body){
  margin:0px;
  background-color: #fff;
  font-family: 'Noto Sans JP', sans-serif;
  background: linear-gradient(to right bottom, #333366, #336633);
  height:calc(100vh - 70px)
}

h1{
  color:#fef;
  margin:70px auto;
  font-size: 3.6em;
  text-align: center;
}

.board{
  width:80%;
  min-width:700px;
  margin:auto;
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
}

.card{
  cursor: pointer;
  width: 200px;
  height: 150px;
  margin: 20px;
  padding: 20px 20px 40px 20px;
  border: 1px solid #ddd;
  border-radius: 10px;
  box-shadow: 2px 4px 4px 0px #333;
  background-color: #ccc;
  font-family: 'Noto Sans JP', sans-serif;
}

.card:hover{
  background-color: #fef;
  color: #333;
}
</style>
