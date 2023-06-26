<script>
    import Prompts from './Prompts.svelte';

    let title = "ChatGPT Flow Simple"

    /**
   * @type {string[]}
   */
    let systemPrompts = [""]

    /**
   * @type {string[]}
   */
    let userPrompts = [""]
    let result = '';

    /**
   * @param {{detail: string;}} event
   */
    function handleResult(event){
      result = event.detail
      userPrompts = [...userPrompts, result]
      scrolltoSide();
    }

        // Automatic scrolldown in chatfield
        import { afterUpdate } from "svelte";

    const scrolltoSide = () => {
      const promptField = document.querySelector(".prompts_field");
      if (promptField) {
        const width = promptField.scrollWidth;
        promptField.scrollTo(width,0);
      }
    };
    afterUpdate(scrolltoSide);
</script>

<svelte:head>
  <title>{title}</title>
</svelte:head>

<div class="prompts_field">
  {#each userPrompts as userPrompt, i (i)}
    <div class="prompt_field">
      <Prompts bind:systemPrompt={systemPrompts[i]} bind:userPrompt={userPrompt} on:result={handleResult} ended={userPrompts.length === i+1}/>
    </div>
  {/each}
</div>

<style>
  @import url('https://fonts.googleapis.com/css?family=Noto+Sans+JP:400,700&display=swap');

  :global(body){
  --back_color:#eef;
  --btn_color:#999999;
  --chat_color:#666666;
  margin:0px;
  background: linear-gradient(to bottom, #f0f0f0, var(--back_color));
  font-family: 'Noto Sans JP', sans-serif;
  height:calc(100vh - 20px);
  overflow-x:hidden
  }

  .prompts_field {
      display: flex;
      min-width: calc(100% + 1px);
      overflow-x: scroll;
  }

  .prompt_field {
      flex-basis: 450px;
      min-width:450px;
      margin-top:50px;
      margin-left:50px;
      margin-bottom:40px;
  }

</style>
