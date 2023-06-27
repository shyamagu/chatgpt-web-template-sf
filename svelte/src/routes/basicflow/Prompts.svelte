<script>
  import { createEventDispatcher } from "svelte";
  const dispatch = createEventDispatcher();

  /**
   * @type {string}
   */
  export let userPrompt;

  /**
   * @type {string}
   */
  export let systemPrompt;

  let loading = false;

  let token = 0;

  export async function callChatGPT() {
    loading = true;

    const chats = [{"role":"system","content":systemPrompt}, {"role":"user","content":userPrompt}]

    const response = await fetch("/simple", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(chats)
    });

    const data = await response.json();

    const result = data.message;
    token = data.input;

    dispatch("result", result);

    loading = false;
  }

  export let ended = false;
</script>

<div class="main">
  <div class="prompt_filed">
    <textarea
      class="system_textarea"
      class:active={ended}
      readonly={!ended}
      bind:value={systemPrompt}
      placeholder="Enter your system prompt here"
    />
    <textarea
      class="user_textarea"
      class:active={ended}
      readonly={!ended}
      bind:value={userPrompt}
      placeholder="Enter your user prompt here"
    />
    <div class="token_display">
      {token}
    </div>
  </div>

  {#if loading}
  <div class="loader"/>
  {:else}
  <div class="button_field">
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    {#if ended}
      <div class="submit_button" on:click={callChatGPT} />
    {:else}
      <div class="submit_button_disable" />
    {/if}
  </div>
  {/if}
</div>

<style>
  .main {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
  }

  .prompt_filed {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 400px;
  }

  .token_display{
    width: 100%;
    font-size:1.1em;
    color:#444;
    text-align: right;
    margin-bottom: 10px;
    margin-right:10px;
  }

  .button_field {
    margin-left: 20px;
  }

  .submit_button {
    width: 0;
    height: 0;
    border-top: 30px solid transparent;
    border-bottom: 30px solid transparent;
    border-left: 50px solid #666;
    cursor: pointer;
  }

  .submit_button_disable {
    width: 0;
    height: 0;
    border-top: 30px solid transparent;
    border-bottom: 30px solid transparent;
    border-left: 50px solid #ccc;
  }

  .system_textarea {
    width: 100%;
    height: 150px;
    border: 1px solid #ccc;
    border-radius: 4px;
    resize: none;
    padding: 10px;
    box-sizing: border-box;
    margin-bottom: 10px;
    font-family: "Noto Sans JP", sans-serif;
    background-color: #eee;
  }

  .user_textarea {
    width: 100%;
    height: calc(100vh - 300px);
    border: 1px solid #ccc;
    border-radius: 4px;
    resize: none;
    padding: 10px;
    box-sizing: border-box;
    margin-bottom: 10px;
    font-family: "Noto Sans JP", sans-serif;
    background-color: #eee;
  }

  .active {
    background-color: #fff;
  }

  .loader {
    margin: auto 20px;
    width: 20px;
    height: 20px;
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
