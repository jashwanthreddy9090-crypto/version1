
(function () {
    const form = document.getElementById("chat-form");
    const input = document.getElementById("chat-input");
    const chat = document.getElementById("chat");

    if (!form || !input || !chat) return;

    function addMessage(message, type) {
        const element = document.createElement("div");
        element.className = "chat-message " + type;
        element.textContent = message;
        chat.appendChild(element);
        chat.scrollTop = chat.scrollHeight;
    }

    function getAnswer(question) {
        const q = question.toLowerCase();

        if (q.includes("emergency") || q.includes("sos") ||
            q.includes("danger")) {
            return "For immediate danger in India, call 112. " +
                   "Do not rely on this assistant for emergency help.";
        }

        if (q.includes("track") || q.includes("status")) {
            return "Open My Complaints to check your complaint status.";
        }

        if (q.includes("worker") || q.includes("assigned")) {
            return "The assigned worker's name appears on your complaint.";
        }

        if (q.includes("water") || q.includes("electric") ||
            q.includes("clean") || q.includes("wifi") ||
            q.includes("hostel")) {
            return "Open Report Complaint, choose the relevant category, " +
                   "describe the issue and submit it.";
        }

        return "You can report campus problems, track complaints, " +
               "or use Emergency SOS. How can I help you?";
    }

    form.addEventListener("submit", function (event) {
        event.preventDefault();

        const question = input.value.trim();
        if (!question) return;

        addMessage(question, "user-message");
        input.value = "";

        addMessage(getAnswer(question), "ai-message");
    });
})();
