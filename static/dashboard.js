const ideaForm = document.querySelector("#new-idea-form")
const addDescBtn = document.querySelector("#add-desc");
const title = document.querySelector("#title")
const description = document.querySelector("#description");
const parkIdeaBtn = document.querySelector("#submit-idea")

addDescBtn.addEventListener("click", () => {
    description.hidden = false
    description.disabled = false
    addDescBtn.hidden = true
})