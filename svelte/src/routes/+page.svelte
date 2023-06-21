<script>
  import { scale } from "svelte/transition";
  import { quintOut } from "svelte/easing";
  import { afterUpdate } from "svelte";

  let title = "AOAI ChatGPT Samples"

  let isLoaded = false

  /**
   * @param {string | URL | undefined} page
   */
  function movepage(page){
    window.open(page, '_blank')

  }

  afterUpdate(()=>isLoaded=true);
</script>

<svelte:head>
  <title>{title}</title>
</svelte:head>

<!-- /basicへのリンク、新しいタブで開く -->
<h1>{title}</h1>

<div class="board">

  {#if isLoaded}
  <!-- svelte-ignore a11y-click-events-have-key-events -->
  <div class="card" on:click={()=>movepage('/basic')} transition:scale={{ delay: 250, duration: 300, easing: quintOut }}>
    <h2>シンプル</h2>
    <p>ChatGPTの基本系サンプル<br/>
      APIサーバとして利用可能
    </p>
  </div>

  <!-- svelte-ignore a11y-click-events-have-key-events -->
  <div class="card" on:click={()=>movepage('/demae')} transition:scale={{ delay: 300, duration: 300, easing: quintOut }}>
    <h2>注文ボット</h2>
    <p>来々軒の出前受付ボット<br/>
      自然会話と要約抽出
    </p>
  </div>

  <!-- svelte-ignore a11y-click-events-have-key-events -->
  <div class="card" on:click={()=>movepage('/survey')} transition:scale={{ delay: 300, duration: 300, easing: quintOut }}>
    <h2>アンケートボット</h2>
    <p>セミナーアンケートの受付ボット<br/>
      自然会話と要約抽出
    </p>
  </div>
  
  <!-- svelte-ignore a11y-click-events-have-key-events -->
  <div class="card" on:click={()=>movepage('/book')} transition:scale={{ delay: 350, duration: 300, easing: quintOut }}>
    <h2>書籍検索</h2>
    <p>Google Books API との連携 ChatGPT</p>
    <a href="https://qiita.com/shyamagu/items/8a2df72d13c6f8a97be1" target="_blank">参考サイト</a>
  </div>
    
  <!-- svelte-ignore a11y-click-events-have-key-events -->
  <div class="card" on:click={()=>movepage('/bing')} transition:scale={{ delay: 400, duration: 300, easing: quintOut }}>
    <h2>Web検索</h2>
    <p>Bing検索+スクレイピングを取り込んだChatGPT</p>
    <a href="https://qiita.com/shyamagu/items/9c00affc9f403b6d67ed" target="_blank">参考サイト</a>
  </div>

  <!-- svelte-ignore a11y-click-events-have-key-events -->
  <div class="card" on:click={()=>movepage('/pdf')} transition:scale={{ delay: 450, duration: 300, easing: quintOut }}>
    <h2>PDF分析チャット</h2>
    <p>Azure FormRecognizer と Embedding + ChatGPT<br/>
      ※Single Userのみ
    </p>
    <a href="https://qiita.com/shyamagu/items/5e4c8329bdfeb4be3bcd" target="_blank">参考サイト</a>
  </div>

  <!-- svelte-ignore a11y-click-events-have-key-events -->
  <div class="card" on:click={()=>movepage('/long')} transition:scale={{ delay: 450, duration: 300, easing: quintOut }}>
    <h2>長期記憶ボット
    </h2>
    <p>過去会話履歴 + 要約<br/>没) 過去会話履歴+ベクトル検索
    </p>
    <a href="https://qiita.com/shyamagu/items/43e6370dd8937e1711c1" target="_blank">参考サイト</a>
  </div>

  <!-- svelte-ignore a11y-click-events-have-key-events -->
  <div class="card" on:click={()=>movepage('/emb')} transition:scale={{ delay: 450, duration: 300, easing: quintOut }}>
    <h2>Embedding
    </h2>
    <p>ベクトル検索のプレイグランド
    </p>
    <a href="https://qiita.com/shyamagu/items/587274fa1b46c38867a7" target="_blank">参考サイト</a>
  </div>

  <!-- svelte-ignore a11y-click-events-have-key-events -->
  <div class="card" on:click={()=>movepage('/inject')} transition:scale={{ delay: 450, duration: 300, easing: quintOut }}>
    <h2>Anti-Injection
    </h2>
    <p>プロンプトインジェクション対策
    </p>
    <a href="https://qiita.com/shyamagu/items/92274d0956394e954951" target="_blank">参考サイト</a><br/>
    <a href="https://qiita.com/shyamagu/items/19c6e3c7dda54320aa36" target="_blank">参考サイト</a>
  </div>

  <!-- svelte-ignore a11y-click-events-have-key-events -->
  <div class="card" on:click={()=>movepage('/auto')} transition:scale={{ delay: 450, duration: 300, easing: quintOut }}>
    <h2>自律型AI
    </h2>
    <p>時間依存のパラメータをもったChatGPT<br/>※非業務？
    </p>
  </div>

  <!-- svelte-ignore a11y-click-events-have-key-events -->
  <div class="card" on:click={()=>movepage('/stream')} transition:scale={{ delay: 450, duration: 300, easing: quintOut }}>
    <h2>ストリーム出力
    </h2>
    <p>シンプルなChatGPTの出力ストリーム対応版
    </p>
  </div>
  
  {/if}

</div>

<style>
@import url('https://fonts.googleapis.com/css?family=Noto+Sans+JP:400,700&display=swap');

:global(body){
  margin:0px;
  background-color: #000;
  font-family: 'Noto Sans JP', sans-serif;
  background: linear-gradient(to right bottom, #224, #242);
  height:calc(100vh - 70px)
}

h1{
  color:#fef;
  margin:40px auto;
  font-size: 3.0em;
  text-align: center;
}

h2{
  font-size:1.2em;
}

p{
  font-size:0.9em;
}

.board{
  width:80%;
  min-width:400px;
  margin:auto;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}

.card{
  cursor: pointer;
  width: 180px;
  height: 160px;
  margin: 10px;
  padding: 10px 20px 40px 20px;
  border: 1px solid #ddd;
  border-radius: 10px;
  box-shadow: 2px 4px 4px 0px #333;
  background-color: #ccc;
  font-family: 'Noto Sans JP', sans-serif;
}

.card:hover{
  background-color: #fef;
  color: #222;
}
</style>
