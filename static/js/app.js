function execute_sample_prompt(prompt) {
  const textarea = document.getElementById("chatbot-textarea");
  if (textarea) {
    textarea.value = prompt;
  }

  const form = document.getElementById("chat-form");
  const event = new Event("submit", { bubbles: true });
  form.dispatchEvent(event);
}

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
    card.onclick = () => execute_sample_prompt(prompt);
    card.className =
      "flex flex-col items-end justify-between flex-none px-4 py-3 rounded-lg cursor-pointer bg-zinc-100 w-72";
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
        class="text-zinc-500 h-5 w-5 mt-2"
      >
        <path stroke="none" d="M0 0h24v24H0z" fill="none" />
        <path d="M17 7l-10 10" />
        <path d="M8 7l9 0l0 9" />
      </svg>
    `;
    container.appendChild(card);
  });
}

let is_query_running = false;
function set_button_busy_state(is_busy) {
  is_query_running = is_busy;

  const default_content = get_send_icon(5);
  const busy_content = get_busy_icon(5);

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

function format_tool_name(tool_name) {
  const formatted_tool_name = tool_name.replace(/_/g, " ");
  return formatted_tool_name.replace(/\b\w/g, (char) => char.toUpperCase());
}

function update_user_prompt(prompt) {
  const user_prompt = document.getElementById("user-prompt");

  user_prompt.innerHTML = `
        <p class="text-4xl font-normal text-zinc-800">
            ${prompt}
        </p>
    `;
}

function update_tool_calls(tool_calls) {
  const tools_used = document.getElementById("tools-used");

  tool_calls.forEach((tool_call) => {
    const tool_call_div = document.createElement("div");
    tool_call_div.className =
      "inline-flex items-center px-3 py-1 text-sm font-semibold transition-colors border rounded-full focus:outline-hidden focus:ring-2 focus:ring-ring focus:ring-offset-2 text-foreground shrink-0";

    tool_call_div.innerHTML = `
        <span
          id="${tool_call.name}_status"
          class="text-black" style="width: 1rem; height: 1rem; margin-right: 0.5rem;"
        >
          ${get_busy_icon(0)}
        </span>
        ${format_tool_name(tool_call.name)}
    `;

    tools_used.appendChild(tool_call_div);
  });
}

function update_tool_status(tool_response) {
  const tool_id = tool_response.tool_name + "_status";
  const tool_status = document.getElementById(tool_id);

  if (tool_status) {
    tool_status.innerHTML = get_done_icon(0);
  }
}

function update_ai_response(ai_response) {
  const response_area = document.getElementById("ai-response");
  const skeleton = document.getElementById("ai-response-skeleton");

  skeleton.style.display = "none";
  response_area.innerHTML = marked.parse(ai_response);
}

function reset_dialog() {
  const prompt_area = document.getElementById("user-prompt");
  const tools_used = document.getElementById("tools-used");
  const ai_response = document.getElementById("ai-response");
  const skeleton = document.getElementById("ai-response-skeleton");

  prompt_area.innerHTML = "";
  tools_used.innerHTML = "";
  ai_response.innerHTML = "";
  skeleton.style.display = "block";
}

function initiate_socket_connection() {
  return new Promise((resolve, reject) => {
    const socket = new WebSocket("ws://" + window.location.host + "/ws/chat/");

    socket.onmessage = function (e) {
      const data = JSON.parse(e.data);

      switch (data.step) {
        case "user_prompt":
          update_user_prompt(data.data.content);
          break;
        case "tool_calls":
          update_tool_calls(data.data.tool_calls);
          break;
        case "tool_response":
          update_tool_status(data.data);
          break;
        case "agent_response":
          update_ai_response(data.data.content);
          break;
        case "final_response":
          set_button_busy_state(false);
          socket.close();
          break;
      }
    };

    socket.onopen = function () {
      resolve(socket);
    };

    socket.onerror = function (e) {
      console.error("WebSocket error:", e);
      set_button_busy_state(false);
      reject(e);
    };
  });
}

document
  .getElementById("chat-form")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    if (is_query_running) return;

    set_button_busy_state(true);
    reset_dialog();

    window.dispatchEvent(new CustomEvent("show-dialog"));

    const form = e.target;
    const data = new FormData(form);

    try {
      const socket = await initiate_socket_connection();

      socket.send(
        JSON.stringify({
          prompt: data.get("prompt"),
          agent: data.get("agent"),
        })
      );
    } catch (err) {
      set_button_busy_state(false);
    }
  });
