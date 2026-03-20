// cuc du lieu server tra ve duoi dang json
function addToCart(table_id, food_id, name, price) {
  fetch("/api/carts", {
    method: "post",
    body: JSON.stringify({
      table_id: table_id,
      id: food_id,
      name: name,
      price: price,
      note: "",
    }),
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((res) => res.json())
    .then((data) => {
      let elems = document.getElementsByClassName("cart-counter");
      for (let e of elems) e.innerText = data.total_quantity;
    });
}

function updateCart(table_id, food_id, obj) {
  let qty = obj.value;

  if (qty < 1) {
    qty = 1;
    obj.value = 1;
    showToast("Vui lòng nhập số lượng lớn hơn 1!", "Lỗi", "danger");
  }

  fetch(`/api/carts/${table_id}/${food_id}`, {
    method: "put",
    body: JSON.stringify({
      quantity: obj.value,
    }),
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((res) => res.json())
    .then((data) => {
      let elems = document.getElementsByClassName("cart-counter");
      for (let e of elems) e.innerText = data.total_quantity;

      let amounts = document.getElementsByClassName("cart-amount");
      for (let e of amounts)
        e.innerText = data.total_amount.toLocaleString("en");
    });
}

function updateNote(table_id, food_id, note) {
  fetch(`/api/carts/${table_id}/${food_id}/note`, {
    method: "put",
    body: JSON.stringify({
      note: note,
    }),
    headers: { "Content-Type": "application/json" },
  });
}

function openConfirmModal({
  title,
  body,
  btnText,
  btnClass,
  iconClass,
  onConfirm,
}) {
  document.getElementById("confirmModalTitleText").innerText = title;
  document.getElementById("confirmModalBody").innerText = body;

  const icon = document.getElementById("confirmModalIcon");
  icon.className = `bi me-2 ${iconClass}`;

  const btn = document.getElementById("confirmDeleteBtn");
  btn.innerText = btnText;
  btn.className = `btn ${btnClass}`;
  btn.onclick = onConfirm;

  new bootstrap.Modal(document.getElementById("deleteConfirmModal")).show();
}

function deleteCart(table_id, food_id) {
    openConfirmModal({
        title: "Xác nhận xóa",
        body: "Bạn chắc chắn muốn xóa món này khỏi giỏ hàng?",
        btnText: "Xóa",
        btnClass: "btn-danger",
        iconClass: "bi-exclamation-triangle-fill text-danger",
        onConfirm: () => {
            fetch(`/api/carts/${table_id}/${food_id}`, {
                method: "delete"
            })
            .then(res => res.json())
            .then(data => {
                let elems = document.getElementsByClassName("cart-counter");
                for (let e of elems)
                    e.innerText = data.total_quantity;
                let amounts = document.getElementsByClassName("cart-amount");
                for (let e of amounts)
                    e.innerText = data.total_amount.toLocaleString("en");
                document.getElementById(`cart${food_id}`).remove();
                showToast("Đã xóa món", "Thành công", "success");
                if (data.total_amount < 1)
                    location.reload()
                bootstrap.Modal.getInstance(
                    document.getElementById("deleteConfirmModal")
                ).hide();
            });
        }
    });
}

function orderFood(table_id) {
    openConfirmModal({
        title: "Xác nhận gọi món",
        body: "Bạn có chắc chắn muốn gửi đơn gọi món xuống bếp?",
        btnText: "Gọi món",
        btnClass: "btn-success",
        iconClass: "bi-bag-check-fill text-success",
        onConfirm: () => {
            fetch(`/api/orders/${table_id}`, { method: "post" })
                .then(res =>
                    res.json().then(data => ({
                        ok: res.ok,
                        status: res.status,
                        data: data
                    }))
                )
                .then(({ ok, data, status }) => {
                    console.log(status)
                    if (!ok) {
                        showToast(data.message, "Lỗi", "danger");
                    } else {
                        showToast(data.message, "Thành công", "success");
                        setTimeout(() => location.href = "/waiter", 1000);
                    }

                    bootstrap.Modal.getInstance(
                        document.getElementById("deleteConfirmModal")
                    ).hide();
            });
        }
    });
}

function cancelOrderFood(table_id) {
    openConfirmModal({
        title: "Hủy gọi món",
        body: "Bạn có chắc chắn muốn hủy order của bàn này?",
        btnText: "Hủy gọi món",
        btnClass: "btn-danger",
        iconClass: "bi-x-circle-fill text-danger",
        onConfirm: () => {
            fetch(`/api/orders/${table_id}/cancel`, {
                method: "delete"
            })
            .then(res => res.json())
            .then(data => {
                showToast(data.message, "Thành công", "success");
                setTimeout(() => {
                    location.href = "/waiter";
                }, 1000);
            });
        }
    });
}
//api pay
function pay(tableId) {
  if (!confirm("Bạn chắc chắn thanh toán?")) return;
  fetch(`/api/pay/${tableId}`, {
    method: "POST",
  })
    .then((res) => {
      if (res.status === 200) {
        alert("Thanh toán thành công");
        location.href = "/cashier";
      } else {
        alert("Thanh toán thất bại vì tồn tại món chưa hoàn thành ");
      }
    })
    .catch((err) => console.error(err));
}

setInterval(() => {
    fetch('/api/notify')
      .then((res) => res.json())
      .then(data => {
        if (data.message) {
          showToast(data.message, "Thông báo mới", "success");
        }
      }).catch((err) => {
    console.error("Lỗi khi lấy thông báo:", err);
      });
  }, 3000);

