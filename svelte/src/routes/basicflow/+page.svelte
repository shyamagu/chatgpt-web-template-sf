<script>
  import Prompts from "./Prompts.svelte";
  import { afterUpdate } from "svelte";

  let title = "ChatGPT Flow Simple";

  /**
   * @type {string[]}
   */
  let systemPrompts = [""];

  /**
   * @type {string[]}
   */
  let userPrompts = [""];
  let result = "";


  let titles = [""];

  /**
   * @param {{detail: string;}} event
   */
  function handleResult(event) {
    result = event.detail;
    userPrompts = [...userPrompts, result];
  }

  $: if (userPrompts.length > 1){
    scrolltoSide();
  }

  /**
   * @param {number} index
   */
  function deletePrompt(index) {
    systemPrompts.splice(index, 1);
    userPrompts.splice(index, 1);
    titles.splice(index, 1);
    userPrompts = userPrompts;
  }

  function downloadJson() {
    const data = {
      systems: systemPrompts,
      users: userPrompts,
      titles:titles,
    };
    const a = document.createElement("a");

    a.download = "flows_" + Date.now() + ".json";

    a.href = URL.createObjectURL(
      new Blob([JSON.stringify(data, null, 2)], {
        type: "application/json",
      })
    );

    a.click();
    a.remove();
  }

  // ファイルを読み込んでdataにセットする関数
  /**
   * @param {Blob} file
   */
  function readFile(file) {
    const reader = new FileReader();
    reader.onload = () => {
      if(typeof reader.result !== "string") return;
      const data = JSON.parse(reader.result);
      systemPrompts = data.systems;
      userPrompts = data.users;

      if(data.titles){
        titles = data.titles;
      }
    };
    reader.readAsText(file);
  }

  // ファイル選択ダイアログを開く関数
  function openDialog() {
    const input = document.createElement("input");
    input.type = "file";
    input.accept = ".json";
    input.onchange = () => {
      if (input.files) {
        const file = input.files[0];
        readFile(file);
      }
    };
    input.click();
  }

  const scrolltoSide = () => {
    const promptField = document.querySelector(".prompts_field");
    if (promptField) {
      const width = promptField.scrollWidth;
      promptField.scrollTo(width, 0);
    }
  };
  //afterUpdate(scrolltoSide);
</script>

<svelte:head>
  <title>{title}</title>
</svelte:head>

<div class="button_field">
  <button class="port_button" on:click={downloadJson}>Export</button>
  <button class="port_button" on:click={openDialog}>Import</button>
</div>

<div class="prompts_field">
  {#each userPrompts as userPrompt, i (i)}
    <div class="prompt_field">
      <div class="delete_button_field">
        {#if userPrompts.length !== i + 1}
          <button class="delete_button" on:click={() => deletePrompt(i)}
            >x</button
          >
        {/if}
      </div>
      <Prompts
        bind:systemPrompt={systemPrompts[i]}
        bind:userPrompt
        bind:title={titles[i]}
        on:result={handleResult}
        ended={userPrompts.length === i + 1}
      />
    </div>
  {/each}
</div>

<style>
  @import url("https://fonts.googleapis.com/css?family=Noto+Sans+JP:400,700&display=swap");

  :global(body) {
    --back_color: #eef;
    --btn_color: #666;
    --chat_color: #666666;
    margin: 0px;
    background: linear-gradient(to bottom, #f0f0f0, var(--back_color));
    font-family: "Noto Sans JP", sans-serif;
    height: calc(100vh - 20px);
    overflow-x: hidden;
    overflow-y: hidden;
  }

  .prompts_field {
    display: flex;
    min-width: calc(100% + 1px);
    overflow-x: scroll;
  }

  .prompt_field {
    flex-basis: 450px;
    min-width: 450px;
    margin-top: 5px;
    margin-left: 50px;
    margin-bottom: 5px;
  }
  .delete_button_field {
    height: 20px;
  }
  .delete_button {
    color: #f99;
    border: 1px solid #ccc;
    border-radius: 20%;
    margin-bottom: 2px;
  }

  .button_field {
    margin-left: 50px;
    margin-top: 10px;
  }
  .port_button {
    font-size: 0.9em;
    width: 100px;
    background-color: var(--btn_color);
    color: #fff;
    font-family: "Noto Sans JP", sans-serif;
    border: none;
    border-radius: 20px;
  }
</style>
