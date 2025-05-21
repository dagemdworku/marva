function update_welcome_message_and_example_prompts(
  welcome_message,
  example_prompts
) {
  const textarea = document.getElementById("chatbot-textarea");
  if (textarea) {
    textarea.setAttribute("placeholder", "✧˖°. " + welcome_message);
  }

  const container = document.getElementById("example-prompts");
  container.innerHTML = "";

  example_prompts.forEach((prompt) => {
    const card = document.createElement("div");
    card.className =
      "flex flex-col items-end justify-between flex-none h-32 px-4 py-3 rounded-lg bg-zinc-100 w-72";
    card.innerHTML = `
      <p class="text-base text-zinc-800 w-full">${prompt}</p>
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
        class="text-zinc-500 h-5 w-5"
      >
        <path stroke="none" d="M0 0h24v24H0z" fill="none" />
        <path d="M17 7l-10 10" />
        <path d="M8 7l9 0l0 9" />
      </svg>
    `;
    container.appendChild(card);
  });
}

function set_button_busy_state(is_busy) {
  const default_content = `
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      stroke-width="2"
      stroke-linecap="round"
      stroke-linejoin="round"
      class="!h-5 !w-5"
    >
      <path stroke="none" d="M0 0h24v24H0z" fill="none" />
      <path d="M12 5l0 14" />
      <path d="M18 11l-6 -6" />
      <path d="M6 11l6 -6" />
    </svg>
  `;

  const busy_content = `
    <svg
      viewBox="0 0 64 64"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      class="!h-5 !w-5 animate-spin"
    >
      <path
        d="M32 3C35.8083 3 39.5794 3.75011 43.0978 5.20749C46.6163 6.66488 49.8132 8.80101 52.5061 11.4939C55.199 14.1868 57.3351 17.3837 58.7925 20.9022C60.2499 24.4206 61 28.1917 61 32C61 35.8083 60.2499 39.5794 58.7925 43.0978C57.3351 46.6163 55.199 49.8132 52.5061 52.5061C49.8132 55.199 46.6163 57.3351 43.0978 58.7925C39.5794 60.2499 35.8083 61 32 61C28.1917 61 24.4206 60.2499 20.9022 58.7925C17.3837 57.3351 14.1868 55.199 11.4939 52.5061C8.801 49.8132 6.66487 46.6163 5.20749 43.0978C3.7501 39.5794 3 35.8083 3 32C3 28.1917 3.75011 24.4206 5.2075 20.9022C6.66489 17.3837 8.80101 14.1868 11.4939 11.4939C14.1868 8.80099 17.3838 6.66487 20.9022 5.20749C24.4206 3.7501 28.1917 3 32 3L32 3Z"
        stroke="currentColor"
        stroke-width="5.2"
        stroke-linecap="round"
        stroke-linejoin="round"
      ></path>
      <path
        d="M32 3C36.5778 3 41.0906 4.08374 45.1692 6.16256C49.2477 8.24138 52.7762 11.2562 55.466 14.9605C58.1558 18.6647 59.9304 22.9531 60.6448 27.4748C61.3591 31.9965 60.9928 36.6232 59.5759 40.9762"
        stroke="currentColor"
        stroke-width="5.2"
        stroke-linecap="round"
        stroke-linejoin="round"
        class="text-zinc-600"
      ></path>
    </svg>
  `;

  const button = document.getElementById("send-button");

  if (is_busy) {
    button.innerHTML = busy_content;
    button.setAttribute("disabled", true);
  } else {
    button.innerHTML = default_content;
    button.removeAttribute("disabled");
  }
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function update_user_prompt(user_prompt) {
  const prompt_area = document.getElementById("user-prompt");
  const dialog_title = document.getElementById("dialog-title");

  prompt_area.innerHTML = `
        <p class="mt-5 mb-2 text-4xl font-normal text-zinc-800">
            ${user_prompt}
        </p>
    `;

  dialog_title.textContent = "Finished with your request!";
}

function update_ai_response(ai_response) {
  const response_area = document.getElementById("ai-response");

  response_area.innerHTML = marked.parse(ai_response);
}

function clear_user_prompt() {
  const prompt_area = document.getElementById("user-prompt");
  const dialog_title = document.getElementById("dialog-title");

  prompt_area.innerHTML = "";
  dialog_title.textContent = "On it boss...";
}

function clear_ai_response() {
  const response_area = document.getElementById("ai-response");

  response_area.innerHTML = "";
}

function openDialog() {}

document.getElementById("chat-form").addEventListener("submit", function (e) {
  e.preventDefault();

  set_button_busy_state(true);

  clear_user_prompt();
  clear_ai_response();

  window.dispatchEvent(new CustomEvent("show-dialog"));

  const form = e.target;
  const data = new FormData(form);

  fetch("", {
    method: "POST",
    headers: {
      "X-Requested-With": "XMLHttpRequest",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: data,
  })
    .then((response) => response.json())
    .then((data) => {
      set_button_busy_state(false);

      update_user_prompt(data.prompt);
      update_ai_response(data.response);
    });
});
