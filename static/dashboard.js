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

const switchDialog = document.querySelector("#switch-dialog");

if (switchDialog) {
    const switchForm = document.querySelector("#switch-idea-form");
    const switchTargetTitle = document.querySelector("#switch-target-title");
    const switchTriggers = document.querySelectorAll(".switch-trigger");
    const switchCloseBtn = document.querySelector("#switch-dialog-close");
    const switchCancelBtn = document.querySelector("#switch-dialog-cancel");

    switchTriggers.forEach((trigger) => {
        trigger.addEventListener("click", () => {
            switchForm.action = `/switch/${encodeURIComponent(trigger.dataset.ideaId)}`;
            switchTargetTitle.textContent = trigger.dataset.ideaTitle;
            switchDialog.showModal();
            switchForm.querySelector("input[type='radio']").focus();
        });
    });

    switchCloseBtn.addEventListener("click", () => switchDialog.close());
    switchCancelBtn.addEventListener("click", () => switchDialog.close());

    switchDialog.addEventListener("close", () => {
        switchForm.reset();
        switchForm.action = "/switch";
        switchTargetTitle.textContent = "";
    });
}