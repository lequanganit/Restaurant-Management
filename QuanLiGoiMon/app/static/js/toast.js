function showToast(message, title = "Thông báo", type = "success") {
    const toastEl = document.getElementById("liveToast");

    const titleEl = toastEl.querySelector("#toast-title");
    const bodyEl = toastEl.querySelector("#toast-body");

    titleEl.textContent = title;
    bodyEl.textContent = message;

    toastEl.classList.remove(
        "text-bg-success",
        "text-bg-danger",
        "text-bg-warning",
        "text-bg-info"
    );
    toastEl.classList.add(`text-bg-${type}`);

    const toast = bootstrap.Toast.getOrCreateInstance(toastEl, {
        delay: 3000
    });

    toast.show();
}
